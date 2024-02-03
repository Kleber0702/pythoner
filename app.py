from flask import Flask, render_template, request, jsonify, redirect
import fitz  # PyMuPDF
from tkinter import Tk, filedialog
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar_pdf', methods=['POST'])
def procesar_pdf():
    pdf_path = obtener_ruta_pdf()

    if pdf_path:
        return jsonify({'pdf_path': pdf_path})
    else:
        mensaje_error = 'No se seleccionó ningún archivo PDF.'
        return jsonify({'error': mensaje_error})

@app.route('/extraer_coordenadas', methods=['POST'])
def extraer_coordenadas():
    data = request.get_json()
    pdf_path = data['pdf_path']
    pagina = int(data['pagina'])
    coordenadas = data['coordenadas']

    if pdf_path and pagina and coordenadas:
        coordenadas = coordenadas.split(',')
        x, y, ancho, alto = map(float, coordenadas)

        # Lógica para procesar el PDF y extraer texto o realizar otras acciones con las coordenadas
        resultado = {'x': x, 'y': y, 'ancho': ancho, 'alto': alto}
        return redirect('/procesar_pdf.html')  # Redirigir al usuario después de extraer las coordenadas

    mensaje_error = 'Error al extraer coordenadas.'
    return jsonify({'error': mensaje_error})

def obtener_ruta_pdf():
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    file_path = filedialog.askopenfilename(title='Seleccionar archivo PDF', filetypes=[('PDF files', '*.pdf')])
    root.destroy()
    return file_path

if __name__ == '__main__':
    app.run(debug=True)
