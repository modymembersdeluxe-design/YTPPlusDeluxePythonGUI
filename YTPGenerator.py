from __future__ import annotations

import random
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Sequence

from EffectsFactory import EFFECTS_REGISTRY, apply_probability, build_filters
from Utilities import run_ffmpeg

RESOURCE_FOLDERS = [
    "resources/images",
    "resources/memes",
    "resources/meme_sounds",
    "resources/sounds",
    "resources/overlay_videos",
    "resources/adverts",
    "resources/errors",
    "resources/spadinner",
    "resources/spadinner_sounds",
]


@dataclass
class GenerationOptions:
    effects: Sequence[str] = field(default_factory=list)
    effect_probability: float = 0.7
    max_effect_level: int = 70
    random_sound: bool = False
    overlay: bool = False
    seed: int | None = None
    extra_sources: Sequence[str] = field(default_factory=list)


class YTPGenerator:
    def __init__(self) -> None:
        self.effects_registry = EFFECTS_REGISTRY

    def discover_resource_files(self, root: str = ".", extra_sources: Sequence[str] | None = None) -> List[str]:
        found: List[str] = []
        for folder in RESOURCE_FOLDERS:
            path = Path(root) / folder
            if path.exists():
                found.extend(str(p) for p in path.iterdir() if p.is_file())

        for source in extra_sources or []:
            src_path = Path(source)
            if src_path.is_dir():
                found.extend(str(p) for p in src_path.iterdir() if p.is_file())
            elif src_path.is_file():
                found.append(str(src_path))

        return found

    def process(self, input_file: str, output_file: str, options: GenerationOptions) -> str:
        rng = random.Random(options.seed)
        base_effects = [e for e in options.effects if e in self.effects_registry]
        selected = apply_probability(base_effects, options.effect_probability, rng)
        if not selected:
            selected = base_effects[:1] if base_effects else ["hue_spin"]

        vfilter, afilter = build_filters(selected, options.max_effect_level)

        args = ["-i", input_file]

        if options.random_sound:
            sound_candidates = [
                p
                for p in self.discover_resource_files(extra_sources=options.extra_sources)
                if Path(p).suffix.lower() in {".mp3", ".wav", ".ogg", ".aac", ".flac"}
            ]
            if sound_candidates:
                pick = rng.choice(sound_candidates)
                args.extend(["-i", pick])
                if afilter:
                    afilter = f"{afilter},[1:a]volume=0.25[a1];[0:a][a1]amix=inputs=2:duration=first"
                else:
                    afilter = "[1:a]volume=0.25[a1];[0:a][a1]amix=inputs=2:duration=first"

        if vfilter:
            args.extend(["-vf", vfilter])
        if afilter:
            args.extend(["-af", afilter])

        args.extend(["-c:v", "libx264", "-c:a", "aac", output_file])
        run_ffmpeg(args)
        return output_file
