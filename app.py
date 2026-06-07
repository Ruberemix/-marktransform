import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
import pyperclip
from pathlib import Path
from markitdown import MarkItDown

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

SUPPORTED_FORMATS = {
    "Documentos": [".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls"],
    "Texto": [".txt", ".csv", ".json", ".xml", ".html", ".htm"],
    "Medios": [".jpg", ".jpeg", ".png", ".gif", ".mp3", ".wav"],
    "Otros": [".epub", ".zip", ".ipynb"],
}

ALL_EXTENSIONS = [ext for exts in SUPPORTED_FORMATS.values() for ext in exts]

FILETYPES = [
    ("Todos los soportados", " ".join(f"*{e}" for e in ALL_EXTENSIONS)),
    ("PDF", "*.pdf"),
    ("Word", "*.docx *.doc"),
    ("PowerPoint", "*.pptx *.ppt"),
    ("Excel", "*.xlsx *.xls"),
    ("Imágenes", "*.jpg *.jpeg *.png *.gif"),
    ("Audio", "*.mp3 *.wav"),
    ("HTML", "*.html *.htm"),
    ("Texto/CSV", "*.txt *.csv *.json *.xml"),
    ("Epub/Zip", "*.epub *.zip"),
    ("Todos los archivos", "*.*"),
]


class FileItem(ctk.CTkFrame):
    def __init__(self, parent, filepath, on_remove, **kwargs):
        super().__init__(parent, fg_color="#2a2a3e", corner_radius=8, **kwargs)
        self.filepath = filepath
        self.on_remove = on_remove

        name = Path(filepath).name
        ext = Path(filepath).suffix.lower()
        icon = self._icon(ext)

        self.columnconfigure(1, weight=1)

        ctk.CTkLabel(self, text=icon, font=("Segoe UI Emoji", 16), width=30).grid(
            row=0, column=0, padx=(10, 4), pady=8
        )
        ctk.CTkLabel(
            self,
            text=name,
            font=("Segoe UI", 12),
            anchor="w",
            wraplength=300,
        ).grid(row=0, column=1, sticky="ew", padx=4, pady=8)
        ctk.CTkButton(
            self,
            text="✕",
            width=28,
            height=28,
            fg_color="#ff4d4d",
            hover_color="#cc0000",
            font=("Segoe UI", 11, "bold"),
            command=self._remove,
        ).grid(row=0, column=2, padx=(4, 10), pady=8)

    def _icon(self, ext):
        icons = {
            ".pdf": "📄", ".docx": "📝", ".doc": "📝",
            ".pptx": "📊", ".ppt": "📊", ".xlsx": "📈",
            ".xls": "📈", ".csv": "📋", ".json": "🔧",
            ".xml": "🔧", ".html": "🌐", ".htm": "🌐",
            ".jpg": "🖼️", ".jpeg": "🖼️", ".png": "🖼️",
            ".gif": "🖼️", ".mp3": "🎵", ".wav": "🎵",
            ".epub": "📚", ".zip": "🗜️", ".txt": "📃",
            ".ipynb": "📓",
        }
        return icons.get(ext, "📁")

    def _remove(self):
        self.on_remove(self.filepath)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MarkTransform — Conversor a Markdown")
        self.geometry("1100x720")
        self.minsize(900, 600)

        self.md = MarkItDown()
        self.files: list[str] = []
        self.results: dict[str, str] = {}
        self.active_file: str | None = None
        self.converting = False

        self._build_ui()

    # ── UI ──────────────────────────────────────────────────────────────────

    def _build_ui(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

        self._header()
        self._left_panel()
        self._right_panel()
        self._status_bar()

    def _header(self):
        hdr = ctk.CTkFrame(self, fg_color="#12122a", corner_radius=0, height=64)
        hdr.grid(row=0, column=0, columnspan=2, sticky="ew")
        hdr.grid_propagate(False)

        ctk.CTkLabel(
            hdr,
            text="⬇  MarkTransform",
            font=("Segoe UI", 22, "bold"),
            text_color="#7b8cff",
        ).pack(side="left", padx=24, pady=14)

        ctk.CTkLabel(
            hdr,
            text="Convierte cualquier archivo a Markdown fácilmente",
            font=("Segoe UI", 12),
            text_color="#888aaa",
        ).pack(side="left", padx=4, pady=14)

        # theme toggle
        self._theme_var = ctk.StringVar(value="dark")
        ctk.CTkSegmentedButton(
            hdr,
            values=["dark", "light"],
            variable=self._theme_var,
            command=self._toggle_theme,
            width=130,
        ).pack(side="right", padx=24, pady=14)

    def _left_panel(self):
        left = ctk.CTkFrame(self, fg_color="#16162a", corner_radius=0, width=380)
        left.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        left.grid_propagate(False)
        left.rowconfigure(2, weight=1)
        left.columnconfigure(0, weight=1)

        # Drop zone
        drop = ctk.CTkFrame(left, fg_color="#1e1e38", corner_radius=14, border_width=2, border_color="#3a3a6a")
        drop.grid(row=0, column=0, sticky="ew", padx=16, pady=(16, 8))

        ctk.CTkLabel(drop, text="📂", font=("Segoe UI Emoji", 36)).pack(pady=(20, 4))
        ctk.CTkLabel(
            drop,
            text="Selecciona uno o varios archivos",
            font=("Segoe UI", 13, "bold"),
        ).pack()
        ctk.CTkLabel(
            drop,
            text="PDF · Word · Excel · PowerPoint\nImágenes · Audio · HTML · CSV · más",
            font=("Segoe UI", 11),
            text_color="#888aaa",
            justify="center",
        ).pack(pady=4)
        ctk.CTkButton(
            drop,
            text="Examinar archivos",
            font=("Segoe UI", 13, "bold"),
            height=40,
            command=self._browse_files,
        ).pack(pady=(8, 20), padx=24, fill="x")

        # URL section
        url_frame = ctk.CTkFrame(left, fg_color="#1e1e38", corner_radius=14)
        url_frame.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 8))
        url_frame.columnconfigure(0, weight=1)

        ctk.CTkLabel(url_frame, text="🔗  URL (YouTube / web)", font=("Segoe UI", 12, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w", padx=12, pady=(10, 4)
        )
        self._url_entry = ctk.CTkEntry(url_frame, placeholder_text="https://...", height=36)
        self._url_entry.grid(row=1, column=0, sticky="ew", padx=(12, 4), pady=(0, 10))
        ctk.CTkButton(url_frame, text="Agregar", width=80, height=36, command=self._add_url).grid(
            row=1, column=1, padx=(0, 12), pady=(0, 10)
        )

        # File list
        ctk.CTkLabel(left, text="Archivos seleccionados", font=("Segoe UI", 12, "bold")).grid(
            row=2, column=0, sticky="nw", padx=20, pady=(4, 2)
        )
        self._file_scroll = ctk.CTkScrollableFrame(left, fg_color="#16162a", corner_radius=0)
        self._file_scroll.grid(row=3, column=0, sticky="nsew", padx=8, pady=(0, 8))
        self._file_scroll.columnconfigure(0, weight=1)
        left.rowconfigure(3, weight=1)

        self._empty_label = ctk.CTkLabel(
            self._file_scroll,
            text="Sin archivos aún",
            font=("Segoe UI", 12),
            text_color="#555577",
        )
        self._empty_label.grid(row=0, column=0, pady=30)

        # Convert button
        self._convert_btn = ctk.CTkButton(
            left,
            text="▶  Convertir",
            font=("Segoe UI", 15, "bold"),
            height=48,
            fg_color="#4f5bd5",
            hover_color="#3a46b8",
            command=self._start_conversion,
        )
        self._convert_btn.grid(row=4, column=0, sticky="ew", padx=16, pady=(4, 16))

    def _right_panel(self):
        right = ctk.CTkFrame(self, fg_color="#12122a", corner_radius=0)
        right.grid(row=1, column=1, sticky="nsew")
        right.rowconfigure(1, weight=1)
        right.columnconfigure(0, weight=1)

        # Toolbar
        toolbar = ctk.CTkFrame(right, fg_color="#1a1a30", corner_radius=0, height=48)
        toolbar.grid(row=0, column=0, sticky="ew")
        toolbar.grid_propagate(False)

        ctk.CTkLabel(toolbar, text="Vista previa Markdown", font=("Segoe UI", 13, "bold")).pack(
            side="left", padx=16, pady=12
        )

        self._word_count_lbl = ctk.CTkLabel(toolbar, text="", font=("Segoe UI", 11), text_color="#666688")
        self._word_count_lbl.pack(side="left", padx=8)

        ctk.CTkButton(
            toolbar, text="💾 Guardar", width=100, height=32,
            command=self._save_file,
        ).pack(side="right", padx=8, pady=8)
        ctk.CTkButton(
            toolbar, text="📋 Copiar", width=100, height=32,
            fg_color="#2a2a4a", hover_color="#3a3a6a",
            command=self._copy_to_clipboard,
        ).pack(side="right", padx=(0, 4), pady=8)
        ctk.CTkButton(
            toolbar, text="🗑 Limpiar", width=100, height=32,
            fg_color="#3a1a1a", hover_color="#6a2a2a",
            command=self._clear_preview,
        ).pack(side="right", padx=(0, 4), pady=8)

        # File tabs
        self._tabs_frame = ctk.CTkScrollableFrame(
            right, fg_color="#16162a", corner_radius=0, height=40, orientation="horizontal"
        )
        self._tabs_frame.grid(row=1, column=0, sticky="ew")
        right.rowconfigure(1, weight=0)

        # Preview text
        self._preview = ctk.CTkTextbox(
            right,
            font=("Consolas", 12),
            fg_color="#0e0e1e",
            text_color="#d4d4f0",
            wrap="word",
            state="disabled",
        )
        self._preview.grid(row=2, column=0, sticky="nsew", padx=8, pady=(0, 8))
        right.rowconfigure(2, weight=1)

        self._set_preview_placeholder()

    def _status_bar(self):
        bar = ctk.CTkFrame(self, fg_color="#0e0e1a", corner_radius=0, height=36)
        bar.grid(row=2, column=0, columnspan=2, sticky="ew")
        bar.grid_propagate(False)
        bar.columnconfigure(0, weight=1)

        self._status_lbl = ctk.CTkLabel(bar, text="Listo", font=("Segoe UI", 11), text_color="#666688")
        self._status_lbl.grid(row=0, column=0, sticky="w", padx=16)

        self._progress = ctk.CTkProgressBar(bar, width=200, height=10)
        self._progress.grid(row=0, column=1, padx=16, pady=12)
        self._progress.set(0)
        self._progress.grid_remove()

    # ── Actions ─────────────────────────────────────────────────────────────

    def _browse_files(self):
        paths = filedialog.askopenfilenames(filetypes=FILETYPES, title="Seleccionar archivos")
        for p in paths:
            self._add_file(p)

    def _add_url(self):
        url = self._url_entry.get().strip()
        if not url:
            return
        if url in self.files:
            self._set_status("Esa URL ya está en la lista.")
            return
        self.files.append(url)
        self._url_entry.delete(0, "end")
        self._refresh_file_list()

    def _add_file(self, path: str):
        if path in self.files:
            return
        self.files.append(path)
        self._refresh_file_list()

    def _remove_file(self, path: str):
        self.files.remove(path)
        if path in self.results:
            del self.results[path]
        if self.active_file == path:
            self.active_file = None
            self._set_preview_placeholder()
        self._refresh_file_list()
        self._refresh_tabs()

    def _refresh_file_list(self):
        for w in self._file_scroll.winfo_children():
            w.destroy()
        if not self.files:
            self._empty_label = ctk.CTkLabel(
                self._file_scroll, text="Sin archivos aún",
                font=("Segoe UI", 12), text_color="#555577",
            )
            self._empty_label.grid(row=0, column=0, pady=30)
        else:
            for i, f in enumerate(self.files):
                item = FileItem(self._file_scroll, f, self._remove_file)
                item.grid(row=i, column=0, sticky="ew", pady=3, padx=4)

    def _refresh_tabs(self):
        for w in self._tabs_frame.winfo_children():
            w.destroy()
        for f in self.results:
            name = f if f.startswith("http") else Path(f).name
            btn = ctk.CTkButton(
                self._tabs_frame,
                text=name,
                width=max(120, len(name) * 8),
                height=30,
                fg_color="#2a2a5a" if f == self.active_file else "#1e1e3a",
                hover_color="#3a3a7a",
                font=("Segoe UI", 11),
                command=lambda fp=f: self._show_result(fp),
            )
            btn.pack(side="left", padx=4, pady=4)

    def _start_conversion(self):
        if not self.files:
            messagebox.showwarning("Sin archivos", "Selecciona al menos un archivo o URL.")
            return
        if self.converting:
            return
        self.converting = True
        self._convert_btn.configure(state="disabled", text="Convirtiendo…")
        self._progress.grid()
        self._progress.set(0)
        threading.Thread(target=self._convert_all, daemon=True).start()

    def _convert_all(self):
        total = len(self.files)
        for i, filepath in enumerate(self.files):
            name = filepath if filepath.startswith("http") else Path(filepath).name
            self._set_status(f"Convirtiendo: {name}")
            try:
                result = self.md.convert(filepath)
                self.results[filepath] = result.text_content
            except Exception as e:
                self.results[filepath] = f"❌ Error al convertir:\n\n{e}"
            self._progress.set((i + 1) / total)

        self.converting = False
        self.after(0, self._on_conversion_done)

    def _on_conversion_done(self):
        self._convert_btn.configure(state="normal", text="▶  Convertir")
        self._progress.grid_remove()
        self._set_status(f"Conversión completa — {len(self.results)} archivo(s)")
        self._refresh_tabs()
        if self.results:
            last = list(self.results.keys())[-1]
            self._show_result(last)

    def _show_result(self, filepath: str):
        self.active_file = filepath
        text = self.results.get(filepath, "")
        self._set_preview(text)
        self._refresh_tabs()
        words = len(text.split())
        chars = len(text)
        self._word_count_lbl.configure(text=f"{words} palabras · {chars} caracteres")

    def _set_preview(self, text: str):
        self._preview.configure(state="normal")
        self._preview.delete("1.0", "end")
        self._preview.insert("1.0", text)
        self._preview.configure(state="disabled")

    def _set_preview_placeholder(self):
        self._set_preview("El resultado de la conversión aparecerá aquí…")
        self._word_count_lbl.configure(text="")

    def _clear_preview(self):
        self.results.clear()
        self.active_file = None
        self._set_preview_placeholder()
        self._refresh_tabs()
        self._set_status("Vista previa limpiada.")

    def _copy_to_clipboard(self):
        if not self.active_file or self.active_file not in self.results:
            messagebox.showinfo("Nada que copiar", "Primero convierte un archivo.")
            return
        try:
            pyperclip.copy(self.results[self.active_file])
            self._set_status("Copiado al portapapeles.")
        except Exception:
            # fallback to tkinter clipboard
            self.clipboard_clear()
            self.clipboard_append(self.results[self.active_file])
            self._set_status("Copiado al portapapeles.")

    def _save_file(self):
        if not self.active_file or self.active_file not in self.results:
            messagebox.showinfo("Nada que guardar", "Primero convierte un archivo.")
            return
        default_name = "salida.md"
        if not self.active_file.startswith("http"):
            default_name = Path(self.active_file).stem + ".md"
        path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown", "*.md"), ("Texto", "*.txt")],
            initialfile=default_name,
            title="Guardar archivo Markdown",
        )
        if path:
            Path(path).write_text(self.results[self.active_file], encoding="utf-8")
            self._set_status(f"Guardado en: {path}")

    def _toggle_theme(self, value: str):
        ctk.set_appearance_mode(value)

    def _set_status(self, msg: str):
        self._status_lbl.configure(text=msg)


if __name__ == "__main__":
    app = App()
    app.mainloop()
