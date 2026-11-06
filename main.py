import tkinter as tk
import subprocess, os, time

def run(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0, timeout=10)
    except:
        return None

def log(msg):
    status.config(text=msg)
    root.update()
    print(msg)

def aplicar_todo():
    btn.config(state="disabled", text="APLICANDO AL FULL... NO CIERRES")
    log("1/8 Conectando ADB al MSI prendido...")
    run("adb kill-server")
    time.sleep(1)
    run("adb start-server")
    for p in ["5555", "21503", "6555", "5556", "7555"]:
        run(f"adb connect localhost:{p}")
    r = run("adb devices")
    if not r or "device" not in r.stdout:
        log("No conectado. Prende tu MSI y dale otra vez APLICAR")
        btn.config(state="normal", text="APLICAR")
        return
    log("CONECTADO ✅")

    log("2/8 ROOTEANDO FULL...")
    run("adb root")
    time.sleep(2)
    run("adb remount")
    run("adb shell setprop persist.sys.root 1")
    run("adb shell setprop ro.secure 0")
    run("adb shell setprop ro.debuggable 1")
    run("adb shell setprop service.adb.root 1")
    run("adb shell mount -o rw,remount /system")
    run("adb shell mount -o rw,remount /")

    log("3/8 RESOLUCION FEA PARA MAX FPS...")
    run("adb shell wm size 640x360")
    run("adb shell wm density 120")
    run("adb shell settings put global display_size_forced 640x360")
    run("adb shell wm size 640x360")

    log("4/8 GPU AL FULL - SIN SOMBRAS NI EFECTOS...")
    for c in [
        "adb shell setprop debug.hwui.renderer skiagl",
        "adb shell setprop debug.egl.hw 1",
        "adb shell setprop debug.sf.hw 1",
        "adb shell setprop debug.sf.enable_gl 1",
        "adb shell setprop persist.sys.use_dithering 0",
        "adb shell setprop debug.hwui.disable_vsync true",
        "adb shell settings put global window_animation_scale 0",
        "adb shell settings put global transition_animation_scale 0",
        "adb shell settings put global animator_duration_scale 0",
        "adb shell settings put secure show_touches 0",
        "adb shell settings put global peak_refresh_rate 240",
        "adb shell settings put global min_refresh_rate 120",
        "adb shell settings put global refresh_rate_mode 1",
    ]:
        run(c)

    log("5/8 SENSI CLEAN - SIN ACELERACION...")
    for c in [
        "adb shell settings put system pointer_speed 1",
        "adb shell settings put global pointer_speed 1",
        "adb shell settings put secure touch_sensitivity 1",
        "adb shell settings put global pointer_acceleration 0",
        "adb shell settings put system pointer_acceleration 0",
        "adb shell settings put global accelerometer_rotation 0",
    ]:
        run(c)

    log("6/8 RAM LIMPIA + MODO JUEGO - QUE NO BAJE FPS...")
    for c in [
        "adb shell settings put global background_process_limit 0",
        "adb shell settings put global always_finish_activities 0",
        "adb shell settings put global adaptive_battery_management_enabled 0",
        "adb shell settings put global low_power 0",
        "adb shell settings put global power_saving 0",
        "adb shell dumpsys deviceidle disable",
        "adb shell pm trim-caches 999999999",
        "adb shell cmd activity kill-all",
        "adb shell settings put global wifi_sleep_policy 1",
        "adb shell settings put global wifi_scan_always_enabled 0",
    ]:
        run(c)

    log("7/8 WINDOWS AL FULL - PRIORIDAD MAXIMA...")
    run('powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c')
    run('wmic process where name="HD-Player.exe" CALL setpriority 256')
    run('wmic process where name="HD-Player.exe" CALL setaffinity 255')

    log("8/8 LISTO ✅ TODO AL FULL FULL\nROOT + 640x360 DPI 120 + GPU FULL + RAM LIMPIA + SENSI CLEAN + MSI EN TIEMPO REAL\nSe va a ver feo pero va a volar")
    btn.config(state="normal", text="APLICAR - TODO AL FULL")

root = tk.Tk()
root.title("FPS Booster - MSI FULL FEO")
root.geometry("540x400")
root.configure(bg="black")

tk.Label(root, text="FPS BOOSTER - MSI", bg="black", fg="orange", font=("Arial", 24, "bold")).pack(pady=10)
tk.Label(root, text="TODO AL FULL - AUNQUE SE VEA FEO", bg="black", fg="red", font=("Arial", 12, "bold")).pack()
tk.Label(root, text="ROOT + GPU FULL + 640x360 DPI 120 + RAM LIMPIA + SENSI CLEAN", bg="black", fg="white", font=("Arial", 10)).pack(pady=5)
tk.Label(root, text="✓ Sin sombras  ✓ Sin animaciones  ✓ Sin apps en fondo  ✓ MSI en Tiempo Real", bg="black", fg="#00ff00", font=("Arial", 10, "bold")).pack(pady=5)

btn = tk.Button(root, text="APLICAR", bg="#ff0000", fg="white", font=("Arial", 20, "bold"), width=20, height=2, command=aplicar_todo)
btn.pack(pady=15)

status = tk.Label(root, text="1. Prende tu MSI\n2. Dale APLICAR y espera a que diga LISTO", bg="black", fg="white", font=("Arial", 11), wraplength=480, justify="center")
status.pack(pady=10)
root.mainloop()