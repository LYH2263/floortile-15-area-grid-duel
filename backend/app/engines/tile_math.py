"""Floor tile order count: area method + grid layout, compared head-to-head."""

from app.engines.helpers import ceil_units


def tile_count(
    room_l: float,
    room_w: float,
    tile_l: float,
    tile_w: float,
    waste_pct: float,
) -> dict:
    """
    raw_count: ceil(room_area / tile_piece_area)
    order_count: ceil(raw * (1 + waste_pct/100))

    Both sides of the showdown are computed here from the single set of
    room dimensions and tile edges passed in — never re-derived elsewhere.
    """
    area = float(room_l) * float(room_w)
    piece = float(tile_l) * float(tile_w)
    if piece <= 0 or area < 0:
        raise ValueError("invalid dimensions")
    raw = ceil_units(area / piece)
    with_waste = ceil_units(raw * (1 + float(waste_pct) / 100.0))
    layout = layout_preview(room_l, room_w, tile_l, tile_w)
    return {
        "area_m2": round(area, 3),
        "piece_m2": round(piece, 4),
        "raw_count": raw,
        "waste_pct": float(waste_pct),
        "order_count": with_waste,
        "layout": layout,
        "showdown": showdown(raw, with_waste, float(waste_pct), layout),
    }


def layout_preview(room_l: float, room_w: float, tile_l: float, tile_w: float) -> dict:
    """Grid count if tiles are laid on a full rectangular lattice (may exceed area method)."""
    cols = ceil_units(float(room_l) / float(tile_l))
    rows = ceil_units(float(room_w) / float(tile_w))
    grid_count = cols * rows
    return {
        "cols": cols,
        "rows": rows,
        "grid_count": grid_count,
    }


def showdown(raw_count: int, order_count: int, waste_pct: float, layout: dict) -> dict:
    """Area method vs rectangular grid, both derived from the same room/tile dims.

    Returns both sides, their absolute difference, and which side is larger
    ("area" | "grid" | "tie").
    """
    grid_count = layout["grid_count"]
    if order_count > grid_count:
        larger_side = "area"
    elif grid_count > order_count:
        larger_side = "grid"
    else:
        larger_side = "tie"
    return {
        "area": {
            "raw_count": raw_count,
            "order_count": order_count,
            "waste_pct": waste_pct,
        },
        "grid": {
            "cols": layout["cols"],
            "rows": layout["rows"],
            "grid_count": grid_count,
        },
        "diff": abs(order_count - grid_count),
        "larger_side": larger_side,
    }
