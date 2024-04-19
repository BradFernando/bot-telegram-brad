from flask import Flask, request, render_template
from telegram import Bot
import asyncio

app = Flask(__name__)

# Importamos el token del bot
bot = Bot(token="6556491083:AAFKdXsUErUqMhHzsMNZhzkmN5OXWI7us0Y")

# Variable global para rastrear el número de factura actual
num_pedido_actual = 1

# Crea un nuevo bucle de eventos
loop = asyncio.new_event_loop()


@app.route('/api/receiveData', methods=['POST'])
def receive_data():
    data = request.json
    message_text = parse_web_app_data(data)

    # Utiliza el mismo bucle de eventos para enviar todos los mensajes
    loop.run_until_complete(bot.send_message(chat_id='2084365198', text=message_text))

    return {'status': 'success'}


# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')


def parse_web_app_data(data):
    global num_pedido_actual
    parsed_data = data  # data ya es un diccionario, no es necesario usar json.loads()
    message_text = " "
    numpedido = f"N° Pedido ✅: A#{num_pedido_actual}"
    message_text += f"*** {numpedido} ***\n\n"
    for i, item in enumerate(parsed_data['items'], start=1):
        position = int(item['id'].replace('item', ' '))
        message_text += f"🔸 Producto  {position}\n"
        message_text += f"Precio: {item['price']}\n\n"
    message_text += f" 🟰 El precio total es: {parsed_data['totalPrice']}"
    num_pedido_actual += 1  # Incrementamos el número de factura para el próximo mensaje
    return message_text


if __name__ == "__main__":
    app.run(port=5000)  # Flask server running on port 5000
