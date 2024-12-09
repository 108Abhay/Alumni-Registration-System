from django import forms
from .models import AlumniProfile

class AlumniRegistrationForm(forms.ModelForm):
    class Meta:
        model = AlumniProfile
        fields = [
            'full_name', 
            'email', 
            'phone_number', 
            'graduation_year', 
            'profession', 
            'experience', 
            'address', 
            'gender', 
            'profile_picture'
        ]
        widgets = {
            'graduation_year': forms.NumberInput(attrs={'min': 1970, 'max': 2024}),
            'experience': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if AlumniProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("An alumni with this email already exists.")
        return email