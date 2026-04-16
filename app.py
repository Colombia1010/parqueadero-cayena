from flask import Flask, request, render_template, redirect, session, url_for, send_from_directory
import os
from werkzeug.utils import secure_filename
from usuarios import UsuarioManager
from servicios import UsuarioServicio
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from flask import send_file
import io

app = Flask(__name__)
app.secret_key = "clave_secreta"

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

usuario_manager = UsuarioManager()
usuario_servicio = UsuarioServicio()

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def archivo_permitido(nombre):
    return '.' in nombre and nombre.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ---------------------------
# HOME
# ---------------------------
@app.route('/')
def inicio():
    return render_template('formulario.html')


# ---------------------------
# REGISTRO
# ---------------------------
@app.route('/registro', methods=['POST'])
def registro():

    cedula = request.form['cedula']
    nombre = request.form['nombre']

    torre = request.form['torre']
    apto = request.form['apto']
    nombre_propiedad = request.form['nombre_propiedad']
    celular = request.form['celular']
    correo = request.form['correo']
    nombre_propietario = request.form['nombre_propietario']
    mail_propietario = request.form['mail_propietario']
    celular1 = request.form.get('celular1')
    nombre_arrendatario = request.form.get('nombre_arrendatario')
    vehiculo = request.form['vehiculo']
    placa = request.form['placa']
    marca = request.form['marca']
    modelo = request.form['modelo']
    color = request.form['color']

    # VALIDACIONES
    if len(torre) > 2:
        return "Torre inválida"

    if len(apto) > 4:
        return "Apto inválido"

    if not celular.isdigit() or len(celular) != 10:
        return "Celular inválido"

    if len(placa) > 6:
        return "Placa inválida"

    # Crear carpeta usuario
    ruta_usuario = os.path.join(UPLOAD_FOLDER, cedula)
    os.makedirs(ruta_usuario, exist_ok=True)

    # Guardar archivos
    for campo in ['cedula_doc', 'soat', 'tarjeta']:
        archivo = request.files[campo]

        if archivo and archivo_permitido(archivo.filename):
            nombre_seguro = secure_filename(archivo.filename)
            archivo.save(os.path.join(ruta_usuario, nombre_seguro))
        else:
            return f"Archivo inválido: {campo}"

    # Guardar usuario
    usuario_manager.guardar_usuario(
        cedula, nombre, torre, apto, nombre_propiedad, celular, correo,
        nombre_propietario, mail_propietario, celular1,
        nombre_arrendatario, vehiculo, placa, marca, modelo, color
    )

    return "Registro exitoso"


# ---------------------------
# ADMIN
# ---------------------------
@app.route('/admin')
def admin():
    if not session.get('admin'):
        return redirect('/login')

    usuarios = usuario_servicio.obtener_usuarios_con_estado()
    return render_template('admin.html', usuarios=usuarios)

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image
from flask import send_file
import io


@app.route('/exportar_excel')
def exportar_excel():

    usuarios = usuario_servicio.obtener_usuarios_con_estado()

    wb = Workbook()
    ws = wb.active
    ws.title = "Parqueadero Cayena"

    # -------------------------
    # LOGO
    # -------------------------
    try:
        import os
        ruta_logo = os.path.join(os.getcwd(), "static", "logo.png")
        print("Ruta logo:", ruta_logo)

        img = Image(ruta_logo)
        img.width = 120
        img.height = 80
        ws.add_image(img, "E1")

    except Exception as e:
        print("ERROR LOGO:", e)

    # -------------------------
    # TÍTULO
    # -------------------------
    ws.merge_cells('A5:K5')
    ws['A5'] = "REPORTE PARQUEADERO - CONJUNTO CAYENA"
    ws['A5'].font = Font(size=14, bold=True)
    ws['A5'].alignment = Alignment(horizontal="center")

    # -------------------------
    # HEADERS
    # -------------------------
    headers = [
        "Cédula", "Nombre", "Torre", "Apto", "Vehículo",
        "Placa", "Marca", "Modelo", "Color", "Celular", "Correo"
    ]

    ws.append([])
    ws.append(headers)

    header_row = ws.max_row

    fill = PatternFill(start_color="6366F1", end_color="6366F1", fill_type="solid")
    font = Font(bold=True, color="FFFFFF")

    for col in ws[header_row]:
        col.fill = fill
        col.font = font
        col.alignment = Alignment(horizontal="center")

    # -------------------------
    # DATOS
    # -------------------------
    for u in usuarios:
        ws.append([
            u.get("cedula"),
            u.get("nombre"),
            u.get("torre"),
            u.get("apto"),
            u.get("vehiculo"),
            u.get("placa"),
            u.get("marca"),
            u.get("modelo"),
            u.get("color"),
            u.get("celular"),
            u.get("correo")
        ])

    # -------------------------
    # BORDES
    # -------------------------
    thin = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    for row in ws.iter_rows(min_row=header_row, max_row=ws.max_row):
        for cell in row:
            cell.border = thin

    # -------------------------
    # AUTO AJUSTE
    # -------------------------
    for col in ws.columns:
        max_length = 0
        col_letter = col[0].column_letter

        for cell in col:
            try:
                if cell.value:
                    max_length = max(max_length, len(str(cell.value)))
            except:
                pass

        ws.column_dimensions[col_letter].width = max_length + 3

    # -------------------------
    # FILTROS
    # -------------------------
    ws.auto_filter.ref = f"A{header_row}:K{header_row}"

    # -------------------------
    # EXPORTAR
    # -------------------------
    stream = io.BytesIO()
    wb.save(stream)
    stream.seek(0)

    return send_file(
        stream,
        as_attachment=True,
        download_name="reporte_cayena.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ---------------------------
# LOGIN
# ---------------------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

        if request.form['usuario'] == "admin" and request.form['password'] == "admin":
            session['admin'] = True
            return redirect('/admin')

        return "Credenciales incorrectas"

    return render_template('login.html')


# ---------------------------
# DESCARGAR ARCHIVOS
# ---------------------------
@app.route('/uploads/<cedula>/<filename>')
def descargar_archivo(cedula, filename):
    return send_from_directory(f'uploads/{cedula}', filename)


if __name__ == '__main__':
    app.run(debug=True)