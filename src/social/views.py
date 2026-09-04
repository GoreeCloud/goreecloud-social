from django.db import connection
from django.http import JsonResponse
from django.shortcuts import render

from goreecloud_social import __version__

PLATFORM_INTEGRATIONS = {
    "manager": "blocked",
    "privacy_shield": "blocked",
    "wardveil_security": "blocked",
    "everkeep": "blocked",
    "glaze_ui": "blocked",
    "mesh": "blocked",
    "identity": "blocked",
}


def home(request):
    return render(request, "social/home.html", {
        "version": __version__,
        "feed_modes": ["Following", "Chronological", "Discover", "Communities", "Video"],
        "social_primitives": [
            "Profiles",
            "Groups",
            "Communities",
            "Posts",
            "Photos",
            "Video",
            "GIFs",
            "Reactions",
            "Reposts",
            "Blocks",
            "Mutes",
        ],
    })


def livez(request):
    return JsonResponse({"status": "ok", "service": "goreecloud-social"})


def readyz(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        return JsonResponse({"status": "not-ready"}, status=503)
    return JsonResponse({"status": "ready"})


def service_status(request):
    return JsonResponse({
        "product": "GoreeCloud Social",
        "component_id": "goreecloud-social",
        "version": __version__,
        "lifecycle": "development",
        "production_ready": False,
        "capabilities": [
            "social-profile-metadata",
            "groups-and-communities-domain",
            "follow-domain",
            "post-domain",
            "media-reference-domain",
            "reactions-and-reposts-domain",
            "audience-visibility-read-model",
            "relationship-safety-read-enforcement",
            "following-and-chronological-feed-read-models",
        ],
        "platform_integrations": PLATFORM_INTEGRATIONS,
    })
