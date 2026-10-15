"""Report Brahma Upscale's local development environment without modifying it."""

from __future__ import annotations

import importlib
import importlib.metadata
import platform
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def section(title: str) -> None:
    print(f"\n{title}")
    print("-" * len(title))


def command_output(args: list[str], timeout: int = 10) -> str | None:
    try:
        result = subprocess.run(
            args,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )
    except (OSError, subprocess.TimeoutExpired):
        return None

    if result.returncode != 0:
        return None
    return (result.stdout or result.stderr).strip()


def report_package(distribution: str, import_name: str | None = None) -> None:
    try:
        version = importlib.metadata.version(distribution)
        print(f"[OK] {distribution}: {version}")
    except importlib.metadata.PackageNotFoundError:
        print(f"[MISSING] {distribution}")
        return

    if import_name:
        try:
            module = importlib.import_module(import_name)
            detail = getattr(module, "__version__", None)
            if detail:
                print(f"       import check passed ({detail})")
        except Exception as exc:  # report import issues without crashing diagnostic
            print(f"       [IMPORT ERROR] {type(exc).__name__}: {exc}")


def main() -> int:
    section("Brahma Upscale environment check")
    print(f"Project root: {ROOT}")
    print(f"Platform:     {platform.platform()}")
    print(f"Python:       {sys.version.split()[0]}")
    print(f"Executable:   {sys.executable}")

    try:
        usage = shutil.disk_usage(ROOT)
        print(f"Free space:   {usage.free / (1024**3):.1f} GiB")
    except OSError as exc:
        print(f"Free space:   unavailable ({exc})")

    section("Python packages")
    for distribution, import_name in (
        ("torch", "torch"),
        ("torchvision", "torchvision"),
        ("Pillow", "PIL"),
        ("opencv-python", "cv2"),
        ("tqdm", "tqdm"),
        ("psutil", "psutil"),
        ("realesrgan", "realesrgan"),
        ("basicsr", "basicsr"),
    ):
        report_package(distribution, import_name)

    section("NVIDIA GPU / driver")
    nvidia = command_output(
        [
            "nvidia-smi",
            "--query-gpu=name,memory.total,driver_version",
            "--format=csv,noheader",
        ]
    )
    if nvidia:
        print("[OK] nvidia-smi")
        for line in nvidia.splitlines():
            print(f"     {line}")
    else:
        print("[NOT DETECTED] nvidia-smi unavailable or no NVIDIA GPU detected.")

    try:
        torch = importlib.import_module("torch")
        print(f"PyTorch CUDA build: {getattr(torch.version, 'cuda', None)}")
        if torch.cuda.is_available():
            print(f"[OK] PyTorch CUDA available: {torch.cuda.get_device_name(0)}")
            print(f"     Device count: {torch.cuda.device_count()}")
        else:
            print("[NOT AVAILABLE] PyTorch cannot access CUDA in this environment.")
    except Exception as exc:
        print(f"PyTorch CUDA check skipped: {type(exc).__name__}: {exc}")

    section("Media tools")
    ffmpeg = command_output(["ffmpeg", "-version"])
    if ffmpeg:
        print(f"[OK] {ffmpeg.splitlines()[0]}")
    else:
        print("[MISSING] FFmpeg is not on PATH.")

    executable_candidates = (
        ROOT / "tools" / "realesrgan-ncnn-vulkan.exe",
        ROOT / "tools" / "realesrgan-ncnn-vulkan" / "realesrgan-ncnn-vulkan.exe",
        ROOT / "tools" / "Real-ESRGAN-ncnn-vulkan" / "realesrgan-ncnn-vulkan.exe",
    )
    executable = next((path for path in executable_candidates if path.is_file()), None)
    if executable:
        print(f"[OK] Real-ESRGAN NCNN-Vulkan executable: {executable.relative_to(ROOT)}")
    else:
        print("[NOT INSTALLED] Real-ESRGAN NCNN-Vulkan portable executable.")

    print("\nThis script only reports status; it does not install, download, or modify anything.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
