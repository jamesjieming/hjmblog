import re
import markdown
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from markdown.extensions.toc import TocExtension
from django.utils.text import slugify
from pure_pagination import PaginationMixin
from blog.models import Post, Category, Tag

#
# def index(request):
#     post_list = Post.objects.all()
#     return render(request, 'blog/index.html',context={'post_list': post_list})
#


class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    # ListView 传递了以下和分页有关的模板变量供我们在模板中使用：
    # paginator ，即 Paginator 的实例。
    # page_obj ，当前请求页面分页对象。
    # is_paginated，是否已分页。只有当分页后页面超过两页时才算已分页。
    # object_list，请求页面的对象列表，和 post_list 等价。所以在模板中循环文章列表时可以选 post_list ，也可以选 object_list。
    paginate_by = 10


class FullWidthView(IndexView):
    template_name = 'blog/full-width.html'
    
# def detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     md = markdown.Markdown(extensions=[
#         'markdown.extensions.extra',
#         'markdown.extensions.codehilite',
#         TocExtension(slugify=slugify),
#     ])
#     post.body = md.convert(post.body)
# # 空目录处理
#     m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
#     post.toc = m.group(1) if m is not None else ''
#
#     return render(request, 'blog/detail.html', context={'post': post})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    # 默认获取url中的pk 这个名字是 DetailView 用来查找过滤查询集的主键值的默认名称。
    # 如果想用其他名字，你可以在视图上设置 pk_url_kwarg(默认pk_url_kwarg='pk')
    # slug_url_kwarg(默认slug_url_kwarg='slug'）
    def get_object(self, queryset=None):
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                TocExtension(slugify=slugify),
        ])
        post.body = md.convert(post.body)
        # 空目录处理
        m = re.search(r'<div class="toc">\s*<ul>(.*)</ul>\s*</div>', md.toc, re.S)
        post.toc = m.group(1) if m is not None else ''
        return post


# def archive(request, year, month):
#     post_list = Post.objects.filter(created_time__year=year,
#                                     created_time__month=month,
#                                     ).order_by('-created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class ArchiveView(IndexView):
    # url中的参数在self.kwargs字典中
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        return Post.objects.filter(created_time__year=year,
                                   created_time__month=month,
                                   ).order_by('-created_time')

# def category(request, name):
#     cate = get_object_or_404(Category, name=name)
#     post_list = Post.objects.filter(category=cate).order_by('created_time')
#     return render(request, 'blog/index.html', context={'post_list': post_list})


class CategoryView(IndexView):
    def get_queryset(self):
        cate = get_object_or_404(Category, name=self.kwargs.get('name'))
        return Post.objects.filter(category=cate)


# def tag(request, name):
#     t = get_object_or_404(Tag, name=name)
#     post_list = Post.objects.filter(tags=t)
#     return render(request, 'blog/index.html', context={'post_list': post_list})

class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, name=self.kwargs.get('name'))
        return Post.objects.filter(tags=tag)


def search(request):
    q = request.GET.get('q')
    if not q:
        error_msg = "请输入搜索关键词"
        messages.add_message(request, messages.ERROR, error_msg, extra_tags='danger')
        return redirect('blog:index')
    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'post_list': post_list})
