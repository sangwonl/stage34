import handlers


url_patterns = [
    (r'^/auth/social_auth_url/?$', handlers.SocialAuthUrlHandler),
]