from django.conf.urls import include, url

from handlers import auth


urlpatterns = [
    url(r'^auth/', include([
        url(r'^github_auth_url/?$', auth.GithubAuthUrlHandler.as_view()),
        url(r'^github/callback/?$', auth.GithubCallbackHandler.as_view()),
        url(r'^login/?$', auth.LoginHandler.as_view())
    ]))
]