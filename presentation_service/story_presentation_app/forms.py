from django import forms
from .models import PresentationStory
from file_manage.valid_type_file import validate_image_mimetype

class PresentationStoryForm(forms.ModelForm):
    class Meta:
        model = PresentationStory
        fields = [
            'title', 'subtitle', 'author', 'genre',
            'release_date', 'country_of_origin',
            'cast', 'synopsis', 'illustrations'
        ]
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date'}),
            'synopsis': forms.Textarea(attrs={'rows': 5}),
        }
    
    def clean_illustrations(self):
        image = self.cleaned_data.get('illustrations')
        if image:
            validate_image_mimetype(image)
        return image