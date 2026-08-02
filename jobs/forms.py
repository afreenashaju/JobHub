from django import forms
from .models import Job, Application

class UploadCSVForm(forms.Form):
    csv_file = forms.FileField(
        label="Select CSV File"
    )
from .models import Application

class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = [
            "applicant_name",
            "email",
            "phone",
            "resume",
            "cover_letter",
        ]

        widgets = {
            "applicant_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your full name",
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
            }),

            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your phone number",
            }),

            "cover_letter": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 6,
                "placeholder": "Write your cover letter...",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["resume"].widget.attrs.update({
            "class": "form-control",
        })
class PasteExcelForm(forms.Form):
    excel_data = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 15,
            "class": "form-control",
            "placeholder": "Paste Excel data here..."
        })
    )
class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = "__all__"