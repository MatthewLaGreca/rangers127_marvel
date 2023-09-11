from flask import Flask # our flask app
from flask_migrate import Migrate # the ability to create and update our database
from flask_cors import CORS #need to research what this does
from flask_jwt_extended import JWTManager

#internal imports
from config import Config

app = Flask(__name__) # declaring our flask app
app.config.from_object(Config) # we need our flask app to pay attention to the configuration that we instantiated in the Config class
jwt = JWTManager(app) #anywhere in our app, we can use this JWT decorator to protect our routes from people who do not have the correct key to access the api

# to do: instantiate the login_manager 

# to do: register the blueprints for the sites

# to do: instantiate the database and migration calls