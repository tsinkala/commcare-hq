from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404

from domain.decorators import login_and_domain_required, require_domain
from rapidsms.webui.utils import render_to_response, UnicodeWriter

from reports.schemas import SchemaPathPathChwSupervisionchecklist2 as Checklist
from reports.schemas import SchemaPathPathChwFacilityregistration2 as Facility
from reports.schemas import SchemaPathChwSupervisionchecklistPathStaffProfile2 as StaffProfile
from reports.schemas import SchemaPathPathChwClosefacility2 as CloseFacility

@require_domain('path')
def facility(request, checklist_id):
    ''' display supervisor report for a single facility '''
    
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    facility = get_object_or_404(Facility, path_case_case_id=checklist.path_case_case_id)
    profiles = StaffProfile.objects.filter(parent_id=checklist.id)
    
    return render_to_response(request, "custom/path/facility.html", { "i" : checklist, "facility": facility, "profiles" : profiles })
    

@require_domain('path')
def facilities(request):
    ''' facilities index '''

    # Since Django can't join these (AFAIK - need to check newer versions) 
    # Get the checklist reports into an indexed dict and then attach them to facilities
    
    checklists = {} ; facilities = {}

    for c in Checklist.objects.all():
        checklists[c.path_case_case_id] = c

    for f in Facility.objects.all():
        if checklists.has_key(f.path_case_case_id):
            f.checklist = checklists[f.path_case_case_id]
            facilities[f.path_case_case_id] = f
    
    # remove closed cases
    for cl in CloseFacility.objects.all():
        if facilities.has_key(cl.path_case_case_id):
            del(facilities[cl.path_case_case_id])    

    return render_to_response(request, "custom/path/facilities.html", { "facilities": facilities })
    