from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re
from django.contrib.auth.forms import AuthenticationForm
from .models import Subject, AnswerSheet,Student, Evaluation, EvaluationDetail
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # Username validation
    def clean_username(self):
        username = self.cleaned_data.get("username")
        if len(username) < 6:
            raise forms.ValidationError("Username must be at least 6 characters long.")
        return username

    # Password validation
    def clean_password1(self):
        password = self.cleaned_data.get("password1")

        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("Password must contain at least one digit.")
        if not re.search(r'[@$!%*?&]', password):
            raise forms.ValidationError("Password must contain at least one special character (@$!%*?&).")
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")

        return password
    
    # Email validation
    def clean_email(self):
        email = self.cleaned_data.get("email")
        allowed_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com"]
        domain = email.split('@')[-1].lower()

        if domain not in allowed_domains:
            raise forms.ValidationError("Please use a valid email (gmail, yahoo, outlook, hotmail, icloud).")
        
        return email   

# forms.py
class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Username"
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Password"
    }))

class PasswordResetForm(forms.Form):
    username = forms.CharField(max_length=150)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
class AnswerSheetUploadForm(forms.ModelForm):
    rollno = forms.IntegerField(
        label="Roll Number",
        widget=forms.NumberInput(attrs={
            'class': 'w-full p-3 border rounded-lg',
            'placeholder': 'Enter Roll Number'
        })
    )

    subject_name = forms.CharField(
        label="Subject",
        widget=forms.TextInput(attrs={
            'class': 'w-full p-3 border rounded-lg',
            'placeholder': 'Start typing subject...'
        })
    )

    answer_sheet = forms.FileField(
        label="Answer Sheet",
        widget=forms.ClearableFileInput(attrs={
            'class': 'w-full p-3 border rounded-lg',
            'accept': 'image/*,application/pdf'
        })
    )

    class Meta:
        model = AnswerSheet
        fields = ['rollno', 'answer_sheet']  # ⚠ subject excluded, handled manually

class EvaluationForm(forms.Form):
    answer_sheet = forms.ModelChoiceField(   # 🔥 rename to match model
        queryset=AnswerSheet.objects.all(),
        label="Select Answer Sheet",
        empty_label="Choose an answer sheet",
        widget=forms.Select(attrs={'class': 'border rounded p-2 w-full'})
    )

    # Q1–Q10 (4 marks each)
    for i in range(1, 11):
        locals()[f"mark_q4_{i}"] = forms.IntegerField(
            label=f"Q{i} Marks",
            required=False,
            min_value=0,
            max_value=4,
            widget=forms.NumberInput(attrs={'class': 'border rounded w-20'})
        )
        locals()[f"comment_q4_{i}"] = forms.CharField(
            label=f"Q{i} Comment",
            required=False,
            widget=forms.Textarea(attrs={'class': 'border rounded w-full', 'rows': 2})
        )

    # Q11–Q22 (10 marks each)
    for i in range(11, 23):
        locals()[f"mark_q10_{i}"] = forms.IntegerField(
            label=f"Q{i} Marks",
            required=False,
            min_value=0,
            max_value=10,
            widget=forms.NumberInput(attrs={'class': 'border rounded w-20'})
        )
        locals()[f"comment_q10_{i}"] = forms.CharField(
            label=f"Q{i} Comment",
            required=False,
            widget=forms.Textarea(attrs={'class': 'border rounded w-full', 'rows': 2})
        )

    # Checkbox field for Q11–Q22
    for i in range(11, 23):
        locals()[f"q10_checkbox_{i}"] = forms.BooleanField(
            label=f"Select Q{i}",
            required=False,
            widget=forms.CheckboxInput(attrs={'class': 'q10-checkbox', 'value': f"{i}"})
        )


# Form to select a subject
class SubjectSelectForm(forms.Form):
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        label="Select Subject",
        widget=forms.Select(attrs={'class': 'border rounded p-2 w-full'})
    )

# Form to select a student
class StudentSelectForm(forms.Form):
    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        label="Select Student",
        widget=forms.Select(attrs={'class': 'border rounded p-2 w-full'})
    )

# ---------------------------
# Export Results Form
# ---------------------------
class ExportResultsForm(forms.Form):
    EXPORT_CHOICES = [
        ("pdf", "Download as PDF"),
        ("word", "Download as Word (.docx)"),
        ("excel", "Download as Excel (.xlsx)"),
        ("csv", "Download as CSV"),
    ]

    subject = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        required=False,
        label="Filter by Subject",
        widget=forms.Select(attrs={"class": "border rounded p-2 w-full"}),
    )

    student = forms.ModelChoiceField(
        queryset=Student.objects.all(),
        required=False,
        label="Filter by Student",
        widget=forms.Select(attrs={"class": "border rounded p-2 w-full"}),
    )

    export_format = forms.ChoiceField(
        choices=EXPORT_CHOICES,
        label="Choose Export Format",
        widget=forms.RadioSelect,
    )