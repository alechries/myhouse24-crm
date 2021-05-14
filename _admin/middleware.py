from django.shortcuts import redirect
import importlib
from django.utils.cache import patch_vary_headers



class AccessCheckMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        path = request.path

        if 'app-admin' in path:
            if user.is_authenticated:
                if not user.is_superuser:
                    return redirect('admin_login')
            elif 'login' not in path:
                return redirect('admin_login')
        return self.get_response(request)
