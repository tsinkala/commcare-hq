# this is a newer version of intel/schema_models.py
# it generates Django models for all schema_* & view_* tables in the DB, using manage.py inspectdb
# so that the views can then access them with Django's ORM
#
# if you choose to keep it, you might want to:
# 1. put it in /utilities or somewhere like that
# 2. execute it whenever a new xform is registered or a form group defined/edited (ie new schema_/view_ table created)
# 3. change the intel app to use this as well, keeping true to DRY
#
# still it would be a pain, since the staging/dev/etc database schemas do not mirror each other
# solution: make sure the staging/dev/etc database schemas do mirror each other, as staging/dev/etc should.
#
# USAGE:
#   
#    cd apps/reports ; python schema_to_model.py > schemas.py
# 
# Then, in the view, something like:
#
#   from reports.schemas import SchemaPathPathChwFacilityregistration2 as Facility
#   Facility.objects.all()

import os, re

cmd = "cd ../.. ; python manage.py inspectdb" # gotta be in manage.py's dir
out = "from django.db import models\n\n"

inspect = os.popen(cmd, 'r').read()

inspect = inspect.replace(" id = models.IntegerField(\n", " # id = models.IntegerField(\n") # non-implied 'id' seems to confuse Django at some cases
inspect = inspect.replace("models.BigIntegerField", "models.IntegerField") # django < 1.2 doesn't support BigIntegerField

for table in inspect.split("\n\n"):
    table = table.strip()
    if table.startswith("class View") or table.startswith("class Schema"):
        out += "\n\n" + table

print out