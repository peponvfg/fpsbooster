import tkinter as tk
import subprocess, os, time, threading

def run(cmd):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0, timeout=10)
    except:
        return None

def log(msg):
    status.config(text=msg)
    root.update()
    print(msg)

def aplicar_todo_thread():
    threading.Thread(target=aplicar_todo, daemon=True).start()

def aplicar_todo():
    btn.config(state="disabled", text="APLICANDO AL FULL... NO CIERRES")
    log("1/9 Conectando ADB al MSI prendido...")
    run("adb kill-server")
    time.sleep(1)
    run("adb start-server")
    for p in ["5555", "21503", "6555", "5556", "7555"]:
        run(f"adb connect localhost:{p}")
    time.sleep(1)
    r = run("adb devices")
    if not r or "device" not in r.stdout or "unauthorized" in r.stdout or r.stdout.count("device") < 2:
        log("No conectado o sin permiso.\nPrende tu MSI y acepta el permiso de depuración y dale otra vez APLICAR")
        btn.config(state="normal", text="APLICAR")
        return
    log("CONECTADO ✅")

    log("2/9 ROOTEANDO FULL...")
    run("adb root")
    time.sleep(2)
    run("adb remount")
    run("adb shell setprop persist.sys.root 1")
    run("adb shell setprop ro.secure 0")
    run("adb shell setprop ro.debuggable 1")
    run("adb shell setprop service.adb.root 1")

    log("3/9 RESOLUCION FEA PARA MAX FPS...")
    run("adb shell wm size 640x360")
    run("adb shell wm density 120")
    run("adb shell wm size 640x360")

    log("4/9 GPU AL FULL - SIN SOMBRAS NI EFECTOS...")
    for c in [
        "adb shell setprop debug.hwui.renderer skiagl",
        "adb shell setprop debug.egl.hw 1",
        "adb shell setprop debug.sf.hw 1",
        "adb shell setprop debug.sf.enable_gl 1",
        "adb shell setprop persist.sys.use_dithering 0",
        "adb shell settings put global window_animation_scale 0",
        "adb shell settings put global transition_animation_scale 0",
        "adb shell settings put global animator_duration_scale 0",
        "adb shell settings put global peak_refresh_rate 240",
        "adb shell settings put global min_refresh_rate 120",
    ]:
        run(c)

    log("5/9 SENSI CLEAN - SIN ACELERACION...")
    for c in [
        "adb shell settings put system pointer_speed 1",
        "adb shell settings put global pointer_speed 1",
        "adb shell settings put secure touch_sensitivity 1",
        "adb shell settings put global pointer_acceleration 0",
        "adb shell settings put system pointer_acceleration 0",
    ]:
        run(c)

    log("6/9 RAM LIMPIA + MODO JUEGO...")
    for c in [
        "adb shell settings put global background_process_limit 0",
        "adb shell settings put global adaptive_battery_management_enabled 0",
        "adb shell settings put global low_power 0",
        "adb shell dumpsys deviceidle disable",
        "adb shell pm trim-caches 999999999",
        "adb shell settings put global wifi_sleep_policy 1",
    ]:
        run(c)

    log("7/9 MSI EXTRA - GPU FORZADA + DALVIK...")
    for c in [
        "adb shell settings put global force_gpu_rendering 1",
        "adb shell settings put global hardware_accelerated 1",
        "adb shell setprop debug.hwui.force_gpu 1",
        "adb shell setprop persist.sys.ui.hw 1",
        "adb shell setprop debug.sf.disable_hwc 1",
        "adb shell setprop debug.sf.disable_backpressure 1",
        "adb shell setprop debug.sf.latch_unsignaled 1",
        "adb shell setprop debug.hwui.overdraw false",
        "adb shell setprop debug.hwui.show_dirty_regions false",
        "adb shell setprop dalvik.vm.heapsize 512m",
        "adb shell setprop dalvik.vm.heapgrowthlimit 256m",
        "adb shell setprop dalvik.vm.heapstartsize 16m",
        "adb shell setprop dalvik.vm.heaptargetutilization 0.75",
        "adb shell setprop dalvik.vm.heapminfree 4m",
        "adb shell setprop dalvik.vm.heapmaxfree 16m",
        "adb shell settings put global package_verifier_enable 0",
        "adb shell settings put global verifier_verify_adb_installs 0",
        "adb shell setprop debug.egl.swapinterval 0",
        "adb shell setprop debug.sf.high_fps_early_phase_offset_ns 0",
        "adb shell setprop debug.sf.high_fps_late_phase_offset_ns 0",
        "adb shell setprop ro.surface_flinger.max_frame_buffer_acquired_buffers 3",
        "adb shell settings put global stay_on_while_plugged_in 3",
        "adb shell dumpsys battery set level 100",
        "adb shell dumpsys battery set status 2",
    ]:
        run(c)

    log("8/9 MSI ULTRA - CPU FULL + SIN THERMAL + SIN LOGS + TODO APAGADO...")
    for c in [
        # CPU al full - modo performance, que no baje frecuencia
        "adb shell setprop sys.performance.mode 1",
        "adb shell setprop persist.sys.performance 1",
        "adb shell setprop ro.power_mode performance",
        "adb shell settings put global power_mode performance",
        "adb shell settings put global performance_mode 1",
        "adb shell cmd power set-mode 1",
        "adb shell echo performance > /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor",
        "adb shell echo performance > /sys/devices/system/cpu/cpu1/cpufreq/scaling_governor",
        "adb shell echo performance > /sys/devices/system/cpu/cpu2/cpufreq/scaling_governor",
        "adb shell echo performance > /sys/devices/system/cpu/cpu3/cpufreq/scaling_governor",
        # Quitar thermal - que no baje FPS por calentamiento
        "adb shell setprop persist.vendor.thermal 0",
        "adb shell setprop vendor.thermal.enable 0",
        "adb shell stop thermal-engine",
        "adb shell stop thermald",
        "adb shell stop thermal_manager",
        # Quitar logs - que no te de tirones
        "adb shell setprop log.tag VERBOSE",
        "adb shell setprop persist.log.tag VERBOSE",
        "adb shell logcat -c",
        "adb shell stop logd",
        "adb shell setprop persist.sys.log 0",
        # Apagar todo lo que come en fondo
        "adb shell settings put global bluetooth_on 0",
        "adb shell settings put secure bluetooth_on 0",
        "adb shell svc bluetooth disable",
        "adb shell settings put secure location_mode 0",
        "adb shell settings put global location_mode 0",
        "adb shell svc data disable",
        "adb shell settings put global auto_sync 0",
        "adb shell settings put system haptic_feedback_enabled 0",
        "adb shell settings put system vibrate_when_ringing 0",
        "adb shell settings put global vibrate_on 0",
        "adb shell settings put system accelerometer_rotation 0",
        "adb shell settings put global nfc_on 0",
        "adb shell svc nfc disable",
        # Apagar sensores que no usas en Free Fire
        "adb shell settings put global sensors_off 1",
        # Matar servicios de MSI que comen FPS
        "adb shell pm disable-user --user 0 com.msi.gaming",
        "adb shell pm disable-user --user 0 com.bluestacks.appmart",
        "adb shell am force-stop com.android.bluetooth",
        "adb shell am force-stop com.google.android.gms",
        "adb shell cmd appops set --uid com.google.android.gms RUN_IN_BACKGROUND ignore",
    ]:
        run(c)

    log("9/9 WINDOWS AL FULL - PRIORIDAD MAXIMA 256 + ABRIR FREE FIRE...")
    run('powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c')
    run('reg add "HKLM\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" /v "Priority" /t REG_DWORD /d 6 /f')
    run('wmic process where name="HD-Player.exe" CALL setpriority 256')
    run('wmic process where name="HD-Player.exe" CALL setaffinity 255')
    run('powershell -Command "Get-Process HD-Player | ForEach-Object { $_.PriorityClass = [System.Diagnostics.ProcessPriorityClass]::RealTime }"')
    run('wmic process where name="HD-Player.exe" CALL setpriority 256')
    # Auto-abrir Free Fire
    run("adb shell monkey -p com.dts.freefireth -c android.intent.category.LAUNCHER 1")
    run("adb shell monkey -p com.dts.freefiremax -c android.intent.category.LAUNCHER 1")

    log("10/10 LISTO ✅ TODO AL FULL FULL\n640x360 DPI 120 + GPU FORZADA + DALVIK 512m + CPU PERFORMANCE + SIN THERMAL + SIN LOGS + MSI EN TIEMPO REAL 256\nSe va a ver feo pero va a volar - Free Fire abriendo...")
    btn.config(state="normal", text="APLICAR - TODO AL FULL")

def volver_normal():
    log("Volviendo a normal...")
    run("adb shell wm size reset")
    run("adb shell wm density reset")
    run("adb shell wm size 1280x720")
    run("adb shell wm density 240")
    run("adb shell settings put global force_gpu_rendering 0")
    run("adb shell setprop debug.sf.disable_hwc 0")
    run("adb shell dumpsys battery reset")
    run("adb shell settings put global bluetooth_on 1")
    run("adb shell settings put global sensors_off 0")
    run("adb shell start thermal-engine")
    run("adb shell start logd")
    run('wmic process where name="HD-Player.exe" CALL setpriority 32')
    log("LISTO - Volviste a NORMAL 1280x720 DPI 240")

root = tk.Tk()
root.title("FPS Booster - MSI FULL FEO")
root.geometry("540x430")
root.configure(bg="black")

tk.Label(root, text="FPS BOOSTER - MSI", bg="black", fg="orange", font=("Arial", 24, "bold")).pack(pady=10)
tk.Label(root, text="TODO AL FULL - AUNQUE SE VEA FEO", bg="black", fg="red", font=("Arial", 12, "bold")).pack()
tk.Label(root, text="CPU PERFORMANCE + SIN THERMAL + SIN LOGS + GPU FORZADA", bg="black", fg="white", font=("Arial", 10)).pack(pady=5)
tk.Label(root, text="✓ CPU Full  ✓ Sin Thermal  ✓ Sin Logs  ✓ MSI en Tiempo Real 256", bg="black", fg="#00ff00", font=("Arial", 10, "bold")).pack(pady=5)

btn = tk.Button(root, text="APLICAR", bg="#ff0000", fg="white", font=("Arial", 20, "bold"), width=20, height=2, command=aplicar_todo_thread)
btn.pack(pady=10)

btn2 = tk.Button(root, text="VOLVER A NORMAL 1280x720", bg="orange", fg="black", font=("Arial", 11, "bold"), width=26, command=volver_normal)
btn2.pack(pady=5)

status = tk.Label(root, text="1. Prende tu MSI\n2. Dale APLICAR y espera a que diga LISTO\n3. Ejecuta la app como ADMINISTRADOR para que agarre el 256", bg="black", fg="white", font=("Arial", 11), wraplength=480, justify="center")
status.pack(pady=10)
root.mainloop()