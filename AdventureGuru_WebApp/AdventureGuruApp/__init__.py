import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_restful import Api,Resource
#from flask_login import LoginManager

##############################################################

                        #App Setup

##############################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

##############################################################

                        #Mail Setup

##############################################################

mail = Mail()
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'adventuregurutravels@gmail.com'
app.config["MAIL_PASSWORD"] = 'Travel4-ever'
mail.init_app(app)

##############################################################

                        #Database Setup

##############################################################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)



##############################################################

                        #Login Setup

##############################################################

#login_manager = LoginManager()

#login_manager.init_app(app)
#login_manager.login_view = 'user.login'

##############################################################

                        #Restful Api Setup

##############################################################

api = Api(app)
from AdventureGuruApp.destinations.api import destinationAPI,allDestinationAPI

api.add_resource(destinationAPI, '/api/destination/<string:title>')
api.add_resource(allDestinationAPI,'/api/destination/all/<string:location>')

##############################################################

                        #Blueprint Setup

##############################################################

from AdventureGuruApp.core.views import core
#from AdventureGuruApp.users.views import users
from AdventureGuruApp.destinations.views import destinations
from AdventureGuruApp.error_pages.handler import error_pages


app.register_blueprint(core)
#app.register_blueprint(users)
app.register_blueprint(destinations)
app.register_blueprint(error_pages)
