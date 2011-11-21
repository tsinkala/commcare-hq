There are four scripts involved in the migration; to call all four together, you may call
the helper migrate.sh as follows
$ bash 1.0_migration/migrate.sh Dodoma http://www.commcarehq.org/a/dodoma/migration/

You will most likely want to try it first in parts. These are the scripts in the order in which they should be run:

1. bash 1.0_migration/block_domain.sh <domain>

    - Set the post url for <domain> (and only <domain>) to reject all incoming forms

2. bash 1.0_migration/dump_domain.sh <domain>

    - Dump all submissions on record for <domain> to a file located at 1.0_migration/tmp/<domain>.jsons

3. bash 1.0_migration/submit_domain_to_url.sh <domain> <url>

    - Submit each of these submissions in order to <url>

4. bash 1.0_migration/forward_domain_to_url.sh <domain> <url>

    - Set the post url for Dodoma to accept messages but forward them on to <url>
    

Step three will probably take a *long* time to complete (maybe 3-4 hours for 40,000 submissions)

It's a good idea to test the migration before running it for real. One way to do this is to set up a test
CommCare HQ 1.0 instance that you're happy to wipe clean. Then, run dump_domain.sh and submit_domain_to_url.sh,
using a url on the test instance (i.e. http://commcarehq-test.example.org/a/example.domain/migration/). This does not
test whether blocking and forwarding work. 