from domain.models import Domain

_SESSION_KEY_SELECTED_DOMAIN = '_domain_selected_domain'

def add_domain_to_user(request):
    """ used by both the domain middleware as well as the 'add request to user' decorator
    to associate domain with the request.user object """
    user = request.user
    # Lookup is done via the ContentTypes framework, stored in the domain_membership table
    # id(user) == id(request.user), so we can save a lookup into request by using 'user' alone    
    active_domains = Domain.active_for_user(user)
    user.active_domains = active_domains            
    user.selected_domain = None # default case
    
    domain_from_session = request.session.get(_SESSION_KEY_SELECTED_DOMAIN, None)
    
    if domain_from_session and domain_from_session in active_domains:
        user.selected_domain = domain_from_session
        
    if not domain_from_session and len(active_domains) == 1:
        #request.session[_SESSION_KEY_SELECTED_DOMAIN] = active_domains[0]
        user.selected_domain = active_domains[0]
    return request
