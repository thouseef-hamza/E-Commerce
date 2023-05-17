from .models import Category

def nav_links(request):
    links = Category.objects.all()
    return dict(links=links)