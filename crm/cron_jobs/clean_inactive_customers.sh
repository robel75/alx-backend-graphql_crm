#!/bin/bash

cd "$(dirname "$0")/../.."

deleted_count=$(python manage.py shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

cutoff = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(orders__isnull=True, created_at__lt=cutoff)
count = qs.count()
qs.delete()
print(count)
")
echo "$(date '+%Y-%m-%d %H:%M:%S') - Deleted $deleted_count inactive customers" >> /tmp/customer_cleanup_log.txt
