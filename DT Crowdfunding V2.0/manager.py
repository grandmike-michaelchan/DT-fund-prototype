from flask_script import Manager
# obtain info from views.py and instruct manager.py
from app.views import app
from db import dbhelper

# manager.py manages and prompt command to execute in dbhelper.py
# Preliminary setting: pip install flask-script
# Initialize database(type in terminal): python manager.py create_tables
# Insert data(type in terminal): python manager.py load_data
# Start server here: python manager.py runserver

manager = Manager(app)

################################################################
#Execute shell debug: python manager.py shell                  #
#from app.models import Customer, Goods, Orders, OrderLineItem #
#from app.view import db                                       #
#orders = db.session.query(Orders).filter_by(id='xxxxx').one() #
#orders.orderLineItems                                         #
################################################################ 

# Execute dbhelper createtablesfunction
# @manager.command to invoke flask script act as cmd commands
@manager.command
def create_tables():
    dbhelper.create_tables()

# Execute dbhelper to insert store data into the database
@manager.command
def load_data():
    dbhelper.load_data()


if __name__ == '__main__':
    manager.run()
