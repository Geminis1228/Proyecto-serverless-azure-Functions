# Proyecto Serverless con Azure Functions 🚀
Este proyecto es una aplicación serverless construida con **Azure Functions**, diseñada para ofrecer funciones de backend escalables y eficientes sin necesidad de administrar servidores.
## 📂 Estructura del Proyecto
Pasos resumidos para crear y probar una Azure Function (Python) localmente
1. Creamos la estructura del proyecto
PasswordGenerator/
├── .venv/ #  Entorno virtual
├── function_app.py # Código de la función
├── requirements.txt # Dependencias
├── local.settings.json # Variables locales
└── PasswordGen/function.json # Configuración del trigger
2. Creamos y activar entorno virtual
python3 -m venv .venv # Crear entorno virtual
source .venv/bin/activate # Linux/macOS
.venv\Scripts\activate # Windows
3. Instalamos las dependencias
pip install azure-functions
Y creamos el archivo requirements.txt con:
pgsql
azure-functions
4. Código de la función (function_app.py)
python
import azure.functions as func
import logging
import json
import random
import string
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)
@app.route(route="GeneratePassword", methods=["POST"])
def generate_password(req: func.HttpRequest) -> func.HttpResponse:
 logging.info('Solicitud recibida para generar contraseña.')
 try:
 data = req.get_json()
 length = data.get("length", 12)
 include_symbols = data.get("include_symbols", True)
 include_numbers = data.get("include_numbers", True)
 if not isinstance(length, int) or length < 4:
 return func.HttpResponse(
 json.dumps({"error": "La longitud debe ser un número entero mayor o igual a 4."}),
 status_code=400,
 mimetype="application/json"
 )
 characters = string.ascii_letters
 if include_numbers:
 characters += string.digits
 if include_symbols:
 characters += string.punctuation
 password = ''.join(random.choice(characters) for _ in range(length))
 return func.HttpResponse(
 json.dumps({"password": password}),
 status_code=200,
 mimetype="application/json"
 )
 except Exception as e:
 return func.HttpResponse(
 json.dumps({"error": str(e)}),
 status_code=500,
 mimetype="application/json"
 )
5. Configuramos el trigger (PasswordGen/function.json)
{
 "scriptFile": "../function_app.py",
 "bindings": [
 {
 "authLevel": "anonymous",
 "type": "httpTrigger",
 "direction": "in",
 "name": "req",
 "methods": ["post"],
 "route": "GeneratePassword"
 },
 {
 "type": "http",
 "direction": "out",
 "name": "$return"
 }
 ]
}
6. Ejecutar la Azure Function local
func start
Debe aparecer algo asi:
CopyEdit
Functions:
 generate_password: [POST] http://localhost:7071/api/GeneratePassword
7. Probar con curl
curl -X POST http://localhost:7071/api/GeneratePassword \
-H "Content-Type: application/json" \
-d '{"length": 16, "include_symbols": true, "include_numbers": true}'
Respuesta esperada:
json
CopyEdit
{"password": "EjemploDeContraseña!"}
