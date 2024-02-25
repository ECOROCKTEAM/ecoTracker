import pytest


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


@pytest.mark.parametrize(
    "position, window_offset, max_bound, asrt_lbound, asrt_ubound",
    (
        (2, 2, 10, 1, 5),
        (4, 2, 5, 1, 5),
        (2, 2, 3, 1, 3),
        (5, 10, 50, 1, 21),
    ),
)
def test_calc(position: int, window_offset: int, max_bound: int, asrt_lbound: int, asrt_ubound: int):
    lbound, ubound = calc_bounds(position, window_offset, max_bound)
    assert lbound == asrt_lbound
    assert ubound == asrt_ubound
