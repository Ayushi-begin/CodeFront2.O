from authlib.integrations.flask_client import OAuth
from config.settings import Settings

oauth = OAuth()
google = oauth.register(
    name='google',
    client_id=Settings.GOOGLE_CLIENT_ID,
    client_secret=Settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url=Settings.GOOGLE_DISCOVERY_URL,
    client_kwargs={'scope': 'openid email profile'}
)
