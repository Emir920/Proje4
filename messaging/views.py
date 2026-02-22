from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Message, Reaction, Task
from .forms import MessageForm, ReplyForm, SignUpForm, TaskForm

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
    total_reactions = sum(message.like_count + message.laugh_count + message.sad_count + message.fire_count + message.thumbs_up_count + message.angry_count for message in user_messages)

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
        total_reactions += message.thumbs_up_count
        total_reactions += message.angry_count
    
    return render(request, 'messaging/profile.html', {
        'user_profile': user_profile, 
        'user_messages': user_messages,
        'message_count': message_count,
        'total_reactions': total_reactions
    })


# Task Management Views
@login_required
def task_list(request):
    status_filter = request.GET.get('status', '')
    tasks = Task.objects.all().order_by('-created_at')
    
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    context = {
        'tasks': tasks,
        'status_filter': status_filter,
        'status_choices': Task.STATUS_CHOICES
    }
    return render(request, 'messaging/task_list.html', context)


@login_required
def add_task(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()
            messages.success(request, f"'{task.title}' görev başarıyla oluşturuldu!")
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'messaging/add_task.html', {'form': form})


@login_required
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            messages.success(request, f"'{task.title}' görev başarıyla güncellendi!")
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'messaging/edit_task.html', {'form': form, 'task': task})


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task_title = task.title
    task.delete()
    messages.success(request, f"'{task_title}' görev başarıyla silindi!")
    return redirect('task_list')


@login_required
def update_task_status(request, task_id):
    if request.method == 'POST':
        task = get_object_or_404(Task, id=task_id)
        new_status = request.POST.get('status')
        
        if new_status in dict(Task.STATUS_CHOICES):
            task.status = new_status
            if new_status == 'completed':
                task.completed_at = timezone.now()
            task.save()
            return JsonResponse({'success': True, 'status': task.get_status_display()})
    
    return JsonResponse({'success': False}, status=400)
