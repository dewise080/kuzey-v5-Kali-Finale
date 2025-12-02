from django.db import migrations, models
from django.db.models import Q


def normalize_deal_type(apps, schema_editor):
    Listing = apps.get_model('listings', 'Listing')
    for obj in Listing.objects.all().only('id', 'deal_type', 'deposit'):
        raw = (obj.deal_type or '').strip().lower()
        normalized = None
        if raw in {'rent', 'rental', 'lease', 'for rent', 'kiralık', 'kiralik'}:
            normalized = 'rent'
        elif raw in {'sale', 'sell', 'for sale', 'satılık', 'satilik', 'satış', 'satis'}:
            normalized = 'sale'
        else:
            # Heuristic: if deposit exists, assume rent; else default to sale
            if getattr(obj, 'deposit', None):
                try:
                    if int(obj.deposit) > 0:
                        normalized = 'rent'
                except Exception:
                    pass
            if not normalized:
                normalized = 'sale'
        if raw != normalized:
            Listing.objects.filter(pk=obj.pk).update(deal_type=normalized)


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0007_listingimportjob'),
    ]

    operations = [
        migrations.RunPython(normalize_deal_type, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='listing',
            name='deal_type',
            field=models.CharField(
                choices=[('rent', 'Rent'), ('sale', 'Sale')],
                default='sale',
                max_length=10,
                db_index=True,
                verbose_name='Deal type',
            ),
        ),
        migrations.AddConstraint(
            model_name='listing',
            constraint=models.CheckConstraint(check=Q(('deal_type__in', ['rent', 'sale'])), name='listing_deal_type_valid'),
        ),
    ]

