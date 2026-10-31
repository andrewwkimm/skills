"""Hidden tests for the report_job_refactor task: behavior kept, bug fixed."""

import json
from datetime import datetime
from pathlib import Path

import pytest
import report_job as rj

PAYLOADS = {
    "api": {"counts": {"requests": 1000, "errors": 70}},
    "web": {"counts": {"requests": 400, "errors": 4}},
    "idle": {"counts": {"requests": 0, "errors": 0}},
}


class Published:
    def __init__(self) -> None:
        self.objects: dict[str, bytes] = {}

    def __call__(self, key: str, data: bytes) -> None:
        self.objects[key] = data


def run_job(tmp_path: Path, payloads=PAYLOADS, threshold: float = 0.05):
    published = Published()
    job = rj.ReportJob(list(payloads), payloads.__getitem__, published, tmp_path / "out", threshold=threshold)
    return job.run(), published


def test_rows_keep_their_shape_and_order(tmp_path: Path) -> None:
    report, _ = run_job(tmp_path)

    assert [row["service"] for row in report["rows"]] == ["api", "web", "idle"]
    assert report["rows"][0] == {"service": "api", "requests": 1000, "errors": 70, "error_rate": 0.07}
    assert report["rows"][2]["error_rate"] == 0.0


def test_breaching_uses_the_threshold(tmp_path: Path) -> None:
    report, _ = run_job(tmp_path, threshold=0.05)

    assert report["breaching"] == ["api"]


def test_tags_and_generated_at_present(tmp_path: Path) -> None:
    report, _ = run_job(tmp_path)

    assert report["tags"] == ["nightly"]
    datetime.fromisoformat(report["generated_at"])


def test_published_document_matches_returned_report(tmp_path: Path) -> None:
    report, published = run_job(tmp_path)

    assert json.loads(published.objects["reports/error-rates.json"]) == json.loads(json.dumps(report))


def test_local_copy_written_even_when_out_dir_is_missing(tmp_path: Path) -> None:
    report, _ = run_job(tmp_path)

    assert json.loads((tmp_path / "out" / "error-rates.json").read_text()) == json.loads(json.dumps(report))


def test_running_twice_overwrites_the_local_copy(tmp_path: Path) -> None:
    run_job(tmp_path)
    report, _ = run_job(tmp_path)

    assert json.loads((tmp_path / "out" / "error-rates.json").read_text())["rows"] == report["rows"]


@pytest.mark.parametrize(
    ("payload", "field"),
    [({}, "counts"), ({"counts": {"errors": 1}}, "requests"), ({"counts": {"requests": 10}}, "errors")],
    ids=["no-counts", "no-requests", "no-errors"],
)
def test_missing_metrics_fail_by_name_instead_of_reading_zero(tmp_path: Path, payload: dict, field: str) -> None:
    with pytest.raises(Exception) as info:
        run_job(tmp_path, payloads={"api": payload})

    assert field in str(info.value)
