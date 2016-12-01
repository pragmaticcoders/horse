from marshmallow import Schema, fields


class MovieSchema(Schema):
    pk = fields.Str(dump_only=True)
    title = fields.Str(required=True)


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
