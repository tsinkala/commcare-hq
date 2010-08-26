from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden

from domain.decorators import login_and_domain_required, require_domain
from rapidsms.webui.utils import render_to_response, UnicodeWriter

from reports.schemas import SchemaPathPathChwFacilityregistration2 as Facility

from reports.schemas import SchemaPathPathChwSupervisionchecklist2 as Checklist


def supervisor(request):
    data = {}
    
    data['fac'] = Checklist.objects.all()
    
    return render_to_response(request, "path/supervisor.html", data)