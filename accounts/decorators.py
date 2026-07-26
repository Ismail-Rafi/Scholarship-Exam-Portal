"""
Reusable role-based access decorators.
Usage:
    @role_required('STUDENT')
    def my_view(request): ...
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def role_required(*allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            if request.user.role not in allowed_roles:
                messages.error(request, "You are not authorized to view this page.")
                return redirect('accounts:redirect_dashboard')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
