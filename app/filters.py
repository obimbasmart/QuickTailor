"""app, jinja filters
"""

from datetime import datetime, timedelta
import timeago
from babel.numbers import format_currency


def current_datetime_filter(format='%Y-%m-%d %H:%M:%S'):
    return datetime.now().strftime(format)


def format_datetime(value):
    # Parse the input datetime string
    dt = datetime.strptime(str(value), '%Y-%m-%d %H:%M:%S')

    # Get the day of the month and determine the correct suffix
    day = dt.day
    if 11 <= day <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

    # Format the datetime to the desired output
    formatted_date = dt.strftime(f'%b, {day}{suffix} %Y')
    return formatted_date


def sum_price(product_list: list):
    return sum([float(prod.price) for prod in product_list])


def sum_custom_value(product_list: list):
    return sum([float(prod.customization_value) for prod in product_list if prod.customization_value])


def tolist(_list: list):
    return [li.to_dict() for li in _list]


def _timeago(date):
    if date == 'N/A':
        return 'N/A'
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')

    now = datetime.utcnow()
    return timeago.format(date, now)


def completion_date(order):
    date = order.created_at \
           + timedelta(days=order.product.estimated_tc)
    
    return format_datetime(date)


def currency_filter(value):
    if value is None:
        return 'Nil'
    value = int(float(value))
    return format_currency(number=value, currency='₦',  format=u'¤#,##0',  currency_digits=False)
