"""Builds the nightly error-rate report for each service and publishes it."""

import json
import logging
from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, datetime
from pathlib import Path

logger = logging.getLogger(__name__)

FetchMetrics = Callable[[str], Mapping[str, object]]
Publish = Callable[[str, bytes], None]


class ReportJob:
    """Fetches each service's metrics, computes its error rate, and publishes the report."""

    def __init__(
        self,
        services: Sequence[str],
        fetch_metrics: FetchMetrics,
        publish: Publish,
        out_dir: Path,
        threshold: float = 0.05,
    ) -> None:
        self._services = services
        self._fetch_metrics = fetch_metrics
        self._publish = publish
        self._out_dir = out_dir
        self._threshold = threshold

    def run(self) -> dict[str, object]:
        """Runs the report for every service and returns the published document."""
        rows = []
        for service in self._services:
            payload = self._fetch_metrics(service)
            rows.append(self._summarize(service, payload))
        report = self._build_report(rows)
        self._write_local_copy(report)
        self._publish("reports/error-rates.json", json.dumps(report).encode())
        return report

    def _summarize(self, service: str, payload: Mapping[str, object]) -> dict[str, object]:
        counts = payload.get("counts", {})
        requests = int(counts.get("requests", 0))
        errors = int(counts.get("errors", 0))
        rate = errors / requests if requests else 0.0
        return {"service": service, "requests": requests, "errors": errors, "error_rate": rate}

    def _build_report(self, rows: list[dict[str, object]], extra_tags: list[str] = []) -> dict[str, object]:
        breaching = [row["service"] for row in rows if float(row["error_rate"]) > self._threshold]
        tags = ["nightly"] + extra_tags
        return {"generated_at": datetime.now(UTC).isoformat(), "rows": rows, "breaching": breaching, "tags": tags}

    def _write_local_copy(self, report: dict[str, object]) -> None:
        if not self._out_dir.exists():
            self._out_dir.mkdir(parents=True)
        path = self._out_dir / "error-rates.json"
        path.write_text(json.dumps(report))
        logger.info(f"Wrote local copy to {path}")

    def _format_row(self, row: Mapping[str, object]) -> str:
        return f"{row['service']}: {float(row['error_rate']):.2%} ({row['errors']}/{row['requests']})"
