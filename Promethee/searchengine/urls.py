#APP SEARCHENGINE

from django.urls import path
from . import views
urlpatterns = [
    path('search', views.search, name='search'),
    path('reference/<int:reference_id>/', views.reference_detail, name='reference_detail'),
    path('publisher/<int:publisher_id>/', views.publisher_detail, name='publisher_detail'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('genres', views.genres, name='genres'),
    path('countries', views.country_detail, name='country_detail'),
    
    path('add_reference', views.add_reference, name='add_reference'),
    path('add_publisher', views.add_publisher, name='add_publisher'),
    path('add_author', views.add_author, name='add_author'),
    
    path('update_reference/<int:reference_id>/', views.update_reference, name='update_reference'),
    path('update_publisher/<int:publisher_id>/', views.update_publisher, name='update_publisher'),
    path('update_author/<int:author_id>/', views.update_author, name='update_author'),
]