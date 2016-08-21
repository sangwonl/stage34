from handlers import stage


url_patterns = [
    (r'^/api/v1/stages/?$', stage.StageRootHandler),
    (r'^/api/v1/stages/(\d+)/?$', stage.StageDetailHandler),
]