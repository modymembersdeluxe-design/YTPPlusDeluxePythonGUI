from __future__ import annotations

import random
from typing import Dict, Iterable, List, Tuple

EFFECTS_REGISTRY: Dict[str, str] = {
    "reverse": "Reverse clip (audio + video)",
    "speed_up": "Speed up",
    "slow_down": "Slow down",
    "repeatedly_slow": "Repeatedly slow effect",
    "echo": "Echo / chorus / aperiodic-ish echoes",
    "vibrato": "Vibrato",
    "pitch_shift": "Pitch shift approximation",
    "pitch_bend": "Pitch bend approximation",
    "stutter_loop": "Stutter loop approximation",
    "earrape": "Gain spike",
    "autotune_chaos": "Auto-Tune chaos approximation",
    "dance_squidward": "Fast cuts + pitch",
    "get_down_dance": "Get Down dance effect",
    "invert": "Invert colors",
    "rainbow_overlay": "Rainbow-ish hue spin",
    "mirror": "Horizontal mirror",
    "sus_effect": "Pitch chaos + visual jitter",
    "might_confuse_you": "Might Confuse You effect",
    "explosion_spam": "Duplicate-ish frames + heavy audio",
    "frame_shuffle": "Frame shuffle",
    "meme_injection": "Meme injection approximation",
    "sentence_mix": "Sentence mixing / audio slicing approximation",
    "deep_fry_vision": "Saturation + noise",
    "auto_source_switcher": "Auto source switcher (basic)",
    "chaos_timeline": "Random edits approximation",
    "classic_nostalgia": "Classic nostalgia approximation",
    "random_clip_shuffle": "Random clip shuffle approximation",
    "speed_warp": "Alternating speed warp",
    "green_screen_portal": "Chromakey-ish portal approximation",
    "random_clips_cuts": "Random clips and cuts approximation",
    "trailing_reverse": "Trailing reversed ghosting",
    "trailing_reverses": "Trailing Reverses effect",
    "recall_effect": "Recall effect",
    "spadinner_effect": "Spadinner effect",
    "mysterious_zoom": "Mysterious zoom effect",
    "confusion_effects": "Confusion Effects",
    "lagfun_effect": "LagFun Effect",
    "auto_recall_effect": "Auto Recall Effect",
    "super_recall_effect": "Super Recall Effects",
}


def apply_probability(effects: Iterable[str], probability: float, rng: random.Random) -> List[str]:
    chosen: List[str] = []
    for effect in effects:
        if rng.random() <= probability:
            chosen.append(effect)
    return chosen


def build_filters(selected_effects: Iterable[str], level: int) -> Tuple[str, str]:
    lvl = max(0, min(level, 100)) / 100.0
    v_filters: List[str] = []
    a_filters: List[str] = []

    for effect in selected_effects:
        if effect == "reverse":
            v_filters.append("reverse")
            a_filters.append("areverse")
        elif effect == "speed_up":
            speed = 1.15 + (0.85 * lvl)
            v_filters.append(f"setpts=PTS/{speed:.3f}")
            a_filters.append(f"atempo={min(2.0, speed):.3f}")
        elif effect == "slow_down":
            speed = 0.55 + (0.35 * (1 - lvl))
            v_filters.append(f"setpts=PTS/{speed:.3f}")
            a_filters.append(f"atempo={max(0.5, speed):.3f}")
        elif effect == "repeatedly_slow":
            a_filters.append("atempo=0.8,atempo=0.8")
            v_filters.append("setpts=1.5*PTS")
        elif effect == "echo":
            decay = 0.2 + 0.6 * lvl
            a_filters.append(f"aecho=0.8:0.9:40|80|120:{decay:.3f}|{decay/2:.3f}|{decay/3:.3f}")
        elif effect == "vibrato":
            freq = 4 + int(6 * lvl)
            depth = 0.2 + 0.7 * lvl
            a_filters.append(f"vibrato=f={freq}:d={depth:.3f}")
        elif effect in {"pitch_shift", "pitch_bend", "autotune_chaos", "sus_effect", "dance_squidward", "get_down_dance", "might_confuse_you", "spadinner_effect"}:
            semitones = int(2 + 10 * lvl)
            ratio = 2 ** (semitones / 12)
            a_filters.extend([f"asetrate=44100*{ratio:.4f}", "aresample=44100"])
        elif effect in {"stutter_loop", "random_clips_cuts", "chaos_timeline", "recall_effect"}:
            a_filters.append("aselect='not(mod(n,4))',asetpts=N/SR/TB")
            v_filters.append("select='not(mod(n,4))',setpts=N/FRAME_RATE/TB")
        elif effect == "earrape":
            gain = 5 + int(20 * lvl)
            a_filters.append(f"volume={gain}dB")
        elif effect == "invert":
            v_filters.append("negate")
        elif effect in {"rainbow_overlay", "meme_injection", "classic_nostalgia", "might_confuse_you"}:
            spin = int(20 + 320 * lvl)
            v_filters.append(f"hue='H={spin}*t'")
        elif effect == "mirror":
            v_filters.append("hflip")
        elif effect in {"frame_shuffle", "random_clip_shuffle"}:
            v_filters.append("shuffleframes=0|2|1|3")
        elif effect == "explosion_spam":
            v_filters.append("tblend=all_mode='addition':all_opacity=0.7")
            a_filters.append("acrusher=bits=6:mode=lin")
        elif effect == "sentence_mix":
            a_filters.append("aselect='not(mod(n,3))',asetpts=N/SR/TB")
        elif effect == "deep_fry_vision":
            v_filters.append("eq=saturation=2.5:contrast=1.4:brightness=0.06,noise=alls=10:allf=t")
        elif effect == "auto_source_switcher":
            v_filters.append("fps=24")
        elif effect == "speed_warp":
            v_filters.append("setpts='if(gt(mod(N,24),12),PTS*0.6,PTS*1.4)'")
            a_filters.append("atempo=1.3,atempo=0.8")
        elif effect == "green_screen_portal":
            v_filters.append("colorkey=0x00FF00:0.35:0.1")
        elif effect in {"trailing_reverse", "trailing_reverses"}:
            v_filters.append("tmix=frames=3:weights='1 1 1'")
        elif effect == "mysterious_zoom":
            v_filters.append("zoompan=z='min(zoom+0.002,1.3)':d=1")
        elif effect == "confusion_effects":
            v_filters.append("hue='H=2*t*180',hflip")
            a_filters.append("asetrate=44100*1.07,aresample=44100")
        elif effect == "lagfun_effect":
            v_filters.append("tinterlace=mode=merge,framestep=2")
            a_filters.append("aecho=0.7:0.8:120:0.4")
        elif effect == "auto_recall_effect":
            v_filters.append("select='not(mod(n,3))',setpts=N/FRAME_RATE/TB")
            a_filters.append("aselect='not(mod(n,3))',asetpts=N/SR/TB")
        elif effect == "super_recall_effect":
            v_filters.append("select='not(mod(n,5))',setpts=N/FRAME_RATE/TB,tmix=frames=4")
            a_filters.append("aselect='not(mod(n,5))',asetpts=N/SR/TB,aecho=0.8:0.9:70:0.4")

    return ",".join(v_filters), ",".join(a_filters)
