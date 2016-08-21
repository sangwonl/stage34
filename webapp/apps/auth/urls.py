import handlers


url_patterns = [
    (r'^/api/v1/auth/github_auth_url/?$', handlers.GithubAuthUrlHandler),
    (r'^/api/v1/auth/github/callback/?$', handlers.GithubCallbackHandler),
    (r'^/api/v1/auth/login/?$', handlers.LoginHandler)
]