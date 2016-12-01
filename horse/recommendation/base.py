from abc import abstractmethod, ABCMeta


class RecommendationService(metaclass=ABCMeta):
    @abstractmethod
    def recommend(self, user):
        pass
