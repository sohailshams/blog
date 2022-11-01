from django.shortcuts import  render, redirect, reverse
from django.utils import timezone as tz
from .forms import MessageModelForm
from .models import Message, Chat
from accounts.models import Profile
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def message_add_view(request, **kwargs):
    """ A view to add message """
    receiver = kwargs.get('username', None)
    sender = request.user
    current_time = tz.now()

    # Get user or return error message & redirect to home page
    try:
        receiver_user = User.objects.get(username=receiver)
    except:
        messages.error(request, 'Sorry, this user does not exist.')
        return redirect(reverse('home'))

    # Get receiver user profile or return error message & redirect to home page
    try:
        receiver_profile = Profile.objects.get(user=receiver_user)
    except:
        messages.error(request, 'Sorry, this profile does not exist.')
        return redirect(reverse('home'))

    # Get sender user profile or return error message & redirect to home page
    try:
        sender_profile = Profile.objects.get(user=sender)
    except:
        messages.error(request, 'Sorry, this profile does not exist.')
        return redirect(reverse('home'))

    # Get chats list
    chats_list = Chat.objects.filter(chat_profile=sender_profile)

    # Get chats list
    chats_list_two = Chat.objects.filter(chat_profile=receiver_profile)

    # Check if chats list contains chats else create an empty list
    if len(chats_list):
        # Loop over chats_list and conditionally set filters based on user 
        for chat in chats_list:
            filters = {
            
            }
            if chat.chat_profile.user == receiver_user:
                filters['sender'] = receiver_user
                filters['receiver'] = sender
            else:
                filters['sender'] = sender
                filters['receiver'] = receiver_user

            # Get chat related to relevant sender and receiver
            msg_chat_list_one = Chat.objects.filter(**filters)

        # Get messages list
        if len(msg_chat_list_one):
            msg_chat_one=msg_chat_list_one[0]
            messages_list = Message.objects.filter(
                chat=msg_chat_one
            )
    
            # Check if message exists and update datetime format
            if len(messages_list):
                for message in messages_list:

                    # Check if message created day is same as today
                    if message.created.day == current_time.day:
                        message_datetime = message.created.strftime('Today,%I:%M%p')
                    else:
                        message_datetime = message.created.strftime("%b %y,%I:%M%p") 
        else:
         messages_list = []
    else:
         messages_list = []
   
    # Check if chats_list_two contains chats else create an empty list
    if len(chats_list_two):
        # Loop over chats_list and conditionally set filters based on user 
        for chat in chats_list_two:
            filters = {
            
            }
            if chat.chat_profile.user == receiver_user:
                filters['sender'] = receiver_user
                filters['receiver'] = sender
            else:
                filters['sender'] = sender
                filters['receiver'] = receiver_user

            # Get chat related to relevant sender and receiver
            msg_chat_list_two = Chat.objects.filter(**filters)

        # Get messages list
        if len(msg_chat_list_two):
            msg_chat_two=msg_chat_list_two[0]
            messages_list_two = Message.objects.filter(
                chat=msg_chat_two
            )
            # Check if message exists and update datetime format
            if len(messages_list_two):
                for message in messages_list_two:

                    # Check if message created day is same as today
                    if message.created.day == current_time.day:
                        message_datetime = message.created.strftime('Today,%I:%M%p')
                    else:
                        message_datetime = message.created.strftime("%b %y,%I:%M%p") 
        else:
            messages_list_two = []
    else:
        messages_list_two = []

    # Conditionally set values of messages_list, msg_chat and message_datetime
    if messages_list:
        messages_list=messages_list
        msg_chat=msg_chat_one
    elif messages_list_two:
        messages_list=messages_list_two
        msg_chat=msg_chat_two
    else:
        messages_list=[]
        msg_chat=[]
        message_datetime=''
        

    if request.method == 'POST':
        # Get chat or create chat 
        if msg_chat:
            chat = Chat.objects.get(
                    chat_uuid= msg_chat.chat_uuid  
            ) 
        else:
            chat = Chat.objects.create(
                sender=sender,
                receiver=receiver_user,
                chat_profile= sender_profile  
            ) 
            
        # Set sender's role
        msg_sender = 'msgsender' if chat.sender == sender else 'msgreceiver'

        # Instantiate a new instance of blog post form
        form = MessageModelForm(request.POST or None)
        if form.is_valid():
            message_obj = form.save(commit=False)
            message_obj.chat = chat
            message_obj.msg_sender = msg_sender
            message_obj.save()

            return redirect(reverse('message_add', args=[receiver]))
    else:
        # Empty form instantiation
        form = MessageModelForm()

    template_name = 'message.html'

    context = {
        'form': form,
        'receiver_user': receiver_user,
        'messages_list': messages_list,
        'current_time': current_time,
        'message_datetime': message_datetime
    }

    return render(request, template_name, context)
