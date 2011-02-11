To migrate (e.g.) Dodoma to CommCare HQ 1.0 run the following command

bash 1.0_migration/migrate.sh Dodoma http://www.commcarehq.org/a/dodoma/migration/

This is the *whole* deal. This script will:
    1. Set the post url for Dodoma (and only Dodoma) to reject all incoming forms
    2. Dump all submissions on record for Dodoma to a file
    3. Submit each of these submissions in order to http://www.commcarehq.org/a/dodoma/migrate/
    4. Set the post url for Dodoma to accept messages but forward them on to http://www.commcarehq.org/a/dodoma/migrate/

Step three will probably take a *long* time to complete.