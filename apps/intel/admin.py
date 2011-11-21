from django.contrib import admin
from intel.models import *
from intel.schema_models import IntelGrameenSafeMotherhoodFollowup, IntelGrameenMotherRegistration

admin.site.register(Clinic)
admin.site.register(UserClinic)
admin.site.register(ClinicVisit)

admin.site.register(IntelGrameenSafeMotherhoodFollowup)
admin.site.register(IntelGrameenMotherRegistration)
