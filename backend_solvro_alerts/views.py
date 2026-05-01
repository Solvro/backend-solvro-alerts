from django.shortcuts import render
from django.views.decorators.http import require_safe

from alerts.models import ALERT_HTML_TAGS


@require_safe
def index(request):
    return render(
        request,
        "index.html",
        {"alert_html_tags": ", ".join(sorted(ALERT_HTML_TAGS))},
    )
