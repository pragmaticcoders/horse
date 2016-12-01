from marshmallow import Schema, fields

from .movie import MovieSchema


class PopulateUserSchema(Schema):
    name = fields.String()
    followed_users = fields.List(fields.String())
    liked_movies = fields.List(fields.String())


class PopulateSchema(Schema):
    users = fields.Nested(PopulateUserSchema(many=True), required=True)
    movies = fields.Nested(MovieSchema(many=True), required=True)


populate_schema = PopulateSchema()
