import io
from flask import Flask, render_template, request, send_file
from firmador import firmar
from datetime import datetime, timezone

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def formatear_fecha_firma(fecha_firma):
    try:
        # Agregar la zona horaria UTC si no está presente en la cadena
        if 'Z' not in fecha_firma:
            fecha_firma += 'Z'

        # Analizar la fecha y establecer la zona horaria en UTC
        fecha_obj = datetime.strptime(fecha_firma, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        
        # Formatear la fecha en formato PDF
        fecha_formateada = fecha_obj.strftime("D:%Y%m%d%H%M%S%fZ")
        return fecha_formateada
    except ValueError:
        return None
@app.route('/')
def index():
    return render_template("formulario.html")


@app.route('/procesar',  methods=['POST'])
def procesar():
    pdf = request.files.get("pdf")
    firma = request.files.get("firma")
    contraseña = request.form.get("palabra_secreta")
    posicion_x = request.form.get("posicion_x")
    posicion_y = request.form.get("posicion_y")
    pagina_firmar = request.form.get("pagina_firmar")
    fecha_firma = request.form.get("fecha_firma")  # Agregado

    archivo_pdf_para_enviar_al_cliente = io.BytesIO()
    try:
        datau, datas = firmar(contraseña, firma, pdf, posicion_x, posicion_y, pagina_firmar, fecha_firma)
        archivo_pdf_para_enviar_al_cliente.write(datau)
        archivo_pdf_para_enviar_al_cliente.write(datas)
        archivo_pdf_para_enviar_al_cliente.seek(0)
        return send_file(archivo_pdf_para_enviar_al_cliente, mimetype="application/pdf",
                         download_name="firmado" + ".pdf",
                         as_attachment=True)
    except ValueError as e:
        return "Error firmando: " + str(e) + ". Se recomienda revisar la contraseña y el certificado"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=81)
