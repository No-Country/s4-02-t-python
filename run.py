
from application import app
from config import config
from application.routes.users import user_bp


if __name__ == '__main__':
    app.register_blueprint(user_bp)
    app.config.from_object(config['development'])
    app.run()