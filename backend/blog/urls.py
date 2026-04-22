from django.urls import path
from . import views

urlpatterns = [
    # Public
    path('posts/', views.blog_post_list, name='blog-post-list'),
    path('posts/<slug:slug>/', views.blog_post_detail, name='blog-post-detail'),
    path('categories/', views.blog_category_list, name='blog-category-list'),
    path('categories/<slug:slug>/', views.blog_category_detail, name='blog-category-detail'),
    path('tags/', views.blog_tag_list, name='blog-tag-list'),
    path('tags/<slug:slug>/', views.blog_tag_detail, name='blog-tag-detail'),
    path('niveaux/', views.blog_niveau_list, name='blog-niveau-list'),
    path('types/', views.blog_content_type_list, name='blog-content-type-list'),
    path('sitemap/', views.blog_sitemap, name='blog-sitemap'),

    # Admin CRUD — articles
    path('admin/posts/', views.admin_post_list, name='blog-admin-post-list'),
    path('admin/posts/create/', views.admin_post_create, name='blog-admin-post-create'),
    path('admin/posts/<int:pk>/', views.admin_post_update, name='blog-admin-post-update'),
    path('admin/posts/<int:pk>/delete/', views.admin_post_delete, name='blog-admin-post-delete'),

    # Admin CRUD — catégories
    path('admin/categories/', views.admin_category_list, name='blog-admin-category-list'),
    path('admin/categories/create/', views.admin_category_create, name='blog-admin-category-create'),
    path('admin/categories/<int:pk>/', views.admin_category_update, name='blog-admin-category-update'),
    path('admin/categories/<int:pk>/delete/', views.admin_category_delete, name='blog-admin-category-delete'),

    # Admin CRUD — tags
    path('admin/tags/', views.admin_tag_list, name='blog-admin-tag-list'),
    path('admin/tags/create/', views.admin_tag_create, name='blog-admin-tag-create'),
    path('admin/tags/<int:pk>/', views.admin_tag_update, name='blog-admin-tag-update'),
    path('admin/tags/<int:pk>/delete/', views.admin_tag_delete, name='blog-admin-tag-delete'),

    # Admin CRUD — niveaux
    path('admin/niveaux/', views.admin_niveau_list, name='blog-admin-niveau-list'),
    path('admin/niveaux/create/', views.admin_niveau_create, name='blog-admin-niveau-create'),
    path('admin/niveaux/<int:pk>/', views.admin_niveau_update, name='blog-admin-niveau-update'),
    path('admin/niveaux/<int:pk>/delete/', views.admin_niveau_delete, name='blog-admin-niveau-delete'),

    # Admin CRUD — types de contenu
    path('admin/types/', views.admin_content_type_list, name='blog-admin-content-type-list'),
    path('admin/types/create/', views.admin_content_type_create, name='blog-admin-content-type-create'),
    path('admin/types/<int:pk>/', views.admin_content_type_update, name='blog-admin-content-type-update'),
    path('admin/types/<int:pk>/delete/', views.admin_content_type_delete, name='blog-admin-content-type-delete'),
]
