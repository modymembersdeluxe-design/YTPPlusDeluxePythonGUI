from __future__ import annotations

import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from TimeStamp import make_output_path
from YTPGenerator import GenerationOptions, YTPGenerator


class MainApp(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("YTPPlus Deluxe v1.0")
        self.geometry("920x720")

        self.generator = YTPGenerator()
        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.prob_var = tk.DoubleVar(value=0.7)
        self.level_var = tk.IntVar(value=70)
        self.random_sound_var = tk.BooleanVar(value=False)
        self.overlay_var = tk.BooleanVar(value=False)
        self.extra_sources: list[str] = []

        self.effect_vars: dict[str, tk.BooleanVar] = {
            name: tk.BooleanVar(value=False) for name in self.generator.effects_registry
        }

        self._build_ui()

    def _build_ui(self) -> None:
        frame = ttk.Frame(self, padding=12)
        frame.pack(fill="both", expand=True)

        io = ttk.LabelFrame(frame, text="Input / Output", padding=8)
        io.pack(fill="x")

        ttk.Entry(io, textvariable=self.input_var).grid(row=0, column=0, sticky="ew", padx=4, pady=4)
        ttk.Button(io, text="Open File", command=self.pick_input).grid(row=0, column=1, padx=4)

        ttk.Entry(io, textvariable=self.output_var).grid(row=1, column=0, sticky="ew", padx=4, pady=4)
        ttk.Button(io, text="Save As", command=self.pick_output).grid(row=1, column=1, padx=4)
        io.columnconfigure(0, weight=1)

        controls = ttk.LabelFrame(frame, text="Controls", padding=8)
        controls.pack(fill="x", pady=8)
        ttk.Label(controls, text="Effect Probability").grid(row=0, column=0, sticky="w")
        ttk.Scale(controls, from_=0.0, to=1.0, variable=self.prob_var, orient="horizontal").grid(
            row=0, column=1, sticky="ew", padx=8
        )
        ttk.Label(controls, text="Max Effect Level").grid(row=1, column=0, sticky="w")
        ttk.Scale(controls, from_=0, to=100, variable=self.level_var, orient="horizontal").grid(
            row=1, column=1, sticky="ew", padx=8
        )
        ttk.Checkbutton(controls, text="Random Sound Injection", variable=self.random_sound_var).grid(
            row=2, column=0, sticky="w", pady=4
        )
        ttk.Checkbutton(controls, text="Overlay (foundation)", variable=self.overlay_var).grid(
            row=2, column=1, sticky="w", pady=4
        )
        controls.columnconfigure(1, weight=1)

        sources = ttk.LabelFrame(frame, text="Additional Sources", padding=8)
        sources.pack(fill="both", pady=8)
        source_buttons = ttk.Frame(sources)
        source_buttons.pack(fill="x")
        ttk.Button(source_buttons, text="Add Video Source", command=lambda: self.add_source_file("video")).pack(
            side="left", padx=4
        )
        ttk.Button(source_buttons, text="Add Audio Source", command=lambda: self.add_source_file("audio")).pack(
            side="left", padx=4
        )
        ttk.Button(source_buttons, text="Add Image/GIF Source", command=lambda: self.add_source_file("image")).pack(
            side="left", padx=4
        )
        ttk.Button(source_buttons, text="Add Folder", command=self.add_source_folder).pack(side="left", padx=4)
        ttk.Button(source_buttons, text="Clear", command=self.clear_sources).pack(side="right", padx=4)

        self.sources_list = tk.Listbox(sources, height=5)
        self.sources_list.pack(fill="x", padx=4, pady=6)

        fx = ttk.LabelFrame(frame, text="Effects", padding=8)
        fx.pack(fill="both", expand=True)

        cols = 2
        for idx, (name, desc) in enumerate(self.generator.effects_registry.items()):
            r = idx // cols
            c = idx % cols
            ttk.Checkbutton(fx, text=f"{name}: {desc}", variable=self.effect_vars[name]).grid(
                row=r, column=c, sticky="w", padx=6, pady=4
            )

        button_bar = ttk.Frame(frame)
        button_bar.pack(fill="x", pady=10)
        ttk.Button(button_bar, text="Auto Output Name", command=self.autofill_output).pack(side="left", padx=4)
        ttk.Button(button_bar, text="Process", command=self.process).pack(side="right", padx=4)

    def add_source_file(self, source_type: str) -> None:
        if source_type == "video":
            filetypes = [("Video files", "*.mp4 *.mkv *.avi *.mov *.webm"), ("All files", "*.*")]
        elif source_type == "audio":
            filetypes = [("Audio files", "*.mp3 *.wav *.ogg *.flac *.aac"), ("All files", "*.*")]
        else:
            filetypes = [("Image/GIF files", "*.png *.jpg *.jpeg *.gif *.webp"), ("All files", "*.*")]

        picked = filedialog.askopenfilenames(title=f"Choose {source_type} sources", filetypes=filetypes)
        for p in picked:
            if p not in self.extra_sources:
                self.extra_sources.append(p)
                self.sources_list.insert("end", p)

    def add_source_folder(self) -> None:
        folder = filedialog.askdirectory(title="Choose source folder")
        if folder and folder not in self.extra_sources:
            self.extra_sources.append(folder)
            self.sources_list.insert("end", folder)

    def clear_sources(self) -> None:
        self.extra_sources.clear()
        self.sources_list.delete(0, "end")

    def pick_input(self) -> None:
        f = filedialog.askopenfilename(title="Choose media")
        if f:
            self.input_var.set(f)
            if not self.output_var.get():
                self.output_var.set(make_output_path(f))

    def pick_output(self) -> None:
        f = filedialog.asksaveasfilename(title="Save output as", defaultextension=".mp4")
        if f:
            self.output_var.set(f)

    def autofill_output(self) -> None:
        if self.input_var.get():
            self.output_var.set(make_output_path(self.input_var.get()))

    def process(self) -> None:
        input_file = self.input_var.get().strip()
        output_file = self.output_var.get().strip()

        if not input_file or not Path(input_file).exists():
            messagebox.showerror("Missing input", "Please choose a valid input file.")
            return
        if not output_file:
            messagebox.showerror("Missing output", "Please choose an output path.")
            return

        selected_effects = [name for name, flag in self.effect_vars.items() if flag.get()]
        options = GenerationOptions(
            effects=selected_effects,
            effect_probability=max(0.0, min(float(self.prob_var.get()), 1.0)),
            max_effect_level=max(0, min(int(self.level_var.get()), 100)),
            random_sound=self.random_sound_var.get(),
            overlay=self.overlay_var.get(),
            extra_sources=list(self.extra_sources),
        )

        try:
            self.generator.process(input_file, output_file, options)
            messagebox.showinfo("Done", f"Created remix:\n{output_file}")
        except Exception as exc:  # noqa: BLE001
            messagebox.showerror("Processing failed", str(exc))


def main() -> None:
    app = MainApp()
    app.mainloop()


if __name__ == "__main__":
    main()
