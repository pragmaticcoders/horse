from horse.models import User


class ObjectDoesNotExist(Exception):
    def __init__(self, model, pk):
        super().__init__('{}: {}'.format(model, pk))


class UserRepository:
    model = User

    def __init__(self):
        self.users = []

    def get(self, pk):
        obj = next((u for u in self.users if u.pk == pk), None)
        if obj is None:
            raise ObjectDoesNotExist(self.model.__name__, pk)

        return obj

    def store(self, obj):
        self.users.append(obj)

    def all(self):
        return self.users
