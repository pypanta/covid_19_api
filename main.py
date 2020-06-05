from flask import Flask
from flask_babel import Babel

from settings import Config


app = Flask(__name__)
app.config.from_object(Config)
#app.config['JSON_SORT_KEYS'] = False
babel = Babel(app)

from routes import views
app.register_blueprint(views.covid)
