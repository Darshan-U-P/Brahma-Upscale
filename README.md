# Brahma Upscale

**Local-first AI image and video upscaler for Windows.**

Brahma Upscale is being developed in two phases:

- **Phase 1 — Standard AI upscaler:** Build a working image and video upscaling application using established pretrained models. Start with image inference, GPU verification, and before/after comparisons, then add batch/tiled processing and video processing.
- **Phase 2 — Custom PB-ANN:** Develop a new PB-ANN-based super-resolution model and benchmark it against the Phase 1 baseline.

## Phase 1 goals

- Image super-resolution with 2× and 4× scaling where supported by the selected model
- Video upscaling with attention to temporal consistency
- NVIDIA GPU acceleration and memory-aware tiled inference
- Video frame extraction/reconstruction with audio preservation
- Reproducible image-quality and performance benchmarks

## Initial baseline

- **Image model:** Real-ESRGAN
- **Video pipeline:** FFmpeg plus a suitable video-restoration model selected after checking dependencies and available VRAM
- **Stack:** Python, PyTorch, Pillow/OpenCV, FFmpeg

The first milestone is to verify the local environment and then run Real-ESRGAN on a single test image. We will record GPU availability and save an input/output comparison before implementing the larger pipeline.

## Quick start (Windows PowerShell)

Clone the repository:

```powershell
git clone https://github.com/Darshan-U-P/Brahma-Upscale.git D:\Brahma-Upscale
cd D:\Brahma-Upscale

py -0p
python --version
git --version
nvidia-smi

python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python scripts/check_environment.py
```

The environment-check script reports Python packages, NVIDIA driver/GPU information, PyTorch CUDA availability, FFmpeg, and whether the optional Real-ESRGAN NCNN-Vulkan executable is present. It does not install or change anything.

**Important:** PyTorch must be installed with a build compatible with your NVIDIA driver. Use the official [PyTorch installation selector](https://pytorch.org/get-started/locally/) and choose Windows + Pip + the appropriate CUDA platform. Then run `python scripts/check_environment.py` again. Do not install a CPU-only build if GPU inference is required.

If PowerShell blocks virtual-environment activation, use this for the current PowerShell process only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

## Project structure

```text
Brahma-Upscale/
├── input/              # Local test images and videos (not committed)
├── output/             # Generated results (not committed)
├── models/             # Downloaded model weights (not committed)
├── tools/              # Optional portable model executables (not committed)
├── src/                # Application source
├── scripts/
│   └── check_environment.py
├── tests/
├── docs/
│   └── PHASE_1_PLAN.md
├── requirements.txt
├── requirements-dev.txt
└── README.md
```

## Hardware note

The initial target is a Windows laptop with an NVIDIA RTX 3050 Ti-class GPU and limited VRAM. Inference settings and tile sizes must be tuned to the actual machine. Training a custom PB-ANN model is outside Phase 1.

## Development principles

- Keep model weights, third-party binaries, input media, generated outputs, and virtual environments out of Git.
- Record model names, model-weight sources, software versions, test images, and benchmark settings.
- Compare Phase 2 against Phase 1 using the same evaluation data and conditions.
- AI upscaling can synthesize plausible details; it cannot guarantee that every reconstructed detail matches the original scene.

## License and model terms

Check the license of each upstream repository and each pretrained checkpoint before redistribution or commercial use. No upstream weights are bundled in this repository.
