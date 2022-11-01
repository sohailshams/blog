import uuid
from django.db import models
from accounts.models import Profile


class Chat(models.Model):
    """
    A Chat model to allow creating a chat
    """
    chat_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    sender = models.ForeignKey('auth.User', related_name="sender", on_delete=models.CASCADE)
    receiver = models.ForeignKey('auth.User', related_name="receiver", on_delete=models.CASCADE)
    chat_profile = models.ForeignKey(Profile, related_name='user_chat', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Chat'
        verbose_name_plural = 'Chats'
        

SENDER_CHOICES = (
    ('msgsender', 'MsgSender'),
    ('msgreceiver', 'MsgReceiver')
)


class Message(models.Model):
    message_uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    chat = models.ForeignKey(Chat, related_name='user_messages', on_delete=models.CASCADE)
    msg_content = models.TextField(blank=False)
    msg_sender = models.CharField(choices=SENDER_CHOICES,  max_length=11)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.chat.sender.username
