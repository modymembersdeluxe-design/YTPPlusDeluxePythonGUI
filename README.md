# YTPPlus Deluxe v1.0 (Python GUI)

A Python mega YouTube Poop (YTP)-style remix generator using **Python + FFmpeg** with a simple **Tkinter GUI** and CLI.

## Requirements

- Python **3.10+** (3.7+ workable, 3.8+ recommended)
- FFmpeg (`ffmpeg` and `ffprobe` in `PATH`, or set `FFMPEG_PATH`)

## Quick Start

```bash
pip install -r requirements.txt
python MainApp.py
```

CLI example:

```bash
python PythonController.py input.mp4 output.mp4 --segments 12 --effects reverse speed_up --random-sound --overlay
```

## Features included (implemented or approximated)

- Random Sound Injection
- Reverse Clip
- Speed Up / Slow Down
- Chorus / Echo / Aperiodic echoes
- Vibrato / Pitch bend / Pitch shift
- Stutter Loop (approximated)
- Earrape Mode (gain spikes)
- Auto-Tune Chaos (approximated via pitch randomness)
- Dance & Squidward Mode (fast cuts + pitch approximation)
- Invert Colors
- Rainbow Overlay (approximated via hue spin)
- Mirror Mode
- Sus Effect (random audio pitch + visual jitter approximation)
- Explosion Spam (duplicate frames + heavy audio approximation)
- Frame Shuffle
- Full "YTP Deluxe Complete" preset
- Meme injection, Sentence mixing (audio slicing approximation), Deep Fry Vision (saturation/noise approximation)
- Auto Source Switcher (basic)
- Chaos Timeline (random edits approximation)
- Classic Nostalgia Mode (XP sounds / Sparta remix approximation)
- Random Clip Shuffle, Speed Warp, Green Screen Portal, Random Clips & Cuts, Trailing reversed effects (approximations)
- Many toggles with probability + max-level controls
- Trailing Reverses Effect
- Repeatedly Slow Effect
- Get Down Dance Effect
- Might Confuse You Effect
- Recall Effect
- Spadinner Effect
- Mysterious Zoom Effect
- Confusion Effects
- LagFun Effect
- Auto Recall Effect
- Super Recall Effects

## UI capabilities

The UI lets you:

- Choose input video and output path
- Toggle effects and randomization intensity
- Enable random sounds and overlay support
- Browse local **video/audio/image/GIF** sources
- Add custom source folders for extra assets

## Resource folders

The UI pre-loads sources from these folders if they exist:

- `resources/images`
- `resources/memes`
- `resources/meme_sounds`
- `resources/sounds`
- `resources/overlay_videos`
- `resources/adverts`
- `resources/errors`
- `resources/spadinner`
- `resources/spadinner_sounds`

You can also add additional sources using the UI browsers.

## Project structure

- `MainApp.py` — GUI and source browsers
- `PythonController.py` — CLI entry
- `YTPGenerator.py` — remix pipeline
- `EffectsFactory.py` — effect definitions/filter generation
- `Utilities.py` — FFmpeg location and execution helpers
- `TimeStamp.py` — timestamped output naming
- `presets.json` — sample deluxe preset

## Notes / limitations

- Many complex effects are approximated with native FFmpeg filters.
- Processing can be CPU-heavy.
- Some generated outputs can be very loud.
