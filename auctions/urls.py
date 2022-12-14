from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path('add/<int:auction_id>', views.add_to_wishlist, name='add_to_wishlist'),
    path('watchlist', views.watchlist, name='watchlist'),
    path('categories', views.categories, name='categories'),
    path('categorized/<int:category_id>', views.categorized, name='categorized'),
    path('listing/<int:auction_id>', views.listing, name='listing'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
