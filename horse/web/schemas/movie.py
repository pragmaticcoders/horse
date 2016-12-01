from marshmallow import Schema, fields


class MovieSchema(Schema):
    pk = fields.Str(dump_only=True)
    title = fields.Str(required=True)
    likes = fields.Int(dump_only=True)


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)
