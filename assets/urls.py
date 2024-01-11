from django.urls import path
from assets import views


app_name = 'assets'


urlpatterns = [
    path('report/', views.report, name='report'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('index/', views.index, name='index'),
    path('sales_predictions/', views.sales_predictions, name='sales_predictions'),
    path('sales_ranking/', views.sales_ranking, name='sales_ranking'),
    path('rating_ranking/', views.rating_ranking, name='rating_ranking'),
    path('detail/<int:asset_id>/', views.detail, name='detail'),
    path('', views.dashboard),
]