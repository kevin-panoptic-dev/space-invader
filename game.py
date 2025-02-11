import time


def is_intersecting(host, opposites):
    returned_list = []
    for opposite in opposites:
        offset_x: float = opposite.x - host.x
        offset_y: float = opposite.y - host.y
        is_overlap = host.mask.overlap(opposite.mask, (offset_x, offset_y))
        if is_overlap:
            returned_list.append(opposite)

    return returned_list


def is_available(last_time: float, limit: float):
    current_time = time.time()
    time_since_last_shot = current_time - last_time
    if time_since_last_shot > limit:
        return True
    return False
