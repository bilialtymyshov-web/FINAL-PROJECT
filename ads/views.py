from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from .models import Ad, Category


class AdListView(ListView):
    model = Ad
    template_name = 'ads/ad_list.html'
    context_object_name = 'ads'
    paginate_by = 10

    def get_queryset(self):
        return Ad.objects.filter(status='active').select_related('category', 'author')

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
