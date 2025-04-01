from flask import Flask
from routes import quarter, lastyear, operadoras

app = Flask(__name__)

app.register_blueprint(quarter.bp)
app.register_blueprint(lastyear.bp)
app.register_blueprint(operadoras.bp)

if __name__ == '__main__':
    app.run(debug=True)



