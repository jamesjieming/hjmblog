from django.urls import path

from blog import views

app_name = 'blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('fullwidths/', views.FullWidthView.as_view(), name='fullwidth'),
    path('fullwidths/<int:pk>/', views.PostDetailView.as_view(template_name='blog/full-detail.html'), name='fulldetail'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='detail'),
    path('archives/<int:year>/<int:month>/', views.ArchiveView.as_view(), name='archive'),
    path('categories/<str:name>/', views.CategoryView.as_view(), name='category'),
    path('tags/<str:name>/', views.TagView.as_view(), name='tag'),
    path('search/', views.search, name='search'),
]
