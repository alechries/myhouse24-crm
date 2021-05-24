import time
from importlib import import_module
from django.conf import settings
from django.contrib.sessions.backends.base import UpdateError
from django.core.exceptions import SuspiciousOperation
from django.utils.cache import patch_vary_headers
from django.utils.deprecation import MiddlewareMixin
from django.utils.http import http_date
from django.shortcuts import redirect
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware


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
        name = settings.SESSION_COOKIE_NAME
        return 'admin_' + name if request.path.startswith('/admin') else 'cabinet_' + name

    def process_request(self, request):
        print(self.cookie_name(request))
        session_key = request.COOKIES.get(self.cookie_name(request))
        request.session = self.SessionStore(session_key)
