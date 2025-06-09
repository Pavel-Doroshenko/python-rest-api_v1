from typing import Optional, List

from eshop.businsess_logic.product import Product
from eshop.data_access.product_repo import get_by_id, get_many, save, delete_by_id


def product_create(product) -> Product:
    product = Product(id=product["id"], name=product["name"], price=product["price"])
    save(product)
    return product


def product_get_by_id(id: str) -> Optional[Product]:
    # raise Exception('Not implemented yet')
    return get_by_id(id)


def product_get_many(page: int, limit: int) -> List[Product]:
    # raise Exception('Not implemented yet')
    return get_many(page, limit)


def product_delete(id: str):
    product = get_by_id(id)
    if product is None:
        raise Exception(f"Failed to delete product: Product with this {id} not found")
    return delete_by_id(product.id)
