from couchdbkit.ext.django.schema import *
from datetime import datetime
from django.conf import settings


class HqDeploy(Document):
    environment = StringProperty() #production, staging, etc
    date = DateTimeProperty()
    user = StringProperty()
    project_snapshot = DictProperty() #dict of git info and submodules

    @classmethod
    def envstring(cls):
        return "%(couch_server)s_"

        pass

    @classmethod
    def new_deploy(cls, username, snapshot, environment):
        deploy = cls(
            date=datetime.utcnow(),
            user=username,
            project_snapshot=snapshot,
            environment=environment
        )
        deploy.save()



    @classmethod
    def get_latest(cls):
        return HqDeploy.view('hqadmin/deploy_history', reduce=False, limit=1, descending=True).one()