from django.shortcuts import render,get_object_or_404,redirect
from django.views.generic import View,ListView   #FormView
from django.http import JsonResponse
from prods.models import Cart
from .models import Order
from django.db.models import Sum
from profiles.models import BillingProfile
from profiles.forms import BillingProfileForm
class ListOrder(ListView):
    """list of all pre-orders(based on accepted carts) but not paid yet"""
    model = Order
    context_object_name = "orders"
    template_name = 'orders/list_orders.html'
    ordering = ['-date']

    def get_queryset(self):
        return  Order.objects.filter(cart__user = self.request.user,accepted=False)
class OrderHistory(ListView):
    model = Order
    template_name = 'orders/order-history.html'
    ordering = ['-date']

    def get_queryset(self):
        return Order.objects.filter(cart__user = self.request.user,accepted=True)

class DeleteOrder(View):
    """user can remove pre-order from list of orders"""
    def post(self,request):
        pk = request.POST.get('pk')
        order = get_object_or_404(Order,id=pk,accepted=False)
        cart = get_object_or_404(Cart,id=order.cart.id,accepted=True)
        order.delete()
        cart.delete()
        return redirect('orders:list-orders')
#
class CreateOrder(View):
    """
    Display existing order or
    create a new one triggered by cart status => accepted False
    """
    def post(self,request):
        pk_cart = request.POST.get('pk','pk not found')
        cart = Cart.objects.get(id=pk_cart,accepted=False)
        order = Order.objects.create(cart=cart) # per default accepted=False)
        order.update_total()
        print("inside create order..created new one with id:",order.id)
        print("inside create order..and accepted :",order.accepted)
        cart.accepted = True
        cart.save()
        new_cart = Cart.objects.create(user=request.user)
        request.session["cart_id"] = new_cart.id
        return redirect('orders:list-orders')

class Checkout(View):
    def get(self,request):
        """make final order """
        pk=request.GET.get('pk')
        print("checkout calling... got pk Order obj with id=",pk)
        form = BillingProfileForm(
                instance=BillingProfile.objects.get(user__email=request.user.email)
                )
        order = get_object_or_404(Order,id=pk,accepted=False,cart__user=request.user)
        order.accepted = True
        order.save()
        return render(request,'orders/checkout.html',{'form':form,'order':order})
