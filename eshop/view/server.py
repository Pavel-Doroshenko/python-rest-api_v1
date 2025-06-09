from flask import Flask, request
from marshmallow import ValidationError

from eshop.businsess_logic.order_usecases import (
    order_create,
    order_get_many,
    order_get_by_id,
)
from eshop.businsess_logic.product_usecases import (
    product_get_by_id,
    product_get_many,
    product_create,
    product_delete,
)
from eshop.view.order_schemas import (
    OrderCreateDtoSchema,
    OrderSchema,
    OrderGetManyParams,
)
from eshop.view.product_schemas import ProductGetManyParams, ProductSchema

app = Flask(__name__)


@app.post("/api/v1/order")
def order_create_endpoint():
    try:
        order_create_dto = OrderCreateDtoSchema().load(request.json)
    except ValidationError as err:
        return err.messages, 400

    try:
        order = order_create(product_ids=order_create_dto["product_ids"])
    except Exception as e:
        return {"error": str(e)}

    return OrderSchema().dump(order)


@app.get("/api/v1/order")
def order_get_many_endpoint():
    try:
        order_get_many_params = OrderGetManyParams().load(request.args)
    except ValidationError as err:
        return err.messages, 400

    order = order_get_many(
        page=order_get_many_params["page"],
        limit=order_get_many_params["limit"],
    )

    return OrderSchema(many=True).dump(order)


@app.get("/api/v1/order/<id>")
def order_get_by_id_endpoint(id):
    """Отоброжение ордера по его ID"""
    order = order_get_by_id(id)

    if order is None:
        return {"error": "Not found"}, 404

    return OrderSchema().dump(order)


@app.get("/api/v1/product/<id>")
def product_get_by_id_endpoint(id: str):
    """Отображение продукта по его id"""
    product = product_get_by_id(id)
    if product is None:
        return {"error": "Not found"}, 404

    return ProductSchema().dump(product)


@app.get("/api/v1/product")
def product_get_many_endpoint():
    try:
        params = ProductGetManyParams().load(request.args)
    except ValidationError as err:
        return err.messages, 400

    product = product_get_many(
        page=params["page"],
        limit=params["limit"],
    )

    return ProductSchema(many=True).dump(product)


@app.post("/api/v1/product")
def product_create_endpoint():
    try:
        product_json = ProductSchema().load(request.json)
    except ValidationError as err:
        return err.messages, 400
    try:
        product = product_create(product_json)
    except Exception as e:
        return {"error": str(e)}

    return ProductSchema().dump(product)


@app.delete("/api/v1/product/<id>")
def product_delete_by_id(id: str):
    """Удаление продукта по id"""
    product_id = product_get_by_id(
        id
    )  # Поиск продукта по id, если не найдено возвращает 404
    if product_id is None:
        return {"error": "Not found"}, 404
    product_id = product_delete(id)
    return "Продукт удален"


def run_server():
    app.run()
