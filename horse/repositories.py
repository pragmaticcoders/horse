from abc import ABCMeta, abstractmethod
from uuid import uuid4

from horse.models import User, Movie


class ObjectDoesNotExist(Exception):
    def __init__(self, model, field):
        super().__init__('{}: {}'.format(model, field))


class Repository(metaclass=ABCMeta):
    @abstractmethod
    def get(self, pk): pass

    @abstractmethod
    def store(self, obj): pass

    @abstractmethod
    def all(self): pass

    @abstractmethod
    def clear(self): pass


class InMemoryRepository(Repository):
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

    def clear(self):
        self.objects = []


class UserRepository(InMemoryRepository):
    model = User

    def get_by_name(self, name):
        user = next((u for u in self.objects if u.name == name), None)
        if user is None:
            raise ObjectDoesNotExist(self.model.__name__, name)

        return user


class MovieRepository(InMemoryRepository):
    model = Movie

    def get_by_title(self, title):
        movie = next((m for m in self.objects if m.title == title), None)
        if movie is None:
            raise ObjectDoesNotExist(self.model.__name__, title)

        return movie
