import os

from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy

from pyramid_beaker import session_factory_from_settings

from trans.resources import Root
from trans.security import getgroup
from trans.security import logout

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    root = settings.get('root', None)
    print 'root = %s' % root
    if root is None:
        raise ValueError('Root directory required!')

    def get_root(request):
        return Root(os.path.abspath(os.path.normpath(root)))

    config = Configurator(root_factory=get_root, settings=settings,
                          session_factory=session_factory_from_settings(settings),
                          authentication_policy=AuthTktAuthenticationPolicy(settings.pop('authkey'), callback=getgroup),
                          authorization_policy=ACLAuthorizationPolicy())
    config.add_static_view(name='static', path='trans:static')
    config.add_view(logout)

    config.scan()

    return config.make_wsgi_app()

