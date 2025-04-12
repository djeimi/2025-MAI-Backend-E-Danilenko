from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from django.db.models import Q
from .models import Pattern, Category
from django.contrib.auth.models import User
from .serializers import PatternSerializer, CategorySerializer, UserSerializer

from django.contrib.auth.decorators import login_required

from django.core.exceptions import PermissionDenied
from rest_framework import status

from .utils import allow_anonymous

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
@login_required
def create_pattern(request):
    serializer = PatternSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
    # return Response({"message": f"Hello, {request.user.username}!"})


# для стандартных операций CRUD (создание, чтение, обновление, удаление)
class PatternListCreateView(generics.ListCreateAPIView):
    serializer_class = PatternSerializer

    def get_queryset(self):
        if not self.request.user.is_anonymous:
            queryset = Pattern.objects.filter(author=self.request.user)
        else:
            queryset = Pattern.objects.all()
        
        return queryset

class PatternDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PatternSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Pattern.objects.filter(id=pk)

    def delete(self, request, pk):
        pattern = Pattern.objects.get(id=pk)
        if pattern is not None:
            if self.request.user == pattern.author:
                pattern.delete()
                return Response({"detail": "Pattern {pattern.title} succesfully is deleted"}, status=status.HTTP_200_OK)
            else:
                raise PermissionDenied("You cannot delete this pattern.")
        else:
            raise PermissionDenied("You cannot delete this pattern, it doesn't exist.")
    
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        try:
            serializer = CategorySerializer(Category.objects.only('name').order_by('id')[pk-1])
            return Response(serializer.data)
        except:
            return Response(
                {"detail": f"Category with id {pk} not found"},
                status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
            )    
    
    def delete(self, request, *args, **kwargs):
        instance = self.get()
        self.perform_destroy(instance)
        return Response(
            {"detail": f"Category {instance.name} successfully deleted"},
            status=status.HTTP_200_OK
        )
    
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, pk):
        user = User.objects.get(id=pk)
        if user is not None:
            user.delete()
            return Response({"detail": "User {user.name} succesfully is deleted"}, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied("You cannot delete this user, he doesn't exist.")


from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def zone51(request):
    return render(request, 'area51.html')

@allow_anonymous
def anon(request):
    return render(request, 'anon.html')