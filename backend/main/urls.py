from django.urls import path, re_path
from .views import FrontendAppView, wordle_solver_api, set_csrf, word_correction_api, IndexView
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    # path('hello/', hello_world),
    path("api/django/csrf/", set_csrf),
    path('api/django/wordle-solver/', wordle_solver_api),
    path('api/django/word-correction/', word_correction_api),

    re_path(r'^(?!static/|assets/).*$', FrontendAppView.as_view()),
    re_path(r'^.*$', IndexView.as_view(), name='react_app'),

]


urlpatterns += static(settings.STATIC_URL, document_root=os.path.join(settings.BASE_DIR, 'frontend_dist'))
