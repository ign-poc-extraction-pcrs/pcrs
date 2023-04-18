from flask import Flask
from flask_cors import CORS
from app.controllers import pcrs, api


app = Flask(__name__)
CORS(app)

app.register_blueprint(pcrs.pcrs)
app.register_blueprint(api.api)
