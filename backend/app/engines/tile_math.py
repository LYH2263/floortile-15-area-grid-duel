"""Floor tile order count: area method + optional grid layout preview."""

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
    duel: area-method order count vs rectangular grid count. Both sides are
    derived from the SAME room dimensions and tile edges passed to this call.
    """
    area = float(room_l) * float(room_w)
    piece = float(tile_l) * float(tile_w)
    if piece <= 0 or area < 0:
        raise ValueError("invalid dimensions")
    raw = ceil_units(area / piece)
    with_waste = ceil_units(raw * (1 + float(waste_pct) / 100.0))
    layout = layout_preview(room_l, room_w, tile_l, tile_w)
    duel = area_grid_duel(with_waste, layout["grid_count"])
    return {
        "area_m2": round(area, 3),
        "piece_m2": round(piece, 4),
        "raw_count": raw,
        "waste_pct": float(waste_pct),
        "order_count": with_waste,
        "layout": layout,
        "duel": duel,
    }


def area_grid_duel(order_count: int, grid_count: int) -> dict:
    """Compare area-method order count against rectangular grid count.

    Returns both sides, the absolute difference, and the larger-side marker
    ("area" | "grid" | "tie"). Callers must pass counts computed from the same
    room dimensions and tile edges — never re-measure per side.
    """
    order_count = int(order_count)
    grid_count = int(grid_count)
    if order_count > grid_count:
        larger = "area"
    elif grid_count > order_count:
        larger = "grid"
    else:
        larger = "tie"
    return {
        "area_order_count": order_count,
        "grid_count": grid_count,
        "diff": abs(order_count - grid_count),
        "larger": larger,
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
