from django import forms

##### FORM TO CONNECT WITH MAIL
class MailPostForm(forms.Form):
    name        = forms.CharField(max_length=250)
    email       = forms.EmailField()
    to          = forms.EmailField()
    comments    = forms.CharField(required=False, widget=forms.Textarea)