from django.shortcuts import render,redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import BillingProfileForm
from .models import BillingProfile
from django.urls import reverse
# from .models import Guest
# from .forms import GuestForm
# from django.views import generic
#
# class GuestRegisterView(NextUrlMixin,RequestFormAttachMixin,generic.CreateView):
#     form_class = GuestForm
#     default_next = '/register/'
#     template_name = 'profiles/guest_register.html'
#
#     def get_success_url(self):
#         return self.get_next_url()
#
#     def form_invalid(self,form):
#         return redirect('profiles:register-guest')
#
class ProfileInfo(LoginRequiredMixin,generic.DetailView,generic.UpdateView):
    # model = BillingProfile
    form_class = BillingProfileForm
    template_name = 'profiles/profile.html'
    def get_object(self):
        pk = self.kwargs.get('pk')
        profile_id = BillingProfile.objects.get(user_id=pk)
        return profile_id

    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

class AdjustProfile(generic.UpdateView):
    form_class = BillingProfileForm
    template_name = 'profiles/adjust_profile.html'

    def get_object(self):
        pk = self.kwargs.get('pk')
        profile_id = BillingProfile.objects.get(user_id=pk)
        return profile_id

    def get_success_url(self):
        return reverse('payments:pay')

class AccountOverview(generic.TemplateView):
    template_name = 'profiles/account-overview.html'
