DOMAIN=$1
echo "
from apps.domain.models import Domain
from apps.receiver.models import MigrationStatus

domain = Domain.objects.get(name='$DOMAIN')
ms, _ = MigrationStatus.objects.get_or_create(domain=domain)
ms.block = True
ms.save()
" | python manage.py shell &> /dev/null