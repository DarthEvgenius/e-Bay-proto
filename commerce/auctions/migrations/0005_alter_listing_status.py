# Generated by Django 4.1.5 on 2023-02-19 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0004_rename_bids_bid_rename_categories_category_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='status',
            field=models.BooleanField(default=True),
        ),
    ]
