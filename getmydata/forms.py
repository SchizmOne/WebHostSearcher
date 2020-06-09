from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from getmydata.scripts.subnetmasks import get_subnet_masks


class NetDataForm(forms.Form):

    ip_address = forms.CharField()
    subnet_mask = forms.CharField()

    def clean_subnet_mask(self):
        data = self.cleaned_data['subnet_mask']

        # Проверка того, что маска введена корректно.
        subnet_masks = get_subnet_masks()
        if data not in subnet_masks:
            raise ValidationError(_('Invalid mask'))

        # Помните, что всегда надо возвращать "очищенные" данные.
        return data
