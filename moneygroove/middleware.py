from django.http import HttpResponseRedirect


ANONYMOUS_ALLOW_LIST = [
    '/static/',
    '/api/',
    '/favicon.ico',
    '/login/',
    '/login/',
]


def is_whitelist(path):
    return any(path.startswith(x) for x in ANONYMOUS_ALLOW_LIST)


def auth_middleware(get_response):

    def auth_middleware_inner(request):
        if not request.user.is_authenticated and not is_whitelist(request.path):
            return HttpResponseRedirect('/login/?next=/')

        return get_response(request)

    return auth_middleware_inner
