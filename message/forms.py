from django import forms 
from .models import Message


class MessageModelForm(forms.ModelForm):

    class Meta:
        """
        Telling django it is associated with Message model
        """
        model = Message
                        
        # Render all fields except sender and receiver
        exclude = ('sender', 'receiver', 'msg_profile', 'chat', 'chat_profile', 'msg_sender',)

    # Override the default init method which allows the form to be customized
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Added placehoder to the form fields
        self.fields['msg_content'].widget.attrs['placeholder'] = 'Write a message...'

        # Removed the form lables
        for field_name, field in self.fields.items():
            field.label = ""
        