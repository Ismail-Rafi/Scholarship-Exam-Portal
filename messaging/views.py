from django.shortcuts import render, redirect
from django.contrib import messages as flash
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from accounts.decorators import role_required
from accounts.models import User
from .models import SupportMessage
from .forms import SupportMessageForm, ReplyForm


@role_required(User.Role.STUDENT)
def send_message(request):
    if request.method == 'POST':
        form = SupportMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.student = request.user
            msg.save()
            flash.success(request, "Your message has been sent to support.")
            return redirect('messaging:my_messages')
    else:
        form = SupportMessageForm()
    return render(request, 'messaging/send_message.html', {'form': form})


@role_required(User.Role.STUDENT)
def my_messages(request):
    msgs = SupportMessage.objects.filter(student=request.user)
    return render(request, 'messaging/my_messages.html', {'messages_list': msgs})


@role_required(User.Role.STAFF, User.Role.ADMIN)
def inbox(request):
    msgs = SupportMessage.objects.select_related('student').all()
    return render(request, 'messaging/inbox.html', {'messages_list': msgs})


@role_required(User.Role.STAFF, User.Role.ADMIN)
def reply_message(request, pk):
    msg = SupportMessage.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReplyForm(request.POST, instance=msg)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.status = SupportMessage.Status.REPLIED
            msg.replied_at = timezone.now()
            msg.save()
            flash.success(request, "Reply sent.")
            return redirect('messaging:inbox')
    else:
        form = ReplyForm(instance=msg)
    return render(request, 'messaging/reply_message.html', {'form': form, 'msg': msg})
