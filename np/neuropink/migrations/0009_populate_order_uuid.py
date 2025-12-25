from django.db import migrations
import uuid


def populate_tokens(apps, schema_editor):
    Order = apps.get_model('neuropink', 'Order')

    for order in Order.objects.filter(access_token__isnull=True):
        order.access_token = uuid.uuid4()
        order.save(update_fields=['access_token'])


class Migration(migrations.Migration):

    dependencies = [
        ('neuropink', '0008_order_access_token'),
    ]

    operations = [
        migrations.RunPython(populate_tokens),
    ]
