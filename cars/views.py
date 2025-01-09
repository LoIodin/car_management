from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import PermissionDenied

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token

from .serializers import CarSerializer, CommentSerializer
from .models import Car, Comment
from .forms import CommentForm


# представление списка машин
class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'


# представление конкретной машины
class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    # метод для отправки комментариев
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.car = self.object
            comment.author = request.user
            comment.save()
            return redirect('car_detail', pk=self.object.pk)
        return self.get(request, *args, **kwargs)


# форма для добавления новых машин
class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    template_name = 'cars/car_form.html'
    fields = ['make', 'model', 'year', 'description']
    success_url = reverse_lazy('car_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


# форма для редактирования машины
class CarUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Car
    template_name = 'cars/car_form.html'
    fields = ['make', 'model', 'year', 'description']
    success_url = reverse_lazy('car_list')

    def test_func(self):
        car = self.get_object()
        return self.request.user == car.owner


# удаление машины
class CarDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Car
    success_url = reverse_lazy('car_list')

    def test_func(self):
        car = self.get_object()
        return self.request.user == car.owner


# форма регистрации
class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


# представление для отображения списка автомобилей и добавления машины через API
class CarListCreateAPIView(generics.ListCreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# представление для получения, обновления и удаления конкретного автомобиля
class CarDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.get_object().owner != self.request.user:
            raise PermissionDenied('Вы можете редактировать только свои автомобили.')
        serializer.save()

    def perform_destroy(self, instance):
        if instance.owner != self.request.user:
            raise PermissionDenied('Вы можете удалять только свои автомобили.')
        instance.delete()


# представление для получения и добавления комментариев к определенному автомобилю
class CarCommentAPIView(APIView):
    def get(self, request, pk):
        comments = Comment.objects.filter(car_id=pk)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, car_id=pk)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


# представление для отображения API документации
def api_info_view(request):
    return render(request, 'cars/api_info.html')
