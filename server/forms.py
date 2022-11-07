from django import forms

class Codeform(forms.Form):
    code = forms.IntegerField(label="Code")
