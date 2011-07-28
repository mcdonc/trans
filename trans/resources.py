import os
import json
import re
import datetime
from pyramid.security import Allow, DENY_ALL

class Root(object):
    __name__ = None
    __parent__ = None

    __acl__ = [
        (Allow, 'group:users', 'view'),
        (Allow, 'group:users', 'add'),
        (Allow, 'group:users', 'edit'),
        DENY_ALL
    ]

    def __init__(self, location):
        self.location = location

    def __getitem__(self, name):
        trans_name = os.path.join(self.location, u'trans_%s.json' % name)

        # Security to prevent directory escalation
        if trans_name.startswith(self.location) and os.path.isfile(trans_name):
            return Trans(trans_name, self)
        raise KeyError(name)

    def _get_current(self):
        if os.path.isdir(self.location):
            all_files = []
            for _, __, files in os.walk(self.location):
                for file in files:
                    all_files.append(file)

            # Now extract language "code"
            lang_re = re.compile(u'trans_(?P<lang_id>.+)\.json')
            all_lang = []
            for f in all_files:
                match = lang_re.match(f)
                if match != None:
                    m = match.group('lang_id')
                    all_lang.append(m)

            return all_lang if len(all_lang) > 0 else None
        else:
            raise RuntimeError('Configuration error - root is not a dir?')

    def createnew(self, lang):
        _default_l = os.path.join(self.location, 'default.json')
        _default = open(_default_l, 'r')
        _default_lang = json.load(_default)
        _default.close()

        _new = {
            'created': '%s' % datetime.datetime.now(),
            'last_edited': '%s' % datetime.datetime.now(),
            'created_by': "you",
            'lang_code': lang,
            'lang': _default_lang
        }

        l = os.path.join(self.location, 'trans_%s.json' % lang)
        f = open(l, 'w+')
        json.dump(_new, f)
        f.close()

        return True

    current = property(_get_current)

class Trans(object):
    __acl__ = [
        (Allow, 'group:users', 'view'),
        (Allow, 'group:users', 'add'),
        (Allow, 'group:users', 'edit'),
        DENY_ALL
    ]

    def __init__(self, file, parent):
        self.file = file

        f = open(self.file, 'r')
        self.contain = json.load(f)
        f.close()
        self.map = self.contain['lang']

        self.__name__ = file
        self.__parent__ = parent

    def __getitem__(self, name):
        return Element(self, self.map, name) if self.map.has_key(name) else KeyError(name)

    def save(self):
        self.contain['lang'] = self.map
        self.contain['last_edited'] = '%s' % datetime.datetime.now()
        f = open(self.file, 'w+')
        json.dump(self.contain, f)
        f.close()
        return True

class Element(object):
    __acl__ = [
        (Allow, 'group:users', 'view'),
        (Allow, 'group:users', 'add'),
        (Allow, 'group:users', 'edit'),
        DENY_ALL
    ]

    def __init__(self, trans, map, element_name):
        self.trans = trans
        self.map = map
        self.element_name = element_name

        self.__parent__ = trans
        self.__name__ = element_name
