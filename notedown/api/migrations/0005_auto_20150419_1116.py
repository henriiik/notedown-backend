# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20150419_0808'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='googleauth',
            name='url',
            field=models.CharField(max_length=200, blank=True),
        ),
    ]
