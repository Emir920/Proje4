from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message, Reaction
from .forms import MessageForm, ReplyForm, SignUpForm

@login_required
def message_list(request):
    messages = Message.objects.all().order_by('-timestamp')
    user_reactions = {}
    for message in messages:
        reaction = Reaction.objects.filter(user=request.user, message=message).first()
        if reaction:
            user_reactions[message.id] = reaction.reaction_type
    return render(request, 'messaging/message_list.html', {'messages': messages, 'user_reactions': user_reactions})

@login_required
def add_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.save()
            return redirect('message_list')
    else:
        form = MessageForm()
    return render(request, 'messaging/add_message.html', {'form': form})

@login_required
def add_reply(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.message = message
            reply.author = request.user
            reply.save()
            return redirect('message_list')
    else:
        form = ReplyForm()
    return render(request, 'messaging/add_reply.html', {'form': form, 'message': message})

@login_required
def react(request, message_id, reaction_type):
    if request.method == 'POST':
        message = get_object_or_404(Message, id=message_id)
        existing_reaction = Reaction.objects.filter(user=request.user, message=message).first()
        if existing_reaction:
            if existing_reaction.reaction_type == reaction_type:
                # If same reaction, do nothing (or toggle off, but template doesn't support toggle)
                return JsonResponse({'count': getattr(message, f'{reaction_type}_count')})
            else:
                # Change reaction: decrement old, increment new
                old_type = existing_reaction.reaction_type
                setattr(message, f'{old_type}_count', getattr(message, f'{old_type}_count') - 1)
                setattr(message, f'{reaction_type}_count', getattr(message, f'{reaction_type}_count') + 1)
                existing_reaction.reaction_type = reaction_type
                existing_reaction.save()
        else:
            # New reaction
            setattr(message, f'{reaction_type}_count', getattr(message, f'{reaction_type}_count') + 1)
            Reaction.objects.create(user=request.user, message=message, reaction_type=reaction_type)
        message.save()
        return JsonResponse({'count': getattr(message, f'{reaction_type}_count')})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.author == request.user:
        message.delete()
        messages.success(request, 'Message deleted successfully.')
    else:
        messages.error(request, 'You can only delete your own messages.')
    return redirect('message_list')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('message_list')
    else:
        form = SignUpForm()
    return render(request, 'messaging/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('message_list')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'messaging/login.html')

@login_required
def profile(request, username):
    from django.contrib.auth import get_user_model
    User = get_user_model()
    user_profile = get_object_or_404(User, username=username)
    user_messages = Message.objects.filter(author=user_profile).order_by('-timestamp')
    
    # Calculate message count
    message_count = user_messages.count()
    
    # Calculate total reactions on all messages
    total_reactions = 0
    for message in user_messages:
        total_reactions += message.fire_count
        total_reactions += message.laugh_count
        total_reactions += message.like_count
        total_reactions += message.sad_count
    
    return render(request, 'messaging/profile.html', {
        'user_profile': user_profile, 
        'user_messages': user_messages,
        'message_count': message_count,
        'total_reactions': total_reactions
    })
