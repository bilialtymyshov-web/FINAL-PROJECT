from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import AdForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from .models import Ad, Category
from django.db.models import Q
from django.views.generic import ListView
from .models import Ad, Category


class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'

    def get_queryset(self):
        queryset = Ad.objects.filter(status='active').select_related('category', 'author')

        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(title__icontains=query)

        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        min_price = self.request.GET.get('min_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        max_price = self.request.GET.get('max_price')
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class AdDetailView(DetailView):
    model = Ad
    template_name = 'ads/ad_detail.html'
    context_object_name = 'ad'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        Ad.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
        obj.refresh_from_db()
        return obj


class MyAdsListView(LoginRequiredMixin, ListView):
    model = Ad
    template_name = 'ads/my_ads.html'
    context_object_name = 'ads'

    def get_queryset(self):
        return Ad.objects.filter(author=self.request.user).select_related('category')

class AdCreateView(LoginRequiredMixin, CreateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:my_ads')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = 'ads/ad_form.html'
    success_url = reverse_lazy('ads:my_ads')

    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.author


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = 'ads/ad_confirm_delete.html'
    success_url = reverse_lazy('ads:my_ads')

    def test_func(self):
        ad = self.get_object()
        return self.request.user == ad.author
