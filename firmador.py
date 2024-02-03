# *-* coding: utf-8 *-*
import datetime
from cryptography.hazmat import backends
from cryptography.hazmat.primitives.serialization import pkcs12

from endesive.pdf import cms

import PyPDF2
import io
from datetime import datetime, timezone


def obtener_altura_pdf(pdf_content):
    pdf_stream = io.BytesIO(pdf_content)
    reader = PyPDF2.PdfReader(pdf_stream)
    primera_pagina = reader.pages[0]

    return int(primera_pagina.mediabox.top)


def formatear_fecha_firma(fecha_firma):
    try:
        # Analizar la fecha y establecer la zona horaria en UTC
        fecha_obj = datetime.strptime(fecha_firma, "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)
        
        # Formatear la fecha en formato PDF
        fecha_formateada = fecha_obj.strftime("D:%Y%m%d%H%M%S%fZ")
        return fecha_formateada
    except ValueError:
        return None


def firmar(contraseña, certificado, pdf, posicion_x, posicion_y, pagina_firmar, fecha_firma):
    # Leer el contenido del PDF una sola vez
    pdf_content = pdf.read()

    # Obtener Altura del PDF
    altura_pagina = obtener_altura_pdf(pdf_content)

    print(altura_pagina)

    # Obtener las coordenadas de la firma desde el formulario
    x, y = int(posicion_x), int(posicion_y)

    # Obtener la altura de la firma (25 en este caso, puedes ajustarla según sea necesario)
    firma_altura = 45
    firma_ancho = 124

    # Calcular la nueva posición Y para que el punto (0,0) sea la esquina superior izquierda
    y = altura_pagina - y - firma_altura
    x = int(posicion_x)

    # Definir signaturebox con las nuevas coordenadas
    signaturebox = (x, y, x + firma_ancho, y + firma_altura)

    dct = {
        "aligned": 0,
        "sigflags": 3,
        "sigflagsft": 132,
        "sigpage": int(pagina_firmar) - 1,  # Página seleccionada para firmar
        "sigbutton": True,
        "sigfield": "Signature1",
        "auto_sigfield": True,
        "sigandcertify": True,
        "signaturebox": signaturebox,
        "signature_img": "qr.png",
        "contact": "hola@ejemplo.com",
        "location": "",
        "signingdate": formatear_fecha_firma(fecha_firma),  # Utilizar la fecha de firma directamente
        "reason": "",
        "password": contraseña,
    }

    p12 = pkcs12.load_key_and_certificates(
        certificado.read(), contraseña.encode("ascii"), backends.default_backend()
    )

    datas = cms.sign(pdf_content, dct, p12[0], p12[1], p12[2], "sha256")

    return pdf_content, datas
