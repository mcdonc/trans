import random
import string
import hashlib
from trans.resources import Root
from pyramid.httpexceptions import HTTPForbidden, HTTPFound
from pyramid.view import view_config
from pyramid.security import remember, forget
from pprint import pprint

USERS = {
    'user': ['salt', 'pw'],
}

GROUPS = {
    'user': ['group:users'],
}

def generatesalt(n=50):
    return ''.join(random.choice(string.ascii_uppercase +
                                 string.ascii_lowercase + string.digits)
                   for _ in range(n))

def calchash(pw, salt):
    pw = '%s%s' % (salt, pw)
    return hashlib.sha512(pw).hexdigest()

def getgroup(userid, request):
    if USERS.has_key(userid):
        if GROUPS.has_key(userid): return GROUPS[userid]
        else: return []
    else: return None

@view_config(context=HTTPForbidden, renderer='login.mak')
@view_config(context=Root, name='login', renderer='login.mak')
def viewlogin(context, request):
    print '----------- VIEWLOGIN'
    return {'username': ''}

@view_config(context=Root, request_param='login.submitted',
             request_method='POST', renderer='login.mak')
def login(context, request):
    print '------ DOLOGIN'
    username = request.params['username']
    password = request.params['password']

    if USERS.has_key(username) and calchash(password, USERS[username][0]) == USERS[username][1]:
        headers = remember(request, username)
        print '------------- HEADERS'
        pprint(headers)
        print '------------- /HEADERS'
        return HTTPFound(location='/', headers=headers)

    request.session.flash('Username/password combination not found!')

    return {'username': username}

@view_config(context=Root, route_name='logout')
def logout(context, request):
    print '------------ LOGOUT'
    headers = forget(request)
    return HTTPFound(location='/', headers=headers)
