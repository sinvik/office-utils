from functools import wraps
from flask import Blueprint, render_template, redirect, url_for, current_app, request

views = Blueprint("views", __name__)


def get_auth(provider):
    return current_app.config["oauth_providers"].get(provider)


def login_required():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print("decorator called")
            provider = request.args.get("provider")
            oauth = get_auth(provider)
            if not oauth or not oauth.is_authenticated():
                return redirect(url_for(f"{provider}.login"))  # Redirect dynamically
            return f(*args, **kwargs)
        return decorated_function
    return decorator


@views.route("/")
def home():
    return redirect(url_for("views.authorize"))  # Redirect to authorization page


@views.route("/authorize")
def authorize():
    return render_template("authorize.html")  # Show login page with provider options


@views.route("/login/<provider>/final-redirect")
def final_redirect(provider):
    oauth = get_auth(provider)
    if not oauth.is_authenticated():
        print("Failed to authenticate", 500)
        return redirect(url_for(f"{provider}.login"))  # Redirect dynamically

    return redirect(url_for("views.dashboard", provider=provider))  # ✅ Clean URL


@views.route("/dashboard")
@login_required()
def dashboard():
    provider = request.args.get("provider")
    oauth_blueprint = get_auth(provider)  # ✅ Get OAuth blueprint

    if not oauth_blueprint.is_authenticated():
        return redirect(url_for(f"{provider}.login"))

    collected_user_info = {}
    if oauth_blueprint.is_authenticated():
        user_info = oauth_blueprint.get_user_info(current_app.config["USER_INFO_ENDPOINT"][provider])
        if user_info.ok:
            collected_user_info["name"] = user_info.json()[current_app.config["USER_INFO_MAPPING"][provider]["name"]]
            collected_user_info["email"] = user_info.json()[current_app.config["USER_INFO_MAPPING"][provider]["email"]]

        else:
            return "Failed to fetch user info", 500

    print(collected_user_info)

    return render_template("dashboard.html", user=collected_user_info, provider=provider)


@views.route("/logout/<provider>")
def logout(provider):
    oauth = get_auth(provider)
    oauth.logout()
    return redirect(url_for("views.authorize"))


@views.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")

        provider = email.split("@")[1].split(".")[0]
        if provider == "gmail":
            provider = "google"

        elif provider == "outlook":
            provider = "microsoft"

        oauth = get_auth(provider)
        if not oauth.is_authenticated():
            return redirect(url_for(f"{provider}.login"))

    return render_template("signup.html")
