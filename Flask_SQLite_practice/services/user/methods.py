from services.user.sql import execute_data


def get_realties_by_filter(data):
    filter = {
        'city': data['city'],
        'minprice': data['min_price'],
        'maxprice': data['max_price']
    }
    result = execute_data('get_filter', filter)
    return result

def post_realty(data):
    new_post = {
        'title': data['title'],
        'price': data['price'],
        'city': data['city']
    }
    result = execute_data('create', new_post)
    return result


