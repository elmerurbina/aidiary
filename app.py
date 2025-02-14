import os
from flask import Flask
from routes.routes import setup_routes

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

# Configurar las rutas
setup_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
