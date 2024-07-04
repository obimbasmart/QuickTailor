"""app, jinja filters
"""

<<<<<<< HEAD
from datetime import datetime, timedelta, timezone
=======
from datetime import datetime, timedelta
>>>>>>> a03186c2a9fa59fe5729ea032872dd4f8985783d
import timeago, pytz
from babel.numbers import format_currency


def current_datetime_filter(format='%Y-%m-%d %H:%M:%S'):
    return datetime.now().strftime(format)

<<<<<<< HEAD
def now_utc(date):
    return datetime.now(timezone.utc)


=======
>>>>>>> a03186c2a9fa59fe5729ea032872dd4f8985783d
def custom_timeago(date):
    if date == 'N/A':
        return 'N/A'
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')

    now = datetime.utcnow()
    diff = now - date
    if diff < timedelta(hours=24):
        return date.strftime('%H:%M')
    elif diff < timedelta(hours=48):
        return f'Yesterday at {date.strftime("%H:%M")}'
    else:
<<<<<<< HEAD
        return f'{format_datetime(date)} at {date.strftime("%H:%M")}'


=======
        return format_datetime(date)
>>>>>>> a03186c2a9fa59fe5729ea032872dd4f8985783d


def custom_time_format(date, timezone='UTC'):
    if date == 'N/A':
        return 'N/A'
    if isinstance(date, str):
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')

<<<<<<< HEAD
    # Convert date to the specified timezone from parameters
=======
    # Convert date to the specified timezone
>>>>>>> a03186c2a9fa59fe5729ea032872dd4f8985783d
    
    local_tz = pytz.timezone(timezone)
    date = date.replace(tzinfo=pytz.utc).astimezone(local_tz)
    
    now = datetime.now(local_tz)
    diff = now - date

    # If the datetime is under 30 seconds
    if diff < timedelta(seconds=30):
        return 'just now'
    # If the datetime is under 60 seconds
    elif diff < timedelta(minutes=1):
        return f'{int(diff.total_seconds())} seconds ago'
    # If the datetime is under 60 minutes
    elif diff < timedelta(hours=1):
        minutes = int(diff.total_seconds() // 60)
        return f'{minutes} minutes ago'
    # For dates older than 24 hours
    else:
        return date.strftime('%H:%M')

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


def to_date_dmy(value):
    if isinstance(value, datetime):
        return value.strftime("%d/%m/%Y")
    return value


def is_date_more_than_days_ago(value, days):
    if isinstance(value, datetime):
        return value < (datetime.now() - timedelta(days=days))
    return False


def today_date(val):
    date = datetime.now()
    formatted_date = date.strftime("%A, %dth %B %Y")
    return formatted_date

def time_now(val):
    now = datetime.now()
    return now.strftime("%I:%M%p").lower()

def average_reviews(reviews):

    if len(reviews) == 0:
        return  0
    return round(sum([
        review.rating
        for review in reviews
    ]) / len(reviews), 2)
