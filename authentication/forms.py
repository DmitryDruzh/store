from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        try:
            self.user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(f'The user with name "{username}" does not exist')
        if not self.user.check_password(password):
            raise forms.ValidationError(f'The pass is wrong. Please, try again')

        return cleaned_data

class RegisterForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
            visible.field.widget.attrs['onfocus'] = "this.placeholder = ''"
            visible.field.widget.attrs['onblur'] = f"this.placeholder = '{visible.name.title()}'"

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(),
        }
