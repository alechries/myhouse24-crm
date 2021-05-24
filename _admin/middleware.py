from django.shortcuts import redirect
import importlib
from django.utils.cache import patch_vary_headers
import time
from django.utils.cache import patch_vary_headers
from django.utils.module_loading import import_string
from django.contrib.sessions.middleware import SessionMiddleware


class AccessCheckMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        path = request.path

        if '_admin' in path:
            if user.is_authenticated:
                if not user.is_superuser:
                    return redirect('admin_login')
            elif 'login' not in path:
                return redirect('admin_login')
        return self.get_response(request)


class AdminCookieSessionMiddleware(SessionMiddleware):

    def cookie_name(self, request):
        if request.path.startswith(u'/admin'):
            return 'admin_session_cookie'
        return 'user_session_cookie'
