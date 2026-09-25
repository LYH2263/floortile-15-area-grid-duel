import pytest

from app import seed
from app.db import connect
from app.engines.tile_math import area_grid_duel, tile_count
from app.repositories import history
from app.services import estimate_service


def test_duel_area_side_larger():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0)
    assert r["duel"] == {
        "area_order_count": 81,
        "grid_count": 80,
        "diff": 1,
        "larger": "area",
    }


def test_duel_grid_side_larger():
    r = tile_count(2.5, 2.0, 0.6, 0.6, 0.0)
    assert r["duel"]["area_order_count"] == 14
    assert r["duel"]["grid_count"] == 20
    assert r["duel"]["diff"] == 6
    assert r["duel"]["larger"] == "grid"


def test_duel_tie():
    r = tile_count(3.0, 3.0, 1.0, 1.0, 0.0)
    assert r["duel"]["diff"] == 0
    assert r["duel"]["larger"] == "tie"


def test_duel_shares_room_dims_and_tile_edges():
    # 两侧必须来自同一次调用的同一房间尺寸与砖边，禁止各算各的
    r = tile_count(5.3, 2.7, 0.8, 0.8, 12.5)
    assert r["duel"]["area_order_count"] == r["order_count"]
    assert r["duel"]["grid_count"] == r["layout"]["grid_count"]


def test_area_grid_duel_direct():
    assert area_grid_duel(10, 10)["larger"] == "tie"
    assert area_grid_duel(11, 10)["larger"] == "area"
    assert area_grid_duel(10, 11)["larger"] == "grid"


@pytest.fixture()
def temp_db(tmp_path, monkeypatch):
    db_file = tmp_path / "test.db"
    monkeypatch.setattr("app.db.DB_PATH", db_file)
    seed.init_db()
    return db_file


def test_save_appends_single_run_with_duel_embedded(temp_db):
    res = estimate_service.run_estimate(1, 1, None, True, "对决保存")
    assert res["run_id"] is not None
    runs = history.list_runs()
    # 保存只追加一条 run，两侧数字内嵌同一 payload，禁止拆两行
    assert len(runs) == 1
    saved = runs[0]["result"]
    assert saved["duel"]["area_order_count"] == 81
    assert saved["duel"]["grid_count"] == 80
    assert saved["duel"]["diff"] == 1
    assert saved["duel"]["larger"] == "area"


def test_waste_change_keeps_saved_duel_and_applies_to_new(temp_db):
    first = estimate_service.run_estimate(1, 1, None, True, "")
    # 之后仅修改默认损耗百分点
    conn = connect()
    conn.execute("UPDATE settings SET value='15' WHERE key='waste_pct'")
    conn.commit()
    conn.close()

    again = estimate_service.run_estimate(1, 1, None, False, "")
    assert again["waste_pct"] == 15.0
    assert again["duel"]["area_order_count"] == 87

    # 已存对决保持写入时取值
    saved = history.get_run(first["run_id"])
    assert saved["waste_pct"] == 8.0
    assert saved["result"]["waste_pct"] == 8.0
    assert saved["result"]["duel"]["area_order_count"] == 81
    assert saved["result"]["duel"]["grid_count"] == 80
