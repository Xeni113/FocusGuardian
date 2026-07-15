import tkinter as tk


def show_reminder(message):
    root = tk.Tk()

    root.title("FocusGuardian")
    root.geometry("450x200")
    root.attributes("-topmost", True)

    label = tk.Label(
        root,
        text=message,
        font=("Arial", 14),
        wraplength=400,
        justify="center"
    )

    label.pack(expand=True)

    button = tk.Button(
        root,
        text="Back to Work",
        command=root.destroy,
        font=("Arial", 12)
    )

    button.pack(pady=20)

    root.mainloop()