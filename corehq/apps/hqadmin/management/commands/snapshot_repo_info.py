import sys
import os
from optparse import make_option
from django.core.management.base import BaseCommand
from django.core.mail import mail_admins
from dimagi.utils import gitinfo
from django.conf import settings
import simplejson

class Command(BaseCommand):
    args = ''
    help = 'Send args as a one-shot email to the admins.'

    option_list = BaseCommand.option_list + (
        make_option('--print_output', action='store_true', default=False, help='Print repo info to stdout, do not save'),
        make_option('--from_hash', action='store', default=None, help='Run a comparison from a prior project hash'),
    )

    def handle(self, *args, **options):
        do_print = False
        if options['print_output']:
            do_print = True
        from_hash = options['from_hash']
        git_dir = os.path.join(settings.FILEPATH, '.git')

        info = gitinfo.sub_git_info(git_dir)
        print simplejson.dumps(info, indent=4)
        subs = gitinfo.sub_git_submodules(git_dir)
        print simplejson.dumps(list(subs), indent=4)
        project_info = gitinfo.get_project_info(from_sha=from_hash)
        print simplejson.dumps(project_info, indent=4)
