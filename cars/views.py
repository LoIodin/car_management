from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Car, Comment
from .forms import CommentForm


# Create your views here.
class CarListView(ListView):
    model = Car
    template_name = 'car_list.html'
    context_object_name = 'cars'


class CarDetailView(DetailView):
    model = Car
    template_name = 'cars/car_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

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


class CarCreateView(LoginRequiredMixin, CreateView):
    model = Car
    template_name = 'car_form.html'
    fields = ['make', 'model', 'year', 'description']
    success_url = reverse_lazy('car_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CarUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Car
    template_name = 'car_form.html'
    fields = ['make', 'model', 'year', 'description']
    success_url = reverse_lazy('car_list')

    def test_func(self):
        car = self.get_object()
        return self.request.user == car.owner


class CarDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Car
    template_name = 'car_confirm_delete.html'
    success_url = reverse_lazy('car_list')

    def test_func(self):
        car = self.get_object()
        return self.request.user == car.owner


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        return response
