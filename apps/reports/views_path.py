from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404

from domain.decorators import login_and_domain_required, require_domain
from rapidsms.webui.utils import render_to_response, UnicodeWriter

# from reports.schemas import SchemaPathPathChwFacilityregistration2 as Facility

from reports.schemas import SchemaPathPathChwSupervisionchecklist2 as Checklist
from reports.schemas import SchemaPathChwSupervisionchecklistPathStaffProfile2 as StaffProfile


@require_domain('path')
def supervisor(request, checklist_id):
    checklist = get_object_or_404(Checklist, pk=checklist_id)
    
    profiles = StaffProfile.objects.filter(parent_id=checklist.id)
    
    return render_to_response(request, "path/supervisor.html", { "i" : checklist, "profiles" : profiles })
    

# @require_domain('path')
# def all_supervisors(request):
#     data = {}
#     
#     # since the models are created by schema_to_model, we cant use Django's foreign key
#     # 
#     # http://www.caktusgroup.com/blog/2009/09/28/custom-joins-with-djangos-queryjoin/
#     
#     
#     # checklists = Checklist.objects.all()
#     # profiles = StaffProfile.objects.all()
#     # 
#     # for c in checklists:
#     #     checklists[c].profile = StaffProfile
#     
#     data['fac'] = Checklist.objects.all()
#     
#     return render_to_response(request, "path/supervisor.html", data)
# 
# 
