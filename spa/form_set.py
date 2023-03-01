from django import forms
from django.db import transaction
from django.forms import inlineformset_factory
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView

from spa.forms import CustomUserChangeForm, UserSubscriptionForm, PaymentForm
from spa.models import CustomUser, UserSubscription, Profile, Payment


class ProfileListWithPayment(CreateView):
    model = Profile
    form_class = CustomUserChangeForm
    # success_url = reverse_lazy('catalog:Product_list')
    template_name = 'spa/profile_form.html'


    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        FormSet = inlineformset_factory(self.model, Payment, form=PaymentForm, extra=1)
        # print('TTTTTTTTTTTT', self.object)
        if self.request.method == 'POST':
            formset = FormSet(self.request.POST, instance=self.object)#####Zdes rugaetsya, net objecta
            # print('GGGGGGGGGGGGGG', self.object)
        else:
            formset = FormSet(instance=self.object)

        context_data['formset'] = formset
        return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        print(self.request.method)
        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
            else:
                return super(ProfileListWithPayment, self).form_invalid(form)
        return super(ProfileListWithPayment, self).form_valid(form)


# class UserSubscriptionForm(forms.ModelForm):
#
#     class Meta:
#         model = UserSubscription
#         fields = '__all__'
