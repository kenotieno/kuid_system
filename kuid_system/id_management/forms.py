from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, StudentID

class UserRegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=CustomUser.USER_TYPE_CHOICES,
        initial=1,
        widget=forms.RadioSelect
    )
    phone_number = forms.CharField(max_length=15, required=False)
    department = forms.CharField(max_length=100, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type', 'phone_number', 'department']

class IDSearchForm(forms.Form):
    id_number = forms.CharField(label='ID Number', required=False)
    student_name = forms.CharField(label='Student Name', required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('id_number') and not cleaned_data.get('student_name'):
            raise forms.ValidationError("Please provide at least one search criteria.")

class IDForm(forms.ModelForm):
    class Meta:
        model = StudentID
        fields = ['id_number', 'student_name', 'course', 'found_by', 'found_date']
        widgets = {
            'found_date': forms.DateInput(attrs={'type': 'date'}),
        }

class ClaimIDForm(forms.Form):
    verification_code = forms.CharField(label='Verification Code', max_length=6)

class LostIDForm(forms.ModelForm):
    lost_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        required=True,
    )

    class Meta:
        model = StudentID
        fields = ["id_number", "student_name", "course", "lost_date"]
        widgets = {
            "id_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter student ID number"}),
            "student_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter full name"}),
            "course": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter course name"}),
        }