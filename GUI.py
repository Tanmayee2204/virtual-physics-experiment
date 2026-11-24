import tkinter as tk
from tkinter import messagebox
import time
import subprocess
import os
import sys
from PIL import Image, ImageTk


# ---------------------------------------------------------------- helpers
def resource_path(relative_path):
    """Absolute path to a resource (works for scripts and PyInstaller)."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)


def load_image(path, width, height, keep_aspect=False):
    """Load an image scaled to width x height.
    If keep_aspect is True, the image is scaled to fit inside that box
    without distortion."""
    img_path = resource_path(path)
    try:
        img = Image.open(img_path)
    except FileNotFoundError:
        messagebox.showerror("Missing file", f"Image not found:\n{img_path}")
        img = Image.new("RGB", (max(width, 1), min(height, 800)), "lightgray")

    if keep_aspect:
        scale = min(width / img.width, height / img.height)
        width = max(1, int(img.width * scale))
        height = max(1, int(img.height * scale))

    img = img.resize((max(1, width), max(1, height)), Image.LANCZOS)
    return ImageTk.PhotoImage(img)


def run_real2():
    """Run real2.py whether running from script or .exe"""
    script_path = resource_path("real2.py")
    try:
        subprocess.run([sys.executable, script_path], check=True)
    except Exception as e:
        print(f"Error running real2.py: {e}")


# ---------------------------------------------------------------- main window
root = tk.Tk()
root.title("Physics Practical Simulation")
root.geometry("1500x1000")
root.state("zoomed")
root.configure(bg="#808040")

images = {}          # keep references so images aren't garbage collected
current_page = "Home"

# ---- Top bar (clock + moving text) ----
top_bar = tk.Frame(root, bg="#808040")
top_bar.pack(side="top", fill="x", padx=10, pady=10)

clock_label = tk.Label(top_bar, font=("Arial", 15), bg="white", fg="black", width=10)
clock_label.pack(side="left")

canvas = tk.Canvas(top_bar, height=45, bg="white", highlightthickness=0)
canvas.pack(side="left", fill="x", expand=True, padx=(20, 0))
text_id = canvas.create_text(500, 22, text="Welcome to Virtual Physics Lab",
                             font=("Arial", 16, "bold"), fill="black", anchor="w")


def update_text():
    canvas.move(text_id, -2, 0)
    bbox = canvas.bbox(text_id)
    if bbox and bbox[2] < 0:  # fully off the left edge -> restart from right
        canvas.coords(text_id, canvas.winfo_width(), 22)
    root.after(50, update_text)


def update_clock():
    clock_label.config(text=f"{time.strftime('%H:%M:%S')}\n{time.strftime('%d/%m/%Y')}")
    root.after(1000, update_clock)


update_text()
update_clock()

# ---- Body (sidebar + main content) ----
body = tk.Frame(root, bg="#808040")
body.pack(side="top", fill="both", expand=True, padx=10, pady=(0, 10))

sidebar = tk.Frame(body, bg="white")
sidebar.pack(side="left", fill="y")

main_frame = tk.Frame(body, bg="white", highlightbackground="blue", highlightthickness=5)
main_frame.pack(side="left", fill="both", expand=True, padx=(10, 0))
main_frame.pack_propagate(False)   # content must not change the frame's size


def get_main_size():
    root.update_idletasks()
    return max(main_frame.winfo_width() - 10, 400), max(main_frame.winfo_height() - 10, 300)


def switch_page(page_name):
    global current_page
    current_page = page_name
    for widget in main_frame.winfo_children():
        widget.destroy()
    pages[page_name]()


# ---------------------------------------------------------------- pages
def home_page():
    w, h = get_main_size()
    frame = tk.Frame(main_frame, bg="white")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Coefficient Of Static Friction", font=("Arial", 22, "bold"),
             fg="black", bg="lightblue", highlightthickness=2,
             highlightbackground="grey").pack(pady=10)

    images["home"] = load_image(os.path.join("img", "lab.jpg"), w, h - 80)
    tk.Label(frame, image=images["home"], bg="white").pack(fill="both", expand=True)


def lab_page():
    w, h = get_main_size()
    frame = tk.Frame(main_frame, bg="white")
    frame.pack(fill="both", expand=True)
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    frame.grid_rowconfigure(1, weight=1)

    tk.Button(frame, text="Run Experiment", command=run_real2, bg="blue", fg="white",
              font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

    # Notes (left)
    notes_frame = tk.Frame(frame, bg="white")
    notes_frame.grid(row=1, column=0, sticky="nw", padx=40)
    note_texts = [
        ("Note:", "red"),
        ("1. Click 'Run Experiment' to execute the experiment.", "black"),
        ("2. The Static Friction is shown between wooden block and glass.", "black"),
        ("3. Mass of the Wooden Block(Wo)=205 gwt.", "black"),
        ("4. Mass of the Pan(Po)=19 gwt.", "black"),
        ("5. Increase weight on block by 50 while doing experiment.", "black"),
        ("6. If any error occurs, check your values.", "black"),
    ]
    for text, color in note_texts:
        tk.Label(notes_frame, text=text, font=("Arial", 13), fg=color, bg="white",
                 anchor="w", justify="left").pack(anchor="w", pady=6)

    # Image (right) - keeps its aspect ratio
    images["lab"] = load_image(os.path.join("img", "app1.png"),
                               w // 2 - 60, h - 150, keep_aspect=True)
    tk.Label(frame, image=images["lab"], bg="white").grid(row=1, column=1, sticky="n", padx=20)


def observation_page():
    frame = tk.Frame(main_frame, bg="white")
    frame.pack(fill="both", expand=True)

    # Table container, centered horizontally
    table = tk.Frame(frame, bg="white")
    table.place(relx=0.5, rely=0.05, anchor="n")

    W0 = 205  # Base Weight
    P0 = 19   # Base Effort

    headers = ["Obs No.", "Mass on Block (W1)", "Total Load (W)", "Mass in Pan (P1)",
               "Total Effort (P)", "μ = P / W"]
    for col, header in enumerate(headers):
        tk.Label(table, text=header, font=("Arial", 12, "bold"), bg="lightgray",
                 width=18).grid(row=0, column=col, padx=5, pady=8)

    entries_W1, entries_P1 = [], []
    labels_W, labels_P, labels_mu = [], [], []
    mu_values = []

    def update_W(index):
        W1_value = entries_W1[index].get()
        if W1_value:
            try:
                labels_W[index].config(text=str(W0 + int(W1_value)))
            except ValueError:
                messagebox.showerror("Input Error", "Please enter an integer value for W1.")
                entries_W1[index].delete(0, tk.END)

    def update_P(index):
        P1_value = entries_P1[index].get()
        if P1_value:
            try:
                labels_P[index].config(text=str(P0 + int(P1_value)))
                if index == 4:
                    calculate()
            except ValueError:
                messagebox.showerror("Input Error", "Please enter an integer value for P1.")
                entries_P1[index].delete(0, tk.END)

    def calculate():
        try:
            mu_values.clear()
            for i in range(5):
                W1_value = entries_W1[i].get()
                P1_value = entries_P1[i].get()
                if W1_value and P1_value:
                    W = W0 + int(W1_value)
                    P = P0 + int(P1_value)
                    labels_W[i].config(text=str(W))
                    labels_P[i].config(text=str(P))
                    mu = round(P / W, 5)
                    labels_mu[i].config(text=str(mu))
                    mu_values.append(mu)
                else:
                    labels_mu[i].config(text="")

            if mu_values:
                mean_label.config(text=f"Mean μ: {round(sum(mu_values) / len(mu_values), 5)}")
            else:
                mean_label.config(text="Mean μ: -")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values.")

    def reset():
        for i in range(5):
            entries_W1[i].delete(0, tk.END)
            entries_P1[i].delete(0, tk.END)
            labels_W[i].config(text="")
            labels_P[i].config(text="")
            labels_mu[i].config(text="")
        mean_label.config(text="Mean μ: -")

    for i in range(5):
        tk.Label(table, text=str(i + 1), font=("Arial", 12), bg="white").grid(
            row=i + 1, column=0, padx=5, pady=8)

        w1_entry = tk.Entry(table, font=("Arial", 12), width=14, justify="center")
        w1_entry.grid(row=i + 1, column=1, padx=5, pady=8)
        w1_entry.bind("<FocusOut>", lambda e, index=i: update_W(index))
        w1_entry.bind("<Return>", lambda e, index=i: update_W(index))
        entries_W1.append(w1_entry)

        w_label = tk.Label(table, text="", font=("Arial", 12), width=14, bg="lightyellow")
        w_label.grid(row=i + 1, column=2, padx=5, pady=8)
        labels_W.append(w_label)

        p1_entry = tk.Entry(table, font=("Arial", 12), width=14, justify="center")
        p1_entry.grid(row=i + 1, column=3, padx=5, pady=8)
        p1_entry.bind("<FocusOut>", lambda e, index=i: update_P(index))
        p1_entry.bind("<Return>", lambda e, index=i: update_P(index))
        entries_P1.append(p1_entry)

        p_label = tk.Label(table, text="", font=("Arial", 12), width=14, bg="lightyellow")
        p_label.grid(row=i + 1, column=4, padx=5, pady=8)
        labels_P.append(p_label)

        mu_label = tk.Label(table, text="", font=("Arial", 12), width=14, bg="lightblue")
        mu_label.grid(row=i + 1, column=5, padx=5, pady=8)
        labels_mu.append(mu_label)

    mean_label = tk.Label(table, text="Mean μ: -", font=("Arial", 14, "bold"),
                          fg="black", bg="white")
    mean_label.grid(row=6, column=0, columnspan=6, pady=(20, 10))

    btn_row = tk.Frame(table, bg="white")
    btn_row.grid(row=7, column=0, columnspan=6, pady=10)
    tk.Button(btn_row, text="Calculate", font=("Arial", 12, "bold"), command=calculate,
              bg="lightblue", fg="black", width=10).pack(side="left", padx=10)
    tk.Button(btn_row, text="Reset", font=("Arial", 12, "bold"), command=reset,
              bg="lightblue", fg="black", width=10).pack(side="left", padx=10)


def about_page():
    w, h = get_main_size()
    frame = tk.Frame(main_frame, bg="white")
    frame.pack(fill="both", expand=True)

    page_canvas = tk.Canvas(frame, bg="white", highlightthickness=0)
    scrollbar = tk.Scrollbar(frame, orient="vertical", command=page_canvas.yview)
    page_canvas.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    page_canvas.pack(side="left", fill="both", expand=True)

    scroll_frame = tk.Frame(page_canvas, bg="white")
    window = page_canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

    img_width = w - 40  # leave room for the scrollbar
    for idx, img_name in enumerate(["page1.jpg", "page2.jpg", "page3.jpg"]):
        # height is huge on purpose -> only the width limits the size (no distortion)
        img = load_image(os.path.join("img", img_name), img_width, 10 ** 6, keep_aspect=True)
        images[f"about_{idx}"] = img
        tk.Label(scroll_frame, image=img, bg="white").pack(pady=10)

    def on_frame_configure(event):
        page_canvas.configure(scrollregion=page_canvas.bbox("all"))

    def on_canvas_configure(event):
        page_canvas.itemconfig(window, width=event.width)  # centers the images

    scroll_frame.bind("<Configure>", on_frame_configure)
    page_canvas.bind("<Configure>", on_canvas_configure)

    # Mouse-wheel scrolling
    def on_wheel(event):
        page_canvas.yview_scroll(int(-event.delta / 120), "units")

    page_canvas.bind("<Enter>", lambda e: page_canvas.bind_all("<MouseWheel>", on_wheel))
    page_canvas.bind("<Leave>", lambda e: page_canvas.unbind_all("<MouseWheel>"))


pages = {
    "Home": home_page,
    "Lab": lab_page,
    "Observation": observation_page,
    "Theory": about_page,
}


def exit_app():
    root.destroy()


# ---------------------------------------------------------------- sidebar
buttons = [
    ("Home", "🏠", "Home"),
    ("Lab", "🔬", "Lab"),
    ("Observation", "📊", "Observation"),
    ("Theory", "📑", "Theory"),
    ("Exit", "⏻", None),
]

BUTTON_GAP = 12   # vertical space between buttons (increase/decrease to taste)

for i, (text, icon, page) in enumerate(buttons):
    if text == "Exit":
        btn = tk.Button(sidebar, text=f"{icon} {text}", font=("Arial", 12), bg="tomato",
                        fg="white", width=12, height=2, command=exit_app)
    else:
        btn = tk.Button(sidebar, text=f"{icon} {text}", font=("Arial", 12), bg="#008CFF",
                        fg="white", width=12, height=2,
                        command=lambda p=page: switch_page(p))
    btn.pack(padx=15, pady=(30 if i == 0 else 0, BUTTON_GAP))


# ---------------------------------------------------------------- resize handling
resize_job = None
last_size = (0, 0)


def refresh_page():
    """Redraw the current page when the window size really changed."""
    global last_size
    size = (main_frame.winfo_width(), main_frame.winfo_height())
    if size == last_size:
        return
    last_size = size
    if current_page != "Observation":   # don't wipe values the user typed
        switch_page(current_page)


def on_resize(event):
    global resize_job
    if resize_job:
        root.after_cancel(resize_job)
    resize_job = root.after(250, refresh_page)


main_frame.bind("<Configure>", on_resize)

# ---------------------------------------------------------------- start
root.update()   # let the window reach its maximized size before drawing the first page
last_size = (main_frame.winfo_width(), main_frame.winfo_height())
switch_page("Home")

root.mainloop()
