from django.conf.urls import include, url

from handlers import auth
from handlers import stage


urlpatterns = [
    url(r'^auth/', include([
        url(r'^github_auth_url/$', auth.GithubAuthUrlHandler.as_view()),
        url(r'^github/callback/$', auth.GithubCallbackHandler.as_view()),
        url(r'^login/$', auth.LoginHandler.as_view())
    ])),
    url(r'^api/v1/stages/', include([
        url(r'^$', stage.StageRootHandler.as_view()),
        url(r'^(?P<stage_id>\d+)/$', stage.StageDetailHandler.as_view()),
        url(r'^(?P<stage_id>\d+)/log/$', stage.StageLogHandler.as_view())
    ]))
]