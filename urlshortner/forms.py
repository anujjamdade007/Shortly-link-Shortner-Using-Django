from django.contrib.auth.models import User
from django import forms
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }
    
class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 
    		    'password', 
    		    'email', 
    		    'first_name', 
    		    'last_name'
                ]
        widgets = {
            'password': forms.PasswordInput(render_value=True),
        }

        def __init__(self, *args, **kwargs):
            super(UserRegistrationForm, self).__init__(*args, **kwargs)

            for name, field in self.fields.items():
                field.widget.attrs.update({'class': 'input'})