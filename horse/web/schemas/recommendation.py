from marshmallow import Schema, fields

from .movie import MovieSchema


class RecommendationSchema(Schema):
    movie = fields.Nested(MovieSchema, dump_only=True)
    weight = fields.Float(dump_only=True)


recommendations_schema = RecommendationSchema(many=True)
