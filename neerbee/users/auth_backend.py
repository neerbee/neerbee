from neerbee.users.models import Bee

class BeeAuthBackend(object):
    """ Authenticate Bee. Code copied from MongoEngine auth.
    """

    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def authenticate(self, username=None, password=None):
        user = Bee.objects(username=username.lower()).first()
        if user:
            if password and user.check_password(password):
                return user
        return None

    def get_user(self, user_id):
        return Bee.objects.with_id(user_id)
