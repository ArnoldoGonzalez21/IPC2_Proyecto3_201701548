from django import forms

class RangoForm(forms.Form):
   fecha_1 = forms.CharField(label="fecha_1")
   fecha_2 = forms.CharField(label="fecha_2")