from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.shortcuts import get_object_or_404

from domain.decorators import login_and_domain_required, require_domain
from rapidsms.webui.utils import render_to_response, UnicodeWriter

try:
    from reports.schemas import SchemaPathPathChwSupervisionchecklist2 as Checklist
    from reports.schemas import SchemaPathPathChwFacilityregistration2 as Facility
    from reports.schemas import SchemaPathChwSupervisionchecklistPathStaffProfile2 as StaffProfile
    from reports.schemas import SchemaPathPathChwClosefacility2 as CloseFacility
    
    from reports.schemas import SchemaPathPathChwTbHiv2 as TbHiv
    from reports.schemas import SchemaPathPathChwTbHivPathOfferedDct2 as DctOffered
    from reports.schemas import SchemaPathPathChwTbHivPathRefCtc2 as CtcTested
    from reports.schemas import SchemaPathPathChwTbHivPathTestedHiv2 as HivTested
    from reports.schemas import SchemaPathPathChwTbHivPathNumHivPositive2 as HivPositive
    from reports.schemas import SchemaPathPathChwTbHivPathNumRegistered2 as TbRegistered
    from reports.schemas import SchemaPathPathChwTbHivPathHivCare2 as HivCare
    from reports.schemas import SchemaPathPathChwTbHivPathStartArt2 as StartArt
    from reports.schemas import SchemaPathPathChwTbHivPathStartCpt2 as StartCpt
    
except ImportError: # because perhaps the Schema file isn't up to date
    # the script still would throw an error, but not shut down the server. important since dev DB != staging DB, and both have users relying on.
    pass
    
@require_domain('path')
def index(request):
    ''' facilities index '''

    # Since Django can't join these (AFAIK - need to check newer versions) 
    # Get the checklist reports into an indexed dict and then attach them to facilities
    
    checklists = {} ; facilities = {} ; reports = {}

    for r in TbHiv.objects.all():
        reports[r.path_case_case_id] = r
        
    for c in Checklist.objects.all():
        checklists[c.path_case_case_id] = c

    for f in Facility.objects.all():
        if checklists.has_key(f.path_case_case_id):
            f.checklist = checklists[f.path_case_case_id]
        if reports.has_key(f.path_case_case_id):
            f.report = reports[f.path_case_case_id]
            
        facilities[f.path_case_case_id] = f
    
    # remove closed cases
    for cl in CloseFacility.objects.all():
        if facilities.has_key(cl.path_case_case_id):
            del(facilities[cl.path_case_case_id])    

    return render_to_response(request, "custom/path/facilities.html", { "facilities": facilities })


@require_domain('path')
def facility(request, checklist_id):
    ''' display supervisor report for a single facility '''

    checklist = get_object_or_404(Checklist, pk=checklist_id)
    facility = get_object_or_404(Facility, path_case_case_id=checklist.path_case_case_id)
    profiles = StaffProfile.objects.filter(parent_id=checklist.id)

    return render_to_response(request, "custom/path/facility.html", { "i" : checklist, "facility": facility, "profiles" : profiles })


@require_domain('path')
def quarterly(request, report_id):
    
    report = get_object_or_404(TbHiv, pk = report_id)
    facility = get_object_or_404(Facility, path_case_case_id=report.path_case_case_id)

    dct = get_object_or_404(DctOffered, parent_id = report.id)
    hivt= get_object_or_404(HivTested,  parent_id = report.id)
    hivp= get_object_or_404(HivPositive,  parent_id = report.id)
    ctc = get_object_or_404(CtcTested,  parent_id = report.id)
    hivc= get_object_or_404(HivCare,    parent_id = report.id)
    sart= get_object_or_404(StartArt, parent_id = report.id)
    scpt= get_object_or_404(StartCpt, parent_id = report.id)
    
    # tb  = get_object_or_404(TbRegistered,  parent_id = report.id)
    
    # get quarter
    report.quarter = ("Jan-Mar", "Apr-Jun", "Jul-Sep", "Oct-Dec")[(int(report.meta_timeend.strftime("%m")) - 1) / 3]

    # because the xform totals are broken
    # and django templates, thanks their lame design, cant do arithmetics

    for i in [dct, hivt, hivp, ctc, hivc, sart, scpt]:
        i.total_ss_patients_male = i.facility_based_ss_patients_male + i.home_based_ss_patients_male
        i.total_ss_patients_female = i.facility_based_ss_patients_female + i.home_based_ss_patients_female
        i.total_other_patients_male = i.facility_based_other_patients_male + i.home_based_other_patients_male
        i.total_other_patients_female = i.facility_based_other_patients_female + i.home_based_other_patients_female
        
        i.grand_total = i.total_ss_patients_male + i.total_ss_patients_female + i.total_other_patients_male + i.total_other_patients_female
        
    
    for i in [dct, hivt, hivp]:
        i.male_total = i.age_category_under_15_male + i.age_category_above_15_male
        i.female_total = i.age_category_under_15_female + i.age_category_above_15_female
    
    

    # Age totals. These aren't in the xforms AFAIK so will remain here even when they are fixed    
    total_under_15 =dct.age_category_under_15_male + hivp.age_category_under_15_male + hivt.age_category_under_15_male + \
                    dct.age_category_under_15_female + hivp.age_category_under_15_female + hivt.age_category_under_15_female
                    
    total_over_15 = dct.age_category_above_15_male + hivp.age_category_above_15_male + hivt.age_category_above_15_male + \
                    dct.age_category_above_15_female + hivp.age_category_above_15_female + hivt.age_category_above_15_female

    total_total = total_over_15 + total_under_15
    
    return render_to_response(request, "custom/path/quarterly.html", { 
                                                                    "facility"  : facility,
                                                                    "report"    : report,
                                                                    "dct"   : dct,
                                                                    "ctc"   : ctc,
                                                                    "hivt"  : hivt,
                                                                    "hivp"  : hivp,
                                                                    "hivc"  : hivc,
                                                                    "sart"  : sart,
                                                                    "scpt"  : scpt,
                                                                    # "tb"    : tb
                                                                    
                                                                    "total_under_15": total_under_15,
                                                                    "total_over_15" : total_over_15,
                                                                    "total_total"   : total_total
                                                                    }
                             )
    
    