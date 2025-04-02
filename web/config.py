import os


class Config:

    USER_INFO_MAPPING = {
        "google": {
            "email": "email",
            "name": "name"},
        "microsoft": {
            "email": "userPrincipalName",
            "name": "displayName"}
    }

    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "supersecretkey")  # Change for production

    USER_INFO_ENDPOINT = {
            "google": "https://www.googleapis.com/oauth2/v2/userinfo",
            "github": "https://api.github.com/user",
            "gitlab": "https://gitlab.com/api/v4/user",
            "microsoft": "https://graph.microsoft.com/v1.0/me",
        }

    OAUTH_PROVIDERS = {
        "google": {
            "client_id": os.environ.get("GOOGLE_CLIENT_ID"),
            "client_secret": os.environ.get("GOOGLE_CLIENT_SECRET"),
            "authorization_url": "https://accounts.google.com/o/oauth2/auth",
            "token_url": "https://oauth2.googleapis.com/token",
            "base_url": "https://www.googleapis.com/oauth2/v4/",
            "scope": [
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile"
            ],
        },
        "microsoft": {
            "client_id": os.environ.get("MICROSOFT_CLIENT_ID"),
            "client_secret": os.environ.get("MICROSOFT_CLIENT_SECRET"),
            "authorization_url": "https://login.microsoftonline.com/common/oauth2/v2.0/authorize",
            "token_url": "https://login.microsoftonline.com/common/oauth2/v2.0/token",
            "base_url": "https://graph.microsoft.com/v1.0/",
            "scope": [
                "openid",
                "email",
                "profile",
                "User.Read"  # ✅ Allows reading basic user info
             ],
        },
        # "gitlab": {
        #     "client_id": os.environ.get("GITLAB_CLIENT_ID"),
        #     "client_secret": os.environ.get("GITLAB_CLIENT_SECRET"),
        #     "authorization_url": "https://accounts.google.com/o/oauth2/auth",
        #     "token_url": "https://oauth2.googleapis.com/token",
        #     "base_url": "https://www.googleapis.com/oauth2/v4/",
        #     "scope": ["read_user"],
        # },
        # "github": {
        #     "client_id": os.environ.get("GITHUB_CLIENT_ID"),
        #     "client_secret": os.environ.get("GITHUB_CLIENT_SECRET"),
        #     "authorization_url": "https://accounts.google.com/o/oauth2/auth",
        #     "token_url": "https://oauth2.googleapis.com/token",
        #     "base_url": "https://www.googleapis.com/oauth2/v3/userinfo",
        #     "scope": ["read:user"],
        # },
    }
