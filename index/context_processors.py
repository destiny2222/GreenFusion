from .models import Category

# def nav_cats(request):
#     objects = Category.objects.filter(status=True, featured=True)
#     return {'nav_cats': objects}

def nav_cats(request):
        return {'nav_cats': Category.objects.all()} 

