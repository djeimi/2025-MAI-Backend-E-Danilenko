from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET", "POST"])
def profile(request):
    return JsonResponse({'message': 'This is the profile endpoint.'})

@require_http_methods(["GET", "POST"])
def product_list(request):
    return JsonResponse({'message': 'This is the product list endpoint.'})

@require_http_methods(["GET", "POST"])
def category_page(request):
    return JsonResponse({'message': 'This is the category page endpoint.'})
