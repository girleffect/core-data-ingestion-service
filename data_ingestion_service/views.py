from django.views.generic import (
    TemplateView,
    RedirectView
)
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator


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

    template_name = "data_ingestion_service/temp.html"
