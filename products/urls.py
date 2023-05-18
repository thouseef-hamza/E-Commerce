from django.urls import path
from . import views

urlpatterns = [
    # path('games/',views.games,name='games'),
    path('<slug:category_slug>/',views.products,name='products'),
    path('<slug:category_slug>/<slug:product_slug>',views.product_detail,name='product_detail'),
]
