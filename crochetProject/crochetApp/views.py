from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from django.db.models import Q
from .models import Pattern, Category, Author
from .serializers import PatternSerializer, CategorySerializer, AuthorSerializer

@api_view(['GET'])
def search(request):
    query = request.GET.get('q', '')
    if query:
        patterns = Pattern.objects.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        serializer = PatternSerializer(patterns, many=True)
        return Response(serializer.data)
    return Response([])

@api_view(['GET'])
def patterns_list(request):
    patterns = Pattern.objects.all()
    serializer = PatternSerializer(patterns, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_pattern(request):
    serializer = PatternSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# для стандартных операций CRUD (создание, чтение, обновление, удаление)
class PatternListCreateView(generics.ListCreateAPIView):
    queryset = Pattern.objects.all()
    serializer_class = PatternSerializer

class PatternDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pattern.objects.all()
    serializer_class = PatternSerializer
    
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
