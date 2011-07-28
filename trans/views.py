from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound

from trans.resources import Root
from trans.resources import Trans
from trans.resources import Element

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
