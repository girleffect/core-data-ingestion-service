from django.contrib import messages
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import (
    TemplateView,
    RedirectView
)
from django.views.decorators.cache import never_cache
from django.views.generic.edit import CreateView

from data_ingestion_service.models import StoredFiles


@method_decorator(never_cache, "dispatch")
class LoginRedirectWithQueryStringView(RedirectView):
    """
    This view is used when a user needs to be redirected to the Authentication Service
    for login. The problem is that this view is also used when a user is already logged
    in but does not have the required permissions to view a resource.

    This view specifically checks if a user is already logged in, in which case it redirects
    the user to the homepage with a message explaining that access to the resource that was
    accessed is not allowed.
    """
    query_string = True
    pattern_name = "oidc_authentication_init"

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            # Since the user is already logged in, we take them to the home page.
            messages.info(self.request, "You are already logged in, but may not have the "
                                        "required permissions.")
            return redirect(reverse("home"))

        return super().dispatch(request, *args, **kwargs)


class HomePageView(TemplateView):
    template_name = "data_ingestion_service/home.html"


class FileSaveView(CreateView):
    template_name = "data_ingestion_service/form.html"
    model = StoredFiles
    fields = ["category", "file"]

    def form_valid(self, form):
        # Add current user to form instance, before checking form validity and
        # allowing it to save the instance.
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS,
            "File successfully uploaded to:" \
            f" {self.get_form().instance.file.name}"
        )
        return reverse("fileupload")
