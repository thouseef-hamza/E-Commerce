from django.urls import path
from . import views

urlpatterns = [
    # path('games/',views.games,name='games'),
    path('category/<slug:category_slug>/',views.products,name='products'),
    path('category/<slug:category_slug>/<slug:product_slug>',views.product_detail,name='product_detail'),
    path('search/',views.search,name='search'),
    path('submit_review/<int:product_id>/',views.submit_review,name="submit_review"),
]
