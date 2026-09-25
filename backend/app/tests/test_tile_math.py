from app.engines.tile_math import layout_preview, tile_count


def test_guest_room_600_waste8():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0)
    assert r["area_m2"] == 27.0
    assert r["raw_count"] == 75
    assert r["order_count"] == 81
    assert r["layout"]["cols"] == 10
    assert r["layout"]["rows"] == 8
    assert r["layout"]["grid_count"] == 80


def test_layout_preview_small_room():
    lp = layout_preview(2.5, 2.0, 0.6, 0.6)
    assert lp["cols"] == 5
    assert lp["rows"] == 4
    assert lp["grid_count"] == 20


def test_zero_waste():
    r = tile_count(3.0, 3.0, 1.0, 1.0, 0.0)
    assert r["raw_count"] == 9
    assert r["order_count"] == 9


def test_showdown_shares_dims_with_layout_and_area():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0)
    s = r["showdown"]
    assert s["area"]["raw_count"] == r["raw_count"]
    assert s["area"]["order_count"] == r["order_count"]
    assert s["area"]["waste_pct"] == r["waste_pct"]
    assert s["grid"]["cols"] == r["layout"]["cols"]
    assert s["grid"]["rows"] == r["layout"]["rows"]
    assert s["grid"]["grid_count"] == r["layout"]["grid_count"]


def test_showdown_area_side_larger():
    s = tile_count(6.0, 4.5, 0.6, 0.6, 8.0)["showdown"]
    assert s["area"]["order_count"] == 81
    assert s["grid"]["grid_count"] == 80
    assert s["diff"] == 1
    assert s["larger_side"] == "area"


def test_showdown_grid_side_larger():
    s = tile_count(8.0, 1.2, 0.8, 0.8, 8.0)["showdown"]
    assert s["area"]["order_count"] == 17
    assert s["grid"]["grid_count"] == 20
    assert s["diff"] == 3
    assert s["larger_side"] == "grid"


def test_showdown_tie():
    s = tile_count(3.0, 3.0, 1.0, 1.0, 0.0)["showdown"]
    assert s["area"]["order_count"] == 9
    assert s["grid"]["grid_count"] == 9
    assert s["diff"] == 0
    assert s["larger_side"] == "tie"
