import tkinter as tk
import configparser
import keyboard

def reset_streak():
    return 0

def full_reset():
    return 0, 0

def save_hotkeys():
    config = configparser.ConfigParser()
    config['Settings'] = {
        'IncreaseStreakHotkey': hotkeys['increase_streak_hotkey'],
        'ResetStreakHotkey': hotkeys['reset_streak_hotkey'],
        'FullResetStreakHotkey': hotkeys['full_reset_streak_hotkey']
    }
    with open('config.ini', 'w') as f:
        config.write(f)

def save_data(streak, pb):
    with open('data.txt', 'w') as f:
        f.write(f"{streak}\n")
        f.write(f"{pb}\n")

def load_data():
    try:
        with open('data.txt', 'r') as f:
            data = f.readlines()
        return int(data[0]), int(data[1])
    except FileNotFoundError:
        return 0, 0

def load_hotkeys():
    config = configparser.ConfigParser()
    config.read('config.ini')
    hotkeys['increase_streak_hotkey'] = config.get('Settings', 'IncreaseStreakHotkey', fallback='+')
    hotkeys['reset_streak_hotkey'] = config.get('Settings', 'ResetStreakHotkey', fallback='-')
    hotkeys['full_reset_streak_hotkey'] = config.get('Settings', 'FullResetStreakHotkey', fallback='*')

def save_results(streak, pb):
    with open('results.txt', 'w') as f:
        f.write(f"C : {streak} ")
        if pb > streak:
            f.write(f"PB : {pb}\n")
        else:
            f.write(f"PB : C\n")

def handle_reset(event=None):
    global streak, pb
    if streak > pb:
        pb = streak
    streak = reset_streak()
    save_data(streak, pb)
    save_results(streak, pb)
    update_label()

def handle_full_reset(event=None):
    global streak, pb
    streak, pb = full_reset()
    save_data(streak, pb)
    save_results(streak, pb)
    update_label()

def handle_quit(event=None):
    save_data(streak, pb)
    save_results(streak, pb)
    root.destroy()

def handle_increase_streak(event=None):
    global streak, pb
    streak += 1
    if streak > pb:
        pb = streak
    save_data(streak, pb)
    save_results(streak, pb)
    update_label()

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Paramètres")
    settings_window.protocol("WM_DELETE_WINDOW", close_settings)

    increase_streak_label = tk.Label(settings_window, text="Incrémenter la streak :")
    increase_streak_label.pack()

    increase_streak_entry = tk.Entry(settings_window)
    increase_streak_entry.pack()

    reset_streak_label = tk.Label(settings_window, text="Réinitialiser la streak :")
    reset_streak_label.pack()

    reset_streak_entry = tk.Entry(settings_window)
    reset_streak_entry.pack()

    full_reset_streak_label = tk.Label(settings_window, text="Réinitialiser Complète de la streak :")
    full_reset_streak_label.pack()

    full_reset_streak_entry = tk.Entry(settings_window)
    full_reset_streak_entry.pack()

    confirm_button = tk.Button(settings_window, text="Valider", command=lambda: update_hotkeys(settings_window, increase_streak_entry.get(), reset_streak_entry.get(), full_reset_streak_entry.get()))
    confirm_button.pack()

def close_settings():
    root.focus_set()

def update_hotkeys(settings_window, increase_streak_hotkey, reset_streak_hotkey,full_reset_streak_hotkey):
    hotkeys['increase_streak_hotkey'] = increase_streak_hotkey.lower()
    hotkeys['reset_streak_hotkey'] = reset_streak_hotkey.lower()
    hotkeys['full_reset_streak_hotkey'] = full_reset_streak_hotkey.lower()
    save_hotkeys()
    bind_hotkeys()
    settings_window.destroy()

def bind_hotkeys():
    keyboard.unhook_all()
    keyboard.add_hotkey(hotkeys['increase_streak_hotkey'], handle_increase_streak)
    keyboard.add_hotkey(hotkeys['reset_streak_hotkey'], handle_reset)
    keyboard.add_hotkey(hotkeys['full_reset_streak_hotkey'], handle_full_reset)

def update_label():
    streak_text = f"Streak: {streak}"
    pb_text = f"Personal Best: {pb}" if pb > streak else "Personal Best: C"
    streak_label.config(text=streak_text)
    pb_label.config(text=pb_text)

# Charger la configuration des touches
hotkeys = {}
load_hotkeys()

# Charger la "streak" et le "personal best" précédents (s'il y en a)
streak, pb = load_data()

# Créer la fenêtre principale
root = tk.Tk()
root.title("Streak Tracker")

# Créer les éléments de l'interface
streak_label = tk.Label(root, text=f"Streak: {streak}")
streak_label.pack()

pb_label = tk.Label(root, text=f"Personal Best: {pb}" if pb > streak else "Personal Best: C")
pb_label.pack()

reset_button = tk.Button(root, text="Réinitialiser", command=handle_reset)
reset_button.pack()

full_reset_button = tk.Button(root, text="Réinitialiser Complète", command=handle_full_reset)
full_reset_button.pack()

settings_button = tk.Button(root, text="Paramètres", command=open_settings)
settings_button.pack()

# Lier le raccourci clavier "Q" à la fonction handle_quit
root.bind("q", handle_quit)

# Lier les raccourcis clavier initiaux
bind_hotkeys()

# Mettre à jour l'affichage initial
update_label()

# Lancer la boucle principale de l'interface
root.mainloop()
