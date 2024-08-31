from .generated_apis.makegame import makegame


from django.urls import path

urlpatterns = [
    path('game/', makegame),
]
