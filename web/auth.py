from flask_dance.consumer import OAuth2ConsumerBlueprint
from flask import session


class OAuthHandler:
    def __init__(self, app, provider_name, config):
        self.provider_name = provider_name
        provider_config = config.OAUTH_PROVIDERS.get(provider_name)

        if not provider_config:
            raise ValueError(f"Invalid OAuth provider: {provider_name}")

        self.blueprint = OAuth2ConsumerBlueprint(
            provider_name,
            __name__,
            client_id=provider_config["client_id"],
            client_secret=provider_config["client_secret"],
            authorization_url=provider_config["authorization_url"],
            token_url=provider_config["token_url"],
            base_url=provider_config["base_url"],
            scope=provider_config["scope"],
            redirect_url="final-redirect",
        )
        app.secret_key = config.SECRET_KEY
        app.register_blueprint(self.blueprint, url_prefix="/login")

    def is_authenticated(self):
        return self.blueprint.session.authorized

    def get_user_info(self, user_info_endpoint):
        if not self.is_authenticated():
            return None
        return self.blueprint.session.get(user_info_endpoint)

    def logout(self):
        session.pop(f"{self.provider_name}_oauth_token", None)
        session.clear()
