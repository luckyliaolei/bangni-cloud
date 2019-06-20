from flask import Flask
import auth, mate, data

app = Flask(__name__)

app.register_blueprint(auth.bp)
app.register_blueprint(mate.bp)
app.register_blueprint(data.bp)


if __name__ == '__main__':
    app.run()
