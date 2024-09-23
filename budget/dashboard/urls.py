from django.urls import path


from .views import home_dashboard, stock

app_name = "dashboard"

urlpatterns = [
    path("", home_dashboard, name="home_dashboard"),
    path("stock/", stock, name="stock"),
]