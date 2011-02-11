DOMAIN=$1
URL=$2
mkdir 1.0_migration/errors/ &> /dev/null
rm 1.0_migration/errors/* &> /dev/null
python 1.0_migration/submit.py $URL < 1.0_migration/tmp/$DOMAIN.jsons
