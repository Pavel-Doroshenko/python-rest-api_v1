from marshmallow import Schema, fields


class ProductSchema(Schema):
    id = fields.String()
    name = fields.String()
    price = fields.Float()


class ProductGetManyParams(Schema):
    page = fields.Int(required=True)
    limit = fields.Int(required=True)


class ProductCreateDtoSchema(Schema):
    products = fields.List(fields.Str(), required=True)
