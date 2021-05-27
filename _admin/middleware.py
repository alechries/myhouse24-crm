from django.conf import settings
from django.shortcuts import redirect
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.auth import logout


class AccessCheckMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        path = request.path

        if user.is_authenticated:
            if 'login' not in path:
                if user.is_superuser:
                    if 'cabinet' in path:
                        logout(request)
                        return redirect('cabinet_login')
                else:
                    if 'admin' in path:
                        logout(request)
                        return redirect('admin_login')
        else:
            if 'login' not in path:
                if 'cabinet' in path:
                    logout(request)
                    return redirect('cabinet_login')
                elif 'admin' in path:
                    logout(request)
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
