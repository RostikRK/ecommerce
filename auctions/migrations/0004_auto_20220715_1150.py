# Generated by Django 3.1.3 on 2022-07-15 11:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20220715_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='auctions',
            field=models.ManyToManyField(default=None, to='auctions.Auction_listing'),
        ),
    ]
