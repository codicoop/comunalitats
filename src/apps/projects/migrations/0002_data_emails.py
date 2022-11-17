from django.db import migrations


def populate_mail_templates(apps, schema_editor):
    print('')
    mail_model = apps.get_model('mailing_manager', 'Mail')

    obj, created = mail_model.objects.update_or_create(
        text_identifier='EMAIL_NEW_PROJECT',
        defaults={
            'text_identifier': 'EMAIL_NEW_PROJECT',
            'subject': "Nova sol·licitud d'acompanyament: {projecte_nom}",
            'body': """<h2>Nova sol·licitud d'acompanyament</h2><br /><br />
        Nom del projecte: {projecte_nom} <br />
        Telèfon de contacte: {projecte_telefon} <br />
        Correu electrònic de contacte del projecte: {projecte_email} <br />
        Correu electrònic de l'usuari que l'ha creat: {usuari_email} <br />""",
            'default_template_path': 'emails/front_generic.html'
        },
    )
    print('EMAIL_NEW_PROJECT template updated.')

    obj, created = mail_model.objects.update_or_create(
        text_identifier='EMAIL_PROJECT_REQUEST_CONFIRMATION',
        defaults={
            'text_identifier': 'EMAIL_PROJECT_REQUEST_CONFIRMATION',
            'subject': "Nova sol·licitud d'acompanyament: {projecte_nom}",
            'body': """<p><strong>Confirmació de sol·licitud d'acompanyament 
pel projecte {projecte_nom}</strong></p>
<p style="padding-top: 20px">En els propers dies una persona de l'equip de 
la comunalitat es posarà en contacte amb tu per parlar dels propers 
passos.</p>
<p style="padding-top: 20px">Per consultar i modificar la fitxa del projecte 
accedeix a <a href="{url_backoffice}">l'aplicació dels serveis de la comunalitat</a>.
</p>
            """,
            'default_template_path': 'emails/front_single_text.html'
        },
    )
    print('EMAIL_PROJECT_REQUEST_CONFIRMATION template updated.')


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0001_initial'),
        ('mailing_manager', '__latest__'),
    ]

    operations = [
        migrations.RunPython(populate_mail_templates),
    ]
