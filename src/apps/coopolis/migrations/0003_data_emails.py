# Generated by Django 2.2.7 on 2020-08-07 07:45

from django.db import migrations


def populate_mail_templates(apps, schema_editor):
    print('')
    mail_model = apps.get_model('mailing_manager', 'Mail')

    mail_model.objects.bulk_create([
        mail_model(
            text_identifier='EMAIL_ENROLLMENT_CONFIRMATION',
            subject="Confirmació d'inscripció a l'activitat: {activitat_nom}",
            body="""
    <table align="center" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f0f0f0">
    <tr>
      <td align="center" valign="top" class="em_text1 pad10">
        <p>T'has inscrit a la formació</p>
      </td>
    </tr>
    <tr>
      <td height="15" style="font-size:0px; line-height:0px; height:15px;">&nbsp;</td>
    </tr>
    <tr>
      <td align="center" valign="top" style="font-family:'Open Sans', Arial, sans-serif; font-size:22px;
      line-height:22px; color:#000; letter-spacing:2px; padding-bottom:12px;" class="pad10">
        <strong>{activitat_nom}</strong> de {comunalitat_nom}
      </td>
    </tr>
    <tr>
      <td height="25" class="em_h20" style="font-size:0px; line-height:0px; height:25px;">&nbsp;</td>
    </tr>
    <tr>
      <td align="left" valign="top" style="padding: 0px 40px 10px 40px" bgcolor="#fafafa" class="em_text1 pad10">
        <p style="margin-left: 60px"><strong>Data:</strong> {activitat_data_inici}</p>
        <p style="margin-left: 60px"><strong>Hora:</strong> {activitat_hora_inici}</p>
        <p style="margin-left: 60px"><strong>Lloc:</strong> {activitat_lloc}</p>
        <p style="padding-top: 20px">Es tracta d'una formació gratuïta subvencionada, per això et demanem que, si
          finalment no pots venir, ens avisis amb antelació per poder obrir la plaça a una altra persona.<br>
          Per fer-ho pots gestionar les teves inscripcions accedint a l'aplicació amb el teu compte i anant a 
        l'apartat <a href="{absolute_url_my_activities}">Perfil -> Els Meus Cursos</a>.</p>
      </td>
    </tr>
    <tr>
      <td align="center" class="em_text1 pad10" bgcolor="#fafafa" style="padding-bottom: 15px;">
        <a href="{url_web_comunalitat}" style="color:#e94e1b; text-decoration:none; font-weight: bold;">Fins aviat!</a>
      </td>
    </tr>
    </table>
    """,
            default_template_path='emails/front_generic.html'
        ),
        mail_model(
            text_identifier='EMAIL_ENROLLMENT_WAITING_LIST',
            subject="Ets en llista d'espera per l'activitat: {activitat_nom}",
            body="""
    <table align="center" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f0f0f0">
    <tr>
      <td align="center" valign="top" class="em_text1 pad10">
        <p>Has entrat en llista d'espera per participar a la formació</p>
      </td>
    </tr>
    <tr>
      <td height="15" style="font-size:0px; line-height:0px; height:15px;">&nbsp;</td>
    </tr>
    <tr>
      <td align="center" valign="top" style="font-family:'Open Sans', Arial, sans-serif; font-size:22px;
      line-height:22px; color:#000; letter-spacing:2px; padding-bottom:12px;" class="pad10">
        <strong>{activitat_nom}</strong> de {comunalitat_nom}
      </td>
    </tr>
    <tr>
      <td height="25" class="em_h20" style="font-size:0px; line-height:0px; height:25px;">&nbsp;</td>
    </tr>
    <tr>
      <td align="left" valign="top" style="padding: 0px 40px 10px 40px" bgcolor="#fafafa" class="em_text1 pad10">
        <p style="margin-left: 60px"><strong>Data:</strong> {activitat_data_inici}</p>
        <p style="margin-left: 60px"><strong>Hora:</strong> {activitat_hora_inici}</p>
        <p style="margin-left: 60px"><strong>Lloc:</strong> {activitat_lloc}</p>
        <p style="padding-top: 20px">Si queda una plaça disponible, automàticament s'assignarà a la següent persona de la 
        llista d'espera. De donar-se el cas, rebràs un correu electrònic informant-te que la teva inscripció ha estat 
        confirmada. Sempre pots comprovar l'estat de la teva inscripció accedint a l'aplicació amb el teu compte i anant a 
        l'apartat <a href="{url_els_meus_cursos}">Perfil -> Els Meus Cursos</a>.</p>
      </td>
    </tr>
    <tr>
      <td align="center" class="em_text1 pad10" bgcolor="#fafafa" style="padding-bottom: 15px;">
        <a href="{url_comunalitat}" style="color:#e94e1b; text-decoration:none; font-weight: bold;">Fins aviat!</a>
      </td>
    </tr>
    </table>""",
            default_template_path='emails/front_generic.html'
        ),
        mail_model(
            text_identifier='EMAIL_ENROLLMENT_REMINDER',
            subject="Recordatori d'inscripció a l'activitat: {activitat_nom}",
            body="""
    <table align="center" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f0f0f0">
    <tr>
      <td align="center" valign="top" class="em_text1 pad10">
        <p>Instruccions per participar al taller</p>
      </td>
    </tr>
    <tr>
      <td height="15" style="font-size:0px; line-height:0px; height:15px;">&nbsp;</td>
    </tr>
    <tr>
      <td align="center" valign="top" style="font-family:'Open Sans', Arial, sans-serif; font-size:22px;
      line-height:22px; color:#000; letter-spacing:2px; padding-bottom:12px;" class="pad10">
        <strong>{activitat_nom}</strong> de {comunalitat_nom}
      </td>
    </tr>
    <tr>
      <td height="25" class="em_h20" style="font-size:0px; line-height:0px; height:25px;">&nbsp;</td>
    </tr>
    <tr>
      <td align="left" valign="top" style="padding: 0px 40px 10px 40px" bgcolor="#fafafa" class="em_text1 pad10">
        <p style="padding-top: 20px">Hola {persona_nom}!</p>
        <p style="padding-top: 20px">T'enviem aquest correu perquè tens una inscripció a aquesta sessió i s'acosta la data:</p>
        <p style="margin-left: 60px"><strong>Data:</strong> {activitat_data_inici}</p>
        <p style="margin-left: 60px"><strong>Hora:</strong> {activitat_hora_inici}</p>
        <p style="margin-left: 60px"><strong>Lloc:</strong> {activitat_lloc}</p>
        <p style="padding-top: 20px">{activitat_instruccions}</p>
        <p style="padding-top: 20px">Per accedir als fitxers adjunts, enllaç a la videotrucada i gestionar la teva 
            inscripció, ves a <a href="{absolute_url_activity}">la fitxa de la sessió</a>.</p>
        <p style="padding-top: 20px">Es tracta d'una formació gratuïta subvencionada, per això et demanem que 
            si finalment no pots venir ens avisis amb antelació per poder obrir la plaça a una altra persona.<br>
          Per fer-ho pots gestionar les teves inscripcions accedint a l'aplicació amb el teu compte i anant a 
        l'apartat <a href="{absolute_url_my_activities}">Perfil -> Els Meus Cursos</a>.</p>
      </td>
    </tr>
    <tr>
      <td align="center" class="em_text1 pad10" bgcolor="#fafafa" style="padding-bottom: 15px;">
        <a href="{url_web_comunalitat}" style="color:#e94e1b; text-decoration:none; font-weight: bold;">Fins aviat!</a>
      </td>
    </tr>
    </table>""",
            default_template_path='emails/front_generic.html'
        ),
        mail_model(
            text_identifier='EMAIL_SIGNUP_WELCOME',
            subject="Nou compte creat a {comunalitat_nom}",
            body="""
    <h2>Benvingut/da a {comunalitat_nom}!</h2>
    <p><em>Estàs rebent aquest correu perquè s'ha completat un registre a la plataforma {url_backoffice}.<br />
    Si aquest registre no l'has fet tu o cap altra persona amb qui comparteixis aquest compte, ignora aquest correu o 
    avisa'ns per tal que l'eliminem de la base de dades.</em></p><br />
    <p>Amb el teu compte pots:</p>
    <ul>
    <li>Inscriure't a les sessions formatives, que trobaràs <a href="{url_accions}">aquí</a>.</li>
    <li>Consultar o editar les dades del teu perfil i recuperar la contrassenya. </li>
    </ul>
    <p>Més informació a <a href="{url_backoffice}">{url_backoffice}</a>.</p>""",
            default_template_path='emails/front_single_text.html'
        ),
        mail_model(
            text_identifier='EMAIL_PASSWORD_RESET',
            subject="Reinicialització de contrasenya del teu compte a {comunalitat_nom}",
            body="""
    <table align="center" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f0f0f0">
    <tr>
      <td align="center" valign="top" class="em_text1 pad10">
        <p>Instruccions per reiniciar la contrasenya</p>
      </td>
    </tr>
    <tr>
      <td height="15" style="font-size:0px; line-height:0px; height:15px;">&nbsp;</td>
    </tr>
    <tr>
      <td align="left" valign="top" style="padding: 0px 40px 10px 40px" bgcolor="#fafafa" class="em_text1 pad10">
        <p style="padding-top: 20px">Hola {persona_nom}!</p>
        <p style="padding-top: 20px">T'enviem aquest correu perquè algú ha 
            sol·licitat el reinici de la contrasenya del compte {persona_email}
            a {absolute_url}</p>
        <p style="margin-left: 60px">Si no has estat tu qui ho ha demanat, 
            ignora aquest correu. Si segueixes rebent aquest correu repetidament,
            podria voler dir que algú està intentant obtenir accés al teu 
            compte, et recomanem que posis una contrasenya el més llarga 
            possible i que avisis a les administradores de la plataforma.</p>
        <p style="margin-left: 60px">Per establir una nova contrasenya fes
            servir aquest enllaç: {password_reset_url}</p>
      </td>
    </tr>
    <tr>
      <td align="center" class="em_text1 pad10" bgcolor="#fafafa" style="padding-bottom: 15px;">
        <a href="{url_web_comunalitat}" style="color:#e94e1b; text-decoration:none; font-weight: bold;">Fins aviat!</a>
      </td>
    </tr>
    </table>""",
            default_template_path='emails/front_generic.html'
        )
    ])

    obj, created = mail_model.objects.update_or_create(
        text_identifier='EMAIL_ENROLLMENT_POLL',
        defaults={
            'text_identifier': 'EMAIL_ENROLLMENT_POLL',
            'subject': "Enquesta de valoració de {activitat_nom}",
            'body': """<table align="center" width="100%" border="0" cellspacing="0" cellpadding="0" bgcolor="#f0f0f0">
    <tr>
      <td align="center" valign="top" class="em_text1 pad10">
        <p>Enquesta de valoració</p>
      </td>
    </tr>
    <tr>
      <td height="15" style="font-size:0px; line-height:0px; height:15px;">&nbsp;</td>
    </tr>
    <tr>
      <td align="center" valign="top" style="font-family:'Open Sans', Arial, sans-serif; font-size:22px;
      line-height:22px; color:#000; letter-spacing:2px; padding-bottom:12px;" class="pad10">
        <strong>{activitat_nom}</strong> de {comunalitat_nom}
      </td>
    </tr>
    <tr>
      <td height="25" class="em_h20" style="font-size:0px; line-height:0px; height:25px;">&nbsp;</td>
    </tr>
    <tr>
      <td align="left" valign="top" style="padding: 0px 40px 10px 40px" bgcolor="#fafafa" class="em_text1 pad10">
        <p style="padding-top: 20px">Hola {persona_nom}!</p>
        <p style="padding-top: 20px">T'enviem aquest correu perquè has participat a aquesta sessió:</p>
        <p style="margin-left: 60px"><strong>Data:</strong> {activitat_data_inici}</p>
        <p style="margin-left: 60px"><strong>Hora:</strong> {activitat_hora_inici}</p>
        <p style="margin-left: 60px"><strong>Lloc:</strong> {activitat_lloc}</p>
        <p style="padding-top: 20px">Els resultats de les enquestes de valoració 
        son una eina imprescindible pel funcionament d'aquesta formació 
        gratuïta subvencionada.</p>
        <p style="padding-top: 20px">Si us plau, omple <a href="{absolute_url_poll}">l'enquesta de valoració</a>.
        </p> 
        <p style="padding-top: 20px">Descàrrega del material formatiu: <a href="{absolute_url_activity}">Fitxa de la sessió</a>.</p>
        <p>
          Pots gestionar les teves dades i inscripcions accedint a l'aplicació amb el teu compte i anant a 
        l'apartat <a href="{absolute_url_my_activities}">Perfil -> Els Meus Cursos</a>.</p>
      </td>
    </tr>
    <tr>
      <td align="center" class="em_text1 pad10" bgcolor="#fafafa" style="padding-bottom: 15px;">
        <a href="{url_web_comunalitat}" style="color:#e94e1b; text-decoration:none; font-weight: bold;">Fins aviat!</a>
      </td>
    </tr>
    </table>""",
            'default_template_path': 'emails/front_generic.html'
        },
    )
    print('EMAIL_ENROLLMENT_POLL template updated.')


class Migration(migrations.Migration):

    dependencies = [
        ('coopolis', '0002_data_unaccent_enable'),
        ('mailing_manager', '__latest__'),
    ]

    operations = [
        migrations.RunPython(populate_mail_templates),
    ]
