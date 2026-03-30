from __future__ import annotations

import argparse

from YTPGenerator import GenerationOptions, YTPGenerator


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YTPPlus Deluxe CLI")
    parser.add_argument("input", help="Input media file")
    parser.add_argument("output", help="Output media file")
    parser.add_argument("--segments", type=int, default=12, help="Reserved for future timeline slicing")
    parser.add_argument("--effects", nargs="*", default=["reverse", "speed_up", "hue_spin"])
    parser.add_argument("--random-sound", action="store_true")
    parser.add_argument("--overlay", action="store_true")
    parser.add_argument("--extra-source", action="append", default=[], help="Extra file/folder source path")
    parser.add_argument("--probability", type=float, default=0.7)
    parser.add_argument("--max-level", type=int, default=70)
    parser.add_argument("--seed", type=int, default=None)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generator = YTPGenerator()
    options = GenerationOptions(
        effects=args.effects,
        effect_probability=max(0.0, min(args.probability, 1.0)),
        max_effect_level=max(0, min(args.max_level, 100)),
        random_sound=args.random_sound,
        overlay=args.overlay,
        seed=args.seed,
        extra_sources=args.extra_source,
    )
    generator.process(args.input, args.output, options)
    print(f"Created remix: {args.output}")


if __name__ == "__main__":
    main()
