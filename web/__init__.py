import os
from datetime import timedelta

from flask import Flask, redirect, url_for, session, request
from flask_session import Session
from authlib.integrations.flask_client import OAuth


app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET_KEY")

# Session configuration (stores session on filesystem)
app.config["SESSION_TYPE"] = "filesystem"  # Store session data in files instead of cookies
app.config["SESSION_FILE_DIR"] = "./flask_session"
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=30)
Session(app)
Session(app)  # Initialize Flask-Session

# OAuth setup
oauth = OAuth(app)
app.config["GOOGLE_CLIENT_ID"] = os.getenv("GOOGLE_CLIENT_ID")
app.config["GOOGLE_CLIENT_SECRET"] = os.getenv("GOOGLE_CLIENT_SECRET")
# app.config["GOOGLE_DISCOVERY_URL"] = "https://accounts.google.com/.well-known/openid-configuration"

google = oauth.register(
    name="google",
    client_id=app.config["GOOGLE_CLIENT_ID"],
    client_secret=app.config["GOOGLE_CLIENT_SECRET"],
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


# Redirect root URL to login
@app.route("/")
def home():
    return redirect(url_for("login"))


# Login route
@app.route("/login")
def login():
    # session["oauth_state"] = os.urandom(24).hex()  # Generate and store state
    session["oauth_state"] = google.create_authorization_url(
        "https://accounts.google.com/o/oauth2/auth"
    )["state"]
    return google.authorize_redirect(url_for("authorized", _external=True), state=session["oauth_state"])


# OAuth callback
@app.route("/login/callback")
def authorized():
    try:
        # Log request state and session state
        app.logger.debug(f"Received state: {request.args.get('state')}, Session state: {session.get('oauth_state')}")

        if "oauth_state" not in session:
            return "Session expired. Please try logging in again.", 400  # Prevent CSRF error

        if request.args.get("state") != session["oauth_state"]:
            return "State mismatch detected. Possible CSRF attack.", 400  # Prevent CSRF error

        # Retrieve token
        token = google.authorize_access_token()
        user_info = google.get("https://www.googleapis.com/oauth2/v3/userinfo").json()

        session["user"] = user_info  # Store user info in session
        session.pop("oauth_state", None)  # Clear state after successful login

        return f"Hello, {user_info['name']}!"

    except Exception as e:
        app.logger.error(f"OAuth error: {str(e)}")
        return f"Error during OAuth callback: {str(e)}", 500


# Logout route
@app.route("/logout")
def logout():
    session.clear()  # Clears session completely
    return redirect(url_for("login"))
