import azure.functions as func
import logging
import json
import random
import string

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="PasswordGen", methods=["POST"])
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

        characters = string.ascii_letters  # Letras mayúsculas y minúsculas

        if include_numbers:
            characters += string.digits
        if include_symbols:
            characters += string.punctuation

        if not characters:
            return func.HttpResponse(
                json.dumps({"error": "No se seleccionaron tipos de caracteres válidos."}),
                status_code=400,
                mimetype="application/json"
            )

        # Generar contraseña
        password = ''.join(random.choice(characters) for _ in range(length))

        return func.HttpResponse(
            json.dumps({"password": password}),
            status_code=200,
            mimetype="application/json"
        )

    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "El cuerpo de la solicitud no es JSON válido."}),
            status_code=400,
            mimetype="application/json"
        )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
