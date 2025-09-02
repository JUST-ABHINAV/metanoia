from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),       # Landing page
    path("storytelling/", views.storytelling, name="storytelling"),  # Form input
    path("reframer/", views.home, name="home"),     # Handles POST + AI backend
    path("output/", views.output, name="output"),  # Final story page
    path("blog/", views.blog, name="blog"),        # Blog page
    path("about/", views.about, name="about"),     # About Us page
    path("thinking/", views.thinking, name="thinking"),  # Thinking/Processing page
]
