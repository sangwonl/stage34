import handlers


url_patterns = [
    (r'^/auth/github_auth_url/?$', handlers.GithubAuthUrlHandler),
]