from flask import Flask
import auth, mate

app = Flask(__name__)

app.register_blueprint(auth.bp)
app.register_blueprint(mate.bp)


if __name__ == '__main__':
    app.run()
