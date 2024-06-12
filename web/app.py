from flask import Flask
from routes.add_device import simple_page
from routes.list_device import list_devices
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.register_blueprint(simple_page)
app.register_blueprint(list_devices)
