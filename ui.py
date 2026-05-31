import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import threading
import os

from script import remove_background, get_image_preview


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

ACCENT = "#6C63FF"
ACCENT_HOVER = "#574FD6"
BG_DARK = "#0F0F13"
BG_CARD = "#1A1A24"
BG_CARD2 = "#22222F"
TEXT_PRIMARY = "#F0EFF8"
TEXT_MUTED = "#7A7A9A"
BORDER = "#2E2E42"
SUCCESS = "#4ADE80"
ERROR = "#F87171"


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("BG Remover")
        self.geometry("900x620")
        self.minsize(800, 560)
        self.configure(fg_color=BG_DARK)

        self.input_path = None
        self.output_path = None

        self._build_ui()

    def _build_ui(self):
        header = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0, height=64)
        header.pack(fill="x", side="top")
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="✦  BG Remover",
            font=ctk.CTkFont(family="Helvetica", size=20, weight="bold"),
            text_color=TEXT_PRIMARY,
        ).pack(side="left", padx=28, pady=18)

        ctk.CTkLabel(
            header,
            text="Eliminar fondos con IA",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_MUTED,
        ).pack(side="left", padx=0, pady=18)

        body = ctk.CTkFrame(self, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=24, pady=20)
        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.rowconfigure(0, weight=1)

        self.panel_left = self._build_image_panel(body, "Input", 0)

        self.panel_right = self._build_image_panel(body, "Output", 1)

        footer = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=0, height=76)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        inner = ctk.CTkFrame(footer, fg_color="transparent")
        inner.pack(expand=True, fill="both", padx=24)

        self.btn_open = ctk.CTkButton(
            inner,
            text="Abrir imagen",
            width=160,
            height=42,
            corner_radius=10,
            fg_color=BG_CARD2,
            hover_color=BORDER,
            border_color=BORDER,
            border_width=1,
            text_color=TEXT_PRIMARY,
            font=ctk.CTkFont(size=14),
            command=self.open_image,
        )
        self.btn_open.pack(side="left", pady=16)

        self.btn_process = ctk.CTkButton(
            inner,
            text="Eliminar fondo",
            width=180,
            height=42,
            corner_radius=10,
            fg_color=ACCENT,
            hover_color=ACCENT_HOVER,
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.process_image,
            state="disabled",
        )
        self.btn_process.pack(side="left", padx=12, pady=16)

        self.btn_save = ctk.CTkButton(
            inner,
            text="Guardar",
            width=180,
            height=42,
            corner_radius=10,
            fg_color=BG_CARD2,
            hover_color=BORDER,
            border_color=BORDER,
            border_width=1,
            text_color=TEXT_MUTED,
            font=ctk.CTkFont(size=14),
            command=self.save_image,
            state="disabled",
        )
        self.btn_save.pack(side="left", pady=16)

        self.status_label = ctk.CTkLabel(
            inner,
            text="",
            font=ctk.CTkFont(size=13),
            text_color=TEXT_MUTED,
        )
        self.status_label.pack(side="right", pady=16)

    def _build_image_panel(self, parent, title: str, col: int) -> ctk.CTkFrame:
        frame = ctk.CTkFrame(
            parent,
            fg_color=BG_CARD,
            corner_radius=16,
            border_width=1,
            border_color=BORDER,
        )
        frame.grid(row=0, column=col, sticky="nsew", padx=(0, 12) if col == 0 else (12, 0))

        ctk.CTkLabel(
            frame,
            text=title,
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=TEXT_MUTED,
        ).pack(anchor="nw", padx=18, pady=(14, 0))

        placeholder = ctk.CTkFrame(frame, fg_color=BG_CARD2, corner_radius=12)
        placeholder.pack(fill="both", expand=True, padx=14, pady=(8, 14))

        label = ctk.CTkLabel(
            placeholder,
            text="",
            fg_color="transparent",
        )
        label.pack(fill="both", expand=True)

        if col == 0:
            self.img_label_left = label
            self.placeholder_left = placeholder
        else:
            self.img_label_right = label
            self.placeholder_right = placeholder

        return frame

    def _set_placeholder_text(self, label, text):
        label.configure(
            text=text,
            font=ctk.CTkFont(size=13),
            text_color=TEXT_MUTED,
            image=None,
        )

    def open_image(self):
        path = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.webp"), ("Todos", "*.*")],
        )
        if not path:
            return

        self.input_path = path
        self.output_path = None

        img = get_image_preview(path, (380, 380))
        photo = ImageTk.PhotoImage(img)
        self.img_label_left.configure(image=photo, text="")
        self.img_label_left.image = photo

        self._set_placeholder_text(self.img_label_right, "Procesando…")
        self.img_label_right.configure(text="")

        self.btn_process.configure(state="normal")
        self.btn_save.configure(state="disabled", text_color=TEXT_MUTED)
        self.status_label.configure(text=f"📂  {os.path.basename(path)}", text_color=TEXT_MUTED)

    def process_image(self):
        if not self.input_path:
            return

        self.btn_process.configure(state="disabled", text="Procesando…")
        self.btn_open.configure(state="disabled")
        self.status_label.configure(text="⏳  Eliminando fondo…", text_color=TEXT_MUTED)
        self._set_placeholder_text(self.img_label_right, "⏳  Procesando…")

        thread = threading.Thread(target=self._run_removal, daemon=True)
        thread.start()

    def _run_removal(self):
        try:
            out = remove_background(self.input_path)
            self.output_path = out
            self.after(0, self._on_success)
        except Exception as e:
            self.after(0, lambda: self._on_error(str(e)))

    def _on_success(self):
        img = get_image_preview(self.output_path, (380, 380))

        # Fondo de tablero de ajedrez para mostrar transparencia
        checker = Image.new("RGBA", img.size, (0, 0, 0, 0))
        sq = 12
        for y in range(0, img.height, sq):
            for x in range(0, img.width, sq):
                color = (50, 50, 70, 255) if (x // sq + y // sq) % 2 == 0 else (30, 30, 45, 255)
                for py in range(min(sq, img.height - y)):
                    for px in range(min(sq, img.width - x)):
                        checker.putpixel((x + px, y + py), color)

        if img.mode == "RGBA":
            checker.paste(img, mask=img.split()[3])
        else:
            checker.paste(img)

        photo = ImageTk.PhotoImage(checker)
        self.img_label_right.configure(image=photo, text="")
        self.img_label_right.image = photo

        self.btn_process.configure(state="normal", text="Eliminar fondo")
        self.btn_open.configure(state="normal")
        self.btn_save.configure(state="normal", text_color=TEXT_PRIMARY)
        self.status_label.configure(text="✅  Listo", text_color=SUCCESS)

    def _on_error(self, msg: str):
        self.btn_process.configure(state="normal", text="Eliminar fondo")
        self.btn_open.configure(state="normal")
        self._set_placeholder_text(self.img_label_right, f"❌  Error")
        self.status_label.configure(text=f"Error: {msg}", text_color=ERROR)
        messagebox.showerror("Error", msg)

    def save_image(self):
        if not self.output_path:
            return

        dest = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG", "*.png")],
            initialfile="sin_fondo.png",
        )
        if not dest:
            return

        img = Image.open(self.output_path)
        img.save(dest, "PNG")
        self.status_label.configure(text=f"💾  Guardado en {os.path.basename(dest)}", text_color=SUCCESS)