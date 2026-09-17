import pytest
from pydantic import ValidationError
from app.adapters import TestMemoryAdapter
from app.models import DetailIntent

def make(**kwargs): return DetailIntent(action="consultar_detalle_ventas", **kwargs)

def test_detail_filter_and_limit():
    rows = TestMemoryAdapter().execute("sales_detail", make(pais="PERU"), 100)
    assert len(rows) == 100 and all(row["pais"] == "PERU" for row in rows)

def test_detail_pagination():
    adapter = TestMemoryAdapter()
    first = adapter.execute("sales_detail", make(offset_rows=0), 100)
    second = adapter.execute("sales_detail", make(offset_rows=100), 100)
    assert first[-1]["id_venta"] < second[0]["id_venta"]

def test_detail_validation():
    for values in ({"limit_rows": 501}, {"limit_rows": 0}, {"offset_rows": -1}, {"sort_column": "DROP TABLE ventas"}, {"sort_direction": "DROP"}):
        with pytest.raises(ValidationError): make(**values)

def test_detail_safe_sort():
    rows = TestMemoryAdapter().execute("sales_detail", make(sort_column="monto", sort_direction="DESC"), 2)
    assert rows[0]["monto"] > rows[1]["monto"]
