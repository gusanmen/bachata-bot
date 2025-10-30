import os
import requests
import random
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.utils import formataddr

# Configuración de Airtable
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
BASE_ID = 'appQWpQImABOspxQ6'
TABLE_NAME = 'Tabla'
AIRTABLE_URL = f"https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}"
HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}"
}

# Configuración del correo
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
# DESTINATARIOS = "ggusanmen@gmail.com"
DESTINATARIOS = "ggusanmen@gmail.com,mlocamu@gmail.com,thaiscintascamacho@gmail.com,appivan99@gmail.com,luciasc2020@gmail.com,romugarces@gmail.com,mrosacm67@gmail.com,mariangeles.camu@hotmail.com,paaulasscc@gmail.com"
lista_destinatarios = [email.strip() for email in DESTINATARIOS.split(",") if email.strip()]

def obtener_fila_aleatoria():
    response = requests.get(AIRTABLE_URL, headers=HEADERS)
    if response.status_code != 200:
        print("Error al obtener los datos de Airtable")
        print(response.text)
        return None

    records = response.json().get("records", [])
    if not records:
        print("No hay registros en Airtable")
        return None

    registro = random.choice(records)
    return registro["fields"]

def enviar_correo(contenido):
    # Orden específico de campos
    orden_campos = [
        "Data",
        "Nom",
        "Notes",
        "Video",
        "Video Música",
        "Coreografía",
        "Nemotecnia",
        "Calificació"
    ]

    # Construir cuerpo en el orden definido
    cuerpo_lineas = []

    for campo in orden_campos:
        if campo in contenido:
            cuerpo_lineas.append(f"{campo}: {contenido[campo]}")

    # Agregar otros campos no definidos en el orden (si existen)
    otros_campos = [k for k in contenido if k not in orden_campos]
    for campo in otros_campos:
        cuerpo_lineas.append(f"{campo}: {contenido[campo]}")

    # Unir todo en un solo texto
    cuerpo = "\n".join(cuerpo_lineas)

    # Crear mensaje de correo
    mensaje = MIMEText(cuerpo, 'plain', 'utf-8')
    mensaje["Subject"] = Header("¡Qué alegría!, un paso de Bachata al día 💃🏽🕺", "utf-8")
    mensaje["From"] = formataddr((str(Header("Bachata Bot", "utf-8")), EMAIL_USER))
    mensaje["To"] = DESTINATARIOS

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as servidor:
            servidor.starttls()
            servidor.login(EMAIL_USER, EMAIL_PASS)
            servidor.sendmail(EMAIL_USER, lista_destinatarios, mensaje.as_string())
            print("✅ Correo enviado correctamente.")
    except Exception as e:
        print("❌ Error al enviar el correo:", repr(e))

def main():
    fila = obtener_fila_aleatoria()
    if fila:
        enviar_correo(fila)
    else:
        print("No se pudo obtener una fila válida.")

if __name__ == "__main__":
    main()
