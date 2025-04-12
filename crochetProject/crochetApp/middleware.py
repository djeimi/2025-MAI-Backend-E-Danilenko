from django.shortcuts import redirect
from django.urls import reverse

class CheckAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        # print(request.user, request.path_info, request.user.is_authenticated, request.path_info == (reverse('home')))
        if getattr(view_func, 'allow_anonymous', False):
            return None
        if not request.user.is_authenticated and not request.path_info == (reverse('home')) and not request.path_info.startswith('/auth') and not request.path_info.startswith('/api') and not request.path_info.startswith('/admin'):
            return redirect('home')
