from flask import Flask
from config import LocalDevelopmentConfig
from model import db, Users, Role
from flask_security import Security, SQLAlchemyUserDatastore
from create_initial_data import seed_initial_data


def createApp():
    app = Flask(__name__, static_folder="../frontend", static_url_path="/")
    app.config.from_object(LocalDevelopmentConfig)

    # Initialize model
    db.init_app(app)

    # Flask-Security
    datastore = SQLAlchemyUserDatastore(db, Users, Role)
    app.security = Security(app, datastore=datastore, register_blueprint=False)

    with app.app_context():
        db.create_all()
        seed_initial_data(datastore)  # Run the initial data script

    from resources import api  # Import API after app is created

    api.init_app(app)

    return app


app = createApp()

# Pass `app` explicitly to routes
import routes

routes.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
