from django.contrib.auth.models import AnonymousUser
from neerbee.users.models import User

class MongoEngineBackend(object):
    """Authenticate using MongoEngine and mongoengine.django.auth.user
    """

    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        user = User.objects(username=username.lower()).first()
        if user:
            if password and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        return User.objects.with_id(user_id)


def get_user(userid):
    """Returns a User object from an id (User.id). Django's equivalent takes
    request, but taking an id instead leaves it up to the developer to store
    the id in any way they want (session, signed cookie, etc.)
    """
    if not userid:
        return AnonymousUser()
    return MongoEngineBackend().get_user(userid) or AnonymousUser()
