import pymsteams

# myTeamsMessage = pymsteams.connectorcard(
#    "https://outlook.office.com/webhook/cef3cea6-d8e0-4017-b5af-546281f69f1b@d6438082-eb98-4c3f-8397-5dbdfe4036fd"
#    "/IncomingWebhook/ee35026c498d4872ba3f115b4e3ad749/a4c2bede-bbe1-4bac-9e2c-8fcc00187c20")

myTeamsMessage = pymsteams.connectorcard(
    "https://outlook.office.com/webhook/cef3cea6-d8e0-4017-b5af-546281f69f1b@d6438082-eb98-4c3f-8397-5dbdfe4036fd"
    "/IncomingWebhook/a808eac2956548db840dc8f70b89c6dd/a4c2bede-bbe1-4bac-9e2c-8fcc00187c20")


def enviar_notificacion(mensaje):
    myMessageSection = pymsteams.cardsection()
    myTeamsMessage.text("ALERTA: Monitor de servicios")
    myMessageSection.activityTitle("Registro de la alerta")
    myMessageSection.text(mensaje)
    myTeamsMessage.addSection(myMessageSection)
    myTeamsMessage.send()
