from django import forms


class ImageUploadForm(forms.Form):
    user_id = forms.CharField()
    image = forms.ImageField()
