# Phase 1 — Standard AI Upscaler

## Goal

Deliver a working local-first Windows application for image upscaling and video upscaling using established pretrained models. Phase 1 is the baseline against which the custom PB-ANN model in Phase 2 will be compared.

## Milestones

### 1. Environment verification
- Record Windows, Python, NVIDIA driver, GPU model, VRAM, and available disk space.
- Select a compatible PyTorch/CUDA build only after inspecting the installed environment.
- Verify GPU access from PyTorch before installing or testing a Python inference backend.

### 2. Image inference
- Start with Real-ESRGAN and one representative test image.
- Verify output dimensions, image readability, GPU utilization, runtime, and peak VRAM.
- Save a before/after comparison and document model/checkpoint details.
- Add batch processing, error handling, and tiled inference after the first smoke test passes.

### 3. Video pipeline
- Use FFmpeg to inspect video metadata and extract frames.
- Select a video-restoration model suitable for the target content and available VRAM.
- Reconstruct the upscaled video with the original frame rate and preserve audio where possible.
- Test short clips first; inspect motion, flicker, synchronization, output size, and failures.

### 4. Application and benchmarks
- Add a usable interface after the inference pipelines are reliable.
- Benchmark image quality and runtime with documented input images and settings.
- Report limitations honestly; learned super-resolution can synthesize plausible details rather than recover the exact original.

## Initial constraints

- Target platform: Windows.
- Initial hardware assumption: an NVIDIA laptop GPU with around 4 GB VRAM; confirm actual hardware before choosing batch/tile settings.
- Keep downloaded checkpoints, third-party binaries, input media, generated outputs, and virtual environments out of Git.
- Verify upstream code and checkpoint licenses before redistribution or commercial deployment.

## Phase 2 boundary

Phase 2 introduces a custom PB-ANN super-resolution model. It will be evaluated against the Phase 1 baseline on the same test set and inference conditions where practical. Custom model training is not part of Phase 1.
