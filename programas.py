import tkinter as tk
from tkinter import ttk, messagebox

BG       = "#0F1117"
CARD     = "#1A1D2E"
CARD2    = "#222538"
ACCENT   = "#6C63FF"
ACCENT2  = "#FF6584"
GREEN    = "#43E97B"
TEXT     = "#E8E8F0"
TEXT_DIM = "#7B7F9E"
ENTRY_BG = "#2A2D45"
BORDER   = "#3A3D5C"


def apply_styles(root):
    style = ttk.Style(root)
    style.theme_use("clam")
    style.configure("TScrollbar", background=CARD, troughcolor=BG, bordercolor=BG, arrowcolor=TEXT_DIM)


def make_entry(parent, placeholder="", **kwargs):
    e = tk.Entry(parent, bg=ENTRY_BG, fg=TEXT, insertbackground=TEXT,
                relief="flat", font=("Helvetica", 11),
                highlightthickness=1, highlightbackground=BORDER,
                highlightcolor=ACCENT, **kwargs)
    if placeholder:
        e.insert(0, placeholder)
        e.config(fg=TEXT_DIM)
        def on_focus_in(ev):
            if e.get() == placeholder:
                e.delete(0, "end")
                e.config(fg=TEXT)
        def on_focus_out(ev):
            if not e.get():
                e.insert(0, placeholder)
                e.config(fg=TEXT_DIM)
        e.bind("<FocusIn>", on_focus_in)
        e.bind("<FocusOut>", on_focus_out)
    return e


def make_button(parent, text, command, color=ACCENT, small=False):
    sz = 10 if small else 11
    btn = tk.Button(parent, text=text, command=command,
                    bg=color, fg=TEXT, activebackground=ACCENT2, activeforeground=TEXT,
                    relief="flat", font=("Helvetica", sz, "bold"),
                    cursor="hand2", padx=14, pady=6 if small else 10,
                    borderwidth=0)
    def on_enter(e): btn.config(bg=ACCENT2)
    def on_leave(e): btn.config(bg=color)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn


def make_textbox(parent, h=8):
    frame = tk.Frame(parent, bg=BORDER)
    frame.pack(fill="x", padx=20, pady=(0, 16))
    txt = tk.Text(frame, height=h, bg=ENTRY_BG, fg=GREEN, font=("Courier", 10),
                relief="flat", padx=12, pady=8, insertbackground=TEXT,
                wrap="word", state="disabled")
    sb = tk.Scrollbar(frame, command=txt.yview, bg=CARD, relief="flat")
    txt.config(yscrollcommand=sb.set)
    txt.pack(side="left", fill="both", expand=True)
    sb.pack(side="right", fill="y")
    return txt


def append_text(txt_widget, msg):
    txt_widget.config(state="normal")
    txt_widget.insert("end", msg + "\n")
    txt_widget.see("end")
    txt_widget.config(state="disabled")


def clear_text(txt_widget):
    txt_widget.config(state="normal")
    txt_widget.delete("1.0", "end")
    txt_widget.config(state="disabled")


def section_label(parent, text):
    tk.Label(parent, text=text, bg=CARD, fg=TEXT_DIM,
            font=("Helvetica", 9, "bold")).pack(anchor="w", padx=20, pady=(12, 2))


def divider(parent):
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=20, pady=8)


def open_exercise(parent, title, build_fn):
    win = tk.Toplevel(parent)
    win.title(title)
    win.configure(bg=BG)
    win.geometry("620x640")
    win.resizable(True, True)

    hdr = tk.Frame(win, bg=ACCENT, pady=14)
    hdr.pack(fill="x")
    tk.Label(hdr, text=title, bg=ACCENT, fg="white",
            font=("Helvetica", 15, "bold")).pack()

    canvas = tk.Canvas(win, bg=BG, highlightthickness=0)
    sb = tk.Scrollbar(win, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    inner = tk.Frame(canvas, bg=BG)
    cwin = canvas.create_window((0, 0), window=inner, anchor="nw")

    def on_resize(e): canvas.itemconfig(cwin, width=e.width)
    canvas.bind("<Configure>", on_resize)

    def on_frame(e): canvas.configure(scrollregion=canvas.bbox("all"))
    inner.bind("<Configure>", on_frame)

    def on_mousewheel(e): canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    build_fn(inner)
    win.grab_set()


# ── EJERCICIO 1 ── Sistema de aumento de sueldos ─────────────────────────────
def build_ej1(frame):
    historial = []

    def calcular_aumento(sueldo):
        if sueldo < 4000:    return sueldo * 0.15
        elif sueldo <= 7000: return sueldo * 0.10
        else:                return sueldo * 0.08

    def registrar():
        nombre = e_nombre.get().strip()
        if nombre in ("", "Nombre del trabajador"):
            messagebox.showwarning("Dato faltante", "Ingresa el nombre.", parent=frame.winfo_toplevel()); return
        try:
            sueldo = float(e_sueldo.get())
            if sueldo <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Sueldo invalido.", parent=frame.winfo_toplevel()); return

        aumento = calcular_aumento(sueldo)
        nuevo   = sueldo + aumento
        pct     = (aumento / sueldo) * 100
        historial.append((nombre, sueldo, aumento, nuevo))

        clear_text(txt)
        append_text(txt, "Trabajador registrado")
        append_text(txt, f"Nombre   : {nombre}")
        append_text(txt, f"Sueldo   : S/ {sueldo:,.2f}")
        append_text(txt, f"Aumento  : {pct:.0f}%  ->  S/ {aumento:,.2f}")
        append_text(txt, f"Nuevo    : S/ {nuevo:,.2f}")
        for w, ph in [(e_nombre, "Nombre del trabajador"), (e_sueldo, "Sueldo basico")]:
            w.delete(0, "end"); w.insert(0, ph); w.config(fg=TEXT_DIM)

    def ver_historial():
        if not historial:
            messagebox.showinfo("Historial", "Sin registros aun.", parent=frame.winfo_toplevel()); return
        clear_text(txt)
        append_text(txt, f"HISTORIAL ({len(historial)} trabajadores)")
        append_text(txt, "-" * 40)
        for i, (n, s, a, nu) in enumerate(historial, 1):
            append_text(txt, f"{i}. {n}")
            append_text(txt, f"   S/{s:,.2f}  ->  S/{nu:,.2f}  (+{(a/s*100):.0f}%)")

    card = tk.Frame(frame, bg=CARD, pady=20); card.pack(fill="x", padx=20, pady=20)
    section_label(card, "DATOS DEL TRABAJADOR")
    e_nombre = make_entry(card, "Nombre del trabajador"); e_nombre.pack(padx=20, pady=4, fill="x")
    e_sueldo = make_entry(card, "Sueldo basico");         e_sueldo.pack(padx=20, pady=4, fill="x")
    bf = tk.Frame(card, bg=CARD); bf.pack(padx=20, pady=12, fill="x")
    make_button(bf, "Registrar trabajador", registrar).pack(side="left", padx=(0, 8))
    make_button(bf, "Ver historial", ver_historial, color=CARD2).pack(side="left")
    divider(card)
    section_label(card, "RESULTADO")
    txt = make_textbox(card)


# ── EJERCICIO 2 ── Parque de diversiones ─────────────────────────────────────
def build_ej2(frame):
    visitantes = []

    def calcular_descuento(edad):
        if edad < 10:    return 0.25
        elif edad <= 17: return 0.10
        else:            return 0.0

    def registrar():
        nombre = e_nombre.get().strip()
        if nombre in ("", "Nombre del visitante"):
            messagebox.showwarning("Dato faltante", "Ingresa el nombre.", parent=frame.winfo_toplevel()); return
        try:
            edad   = int(e_edad.get())
            juegos = int(e_juegos.get())
            if edad <= 0 or juegos < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Datos invalidos.", parent=frame.winfo_toplevel()); return

        total_base = juegos * 50
        pct_desc   = calcular_descuento(edad)
        descuento  = total_base * pct_desc
        total_pago = total_base - descuento
        visitantes.append((nombre, edad, juegos, total_pago))

        clear_text(txt)
        append_text(txt, "Visitante registrado")
        append_text(txt, f"Nombre   : {nombre}  |  Edad: {edad} anios")
        append_text(txt, f"Juegos   : {juegos}  x  S/50 = S/{total_base:.2f}")
        append_text(txt, f"Descuento: {pct_desc*100:.0f}%  ->  -S/{descuento:.2f}")
        append_text(txt, f"TOTAL    : S/{total_pago:.2f}")
        for w, ph in [(e_nombre, "Nombre del visitante"), (e_edad, "Edad"), (e_juegos, "Numero de juegos")]:
            w.delete(0, "end"); w.insert(0, ph); w.config(fg=TEXT_DIM)

    def ver_total():
        if not visitantes:
            messagebox.showinfo("Total", "Sin visitantes.", parent=frame.winfo_toplevel()); return
        total = sum(v[3] for v in visitantes)
        clear_text(txt)
        append_text(txt, f"REPORTE DEL PARQUE  ({len(visitantes)} visitantes)")
        append_text(txt, "-" * 40)
        for i, (n, e, j, t) in enumerate(visitantes, 1):
            append_text(txt, f"{i}. {n}  (edad:{e})  {j} juegos  ->  S/{t:.2f}")
        append_text(txt, "-" * 40)
        append_text(txt, f"TOTAL RECAUDADO: S/{total:.2f}")

    card = tk.Frame(frame, bg=CARD, pady=20); card.pack(fill="x", padx=20, pady=20)
    section_label(card, "DATOS DEL VISITANTE")
    e_nombre = make_entry(card, "Nombre del visitante"); e_nombre.pack(padx=20, pady=4, fill="x")
    e_edad   = make_entry(card, "Edad");                 e_edad.pack(padx=20, pady=4, fill="x")
    e_juegos = make_entry(card, "Numero de juegos");     e_juegos.pack(padx=20, pady=4, fill="x")
    bf = tk.Frame(card, bg=CARD); bf.pack(padx=20, pady=12, fill="x")
    make_button(bf, "Registrar visitante", registrar).pack(side="left", padx=(0, 8))
    make_button(bf, "Total recaudado", ver_total, color=CARD2).pack(side="left")
    divider(card)
    section_label(card, "RESULTADO")
    txt = make_textbox(card)


# ── EJERCICIO 3 ── Descuentos por mes ────────────────────────────────────────
def build_ej3(frame):
    compras = []
    MESES = {"enero":1,"febrero":2,"marzo":3,"abril":4,"mayo":5,"junio":6,
            "julio":7,"agosto":8,"septiembre":9,"octubre":10,"noviembre":11,"diciembre":12}
    DESCUENTOS = {10: 0.15, 12: 0.20, 7: 0.10}

    def calcular_descuento(mes_num):
        return DESCUENTOS.get(mes_num, 0.0)

    def registrar():
        nombre  = e_nombre.get().strip()
        mes_str = e_mes.get().strip().lower()
        if nombre in ("", "Nombre del cliente"):
            messagebox.showwarning("Falta dato", "Ingresa el nombre.", parent=frame.winfo_toplevel()); return
        if mes_str not in MESES:
            messagebox.showerror("Error", "Mes invalido. Escribe el nombre completo en espaniol.", parent=frame.winfo_toplevel()); return
        try:
            importe = float(e_importe.get())
            if importe <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Importe invalido.", parent=frame.winfo_toplevel()); return

        mes_num = MESES[mes_str]
        pct     = calcular_descuento(mes_num)
        desc    = importe * pct
        total   = importe - desc
        compras.append((nombre, mes_str.capitalize(), importe, total))

        clear_text(txt)
        append_text(txt, "Compra registrada")
        append_text(txt, f"Cliente  : {nombre}")
        append_text(txt, f"Mes      : {mes_str.capitalize()}")
        append_text(txt, f"Importe  : S/{importe:.2f}")
        append_text(txt, f"Descuento: {pct*100:.0f}%  (-S/{desc:.2f})")
        append_text(txt, f"TOTAL    : S/{total:.2f}")
        for w, ph in [(e_nombre,"Nombre del cliente"),(e_mes,"Mes de la compra"),(e_importe,"Importe")]:
            w.delete(0,"end"); w.insert(0, ph); w.config(fg=TEXT_DIM)

    def ver_total():
        if not compras:
            messagebox.showinfo("Total", "Sin compras.", parent=frame.winfo_toplevel()); return
        total = sum(c[3] for c in compras)
        clear_text(txt)
        append_text(txt, f"VENTAS DEL DIA  ({len(compras)} compras)")
        append_text(txt, "-" * 40)
        for i, (n, m, imp, tot) in enumerate(compras, 1):
            append_text(txt, f"{i}. {n} ({m})  S/{imp:.2f} -> S/{tot:.2f}")
        append_text(txt, "-" * 40)
        append_text(txt, f"TOTAL VENDIDO: S/{total:.2f}")

    card = tk.Frame(frame, bg=CARD, pady=20); card.pack(fill="x", padx=20, pady=20)
    section_label(card, "DATOS DE LA COMPRA")
    e_nombre  = make_entry(card, "Nombre del cliente"); e_nombre.pack(padx=20, pady=4, fill="x")
    e_mes     = make_entry(card, "Mes de la compra");   e_mes.pack(padx=20, pady=4, fill="x")
    e_importe = make_entry(card, "Importe");            e_importe.pack(padx=20, pady=4, fill="x")
    bf = tk.Frame(card, bg=CARD); bf.pack(padx=20, pady=12, fill="x")
    make_button(bf, "Registrar compra", registrar).pack(side="left", padx=(0, 8))
    make_button(bf, "Total del dia", ver_total, color=CARD2).pack(side="left")
    divider(card)
    section_label(card, "RESULTADO")
    txt = make_textbox(card)


# ── EJERCICIO 4 ── Validar numero < 10 ───────────────────────────────────────
def build_ej4(frame):
    intentos = [0]

    def validar():
        try:
            n = int(e_num.get())
        except ValueError:
            messagebox.showerror("Error", "Ingresa un numero entero.", parent=frame.winfo_toplevel()); return
        intentos[0] += 1
        if n < 10:
            clear_text(txt)
            append_text(txt, "Numero valido!")
            append_text(txt, f"Numero ingresado   : {n}")
            append_text(txt, f"Intentos realizados: {intentos[0]}")
            intentos[0] = 0
        else:
            append_text(txt, f"Intento {intentos[0]}: {n} no es menor que 10. Intenta de nuevo.")
        e_num.delete(0, "end")

    card = tk.Frame(frame, bg=CARD, pady=20); card.pack(fill="x", padx=20, pady=20)
    tk.Label(card, text="Ingresa un numero entero menor que 10", bg=CARD, fg=TEXT_DIM,
            font=("Helvetica", 11)).pack(padx=20, pady=(0, 10))
    e_num = make_entry(card, "Escribe un numero"); e_num.pack(padx=20, pady=4, fill="x")
    e_num.bind("<Return>", lambda e: validar())
    make_button(card, "Validar", validar).pack(padx=20, pady=12, fill="x")
    divider(card)
    section_label(card, "LOG DE INTENTOS")
    txt = make_textbox(card, h=10)


# ── EJERCICIO 5 ── Validar rango (0, 20) ─────────────────────────────────────
def build_ej5(frame):
    intentos = [0]

    def en_rango(n): return 0 < n < 20

    def validar():
        try:
            n = int(e_num.get())
        except ValueError:
            messagebox.showerror("Error", "Ingresa un numero entero.", parent=frame.winfo_toplevel()); return
        intentos[0] += 1
        if en_rango(n):
            clear_text(txt)
            append_text(txt, "Numero dentro del rango!")
            append_text(txt, f"Numero  : {n}  (rango: 1 - 19)")
            append_text(txt, f"Intentos: {intentos[0]}")
            intentos[0] = 0
        else:
            msg = "demasiado bajo (minimo 1)" if n <= 0 else "demasiado alto (maximo 19)"
            append_text(txt, f"Intento {intentos[0]}: {n} fuera de rango -> {msg}")
        e_num.delete(0, "end")

    card = tk.Frame(frame, bg=CARD, pady=20); card.pack(fill="x", padx=20, pady=20)
    tk.Label(card, text="Ingresa un numero en el rango (0, 20) exclusivo", bg=CARD, fg=TEXT_DIM,
            font=("Helvetica", 11)).pack(padx=20, pady=(0, 10))
    e_num = make_entry(card, "Escribe un numero"); e_num.pack(padx=20, pady=4, fill="x")
    e_num.bind("<Return>", lambda e: validar())
    make_button(card, "Validar", validar).pack(padx=20, pady=12, fill="x")
    divider(card)
    section_label(card, "LOG DE INTENTOS")
    txt = make_textbox(card, h=10)


# ── EJERCICIO 6 ── Registro de intentos ──────────────────────────────────────
def build_ej6(frame):
    historial_nums = []
    intentos_malos = [0]

    def en_rango(n): return 0 < n < 20

    def validar():
        try:
            n = int(e_num.get())
        except ValueError:
            messagebox.showerror("Error", "Ingresa un numero entero.", parent=frame.winfo_toplevel()); return
        historial_nums.append(n)
        if en_rango(n):
            clear_text(txt)
            append_text(txt, f"Numero valido  ->  {n}")
            append_text(txt, f"Todos los intentos     : {historial_nums}")
            append_text(txt, f"Intentos incorrectos   : {intentos_malos[0]}")
            append_text(txt, f"Total de intentos      : {len(historial_nums)}")
            intentos_malos[0] = 0
        else:
            intentos_malos[0] += 1
            append_text(txt, f"#{len(historial_nums)}: {n} fuera de rango -> historial: {historial_nums}")
        e_num.delete(0, "end")

    def ver_historial():
        if not historial_nums:
            messagebox.showinfo("Historial", "No hay intentos aun.", parent=frame.winfo_toplevel()); return
        clear_text(txt)
        append_text(txt, "HISTORIAL DE INTENTOS:")
        for i, n in enumerate(historial_nums, 1):
            estado = "OK" if en_rango(n) else "FUERA"
            append_text(txt, f"  {i}. {n}  [{estado}]")
        append_text(txt, f"Incorrectos: {intentos_malos[0]}  |  Total: {len(historial_nums)}")

    card = tk.Frame(frame, bg=CARD, pady=20); card.pack(fill="x", padx=20, pady=20)
    tk.Label(card, text="Validacion con historial de intentos  (rango 1-19)", bg=CARD, fg=TEXT_DIM,
            font=("Helvetica", 11)).pack(padx=20, pady=(0, 10))
    e_num = make_entry(card, "Escribe un numero"); e_num.pack(padx=20, pady=4, fill="x")
    e_num.bind("<Return>", lambda e: validar())
    bf = tk.Frame(card, bg=CARD); bf.pack(padx=20, pady=12, fill="x")
    make_button(bf, "Validar", validar).pack(side="left", padx=(0, 8))
    make_button(bf, "Ver historial", ver_historial, color=CARD2).pack(side="left")
    divider(card)
    section_label(card, "LOG")
    txt = make_textbox(card, h=10)


# ── EJERCICIO 7 ── Suma de primeros N numeros ─────────────────────────────────
def build_ej7(frame):
    def calcular():
        try:
            n = int(e_n.get())
            if n <= 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Ingresa un entero positivo.", parent=frame.winfo_toplevel()); return
        total     = n * (n + 1) // 2
        secuencia = list(range(1, n + 1))
        clear_text(txt)
        append_text(txt, f"Suma de los primeros {n} numeros:")
        if len(secuencia) <= 15:
            append_text(txt, "  " + " + ".join(str(x) for x in secuencia) + f" = {total}")
        else:
            primeros = " + ".join(str(x) for x in secuencia[:15])
            append_text(txt, f"  {primeros} + ... (hasta {n})")
        append_text(txt, f"Resultado : {total}")
        append_text(txt, f"Formula   : n x (n+1) / 2 = {n} x {n+1} / 2 = {total}")

    card = tk.Frame(frame, bg=CARD, pady=20); card.pack(fill="x", padx=20, pady=20)
    tk.Label(card, text="Calcula la suma de los primeros N enteros positivos", bg=CARD, fg=TEXT_DIM,
            font=("Helvetica", 11)).pack(padx=20, pady=(0, 10))
    e_n = make_entry(card, "Ingresa N"); e_n.pack(padx=20, pady=4, fill="x")
    e_n.bind("<Return>", lambda e: calcular())
    make_button(card, "Calcular suma", calcular).pack(padx=20, pady=12, fill="x")
    divider(card)
    section_label(card, "RESULTADO")
    txt = make_textbox(card, h=10)


# ── EJERCICIO 8 ── Suma acumulativa ──────────────────────────────────────────
def build_ej8(frame):
    numeros   = []
    suma_acum = [0]

    def agregar():
        try:
            n = float(e_num.get())
        except ValueError:
            messagebox.showerror("Error", "Ingresa un numero valido.", parent=frame.winfo_toplevel()); return
        if n == 0:
            finalizar(); return
        numeros.append(n)
        suma_acum[0] += n
        append_text(txt, f"  #{len(numeros):>2}  Numero: {n:>10.2f}  |  Acumulado: {suma_acum[0]:>12.2f}")
        e_num.delete(0, "end")

    def finalizar():
        if not numeros:
            messagebox.showinfo("Info", "No se ingreso ningun numero.", parent=frame.winfo_toplevel()); return
        append_text(txt, "-" * 46)
        append_text(txt, f"Lista    : {numeros}")
        append_text(txt, f"Cantidad : {len(numeros)}")
        append_text(txt, f"SUMA TOTAL: {suma_acum[0]:.2f}")
        numeros.clear(); suma_acum[0] = 0
        e_num.delete(0, "end")

    def reiniciar():
        numeros.clear(); suma_acum[0] = 0
        clear_text(txt)
        append_text(txt, "Reiniciado. Ingresa numeros (0 para terminar):")
        e_num.delete(0, "end")

    card = tk.Frame(frame, bg=CARD, pady=20); card.pack(fill="x", padx=20, pady=20)
    tk.Label(card, text="Ingresa numeros uno a uno. Escribe 0 para finalizar.", bg=CARD, fg=TEXT_DIM,
            font=("Helvetica", 11)).pack(padx=20, pady=(0, 10))
    e_num = make_entry(card, "Ingresa un numero (0 = fin)"); e_num.pack(padx=20, pady=4, fill="x")
    e_num.bind("<Return>", lambda e: agregar())
    bf = tk.Frame(card, bg=CARD); bf.pack(padx=20, pady=12, fill="x")
    make_button(bf, "Agregar", agregar).pack(side="left", padx=(0, 8))
    make_button(bf, "Finalizar (0)", finalizar, color=ACCENT2).pack(side="left", padx=(0, 8))
    make_button(bf, "Reiniciar", reiniciar, color=CARD2).pack(side="left")
    divider(card)
    section_label(card, "SUMA ACUMULADA")
    txt = make_textbox(card, h=10)
    append_text(txt, "Ingresa numeros (0 para finalizar):")


# ── EJERCICIO 9 ── Suma hasta superar limite ─────────────────────────────────
def build_ej9(frame):
    numeros   = []
    suma_acum = [0]
    LIMITE    = 100
    activo    = [True]

    def agregar():
        if not activo[0]:
            messagebox.showinfo("Info", "La suma ya supero 100. Reinicia.", parent=frame.winfo_toplevel()); return
        try:
            n = int(e_num.get())
        except ValueError:
            messagebox.showerror("Error", "Ingresa un entero.", parent=frame.winfo_toplevel()); return
        numeros.append(n)
        suma_acum[0] += n
        append_text(txt, f"  #{len(numeros):>2}  Numero: {n:>8}  |  Suma parcial: {suma_acum[0]:>6}")
        e_num.delete(0, "end")
        if suma_acum[0] > LIMITE:
            activo[0] = False
            append_text(txt, "-" * 44)
            append_text(txt, f"La suma supero {LIMITE}!")
            append_text(txt, f"Numeros  : {numeros}")
            append_text(txt, f"Cantidad : {len(numeros)}")
            append_text(txt, f"SUMA FINAL: {suma_acum[0]}")

    def reiniciar():
        numeros.clear(); suma_acum[0] = 0; activo[0] = True
        clear_text(txt)
        append_text(txt, f"Reiniciado. Ingresa numeros (se detiene al superar {LIMITE}):")
        e_num.delete(0, "end")

    card = tk.Frame(frame, bg=CARD, pady=20); card.pack(fill="x", padx=20, pady=20)
    tk.Label(card, text=f"La suma se detiene cuando supere {LIMITE}", bg=CARD, fg=TEXT_DIM,
            font=("Helvetica", 11)).pack(padx=20, pady=(0, 10))
    e_num = make_entry(card, "Ingresa un numero entero"); e_num.pack(padx=20, pady=4, fill="x")
    e_num.bind("<Return>", lambda e: agregar())
    bf = tk.Frame(card, bg=CARD); bf.pack(padx=20, pady=12, fill="x")
    make_button(bf, "Agregar", agregar).pack(side="left", padx=(0, 8))
    make_button(bf, "Reiniciar", reiniciar, color=CARD2).pack(side="left")
    divider(card)
    section_label(card, "SUMAS PARCIALES")
    txt = make_textbox(card, h=10)
    append_text(txt, f"Ingresa numeros (se detiene al superar {LIMITE}):")


# ── EJERCICIO 10 ── Pago de trabajadores ─────────────────────────────────────
def build_ej10(frame):
    trabajadores = []

    def calcular_pago(h_norm, pago_h, h_extra, hijos):
        p_normal = h_norm * pago_h
        p_extra  = h_extra * (pago_h * 1.5)
        bonif    = hijos * 0.5 * pago_h
        return p_normal, p_extra, bonif, p_normal + p_extra + bonif

    def registrar():
        nombre = e_nombre.get().strip()
        if nombre in ("", "Nombre del trabajador"):
            messagebox.showwarning("Falta dato", "Ingresa el nombre.", parent=frame.winfo_toplevel()); return
        try:
            h_norm  = float(e_hnorm.get())
            pago_h  = float(e_pago.get())
            h_extra = float(e_hextra.get())
            hijos   = int(e_hijos.get())
            if h_norm < 0 or pago_h <= 0 or h_extra < 0 or hijos < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Valores numericos invalidos.", parent=frame.winfo_toplevel()); return

        p_n, p_e, bon, total = calcular_pago(h_norm, pago_h, h_extra, hijos)
        trabajadores.append((nombre, h_norm, pago_h, h_extra, hijos, total))

        clear_text(txt)
        append_text(txt, f"Trabajador: {nombre}")
        append_text(txt, "-" * 40)
        append_text(txt, f"Hrs normales : {h_norm}h x S/{pago_h:.2f} = S/{p_n:.2f}")
        append_text(txt, f"Hrs extras   : {h_extra}h x S/{pago_h*1.5:.2f} = S/{p_e:.2f}")
        append_text(txt, f"Bonif. hijos : {hijos} hijo(s) -> S/{bon:.2f}")
        append_text(txt, "-" * 40)
        append_text(txt, f"PAGO TOTAL   : S/{total:.2f}")
        for w, ph in [(e_nombre,"Nombre del trabajador"),(e_hnorm,"Horas normales"),
                    (e_pago,"Pago por hora"),(e_hextra,"Horas extras"),(e_hijos,"Numero de hijos")]:
            w.delete(0,"end"); w.insert(0, ph); w.config(fg=TEXT_DIM)

    def ver_reporte():
        if not trabajadores:
            messagebox.showinfo("Reporte", "Sin trabajadores.", parent=frame.winfo_toplevel()); return
        total_empresa = sum(t[5] for t in trabajadores)
        clear_text(txt)
        append_text(txt, f"REPORTE DE PAGOS  ({len(trabajadores)} trabajadores)")
        append_text(txt, "-" * 44)
        for i, (n, hn, ph, he, hj, tot) in enumerate(trabajadores, 1):
            append_text(txt, f"{i}. {n:<20}  S/{tot:>10.2f}")
        append_text(txt, "-" * 44)
        append_text(txt, f"TOTAL EMPRESA: S/{total_empresa:.2f}")

    card = tk.Frame(frame, bg=CARD, pady=20); card.pack(fill="x", padx=20, pady=20)
    section_label(card, "DATOS DEL TRABAJADOR")
    e_nombre = make_entry(card, "Nombre del trabajador"); e_nombre.pack(padx=20, pady=4, fill="x")
    e_hnorm  = make_entry(card, "Horas normales");        e_hnorm.pack(padx=20, pady=4, fill="x")
    e_pago   = make_entry(card, "Pago por hora");         e_pago.pack(padx=20, pady=4, fill="x")
    e_hextra = make_entry(card, "Horas extras");          e_hextra.pack(padx=20, pady=4, fill="x")
    e_hijos  = make_entry(card, "Numero de hijos");       e_hijos.pack(padx=20, pady=4, fill="x")
    bf = tk.Frame(card, bg=CARD); bf.pack(padx=20, pady=12, fill="x")
    make_button(bf, "Calcular y guardar", registrar).pack(side="left", padx=(0, 8))
    make_button(bf, "Ver reporte", ver_reporte, color=CARD2).pack(side="left")
    divider(card)
    section_label(card, "RESULTADO")
    txt = make_textbox(card)


# ── MENU PRINCIPAL ────────────────────────────────────────────────────────────
EJERCICIOS = [
    ("01", "Aumento de Sueldos",    build_ej1),
    ("02", "Parque de Diversiones", build_ej2),
    ("03", "Descuentos por Mes",    build_ej3),
    ("04", "Validar Numero < 10",   build_ej4),
    ("05", "Validar Rango (0,20)",  build_ej5),
    ("06", "Registro de Intentos",  build_ej6),
    ("07", "Suma de N Numeros",     build_ej7),
    ("08", "Suma Acumulativa",      build_ej8),
    ("09", "Suma hasta Limite 100", build_ej9),
    ("10", "Pago de Trabajadores",  build_ej10),
]


def main():
    root = tk.Tk()
    root.title("Ejercicios de Programacion")
    root.configure(bg=BG)
    root.geometry("520x680")
    root.resizable(False, False)
    apply_styles(root)

    # Header
    hdr = tk.Frame(root, bg=ACCENT, pady=24)
    hdr.pack(fill="x")
    tk.Label(hdr, text="Ejercicios de Programacion",
            bg=ACCENT, fg="white", font=("Helvetica", 18, "bold")).pack()
    tk.Label(hdr, text="Interfaz grafica con Python & Tkinter",
            bg=ACCENT, fg="#D0CCFF", font=("Helvetica", 10)).pack(pady=(4, 0))

    tk.Label(root, text="Selecciona un ejercicio para comenzar",
            bg=BG, fg=TEXT_DIM, font=("Helvetica", 11)).pack(pady=(16, 4))

    # Footer
    tk.Frame(root, bg=BORDER, height=1).pack(fill="x", pady=(12, 0))
    tk.Label(root, text="Python  -  Tkinter  -  2025",
            bg=BG, fg=TEXT_DIM, font=("Helvetica", 9)).pack(pady=8)

    # Grid de tarjetas
    grid = tk.Frame(root, bg=BG)
    grid.pack(padx=24, pady=8, fill="both")
    canvas = tk.Canvas(root, bg=BG, highlightthickness=0)
    sb = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=sb.set)
    sb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    grid = tk.Frame(canvas, bg=BG)
    cwin = canvas.create_window((0, 0), window=grid, anchor="nw")

    def on_resize(e): canvas.itemconfig(cwin, width=e.width)
    canvas.bind("<Configure>", on_resize)

    def on_frame(e): canvas.configure(scrollregion=canvas.bbox("all"))
    grid.bind("<Configure>", on_frame)

    def on_mousewheel(e): canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
    canvas.bind_all("<MouseWheel>", on_mousewheel)

    for idx, (num, titulo, fn) in enumerate(EJERCICIOS):
        row, col = divmod(idx, 2)
        card = tk.Frame(grid, bg=CARD, padx=14, pady=14,
                        highlightthickness=1, highlightbackground=BORDER)
        card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")
        grid.columnconfigure(col, weight=1)

        tk.Label(card, text=f"#{num}", bg=CARD, fg=ACCENT,
                font=("Helvetica", 10, "bold")).pack(anchor="w")
        tk.Label(card, text=titulo, bg=CARD, fg=TEXT,
                font=("Helvetica", 11, "bold"),
                wraplength=180, justify="left").pack(anchor="w", pady=(4, 8))

        def make_cmd(f=fn, t=titulo):
            return lambda: open_exercise(root, t, f)
        make_button(card, "Abrir", make_cmd(), small=True).pack(anchor="w")

    root.mainloop()


if __name__ == "__main__":
    main()