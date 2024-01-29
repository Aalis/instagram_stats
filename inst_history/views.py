from django.http import JsonResponse
from django.core.serializers import serialize
from django.shortcuts import render
from .models import InstHistory


def instprofile_history(request, profile_id):
    profile_history = InstHistory.objects.filter(profile_id=profile_id).order_by(
        "created_at"
    )

    # Serialize the queryset to JSON
    profile_history_json = serialize("json", profile_history)

    return render(
        request, "instprofile_history.html", {"profile_history": profile_history_json}
    )
