def calc_bounds(position: int, window_offset: int, max_bound: int, min_bound: int = 1) -> tuple[int, int]:
    ubound = position + window_offset
    lbound = position - window_offset

    # check lboud
    if lbound <= 0:
        ubound += min_bound - lbound
        lbound = min_bound

    # check ubound
    if ubound > max_bound and lbound == min_bound:
        ubound = max_bound
    elif ubound > max_bound and lbound - (ubound - max_bound) >= min_bound:
        lbound = lbound - abs(max_bound - ubound)
        ubound = max_bound

    return lbound, ubound
