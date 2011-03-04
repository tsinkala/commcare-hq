#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import settings 
#from django.core.management import setup_environ
import os
import json
import sys

#setup_environ(settings)
from receiver.models import Submission

def run():    
    """
    run through all the submissions and from each create
    a json object {"headers": {}, "body": "", "errors": []}
    print these out to stdin (which is hopefully redirected to a file)
    one per line
    """

    all_submissions = Submission.objects.only(
        "id", "submit_time", "raw_post",
        #"submit_ip",
        "domain", "transaction_uuid"
    )
    if len(sys.argv) >= 4:
        domain_name = sys.argv[3]
        all_submissions = all_submissions.filter(domain__name=domain_name)
    # earliest submissions first
    all_submissions = all_submissions.order_by("submit_time")
    sys.stderr.write("Exporting %s submissions\n" % all_submissions.count())
    for i,submission in enumerate(all_submissions):
        if i % 100 == 0:
            sys.stderr.write("\n%s" % i)
        sys.stderr.write(".")
        sys.stderr.flush()
        sys.stdout.flush()
        try:
            errors = []
            submission_id = submission.id
            submit_time = str(submission.submit_time)
            filename = submission.raw_post
            if not filename:
                errors.append("In submission #%s, filename is None" % submission_id)
                doc = {"errors": errors}
                print json.dumps(doc)
                continue
            submit_ip = str(submission.submit_ip)
            domain_name = submission.domain.name if submission.domain else "---"
            uuid = submission.transaction_uuid
            with open(filename, 'r') as post_file:
#                # first line is content type
#                content_type = post_file.readline().split(":")[1].strip()
#                # second line is content length
#                content_length = post_file.readline().split(":")[1].strip()
#                # third line is empty
#                post_file.readline()
                # ingore first three lines
                for i in range(3): post_file.readline()
                # the rest is the actual body of the post
                payload = post_file.read()
#            headers = {"content-type" : content_type,
#                       "content-length" : content_length,
#                       "time-received" : submit_time,
#                       "original-ip" : submit_ip,
#                       "domain" : domain_name,
#                       "uuid": uuid,
#                       }
#            doc = {"headers": headers, "body": unicode(payload, encoding="utf-8"), "errors": errors}
            if ' ' in submit_time:
                submit_time = "%sT%sZ" % tuple(submit_time.split())
            doc = dict(uuid=uuid, domain=domain_name, submit_time=submit_time, body=unicode(payload, encoding="utf-8"))
            print json.dumps(doc)
        except Exception as e:
            errors.append("In submission #%s: %s" % (submission_id, str(e)))
            #sys.stderr.write(payload + "\n")
            doc = {"errors": errors}
            try:
                print json.dumps(doc)
            except:
                print '{"errors": ["can\'t even print error"]}'
    sys.stderr.write("\n")