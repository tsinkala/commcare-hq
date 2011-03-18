from post import post_data
import sys
import json
import re

url = sys.argv[1]

success = "<?xml version='1.0' encoding='UTF-8'?>\n<OpenRosaResponse xmlns=\"http://openrosa.org/http/response\">\n    <message>Thanks for submitting!</message>\n</OpenRosaResponse>"
new_user = r"""<OpenRosaResponse xmlns="http://openrosa.org/http/response">.*<message>Thanks for registering! Your username is (?P<username>.*)</message>.*<uuid>(?P<user_id>.*)</uuid>"""
for line in sys.stdin:
    try:
        s = json.loads(line)
    except ValueError:
        continue
    if 'errors' in s:
        continue
    def ____(domain, submit_time, uuid, body, url):
        #url = url.format(domain=domain.lower())
        results, errors = post_data(body, url, submit_time)
        reg_match = re.search(new_user, results, flags=re.DOTALL)
        if results == success:
            message = "Success"
        elif reg_match:
            username = reg_match.group('username')
            user_id = reg_match.group('user_id')
            message = "Registered user %s (%s)" % (user_id, username)
        else:
            message = results
        print u"%s: %s" % (uuid, message)
        if results.startswith("\n<!DOCTYPE HTML PUBLIC"):
            with open('1.0_migration/errors/%s.html' % uuid, 'w') as f:
                f.write(results)
    ____(url=url, **dict((str(k), s[k]) for k in s))
    