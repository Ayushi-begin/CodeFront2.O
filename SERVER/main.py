from flask import Flask, session
from routes.chatbot_routes import chatbot_bp
from routes.auth_routes import auth_bp        # ✅ import new auth routes
from utils.oauth_client import oauth          # ✅ import oauth setup
from config.settings import Settings            # ✅ import config for secret key
from routes.weather_routes import weather_bp
from routes.image_routes import image_bp
from routes.agentic_ai_routes import agentic_ai_bp
from flask import send_from_directory
from routes.history_routes import history_bp
import os


app = Flask(__name__)
app.secret_key = Settings.FLASK_SECRET_KEY            # ✅ required for session management

# Initialize OAuth
oauth.init_app(app)

# Register all route blueprints here
# Register the Weather Blueprint
app.register_blueprint(history_bp, url_prefix="/api")
app.register_blueprint(agentic_ai_bp, url_prefix="/api")
app.register_blueprint(image_bp, url_prefix="/api")
app.register_blueprint(weather_bp, url_prefix="/api") #✅ weather routes
app.register_blueprint(chatbot_bp)            # ✅ chatbot routes
app.register_blueprint(auth_bp)               # ✅ auth routes


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


@app.route("/")
def home():
    return '''
        <h2>🌱 Plant Health Scanner Backend is Running!</h2>
        <a href="/auth/login">Login with Google</a>
    '''

if __name__ == "__main__":
    app.run(host="localhost",debug=True, port=5000)
