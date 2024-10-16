from fastapi import FastAPI
from routes.routes import temperatura_router

app = FastAPI()

# Incluir el router de temperatura_router con la etiqueta 'Conversiones de Temperaturas'
app.include_router(temperatura_router, tags=["Conversiones de Temperaturas"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)


mkdir -p /var/www/html/demo_webapp
mkdir -p /var/www/html/demo_webapp/utils
mkdir -p /var/www/html/demo_webapp/templates

#######################################

cat > /var/www/html/demo_webapp/app.py << "EOF"
from flask import Flask, render_template, request, redirect, url_for, flash
from utils.utils import obtener_conversiones, crear_conversion

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesaria para usar flash messages

@app.route('/temperaturas', methods=['GET'])
def get_temperaturas():
    conversiones = obtener_conversiones()
    return render_template('get_temperaturas.html', conversiones=conversiones)

@app.route('/temperaturas/crear', methods=['GET', 'POST'])
def create_temperatura():
    if request.method == 'POST':
        resultado = request.form['resultado']
        tipo = request.form['tipo']
        exito = crear_conversion(resultado, tipo)
        if exito:
            flash('Conversión creada exitosamente', 'success')
            return redirect(url_for('get_temperaturas'))
        else:
            flash('Error al crear la conversión', 'danger')
    return render_template('create_temperatura.html')

if __name__ == '__main__':
    app.run(debug=True)
EOF
########################################
cat > /var/www/html/demo_webapp/utils/utils.py << "EOF"
import requests

API_URL = "http://localhost:80/api/conversiones/temperatura"

def obtener_conversiones():
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener conversiones: {e}")
        return []

def crear_conversion(resultado, tipo):
    nueva_conversion = {
        "resultado": resultado,
        "tipo": tipo
    }
    try:
        response = requests.post(API_URL, json=nueva_conversion)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error al crear la conversión: {e}")
        return False
EOF