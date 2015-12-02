# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PubLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.AlterField(
            model_name='tutorial',
            name='json_data',
            field=jsonfield.fields.JSONField(default={b'requirements': [], b'title': b'Your Title', b'setup': {b'bootstrap_cdn': b'\n\t\t\t\t\t<!-- Latest compiled and minified CSS -->\n\t\t\t\t\t<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" integrity="sha512-dTfge/zgoMYpP7QbHy4gWMEGsbsdZeCXz7irItjcC3sPUFtf0kuFbDz/ixG7ArTxmDjLXDmezHubeNikyKGVyQ==" crossorigin="anonymous">\n\t\t\t\t\t\n\t\t\t\t\t<!-- Optional theme -->\n\t\t\t\t\t<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap-theme.min.css" integrity="sha384-aUGj/X2zp5rLCbBxumKTCw2Z50WgIr1vs/PFN4praOTvYXWlVyh2UtNUU0KAUhAX" crossorigin="anonymous">\n\t\t\t\t', b'javascript_links': b'\n\t\t\t\t    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js" integrity="sha512-K1qjQ+NcF2TYO/eI3M6v8EiNYZfA95pQumfvcVrTHtwQVDG+aHRqLi/ETn2uB+1JqwYqVG3LIvdm9lj6imS/pQ==" crossorigin="anonymous"></script>\n\t\t\t\t    <script src="https://google-code-prettify.googlecode.com/svn/loader/run_prettify.js" async></script>"'}, b'header': b'This will be your Tutorial mission statement', b'warning': b'Please make sure you have the following setup before starting', b'steps': [], b'end_result_image': {}}),
        ),
        migrations.AddField(
            model_name='publink',
            name='tutorial',
            field=models.ForeignKey(to='tb.Tutorial'),
        ),
    ]
