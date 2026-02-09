from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Message, Reaction
from .forms import MessageForm, ReplyForm, SignUpForm

@login_required
def message_list(request):
    query = request.GET.get('q', '')
    messages_list = Message.objects.all().order_by('-timestamp')

    if query:
        messages_list = messages_list.filter(
            Q(text__icontains=query) | Q(author__username__icontains=query)
        )

    paginator = Paginator(messages_list, 10)  # Show 10 messages per page
    page_number = request.GET.get('page')
    messages = paginator.get_page(page_number)

    user_reactions = {}
    for message in messages:
        reaction = Reaction.objects.filter(user=request.user, message=message).first()
        if reaction:
            user_reactions[message.id] = reaction.reaction_type

    return render(request, 'messaging/message_list.html', {
        'messages': messages,
        'user_reactions': user_reactions,
        'query': query
    })

@login_required
def add_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.save()
            messages.success(request, 'Your message has been posted successfully!')
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
    valid_reactions = ['like', 'laugh', 'sad', 'fire', 'thumbs_up', 'angry']
    if reaction_type not in valid_reactions:
        return JsonResponse({'error': 'Invalid reaction type'}, status=400)

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

@login_required
def profile(request):
    user_messages = Message.objects.filter(author=request.user).order_by('-timestamp')
    total_messages = user_messages.count()
    total_reactions = sum(message.like_count + message.laugh_count + message.sad_count + message.fire_count for message in user_messages)

    context = {
        'user_messages': user_messages,
        'total_messages': total_messages,
        'total_reactions': total_reactions,
    }
    return render(request, 'messaging/profile.html', context)

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
