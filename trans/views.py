from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.httpexceptions import HTTPForbidden

from pyramid.security import remember, forget

from trans.resources import Root
from trans.resources import Trans
from trans.resources import Element
from trans.security import USERS
from trans.security import calchash

from pprint import pprint

@view_config(context=Root, renderer='index.mak', permission='view')
def index(context, request):
    print '------- INDEX'
    return {'langs': context.current}

@view_config(context=Root, request_method='POST',
             request_param='form.submitted', permission='add')
def newlang(context, request):
    lang = request.params.get('lang').encode('utf8')

    if lang.strip(' \t\r\n.\\/') != "" and lang != None:
        context.createnew(lang)
        return HTTPFound(location="/%s" % lang)

@view_config(context=Trans, renderer='trans.mak', permission='view')
def trans(context, request):
    return {'map': context.map}

@view_config(context=Trans, request_method='POST',
             request_param='form.submitted', permission='edit')
def savetrans(context, request):
    for key, value in request.POST.items():
        if context.map.has_key(key):
            context.map[key] = value.encode('utf8')
    context.save()

    request.session.flash('Translation saved successfully.')

    return HTTPFound(location="/%s" % context.contain['lang_code'].encode('utf8'))

@view_config(context=Element, request_method='POST', request_param='content',
             renderer='json', permission='edit')
def saveelement(context, request):
    context.__parent__.map[context.__name__] = request.POST['content']
    context.__parent__.save()

    return {
        'name': context.__name__,
        'newvalue': context.__parent__.map[context.__name__],
        'success': True
    }

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

@view_config(context=Root, name='logout')
def logout(context, request):
    print '------------ LOGOUT'
    headers = forget(request)
    return HTTPFound(location='/', headers=headers)
