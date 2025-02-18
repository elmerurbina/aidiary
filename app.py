import os
from flask import Flask
from routes.routes import setup_routes

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', '4921d111085d8c5ca331af4c50a3cc0b11e0db88ea1befb6a257142b83589e49')

# Configurar las rutas
setup_routes(app)

if __name__ == "__main__":
    app.run(debug=True)
