import os
import tempfile

# Point the DB at a throwaway dir before app.config is imported.
os.environ["DATA_DIR"] = tempfile.mkdtemp(prefix="floortile-test-")

from app import seed  # noqa: E402
from app.db import connect  # noqa: E402
from app.repositories import history  # noqa: E402
from app.services import estimate_service  # noqa: E402

seed.init_db()


def _set_default_waste(value: float):
    conn = connect()
    try:
        conn.execute("UPDATE settings SET value=? WHERE key='waste_pct'", (str(value),))
        conn.commit()
    finally:
        conn.close()


def test_save_appends_single_run_with_showdown_embedded():
    before = len(history.list_runs(1000))
    res = estimate_service.run_estimate(1, 1, None, True, "对决保存")
    after = len(history.list_runs(1000))
    assert after == before + 1  # one run only, never two history rows

    run = history.get_run(res["run_id"])
    s = run["result"]["showdown"]
    assert s["area"]["order_count"] == res["order_count"]
    assert s["grid"]["grid_count"] == res["layout"]["grid_count"]
    assert s["diff"] == abs(res["order_count"] - res["layout"]["grid_count"])
    assert s["larger_side"] in ("area", "grid", "tie")


def test_saved_showdown_keeps_waste_snapshot_after_default_change():
    res = estimate_service.run_estimate(1, 1, None, True, "快照")
    saved = history.get_run(res["run_id"])["result"]["showdown"]
    assert saved["area"]["waste_pct"] == 8.0

    _set_default_waste(25.0)
    try:
        # The stored run keeps the numbers written at save time.
        again = history.get_run(res["run_id"])["result"]["showdown"]
        assert again == saved

        # Only new estimates pick up the new default waste.
        fresh = estimate_service.run_estimate(1, 1, None, False, "")
        assert fresh["waste_pct"] == 25.0
        assert fresh["showdown"]["area"]["waste_pct"] == 25.0
        assert fresh["showdown"]["area"]["order_count"] != saved["area"]["order_count"]
    finally:
        _set_default_waste(8.0)
