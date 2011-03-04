DOMAIN=$1
mkdir 1.0_migration/tmp/ &> /dev/null
python manage.py runscript export_data $DOMAIN > 1.0_migration/tmp/$DOMAIN.jsons
