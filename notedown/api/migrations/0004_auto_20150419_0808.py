# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_note'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['created']},
        ),
        migrations.RenameField(
            model_name='note',
            old_name='create',
            new_name='created',
        ),
    ]
