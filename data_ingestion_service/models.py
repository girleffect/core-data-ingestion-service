from django.db import models

from django.conf import settings
from django.utils import timezone

from project.settings import MediaStorage


def user_file_path(instance, filename):
    # Timestamp in microseconds since epoch time, use timezone as created_at is
    # not available till after the first creation.
    now = timezone.now()
    microseconds = int(
        now.strftime("%s")
    ) * 1000000 + now.microsecond

    # File will be uploaded to:
    # <FileStorageRoot>/user_<user_id>/<created_at>_<filename>
    # Make use of the default filename to remove the need to infer the file
    # type and extension.
    return f"user_{instance.user.id}/{microseconds}_{filename}"


class StoredFiles(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    file = models.FileField(
        upload_to=user_file_path,
        storage=MediaStorage()
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
