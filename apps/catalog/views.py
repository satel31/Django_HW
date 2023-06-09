from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect

from apps.catalog.forms import ProductForm, VersionForm
from apps.catalog.models import Product, Post, Version
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy, reverse
from apps.catalog.services import send_email, get_categories_cache


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:products')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        owner_id = self.request.user.id
        kwargs.update({'owner_id': owner_id})
        return kwargs

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class ProductListView(ListView):
    model = Product
    extra_context = {
        'title': 'Products',
        'categories': get_categories_cache(),
    }


class ProductByPageListView(ListView):
    model = Product
    template_name = 'catalog/products_by_page_list.html'
    paginate_by = 3
    extra_context = {
        'title': 'All products'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['object'].product_name
        return context_data


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm

    def test_func(self):
        return self.request.user == self.get_object().owner

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormset(instance=self.object)
        return context_data

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('catalog:product', kwargs={'pk': self.kwargs['pk']})


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:products')

    def test_func(self):
        return self.request.user == self.get_object().owner


class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    fields = ('post_title', 'text', 'preview')
    permission_required = 'catalog.add_post'
    success_url = reverse_lazy('catalog:blog')


class PostListView(ListView):
    model = Post
    extra_context = {
        'title': 'Our blog'
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_published=True)
        return queryset


class PostDetailView(DetailView):
    model = Post

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['title'] = context_data['object'].post_title
        return context_data

    def get_object(self, queryset=None):
        object = self.model.objects.get(pk=self.kwargs['pk'])
        if object:
            object.views += 1
            object.save()
            if object.views == 100:
                send_email(object.post_title)
        return object


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    fields = ('post_title', 'text', 'slug', 'preview')
    permission_required = 'catalog.change_post'

    def get_success_url(self):
        return reverse_lazy('catalog:post', kwargs={'pk': self.kwargs['pk']})


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    model = Post
    permission_required = 'catalog.delete_post'
    success_url = reverse_lazy('catalog:blog')


def toggle_activity(request, pk):
    post_item = get_object_or_404(Post, pk=pk)
    if post_item.is_published:
        post_item.is_published = False
    else:
        post_item.is_published = True

    post_item.save()

    return redirect(reverse('catalog:post', args=[post_item.pk]))
