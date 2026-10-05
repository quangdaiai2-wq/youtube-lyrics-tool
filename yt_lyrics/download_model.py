"""
download_model.py - Tải model nhận dạng giọng nói về máy, có kiểm tra và thử lại.

Vì sao cần file riêng: cơ chế tải tự động của thư viện đôi khi tạo ra file rỗng
khi mạng gián đoạn. File này tải thẳng từng file, kiểm tra kích thước, và thử lại
nếu hỏng — đảm bảo model dùng được.

Dùng: python download_model.py [tiny|base|small|medium]
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

MODELS = {
    "tiny":   "Systran/faster-whisper-tiny",
    "base":   "Systran/faster-whisper-base",
    "small":  "Systran/faster-whisper-small",
    "medium": "Systran/faster-whisper-medium",
}

# Kích thước tối thiểu mong đợi của model.bin (byte) — dùng để phát hiện file rỗng
MIN_BIN_SIZE = {
    "tiny":   30_000_000,
    "base":   60_000_000,
    "small":  200_000_000,
    "medium": 600_000_000,
}

FILES = ["config.json", "model.bin", "tokenizer.json", "vocabulary.txt"]


def cache_dir(repo: str) -> Path:
    base = Path(os.environ.get("HF_HOME", Path.home() / ".cache" / "huggingface"))
    safe = "models--" + repo.replace("/", "--")
    return base / "hub" / safe


def download(repo: str, filename: str, dest: Path, retries: int = 4) -> bool:
    import requests

    url = f"https://huggingface.co/{repo}/resolve/main/{filename}"
    for attempt in range(1, retries + 1):
        try:
            print(f"    [{attempt}/{retries}] {filename} ...", end=" ", flush=True)
            with requests.get(url, stream=True, timeout=60) as r:
                r.raise_for_status()
                total = int(r.headers.get("Content-Length") or 0)
                tmp = dest.with_suffix(dest.suffix + ".part")
                got = 0
                with open(tmp, "wb") as f:
                    for chunk in r.iter_content(chunk_size=1 << 20):
                        if chunk:
                            f.write(chunk)
                            got += len(chunk)
                if total and got != total:
                    print(f"THIEU ({got}/{total})")
                    tmp.unlink(missing_ok=True)
                    time.sleep(2)
                    continue
                tmp.replace(dest)
                print(f"OK ({got/1_048_576:.1f} MB)")
                return True
        except Exception as exc:  # noqa: BLE001
            print(f"LOI: {type(exc).__name__}")
            time.sleep(2)
    return False


def ensure_model(size: str = "small") -> Path | None:
    repo = MODELS.get(size)
    if not repo:
        print(f"Khong ho tro model '{size}'. Chon trong: {', '.join(MODELS)}")
        return None

    snap = cache_dir(repo) / "snapshots" / "manual"
    snap.mkdir(parents=True, exist_ok=True)

    print(f"Dang chuan bi model '{size}' ({repo})")
    ok_all = True
    for fn in FILES:
        dest = snap / fn
        if dest.exists() and dest.stat().st_size > 0:
            if fn != "model.bin" or dest.stat().st_size >= MIN_BIN_SIZE.get(size, 1):
                print(f"    {fn} ... da co san")
                continue
        if not download(repo, fn, dest):
            ok_all = False

    # Kiểm tra lần cuối: model.bin phải đủ lớn
    bin_path = snap / "model.bin"
    if not bin_path.exists() or bin_path.stat().st_size < MIN_BIN_SIZE.get(size, 1):
        print("❌ model.bin van chua dung. Kiem tra ket noi mang roi chay lai.")
        return None

    print(f"✅ Model '{size}' san sang.")
    return snap


if __name__ == "__main__":
    size = sys.argv[1] if len(sys.argv) > 1 else "small"
    p = ensure_model(size)
    sys.exit(0 if p else 1)
