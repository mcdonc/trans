import random
import string
import hashlib

## USERS = {
##     'user': ['salt', 'pw'],
## }

USERS = {'user':
         ['test', 'f4a92ed38b74b373e60b16176a8e19ca0220cd21bf73e46e68c74c0ca77a8cba3f6738b264000d894f7eff5ca17f8cdd01c7beb2ccc2ba2553987c01df152729']
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

