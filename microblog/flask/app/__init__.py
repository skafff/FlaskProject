from flask import Flask

from microblog.flask.myblueprint.main import main_bp


app = Flask(__name__)

app.CSRF_ENABLED = True
app.SECRET_KEY = 'you-will-never-guess'

app.register_blueprint(main_bp)


if __name__ == '__main__':
    app.run()
