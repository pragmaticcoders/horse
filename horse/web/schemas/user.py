from marshmallow import Schema, fields, pre_dump

from horse.web.schemas.movie import MovieSchema


class UserSchema(Schema):
    pk = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    followed_users = fields.Nested(
        'self', only=('pk', 'name'), dump_only=True, many=True
    )
    liked_movies = fields.Nested(MovieSchema, dump_only=True, many=True)

    @pre_dump
    def load_movies_and_users(self, obj):
        obj.followed_users = obj.get_followed_users()
        obj.liked_movies = obj.get_liked_movies()
        return obj


class UserActionSchema(Schema):
    pk = fields.Str(required=True)
