from uuid import uuid4

from horse.models import User, Movie


class ObjectDoesNotExist(Exception):
    def __init__(self, model, pk):
        super().__init__('{}: {}'.format(model, pk))


class InMemoryRepository:
    def __init__(self):
        self.objects = []

    def get(self, pk):
        obj = next((u for u in self.objects if u.pk == pk), None)
        if obj is None:
            raise ObjectDoesNotExist(self.model.__name__, pk)

        return obj

    def store(self, obj):
        assert getattr(obj, 'pk', None) is None
        assert isinstance(obj, self.model)

        obj.pk = str(uuid4())
        self.objects.append(obj)

    def all(self):
        return self.objects


class UserRepository(InMemoryRepository):
    model = User


class MovieRepository(InMemoryRepository):
    model = Movie
