from django import forms 
from captcha.fields import ReCaptchaField 
from captcha.widgets import ReCaptchaV3
from website.models import Contact 

class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact 
		fields = ['name', 'email', 'message']
	captcha = ReCaptchaField(
		required=True
	)
