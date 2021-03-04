# Generated by Django 2.2.7 on 2021-03-04 14:47

from django.db import migrations, models
import django.db.models.deletion
import tagulous.models.fields
import tagulous.models.models


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0079_user_cannot_share_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectstage',
            name='entity',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cc_courses.Entity', verbose_name='entitat'),
        ),
        migrations.AlterField(
            model_name='user',
            name='cannot_share_id',
            field=models.BooleanField(default=False, verbose_name="Si degut a la teva situació legal et suposa un inconvenient indicar el DNI, deixa'l en blanc i marca aquesta casella"),
        ),
        migrations.CreateModel(
            name='Tagulous_User_tags',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('slug', models.SlugField()),
                ('count', models.IntegerField(default=0, help_text='Internal counter of how many times this tag is in use')),
                ('protected', models.BooleanField(default=False, help_text='Will not be deleted when the count reaches 0')),
            ],
            options={
                'ordering': ('name',),
                'abstract': False,
                'unique_together': {('slug',)},
            },
            bases=(tagulous.models.models.BaseTagModel, models.Model),
        ),
        migrations.AddField(
            model_name='user',
            name='tags',
            field=tagulous.models.fields.TagField(_set_tag_meta=True, blank=True, force_lowercase=True, help_text='Prioritza les etiquetes que apareixen auto-completades. Si escrius una etiqueta amb un espai creurà que son dues etiquetes, per evitar-ho escriu-la entre cometes dobles, "etiqueta amb espais".', to='coopolis.Tagulous_User_tags', verbose_name='etiquetes'),
        ),
    ]
