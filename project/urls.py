from django.contrib import admin
from django.urls import include, path

app_name = 'app'


urlpatterns = [
    # path('', include('polls.urls')),
    # path('admin/', admin.site.urls),

    path('admin/', admin.site.urls),
    path('', include('app.urls')),
    path('', include('django.contrib.auth.urls')),
]
