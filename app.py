import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

# 1. Sistema de Logs para rastrear errores
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

app = Flask(__name__)
CORS(app) 

# 2. Configuración segura de la API Key
# Ahora lee la clave desde las variables de entorno de Render
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 3. Personalidad inyectada de forma nativa
INSTRUCCIONES_SISTEMA = """
Eres el 'Pastor SCala', un asistente de IA avanzado diseñado para un ministerio. 
Tu objetivo es brindar orientación, reflexión profunda y crecimiento personal. 
Tu tono debe ser compasivo, muy profesional, maduro y alineado con valores cristianos y bíblicos.

REGLA ESTRICTA: Tus respuestas deben ser precisas, directas y fáciles de entender. 
Responde en un máximo de 1 a 3 párrafos muy cortos. Nunca te extiendas demasiado.
"""

# Inicializamos el modelo de forma global
model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    system_instruction=INSTRUCCIONES_SISTEMA
)

@app.route('/chat', methods=['POST'])
def responder_chat():
    try:
        # Validación de datos entrantes
        datos = request.get_json()
        if not datos or 'mensaje' not in datos:
            return jsonify({"error": "Falta el mensaje"}), 400
        
        mensaje_usuario = datos.get('mensaje')
        if not mensaje_usuario.strip():
            return jsonify({"error": "El mensaje está vacío"}), 400

        # El modelo genera la respuesta
        respuesta = model.generate_content(mensaje_usuario)
        
        return jsonify({"respuesta": respuesta.text}), 200

    except Exception as e:
        logging.error(f"Fallo en la IA: {e}")
        return jsonify({"respuesta": "Dificultades técnicas en este momento. Intenta de nuevo."}), 500

if __name__ == '__main__':
    # Los servidores en la nube asignan el puerto automáticamente
    port = int(os.environ.get("PORT", 5000))
    print("\n=========================================")
    print(f" SERVIDOR IA INICIADO EN EL PUERTO {port}")
    print("=========================================\n")
    # Es vital que diga host='0.0.0.0' para que Render pueda leerlo
    app.run(host='0.0.0.0', port=port)
