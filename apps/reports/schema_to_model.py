# this is a newer version of intel/schema_models.py
# it generates Django models for all schema_* & view_* tables in the DB, using manage.py inspectdb
# so that the views can work with them using Django's ORM
#
# if you choose to keep it, you might want to:
# 1. put it in /utilities or somewhere like that
# 2. execute it whenever a new xform is registered or a form group defined/edited (ie new schema_/view_ table created)
# 3. change the intel app to use this as well, keeping true to DRY
#
# still it would be a pain, since the staging/dev/etc database schemas do not mirror each other
# solution: make sure the staging/dev/etc database schemas do mirror each other, as staging/dev/etc should.


# enough talk.
import os, re

cmd = "cd ../.. ; python manage.py inspectdb" # gotta be in manage.py's dir
out = "from django.db import models\n\n"

inspect = os.popen(cmd, 'r').read()


inspect = inspect.replace(" id = models.IntegerField()\n", " # id = models.IntegerField()\n") # django likes its 'id's implied
inspect = inspect.replace("models.BigIntegerField", "models.IntegerField") # django < 1.2 doesn't support BigIntegerField

for table in inspect.split("\n\n"):
    table = table.strip()
    if table.startswith("class View") or table.startswith("class Schema"):
        out += "\n\n" + table

print out