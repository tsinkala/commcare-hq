DOMAIN=$1
URL=$2

echo -n "* Shutting down $DOMAIN's post url.."
bash 1.0_migration/block_domain.sh $DOMAIN
echo "."

echo "* Dumping $DOMAIN's submission data..."
bash 1.0_migration/dump_domain.sh $DOMAIN

echo "* Submitting data to $URL"
bash 1.0_migration/submit_domain_to_url.sh $DOMAIN $URL

echo -n "* Forwarding all future submissions to $URL.."
bash 1.0_migration/forward_domain_to_url.sh $DOMAIN $URL