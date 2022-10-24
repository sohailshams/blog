from django import forms
from .models import BlogPost, BlogComment

class PostModelForm(forms.ModelForm):
    class Meta:
        """
        Telling django it is associated with BlogPost model
        """
        model = BlogPost

        # Render all fields
        fields = [
            'title',
            'description',
            'body'
        ]
    
    # Validating the form field
    def clean_body(self):
        # The call to super().clean() ensures that any validation logic in parent class is maintained i.e parent class = forms.ModelForm
        cleaned_data = super().clean() 
        data = self.cleaned_data.get('body')
        if len(data) < 20:
            raise forms.ValidationError('This is too short, please add more!')

        return data

    # Validating the form field
    def clean_description(self):
        # The call to super().clean() ensures that any validation logic in parent class is maintained i.e parent class = forms.ModelForm
        cleaned_data = super().clean() 
        data = self.cleaned_data.get('description')
        if len(data) > 400:
            raise forms.ValidationError('Description is too long, please add brief description.')

        return data
  
    # Validating the form field
    def clean_title(self):
        # The call to super().clean() ensures that any validation logic in parent class is maintained i.e parent class = forms.ModelForm
        cleaned_data = super().clean() 
        data = self.cleaned_data.get('title')
        if len(data) < 3:
            raise forms.ValidationError('This title is too short.')

        return data

    
    # Override the default init method which allows the form to be customized
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Added placehoder to the form fields
        self.fields['title'].widget.attrs['placeholder'] = 'Blog Title'
        self.fields['description'].widget.attrs['placeholder'] = 'Description'
        self.fields['body'].widget.attrs['placeholder'] = 'Please add blog description.'
        

        # Removed the form lables
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'my-5 shadow-lg'
            field.label = ""


class CommentModelForm(forms.ModelForm):

    class Meta:
        """
        Telling django it is associated with BlogComment model
        """
        model = BlogComment
    
        # Render comment_body field
       
        fields = [
            'comment_body',
        ]

    # Override the default init method which allows the form to be customized
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Added placehoder to the form fields
        self.fields['comment_body'].widget.attrs['placeholder'] = 'Please add comment here.'

        # Removed the form lables
        for field_name, field in self.fields.items():
            field.label = ""
