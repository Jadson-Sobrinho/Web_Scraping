from flask import Flask
from routes import quarter, lastyear

app = Flask(__name__)

app.register_blueprint(quarter.bp)
app.register_blueprint(lastyear.bp)

if __name__ == '__main__':
    app.run(debug=True)



