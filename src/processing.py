def filter_by_state(operations, state='EXECUTED'):
    return[item for item in operations if item.get ('state') ==state]

def sort_by_date(operations, reverse=True):
    return sorted(operations, key=lambda x: x.get('date', ''), reverse=reverse)