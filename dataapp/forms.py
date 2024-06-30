from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            file_type = file.name.split('.')[-1].lower()
            if file_type not in ['csv', 'json']:
                raise forms.ValidationError('Invalid file Type. File must be a CSV or JSON.')
        return file

