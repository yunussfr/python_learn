import tkinter as tk
from tkinter import filedialog, messagebox
import base64, hashlib, os, threading, time

# ── Şifreleme (XOR tabanlı, anahtar → SHA256) ──────────────────────────────
def derive_key(password: str) -> bytes:
    return hashlib.sha256(password.encode()).digest()

def xor_crypt(data: bytes, key: bytes) -> bytes:
    return bytes(b ^ key[i % len(key)] for i, b in enumerate(data))

def encrypt_text(text: str, password: str) -> str:
    key = derive_key(password)
    encrypted = xor_crypt(text.encode("utf-8"), key)
    return base64.b64encode(encrypted).decode()

def decrypt_text(token: str, password: str) -> str:
    key = derive_key(password)
    decoded = base64.b64decode(token.encode())
    return xor_crypt(decoded, key).decode("utf-8")

# ── Renkler & Sabitler ──────────────────────────────────────────────────────
BG       = "#0d0d0d"
SURFACE  = "#161616"
CARD     = "#1e1e1e"
ACCENT   = "#c8a96e"        # altın
ACCENT2  = "#e8c98e"
TEXT     = "#f0ede8"
MUTED    = "#6b6660"
DANGER   = "#e05c5c"
SUCCESS  = "#5ce07a"
FONT_H   = ("Georgia", 22, "bold")
FONT_LBL = ("Georgia", 10)
FONT_BTN = ("Courier New", 10, "bold")
FONT_IN  = ("Courier New", 11)

# ── AnimasyonYardımcıları ───────────────────────────────────────────────────
def fade_widget(widget, start=0.0, end=1.0, steps=20, delay=15):
    """Bir widget'ı alfa ile soldur / belirt (Label/Frame için arka plan hilesiz)."""
    pass  # tkinter gerçek alfa desteklemiyor; flash animasyonu kullanacağız

def flash_label(label, msg, color=SUCCESS, duration=2500):
    label.config(text=msg, fg=color)
    label.after(duration, lambda: label.config(text="", fg=MUTED))

def animate_button_press(btn, original_bg, original_fg):
    btn.config(bg=ACCENT2, fg=BG)
    btn.after(150, lambda: btn.config(bg=original_bg, fg=original_fg))

def slide_in(widget, target_y, steps=12):
    """Widget'ı yukarıdan aşağı kaydır."""
    start_y = target_y - 30
    widget.place_configure(y=start_y)
    def step(i):
        if i <= steps:
            new_y = start_y + (target_y - start_y) * (i / steps)
            widget.place_configure(y=int(new_y))
            widget.after(18, lambda: step(i + 1))
    step(0)

def typewriter(label, text, delay=35):
    label.config(text="")
    def _type(i=0):
        if i <= len(text):
            label.config(text=text[:i])
            label.after(delay, lambda: _type(i + 1))
    _type()

# ── Ana Uygulama ────────────────────────────────────────────────────────────
class SecretNoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Secret Note")
        self.root.geometry("680x740")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        self._build_header()
        self._build_tabs()
        self._build_encrypt_tab()
        self._build_decrypt_tab()
        self.switch_tab("encrypt")

        # Başlık animasyonu
        self.root.after(200, lambda: typewriter(self.title_lbl, "✦  Secret Note  ✦"))

    # ── Header ──────────────────────────────────────────────────────────────
    def _build_header(self):
        hdr = tk.Frame(self.root, bg=BG, height=90)
        hdr.pack(fill="x")

        self.title_lbl = tk.Label(hdr, text="", font=("Georgia", 26, "bold"),
                                  bg=BG, fg=ACCENT)
        self.title_lbl.pack(pady=(28, 4))

        tk.Label(hdr, text="Notlarını şifrele. Sırrını koru.",
                 font=("Georgia", 10, "italic"), bg=BG, fg=MUTED).pack()

        # İnce çizgi
        tk.Frame(self.root, bg=ACCENT, height=1).pack(fill="x", padx=40, pady=(14, 0))

    # ── Tab butonları ────────────────────────────────────────────────────────
    def _build_tabs(self):
        tab_bar = tk.Frame(self.root, bg=BG)
        tab_bar.pack(fill="x", padx=40, pady=(0, 0))

        self.tab_btns = {}
        for key, label in [("encrypt", "🔒  Şifrele & Kaydet"),
                            ("decrypt", "🔓  Çöz & Oku")]:
            btn = tk.Button(tab_bar, text=label, font=FONT_BTN,
                            bg=BG, fg=MUTED, bd=0, cursor="hand2",
                            activebackground=BG, activeforeground=ACCENT,
                            command=lambda k=key: self.switch_tab(k))
            btn.pack(side="left", padx=(0, 30), pady=12)
            self.tab_btns[key] = btn

        tk.Frame(self.root, bg="#2a2a2a", height=1).pack(fill="x", padx=40)

    def switch_tab(self, key):
        for k, btn in self.tab_btns.items():
            btn.config(fg=ACCENT if k == key else MUTED,
                       font=(FONT_BTN[0], FONT_BTN[1], "bold") if k == key else FONT_BTN)
        self.enc_frame.pack_forget()
        self.dec_frame.pack_forget()
        if key == "encrypt":
            self.enc_frame.pack(fill="both", expand=True, padx=40, pady=20)
        else:
            self.dec_frame.pack(fill="both", expand=True, padx=40, pady=20)

    # ── Şifreleme Sekmesi ────────────────────────────────────────────────────
    def _build_encrypt_tab(self):
        self.enc_frame = tk.Frame(self.root, bg=BG)

        # Dosya adı
        self._section(self.enc_frame, "Dosya Adı")
        self.enc_filename = self._entry(self.enc_frame, "ornek_not.snote")

        # Not içeriği
        self._section(self.enc_frame, "Not İçeriği")
        self.enc_text = tk.Text(self.enc_frame, height=7, font=FONT_IN,
                                bg=CARD, fg=TEXT, insertbackground=ACCENT,
                                relief="flat", bd=0,
                                selectbackground=ACCENT, selectforeground=BG)
        self.enc_text.pack(fill="x", pady=(0, 4))
        self._underline(self.enc_frame)

        # Şifre anahtarı
        self._section(self.enc_frame, "Şifre Anahtarı")
        self.enc_key = self._entry(self.enc_frame, "gizli anahtar...", show="●")

        # Buton
        enc_btn = tk.Button(self.enc_frame, text="🔒  ŞİFRELE & KAYDET",
                            font=FONT_BTN, bg=ACCENT, fg=BG, bd=0,
                            cursor="hand2", activebackground=ACCENT2,
                            activeforeground=BG, pady=10,
                            command=lambda: self._do_encrypt(enc_btn))
        enc_btn.pack(fill="x", pady=(18, 6))

        self.enc_status = tk.Label(self.enc_frame, text="", font=FONT_LBL,
                                   bg=BG, fg=MUTED)
        self.enc_status.pack()

    def _do_encrypt(self, btn):
        animate_button_press(btn, ACCENT, BG)
        filename = self.enc_filename.get().strip()
        text     = self.enc_text.get("1.0", "end").strip()
        key      = self.enc_key.get().strip()

        if not filename or not text or not key:
            flash_label(self.enc_status, "⚠  Tüm alanları doldur!", DANGER)
            return

        if not filename.endswith(".snote"):
            filename += ".snote"

        path = filedialog.asksaveasfilename(
            defaultextension=".snote",
            filetypes=[("Secret Note", "*.snote")],
            initialfile=filename,
            title="Dosyayı Kaydet")
        if not path:
            return

        try:
            token = encrypt_text(text, key)
            with open(path, "w") as f:
                f.write(token)
            flash_label(self.enc_status, f"✔  Kaydedildi → {os.path.basename(path)}", SUCCESS)
        except Exception as e:
            flash_label(self.enc_status, f"✘  Hata: {e}", DANGER)

    # ── Çözme Sekmesi ────────────────────────────────────────────────────────
    def _build_decrypt_tab(self):
        self.dec_frame = tk.Frame(self.root, bg=BG)

        # Dosya yükle
        self._section(self.dec_frame, "Şifreli Dosya")
        file_row = tk.Frame(self.dec_frame, bg=BG)
        file_row.pack(fill="x", pady=(0, 4))

        self.dec_path_var = tk.StringVar(value="")
        self.dec_path_lbl = tk.Label(file_row, textvariable=self.dec_path_var,
                                     font=FONT_IN, bg=CARD, fg=MUTED,
                                     anchor="w", padx=8)
        self.dec_path_lbl.pack(side="left", fill="x", expand=True, ipady=6)

        tk.Button(file_row, text="📂 Seç", font=FONT_BTN,
                  bg="#2a2a2a", fg=ACCENT, bd=0, cursor="hand2",
                  activebackground=ACCENT, activeforeground=BG,
                  padx=10, command=self._pick_file).pack(side="left", padx=(6, 0))

        # Sürükle-bırak alanı
        drop_frame = tk.Frame(self.dec_frame, bg="#1a1a1a",
                              highlightbackground="#2e2e2e",
                              highlightthickness=1, height=60)
        drop_frame.pack(fill="x", pady=(4, 0))
        drop_frame.pack_propagate(False)

        self.drop_lbl = tk.Label(drop_frame,
                                 text="ya da dosyayı buraya sürükle & bırak",
                                 font=("Georgia", 9, "italic"), bg="#1a1a1a", fg=MUTED)
        self.drop_lbl.pack(expand=True)
        self._enable_drag_drop(drop_frame)

        # Şifre anahtarı
        self._section(self.dec_frame, "Şifre Anahtarı")
        self.dec_key = self._entry(self.dec_frame, "gizli anahtar...", show="●")

        # Buton
        dec_btn = tk.Button(self.dec_frame, text="🔓  ÇÖZ & OKU",
                            font=FONT_BTN, bg="#2a2a2a", fg=ACCENT, bd=0,
                            cursor="hand2", activebackground=ACCENT,
                            activeforeground=BG, pady=10,
                            command=lambda: self._do_decrypt(dec_btn))
        dec_btn.pack(fill="x", pady=(18, 6))

        self.dec_status = tk.Label(self.dec_frame, text="", font=FONT_LBL,
                                   bg=BG, fg=MUTED)
        self.dec_status.pack()

        # Sonuç kutusu
        self._section(self.dec_frame, "Çözülmüş Not")
        self.dec_result = tk.Text(self.dec_frame, height=8, font=FONT_IN,
                                  bg=CARD, fg=SUCCESS, insertbackground=ACCENT,
                                  relief="flat", bd=0, state="disabled",
                                  selectbackground=ACCENT, selectforeground=BG)
        self.dec_result.pack(fill="x")
        self._underline(self.dec_frame)

    def _pick_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Secret Note", "*.snote"), ("Tüm Dosyalar", "*.*")],
            title="Şifreli Dosyayı Seç")
        if path:
            self._set_dec_path(path)

    def _set_dec_path(self, path):
        self.dec_path_var.set(path)
        self.dec_path_lbl.config(fg=TEXT)
        self.drop_lbl.config(text=f"✔  {os.path.basename(path)}", fg=ACCENT)

    def _enable_drag_drop(self, widget):
        """TkinterDnD olmadan basit tıklama ile dosya seçimi."""
        widget.bind("<Button-1>", lambda e: self._pick_file())
        widget.bind("<Enter>", lambda e: widget.config(bg="#222222"))
        widget.bind("<Leave>", lambda e: widget.config(bg="#1a1a1a"))

        # TkinterDnD kuruluysa kullan
        try:
            widget.drop_target_register("DND_Files")
            widget.dnd_bind("<<Drop>>", lambda e: self._set_dec_path(e.data.strip("{}")))
        except Exception:
            pass

    def _do_decrypt(self, btn):
        animate_button_press(btn, "#2a2a2a", ACCENT)
        path = self.dec_path_var.get().strip()
        key  = self.dec_key.get().strip()

        if not path or not key:
            flash_label(self.dec_status, "⚠  Dosya ve anahtar gerekli!", DANGER)
            return

        try:
            with open(path, "r") as f:
                token = f.read().strip()
            plain = decrypt_text(token, key)
            self._show_result(plain)
            flash_label(self.dec_status, "✔  Başarıyla çözüldü.", SUCCESS)
        except Exception:
            flash_label(self.dec_status, "✘  Yanlış anahtar veya bozuk dosya.", DANGER)
            self._clear_result()

    def _show_result(self, text):
        self.dec_result.config(state="normal")
        self.dec_result.delete("1.0", "end")
        # Typewriter efekti metin kutusunda
        def _type(i=0):
            if i <= len(text):
                self.dec_result.delete("1.0", "end")
                self.dec_result.insert("end", text[:i])
                self.dec_result.after(18, lambda: _type(i + 1))
        _type()
        self.root.after(len(text) * 20, lambda: self.dec_result.config(state="disabled"))

    def _clear_result(self):
        self.dec_result.config(state="normal")
        self.dec_result.delete("1.0", "end")
        self.dec_result.config(state="disabled")

    # ── Yardımcılar ──────────────────────────────────────────────────────────
    def _section(self, parent, label):
        tk.Label(parent, text=label.upper(),
                 font=("Courier New", 8, "bold"), bg=BG, fg=MUTED,
                 anchor="w").pack(fill="x", pady=(14, 4))

    def _entry(self, parent, placeholder="", show=""):
        var = tk.StringVar()
        e = tk.Entry(parent, textvariable=var, font=FONT_IN,
                     bg=CARD, fg=TEXT, insertbackground=ACCENT,
                     relief="flat", bd=0, show=show)
        e.pack(fill="x", ipady=6, pady=(0, 2))
        self._underline(parent)

        # Placeholder
        if placeholder:
            e.insert(0, placeholder)
            e.config(fg=MUTED)
            def on_focus_in(_):
                if e.get() == placeholder:
                    e.delete(0, "end")
                    e.config(fg=TEXT)
            def on_focus_out(_):
                if not e.get():
                    e.insert(0, placeholder)
                    e.config(fg=MUTED)
            e.bind("<FocusIn>", on_focus_in)
            e.bind("<FocusOut>", on_focus_out)
        return e

    def _underline(self, parent):
        tk.Frame(parent, bg=ACCENT, height=1).pack(fill="x")


# ── Çalıştır ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = SecretNoteApp(root)
    root.mainloop()

