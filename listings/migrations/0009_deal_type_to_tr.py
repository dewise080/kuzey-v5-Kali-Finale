from django.db import migrations, models
from django.db.models import Q


def to_tr_deal_type(apps, schema_editor):
    Listing = apps.get_model('listings', 'Listing')
    for obj in Listing.objects.all().only('id', 'deal_type', 'deposit'):
        raw = (obj.deal_type or '').strip().lower()
        new_val = None
        if raw in {'rent', 'rental', 'lease', 'for rent', 'kiralık', 'kiralik'}:
            new_val = 'kiralik'
        elif raw in {'sale', 'sell', 'for sale', 'satılık', 'satilik', 'satış', 'satis'}:
            new_val = 'satis'
        else:
            # Heuristic: deposit -> kiralik; else satis
            if getattr(obj, 'deposit', None):
                try:
                    if int(obj.deposit) > 0:
                        new_val = 'kiralik'
                except Exception:
                    pass
            if not new_val:
                new_val = 'satis'
        if raw != new_val:
            Listing.objects.filter(pk=obj.pk).update(deal_type=new_val)


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0008_enforce_deal_type_choices'),
    ]

    operations = [
        # 1) Drop old constraint first to allow interim values ('kiralik'/'satis')
        migrations.RemoveConstraint(
            model_name='listing',
            name='listing_deal_type_valid',
        ),
        # 2) Normalize existing data to TR values
        migrations.RunPython(to_tr_deal_type, migrations.RunPython.noop),
        # 3) Update field choices/defaults
        migrations.AlterField(
            model_name='listing',
            name='deal_type',
            field=models.CharField(
                choices=[('kiralik', 'Kiralık'), ('satis', 'Satış')],
                default='satis',
                max_length=10,
                db_index=True,
                verbose_name='Deal type',
            ),
        ),
        # 4) Enforce new constraint
        migrations.AddConstraint(
            model_name='listing',
            constraint=models.CheckConstraint(check=Q(('deal_type__in', ['kiralik', 'satis'])), name='listing_deal_type_valid'),
        ),
    ]
