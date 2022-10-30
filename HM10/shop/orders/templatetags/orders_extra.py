from django import template

register = template.Library()


def search_active_order(orders):
    order = orders.filter(is_active=True)
    if len(order) == 0:
        return None
    else:
        return orders.filter(is_active=True)


@register.filter(name='active_order')
def active_order(orders):
    order = search_active_order(orders)
    return order[0] if order is not None else None


@register.filter(name='total_amount')
def total_amount(orders):
    order = search_active_order(orders)
    return order[0].total_amount if order is not None else None


@register.filter(name='product_list')
def products_list(orders):
    order = search_active_order(orders)
    return order[0].products.all() if order is not None else None
