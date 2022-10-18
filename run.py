
from application import app
from config import config
from application.routes.users import user_bp
from application.routes.post import post_bp
from application.routes.medicines import medicines_bp
from application.routes.meetings import meetings_bp



if __name__ == '__main__':
    app.register_blueprint(user_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(medicines_bp)
    app.register_blueprint(meetings_bp)
    app.config.from_object(config['development'])
    app.run(threaded=True, port=5000)