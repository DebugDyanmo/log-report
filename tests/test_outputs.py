import json
import re
from collections import Counter
from pathlib import Path

REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")


def _expected():
    """Independently recompute the expected summary directly from access.log."""
    paths, ips, total = Counter(), set(), 0
    with open(LOG_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    return {
        "total_requests": total,
        "unique_ips": len(ips),
        "top_path": paths.most_common(1)[0][0],
    }


def test_report_written_as_valid_json():
    """instruction.md criterion 4: results are written to /app/report.json
    as valid JSON containing exactly the keys total_requests, unique_ips, top_path."""
    assert REPORT_PATH.exists(), "no report.json found at /app/report.json"
    data = json.loads(REPORT_PATH.read_text())
    assert set(data.keys()) == {"total_requests", "unique_ips", "top_path"}, (
        f"report.json must contain exactly total_requests, unique_ips, top_path; got {sorted(data.keys())}"
    )


def test_total_requests_correct():
    """instruction.md criterion 1: total number of requests (non-empty lines)
    in the log is counted correctly."""
    data = json.loads(REPORT_PATH.read_text())
    expected = _expected()
    assert data["total_requests"] == expected["total_requests"], (
        f"total_requests: expected {expected['total_requests']}, got {data['total_requests']}"
    )


def test_unique_ips_correct():
    """instruction.md criterion 2: number of unique client IP addresses
    is counted correctly."""
    data = json.loads(REPORT_PATH.read_text())
    expected = _expected()
    assert data["unique_ips"] == expected["unique_ips"], (
        f"unique_ips: expected {expected['unique_ips']}, got {data['unique_ips']}"
    )


def test_top_path_correct():
    """instruction.md criterion 3: the single most frequently requested
    path is identified correctly as top_path."""
    data = json.loads(REPORT_PATH.read_text())
    expected = _expected()
    assert data["top_path"] == expected["top_path"], (
        f"top_path: expected {expected['top_path']!r}, got {data['top_path']!r}"
    )