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
    def get(self, request, *args, **kwargs):
        pk = self.kwargs['pk']
        if not self.request.user.is_anonymous:
            queryset = Pattern.objects.filter(author=self.request.user)
        else:
            queryset = Pattern.objects.all()
        try:
            serializer = PatternSerializer(queryset.order_by('id')[pk-1])
            return Response(serializer.data)
        except:
            return Response(
                {"detail": f"Pattern with id {pk} not found"},
                status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
            )   

    def delete(self, request, pk):
        pk = self.kwargs['pk']
        if not self.request.user.is_anonymous:
            queryset = Pattern.objects.filter(author=self.request.user)
        else:
            raise PermissionDenied("You cannot delete anything.")

        try:
            pattern = queryset.order_by('id')[pk-1]
        except:
            return Response(
                {"detail": f"Pattern with id {pk} not found"},
                status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
            )   
        
        if pattern is not None:
            pattern.delete()
            return Response({"detail": f"Pattern {pattern.title} succesfully is deleted"}, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied("You cannot delete this pattern, it doesn't exist.")
    
    def put(self, request, *args, **kwargs):
        if not self.request.user.is_anonymous:
            queryset = Pattern.objects.filter(author=self.request.user)
        else:
            queryset = Pattern.objects.all()

        pk = kwargs.get('pk')
        try:
            serializer = PatternSerializer(queryset.order_by('id')[pk-1], data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response(
                {"detail": f"Pattern with id {pk} not found"},
                status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
            )   

    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

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
        pk = self.kwargs['pk']
        try:
            instance = Category.objects.only('name').order_by('id')[pk-1]
        except:
            return Response(
                {"detail": f"Category with id {pk} not found"},
                status=status.HTTP_416_REQUESTED_RANGE_NOT_SATISFIABLE
            )    

        if self.request.user.is_anonymous:
            raise PermissionDenied("You cannot delete anything.")

        instance.delete()
        return Response(
            {"detail": f"Category {instance.name} successfully deleted"},
            status=status.HTTP_200_OK
        )
    
    def put(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            
            serializer = self.get_serializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
        except PermissionDenied as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_403_FORBIDDEN
            )

    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)

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
    if request.user.is_authenticated:
        user_patterns = Pattern.objects.filter(author=request.user)
    else:
        user_patterns = None
    
    context = {
        'user_patterns': user_patterns,
        'user_name': request.user.username
    }
    return render(request, 'index.html', context)

def zone51(request):
    return render(request, 'area51.html')

@allow_anonymous
def anon(request):
    return render(request, 'anon.html')