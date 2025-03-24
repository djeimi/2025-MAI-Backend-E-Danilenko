# from django.http import JsonResponse
# from django.views.decorators.http import require_http_methods

# @require_http_methods(["GET", "POST"])
# def profile(request):
#     return JsonResponse({'message': 'This is the profile endpoint.'})

# @require_http_methods(["GET", "POST"])
# def product_list(request):
#     return JsonResponse({'message': 'This is the product list endpoint.'})

# @require_http_methods(["GET", "POST"])
# def category_page(request):
#     return JsonResponse({'message': 'This is the category page endpoint.'})


from django.http import JsonResponse
from django.db.models import Q
from .models import Pattern
from django.views.decorators.http import require_http_methods

@require_http_methods(["GET"])
def search(request):
    query = request.GET.get('q', '')
    if query:
        patterns = Pattern.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        results = [{'title': pattern.title, 'description': pattern.description} for pattern in patterns]
        return JsonResponse({'results': results})
    return JsonResponse({'results': []})

@require_http_methods(["GET"])
def patterns_list(request):
    if request.method == 'GET':
        patterns = Pattern.objects.all().values('title', 'description', 'price', 'difficulty_level')
        return JsonResponse({'patterns': list(patterns)})
    return JsonResponse({'error': 'Invalid method'}, status=405)

import json
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@require_http_methods(["POST"])
def create_pattern(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        title = data.get('title')
        description = data.get('description')
        price = data.get('price')
        difficulty_level = data.get('difficulty_level')
        author_id = data.get('author_id')
        category_ids = data.get('category_ids', [])

        if title and description and author_id:
            pattern = Pattern.objects.create(
                title=title,
                description=description,
                price=price,
                difficulty_level=difficulty_level,
                author_id=author_id
            )
            pattern.categories.set(category_ids)
            return JsonResponse({'message': 'Pattern created successfully!'})
        return JsonResponse({'error': 'Invalid data'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)