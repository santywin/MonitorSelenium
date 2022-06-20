import smtplib
import imghdr
import glob
from email.message import EmailMessage
from email.mime.text import MIMEText


def enviar_correo(id, contenido):
    html = """\
    <html>
      <head></head>
      <body>
        <p>
            Estimado
        </p>
        <p>
            Se ha detectado un error en los servicios web:
        </p>
    """

    msg = EmailMessage()
    msg['Subject'] = 'ALERTA: Monitor de servicios'
    me = 'scastroar@est.ups.edu.ec'
    destinatarios = ['scastroa1@ups.edu.ec']
    msg['From'] = me
    msg['To'] = ', '.join(destinatarios)
    msg.preamble = 'You will not see this in a MIME-aware mail reader.\n'
    # Adjuntar las imágenes de las capturas de pantalla
    pngfiles = glob.glob('imagenes/error_%s_*.png' % id)
    for file in pngfiles:
        with open(file, 'rb') as fp:
            img_data = fp.read()
        msg.add_attachment(img_data, maintype='image',
                           subtype=imghdr.what(None, img_data),
                           filename=file.replace('imagenes/', ''))

    with smtplib.SMTP(host='smtp.office365.com', port=587) as s:
        s.starttls()
        s.login('scastroar@est.ups.edu.ec', 'Motepillo90')

        html = html + "<p style='font-family: monospace;'>" + contenido + "</p>" + "</p></body></html>"

        msg.attach(MIMEText(html, 'html'))
        s.send_message(msg)
