from django.core.management.base import BaseCommand
from corehq.apps.hqadmin.models import HqDeploy
from datetime import datetime
from optparse import make_option
import os

class Command(BaseCommand):
    help = "Creates an HqDeploy document to record a successful deployment."
    args = "[user]"

    option_list = BaseCommand.option_list + (
        make_option('--user', help='User', default=False),
        make_option('--env', help='Environment name', default=False),
    )
    
    def handle(self, *args, **options):
        environment = options['env']
        if not environment:
            os_name = "unknown_env"
            if hasattr(os, "uname"):
                os_name= os.uname()[1]
            environment = os_name

        user=options['user']
        if not user:
            print "\tUsage: manage.py record_deploy_success.py --user <username> [--env {production, staging, etc}]"
            sys.exit()

        deploy = HqDeploy(
            date=datetime.utcnow(),
            user=options['user'],
            environment=environment,
            snapshot=gitinfo.get_project_info(from_hex=from_hash)
        )

        deploy.save()
        