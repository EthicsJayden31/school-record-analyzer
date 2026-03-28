from __future__ import annotations

from pathlib import Path
import re
import tempfile
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen


DRIVE_HOSTS = {"drive.google.com", "docs.google.com"}


def extract_drive_file_id(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc not in DRIVE_HOSTS:
        raise ValueError("Google Drive URL이 아닙니다.")

    path_match = re.search(r"/file/d/([a-zA-Z0-9_-]+)", parsed.path)
    if path_match:
        return path_match.group(1)

    q = parse_qs(parsed.query)
    if "id" in q and q["id"]:
        return q["id"][0]

    raise ValueError("Google Drive 파일 ID를 URL에서 찾지 못했습니다.")


def build_drive_download_url(file_id: str) -> str:
    return f"https://drive.google.com/uc?export=download&id={file_id}"


def download_drive_file(url: str, output_dir: str | Path | None = None) -> Path:
    file_id = extract_drive_file_id(url)
    download_url = build_drive_download_url(file_id)

    target_dir = Path(output_dir) if output_dir else Path(tempfile.gettempdir())
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / f"gdrive_{file_id}.bin"

    with urlopen(download_url, timeout=30) as response:  # nosec B310
        target_path.write_bytes(response.read())

    return target_path
