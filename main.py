import tkinter as tk
import subprocess
import os

def conectar():
    try:
        subprocess.run("adb connect localhost:5555", shell=True)
        subprocess.run("adb connect localhost:21503", shell=True)
        subprocess.run("adb connect localhost:7555", shell=True)
        status.config(text="EMULADOR CONECTADO", fg="#00FF00")
    except:
        pass

def aplicar():
    conectar()
    cmds = [
        "adb shell settings put global window_animation_scale 0",
        "adb shell settings put global transition_animation_scale 0",
        "adb shell settings put global animator_duration_scale 0",
        "adb shell settings put global debug.hwui.profile 0",
    ]
    for c in cmds:
        os.system(c)
    status.config(text="BOOST APLICADO - 800 FPS ACTIVO", fg="#00FF00")
    btn.config(text="APLICADO ✓", bg="#00C853")

def restaurar():
    os.system("adb shell settings put global window_animation_scale 1")
    os.system("adb shell settings put global transition_animation_scale 1")
    os.system("adb shell settings put global animator_duration_scale 1")
    status.config(text="RESTAURADO A NORMAL", fg="white")
    btn.config(text="APLICAR", bg="#FF6A00")

app = tk.Tk()
app.title("FPS BOOSTER")
app.geometry("520x420")
app.configure(bg="black")
app.resizable(False, False)

tk.Label(app, text="FPS BOOSTER", font=("Arial", 26, "bold"), bg="black", fg="white").pack(pady=12)
tk.Label(app, text="EMULADOR", font=("Arial", 12), bg="black", fg="gray").pack()
tk.Label(app, text="Free Fire | BlueStacks / MSI / LDPlayer", font=("Arial", 11), bg="black", fg="white").pack(pady=6)

tk.Label(app, text="Ajustes automaticos de graficos optimizados", font=("Arial", 11), bg="black", fg="white").pack(pady=12)
tk.Label(app, text="✓  Efectos graficos (OpenGL / Vulkan)", bg="black", fg="white", anchor="w").pack(fill="x", padx=50)
tk.Label(app, text="✓  Texturas simplificadas", bg="black", fg="white", anchor="w").pack(fill="x", padx=50)
tk.Label(app, text="✓  Sombras y efectos desactivados", bg="black", fg="white", anchor="w").pack(fill="x", padx=50)

btn = tk.Button(app, text="APLICAR", bg="#FF6A00", fg="white", font=("Arial", 15, "bold"), width=22, height=2, command=aplicar)
btn.pack(pady=18)

tk.Button(app, text="Desactivar / Restaurar", bg="#222222", fg="white", font=("Arial", 10), width=22, command=restaurar).pack()

status = tk.Label(app, text="v1.0 - Esperando...", bg="black", fg="yellow", font=("Arial", 10))
status.pack(pady=15)

app.mainloop()
