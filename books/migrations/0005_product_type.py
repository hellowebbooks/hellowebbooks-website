# Generated by Django 2.1.7 on 2019-04-05 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_membership_last_read'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('book', 'Book'), ('zine', 'Zine')], default='book', max_length=255),
            preserve_default=False,
        ),
    ]
