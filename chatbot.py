import tkinter as tk
from tkinter import simpledialog, messagebox
import json, random, datetime, os

# === Dosyalar ve Kontroller ===
RESPONSES_FILE = "responses.json"
RIDDLES_FILE = "riddles.json"
REMINDERS_FILE = "reminders.json"

for file, default in [(RESPONSES_FILE, {}), (RIDDLES_FILE, ["Deniz olmayan 4 il? (Bayburt, Bilecik, Bingöl, Batman)"]), (REMINDERS_FILE, [])]:
    if not os.path.exists(file):
        with open(file, "w", encoding="utf-8") as f:
            json.dump(default, f, ensure_ascii=False, indent=2)

with open(RESPONSES_FILE, "r", encoding="utf-8") as f:
    responses = json.load(f)
with open(RIDDLES_FILE, "r", encoding="utf-8") as f:
    riddles = json.load(f)

def save_responses():
    with open(RESPONSES_FILE, "w", encoding="utf-8") as f:
        json.dump(responses, f, ensure_ascii=False, indent=2)

def save_reminder(text):
    with open(REMINDERS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    data.append({"text": text, "timestamp": datetime.datetime.now().isoformat()})
    with open(REMINDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_reminders():
    try:
        with open(REMINDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def get_time():
    return datetime.datetime.now().strftime("[%H:%M]")

def get_bot_response(user_input):
    user_input = user_input.lower()

    if "saat" in user_input:
        return f"Şu an saat {datetime.datetime.now().strftime('%H:%M')}"
    if "tarih" in user_input or "gün" in user_input:
        return f"Bugünün tarihi: {datetime.datetime.now().strftime('%d %B %Y')}"
    if "zar at" in user_input:
        return f"🎲 Zar sonucu: {random.randint(1,6)}"
    if "burç" in user_input:
        return random.choice(["Bugün enerjiksin!", "Karşına fırsatlar çıkacak!", "Duygusal bir gün olabilir."])
    if "bilmece" in user_input:
        return random.choice(riddles)
    if "hatırlatıcı ekle" in user_input:
        save_reminder(user_input)
        return "Hatırlatıcı kaydedildi ✅"
    if "hatırlatıcıları göster" in user_input:
        notes = load_reminders()
        if notes:
            return "\n".join([f"- {n['text']}" for n in notes])
        else:
            return "Henüz hatırlatıcı yok."
    
    for key in responses:
        if key in user_input:
            return random.choice(responses[key])
    
    return random.choice(["Bunu tam anlayamadım 🤔", "Daha farklı sorabilir misin?", "Anlamadım, tekrar eder misin?"])

def send_message():
    user_input = entry.get()
    if not user_input.strip():
        return
    timestamp = get_time()
    add_message(f"{user_name}: {user_input}", user=True, timestamp=timestamp)
    response = get_bot_response(user_input)
    add_message(f"Bot: {response}", user=False, timestamp=get_time())
    entry.delete(0, tk.END)

def add_message(msg, user=True, timestamp=""):
    color = "#ffffff" if (dark_theme and not user) else "#333333" if (dark_theme and user) else "#eeeeee" if user else "#d1f5d3"
    fg = "#000000" if not dark_theme else "#ffffff"
    bubble = tk.Label(chat_frame, text=f"{timestamp} {msg}", bg=color, fg=fg,
                      wraplength=400, justify="left", anchor="w", padx=10, pady=6,
                      font=("Arial", 11))

    # Bot cevapları kırmızı renk ve siyah arka plan
    if not user:
        bubble.config(fg="red", bg="black")

    bubble.pack(anchor="e" if user else "w", pady=2, padx=10, fill="x")
    chat_canvas.update_idletasks()
    chat_canvas.yview_moveto(1)

def toggle_theme():
    global dark_theme
    dark_theme = not dark_theme
    apply_theme()

def apply_theme():
    bg = "#2c2f33" if dark_theme else "#f0f0f0"
    fg = "#ffffff" if dark_theme else "#000000"
    window.config(bg=bg)
    chat_frame.config(bg=bg)
    entry_frame.config(bg=bg)
    chat_canvas.config(bg=bg)
    entry.config(bg="#40444b" if dark_theme else "#ffffff", fg=fg, insertbackground=fg)
    send_button.config(bg="#7289da", fg="white")
    theme_button.config(bg="#99aab5", fg="black")
    add_button.config(bg="#43b581", fg="white")
    ask_button.config(bg="#ffaa00", fg="black")

def add_response_gui():
    key = simpledialog.askstring("Yeni Girdi", "Kullanıcıdan gelen hangi kelimeye cevap eklensin?")
    if not key: return
    value = simpledialog.askstring("Yeni Cevap", f"{key} kelimesine verilecek cevap nedir?")
    if not value: return
    if key in responses:
        responses[key].append(value)
    else:
        responses[key] = [value]
    save_responses()
    messagebox.showinfo("Başarılı", "Yeni cevap eklendi!")

def bot_asks_user():
    random_questions = [
        "Bugün nasılsın?",
        "En son izlediğin film neydi?",
        "Favori yemeğin nedir?",
        "Şu anda ne yapıyorsun?"
    ]
    q = random.choice(random_questions)
    add_message(f"Bot: {q}", user=False, timestamp=get_time())

# === Arayüz Başlat ===
window = tk.Tk()
window.title("Gelişmiş Chatbot 💬")
window.geometry("500x650")
window.resizable(False, False)
dark_theme = False
user_name = simpledialog.askstring("İsmin nedir?", "Sana nasıl hitap etmeliyim?") or "Kullanıcı"

# Chat Alanı
chat_canvas = tk.Canvas(window, bg="#f0f0f0", highlightthickness=0)
chat_scrollbar = tk.Scrollbar(window, orient="vertical", command=chat_canvas.yview)
chat_frame = tk.Frame(chat_canvas)

chat_frame.bind("<Configure>", lambda e: chat_canvas.configure(scrollregion=chat_canvas.bbox("all")))
chat_canvas.create_window((0, 0), window=chat_frame, anchor="nw")
chat_canvas.configure(yscrollcommand=chat_scrollbar.set)

chat_canvas.pack(side="top", fill="both", expand=True)
chat_scrollbar.pack(side="right", fill="y")

# Alt Giriş Alanı
entry_frame = tk.Frame(window)
entry_frame.pack(side="bottom", fill="x", pady=5)

entry = tk.Entry(entry_frame, font=("Arial", 12))
entry.pack(side="left", padx=(10, 5), pady=5, fill="x", expand=True)
entry.bind("<Return>", lambda event: send_message())

send_button = tk.Button(entry_frame, text="Gönder", command=send_message)
send_button.pack(side="left", padx=3)

theme_button = tk.Button(entry_frame, text="Tema", command=toggle_theme)
theme_button.pack(side="left", padx=3)

add_button = tk.Button(entry_frame, text="Cevap ➕", command=add_response_gui)
add_button.pack(side="left", padx=3)

ask_button = tk.Button(entry_frame, text="Bot Sorsun", command=bot_asks_user)
ask_button.pack(side="left", padx=3)

apply_theme()
window.mainloop()
