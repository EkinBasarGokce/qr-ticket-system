from django import forms
from .models import Ticket


class TicketCreationForm(forms.ModelForm):
    """Form for creating tickets"""
    
    class Meta:
        model = Ticket
        fields = ['attendee_name', 'plus_ones']
        widgets = {
            'attendee_name': forms.TextInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': 'Adınız ve Soyadınız',
                'required': True
            }),
            'plus_ones': forms.NumberInput(attrs={
                'class': 'form-control form-control-lg',
                'placeholder': '0',
                'min': '0',
                'value': '0',
                'required': True
            })
        }
        labels = {
            'attendee_name': 'Ad Soyad',
            'plus_ones': 'Kaç Kişi Getireceksiniz? (+1, +2, vb.)'
        }
    
    def clean_plus_ones(self):
        """Validate plus_ones is not negative"""
        plus_ones = self.cleaned_data.get('plus_ones')
        if plus_ones < 0:
            raise forms.ValidationError('Plus ones cannot be negative.')
        return plus_ones

