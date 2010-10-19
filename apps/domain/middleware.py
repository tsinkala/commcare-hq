from django.conf import settings
import django.core.exceptions

from domain.models import Domain
from domain.util import add_domain_to_user


############################################################################################################

class DomainMiddleware(object):
    def __init__(self):        
        # Normally we'd expect this class to be pulled out of the middleware list, too,
        # but in case someone forgets, this will stop this class from being used.
        if 'domain' not in settings.INSTALLED_APPS:
            raise django.core.exceptions.MiddlewareNotUsed

    # Always put a user's active domains in request.user object
    # Only fill in a non-null selected_domain for clearly-correct cases: session's domain is
    # in active set, or there's no domain in the session and only one possible domain in the
    # active set.
    #
    # Otherwise, selected_domain is None, and the login_and_domain_requested decorator will
    # catch it and send the user to the appropriate redirect.
    
    # Unclear whether we want this on process_request or process_view - they seem to be called the same
    # number of times, so it's likely a matter of whether we want the absence/presence of a good domain
    # to stop processing. As far as I can tell right now, with our current use cases the choice doesn't 
    # matter.
    
    #def process_request(self, request):
    def process_view(self, request, view_func, view_args, view_kwargs):
        request = add_domain_to_user(request)
        return None

############################################################################################################
