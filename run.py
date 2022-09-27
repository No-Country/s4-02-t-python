from application import app
from config import config
from application import dbConnection




db = dbConnection()


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run()

