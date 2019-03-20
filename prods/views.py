from django.shortcuts import render,redirect,get_object_or_404,reverse
from django.http import JsonResponse
from django.views.generic import (ListView,
                                DetailView,
                                CreateView,
                                DeleteView,
                                RedirectView,
                                View)
from .models import Product,Cart,CartItem,Category
from .forms import *
from django.contrib import messages
from django.db.models import Sum

# class KillSession(View):
#     def get(self,request):
#         del request.session['cart_id']
#         return redirect('/')
#
class ProdList(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'prods/index.html'

class ProdDetail(DetailView):
    model = Product
    context_object_name = 'product'

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(*args,**kwargs)
        form = CartItemForm()
        context['form'] = form
        return context

class AddItemToCart(View):
    def get(self,request,slug,pk):
        #del request.session['cart_id']
        cart = Cart.objects.new_or_get(request)
        prod = get_object_or_404(Product,id=pk)
        flag = False
        try:
            item = CartItem.objects.get(
                cart = cart,
                product = prod,
                cart__accepted=False
            )
            flag = True
            messages.error(request, 'Product is already in your cart.')
        except CartItem.DoesNotExist:
            item  = CartItem.objects.create(
                cart = cart,
                product = prod,
                qty = 1
                )
            #messages.success(request, 'New item added to your cart.')
        total_qty = cart.cart_items.aggregate(total=Sum('qty'))
        num_items = total_qty.get('total')
        total_price = cart.cart_items.aggregate(total_price=Sum('sub_total'))
        price = total_price.get('total_price')
        cart.total = price
        cart.save()
        return JsonResponse({"flag":flag,"numItems":num_items,"price":price})
        #return redirect("/detail/{}/".format(slug))

class CartItemsView(View):
    def get(self,request):
        print("view cartitm calling")
        context = {}
        cart = Cart.objects.new_or_get(self.request,accepted=False)
        print("из вью привет cart accepted:",cart.accepted)
        items = cart.cart_items.all()
        context['cart'] = cart
        context['items'] = items
        qty = cart.get_sum_items_amount()
        if isinstance(qty,int):
            context['qty'] = qty
        else:
            context['qty'] = 0
        return render(request,'prods/cart.html',context)

class RedirectToProduct(View):
    def get(self,request,pk):
        prod = Product.objects.get(id=pk)
        return redirect("/detail/{}/".format(prod.slug))

class EditCart(View):
    def post(self,request,pk):
        #del request.session['cart_id']
        cart = Cart.objects.new_or_get(request)
        qty = request.POST.get('qty')
        cart_item = get_object_or_404(CartItem,id=pk)
        prod= Product.objects.get(id=cart_item.product_id)
        qty = request.POST.get('qty')
        if qty is not None and int(qty)>0:
            item = CartItem.objects.get(
                cart = cart,
                product = prod,
                cart__accepted=False
            )
            item.qty = int(qty)
            item.save()
            #messages.success(request, 'Qty changed.')
        else:
            messages.error(request, 'Amount of product should be 1 or more.')
        item_sub_total = item.sub_total
        num_items_cart = cart.get_sum_items_amount()
        price = cart.get_sum_items_price()
        cart.total = price
        cart.save()
        #return redirect("/detail/{}/".format(pk))
        return JsonResponse({
                        "totalItemsInCart":num_items_cart,
                        "cartTotalPrice":price,
                        "itemSubTotal":item_sub_total,
                        })

class DeleteCartItem(View):
    def get(self,request,pk):
        cart = Cart.objects.new_or_get(request)
        cart_item = get_object_or_404(CartItem,id=pk)
        cart_item.delete()
        cart.save()
        #messages.warning(request,'product deleted from your cart')
        num_items_cart = cart.get_sum_items_amount()
        price = cart.get_sum_items_price()
        return JsonResponse({
                        "totalItemsInCart":num_items_cart,
                        "cartTotalPrice":price})
