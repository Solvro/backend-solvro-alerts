import uuid
from django.db import models
from django.utils.text import slugify


class Application(models.Model):
    """A consumer app (Testownik, Planer, …) that alerts can be scoped to."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    code = models.SlugField(
        max_length=64,
        unique=True,
        help_text="Machine identifier used by the API (e.g. 'topwr'). "
        "Auto-derived from the name.",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.name)
        super().save(*args, **kwargs)
