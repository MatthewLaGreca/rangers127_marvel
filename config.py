import os #operating system
from dotenv import load_dotenv #allows us to load environment variables (aka the ones in .env) to do certain things with our app
from datetime import timedelta


basedir = os.path.abspath(os.path.dirname(__file__)) #this is establishing our base directory or our root folder, aka "haagen_dazs"
load_dotenv(os.path.join(basedir, '.env')) #this is just pointing us to the direction of our environment variables

#reminder, this Config class can be used in many instances, say one for development configuration and one for production configuration
class Config():
    """
    Set the configuration variables for my flask app, the marvel comic books jawn
    Using Environment variables where avaiable otherwise
    Creat config variables
    """

    FLASK_APP = os.environ.get('FLASK_APP') # this is what makes the haagen_dasz folder register as the flask app
    FLASK_ENV = os.environ.get('FLASK_ENV') # the .env shows this to be in development, currently
    FLASK_DEBUG = True # allows us to make changes to the flask app while it's running and give us better error messages when they occur
    SECRET_KEY = os.environ.get('SECRET_KEY') or "I got that one hitta quitta"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False #When our database gets updated in anyway, we want to hide the update messages
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=365) # the token that is given out to interface with our api will expire in 365 days, but then again how does it ever get reset if it's hard coded in .env?
