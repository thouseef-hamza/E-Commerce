from django.urls import path
from . import views

urlpatterns = [
    # path('games/',views.games,name='games'),
    path('<slug:category_slug>/',views.games,name='games'),
]
