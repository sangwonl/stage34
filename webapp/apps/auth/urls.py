import handlers


url_patterns = [
    (r'^/auth/github_auth_url/?$', handlers.GithubAuthUrlHandler),
    (r'^/auth/github/callback/?$', handlers.GithubCallbackHandler),
    (r'^/auth/login/?$', handlers.LoginHandler)
]