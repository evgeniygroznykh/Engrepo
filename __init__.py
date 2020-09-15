from flask import Flask
from models.shared_db import db
from views.routes import BLUEPRINTS
from models.dbconn import DBContext as DBC


app = Flask(__name__)

DBC.setup_db(app)
DBC.create_db(db, app)

for blueprint in BLUEPRINTS:
    app.register_blueprint(blueprint)

if __name__ == "__main__":
    app.run(debug=True)