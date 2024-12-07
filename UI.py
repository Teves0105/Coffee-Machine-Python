import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pygame
from tkinter import PhotoImage
import main


def start_ui():
    Money_machine = main.Money_machine
    Coffee_maker = main.Coffee_maker
    Current_menu = main.Current_menu

    coin_entries = {}

    def on_hover(event, button):
        button.config(bg="lightgreen")  # Màu nền khi hover

    def on_leave(event, button):
        button.config(bg="lightblue")  # Trả lại màu khi chuột ra ngoài

    def make_coffee(drink1):
        drink_obj = Current_menu.find_drink(drink1)
        if drink_obj == -1:
            messagebox.showerror("Error", "Drink not found!")
            return

        if Coffee_maker.is_resource_sufficient(drink_obj):
            global selected_drink
            selected_drink = drink_obj
            notebook.select(payment_tab)  # Hiển thị tab Payment
            setup_payment_tab(drink1)

    def setup_payment_tab(drink1):
        for widget in payment_tab.winfo_children():
            widget.destroy()

        content_frame = tk.Frame(payment_tab, padx=50, pady=50, bg="#f0f0f0")
        content_frame.pack(expand=True, fill=tk.BOTH)

        # Tiêu đề với phông chữ mới
        tk.Label(content_frame, text=f"Insert Coins for {drink1}", font=("Roboto", 24, "bold"), bg="#f0f0f0",
                 fg="#333").pack(pady=10)

        coin_frame = tk.Frame(content_frame, bg="#f0f0f0")
        coin_frame.pack(expand=True, fill=tk.BOTH, pady=20)

        for coin in Money_machine.COIN_VALUES:
            frame = tk.Frame(coin_frame, pady=10, bg="#f0f0f0")
            frame.pack(pady=10)

            # Nhãn với phông chữ mới
            tk.Label(frame, text=f"{coin.capitalize()} (value: {Money_machine.COIN_VALUES[coin]}):",
                     font=("Arial", 14), bg="#f0f0f0", fg="#444").pack(side=tk.LEFT, padx=10)

            # Entry với phông chữ và border đẹp
            entry = tk.Entry(frame, width=5, font=("Arial", 16), bd=2, relief="solid", justify="center")
            entry.pack(side=tk.LEFT, padx=15, pady=5)
            coin_entries[coin] = entry

        button_frame = tk.Frame(content_frame, pady=30, bg="#f0f0f0")
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        # Nút Confirm Payment với phông chữ khác
        confirm_button = tk.Button(button_frame, text="Confirm Payment", font=("Poppins", 18, "bold"), bg="#4CAF50",
                                   fg="white",
                                   width=20, height=2, command=lambda: confirm_payment(drink1), relief="raised")
        confirm_button.pack(pady=20)

        confirm_button.bind("<Enter>", lambda event: confirm_button.config(bg="#45a049"))  # Hover effect
        confirm_button.bind("<Leave>", lambda event: confirm_button.config(bg="#4CAF50"))  # Hover effect

    def confirm_payment(drink1):
        try:
            coin_counts = {}
            for coin, entry in coin_entries.items():
                value = entry.get().strip()
                if not value.isdigit():
                    raise ValueError(f"Invalid input for {coin}. Please enter a valid number.")
                coin_counts[coin] = int(value)

            Money_machine.money_received = sum(
                coin_counts[coin] * Money_machine.COIN_VALUES[coin] for coin in coin_counts
            )

            drink_obj = Current_menu.find_drink(drink1)
            if drink_obj == -1:
                messagebox.showerror("Error", "Drink not found!")
                return

            if Money_machine.make_payment(drink_obj.cost):  # Sử dụng hàm make_payment
                Coffee_maker.make_coffee(drink_obj)
                messagebox.showinfo("Success", f"{drink1} is ready! Enjoy your coffee!")
                notebook.select(menu_tab)
            else:
                messagebox.showerror("Error", "Insufficient funds!")

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def view_report():
        coffee_report = Coffee_maker.report()
        money_report = Money_machine.report()

    def refill_resources():
        Coffee_maker.refill()
        messagebox.showinfo("Success", "Resources have been refilled!")

    def play_music():
        """Phát nhạc nền."""
        pygame.mixer.init()  # Khởi tạo mixer
        pygame.mixer.music.load("images/video.mp3")  # Đường dẫn file nhạc
        pygame.mixer.music.play(-1)  # Phát lặp vô hạn

    def stop_music():
        """Dừng nhạc."""
        pygame.mixer.music.stop()

    def setup_menu_tab():
        logo = PhotoImage(file="images/logo.png")  # Đường dẫn đến file ảnh
        logo = logo.subsample(2, 2)  # Tỷ lệ giảm kích thước, 2 là tỷ lệ chia
        logo_label = tk.Label(menu_tab, image=logo)
        logo_label.image = logo  # Lưu tham chiếu để tránh bị xóa bởi garbage collector
        logo_label.pack(pady=10)

        """Thiết lập nội dung của tab Menu"""
        tk.Label(menu_tab, text="Welcome to Coffee Machine", font=("Arial", 18), pady=10).pack()

        tk.Label(menu_tab, text="Menu", font=("Arial", 14), pady=10).pack()

        buttons_frame = tk.Frame(menu_tab)
        buttons_frame.pack(pady=20)

        # Danh sách các loại đồ uống
        for drink in ["Latte", "Espresso", "Cappuccino"]:
            btn = tk.Button(buttons_frame, text=drink, font=("Arial", 12, "bold"), width=20, height=2, bg="lightblue",
                            fg="white", command=lambda d=drink: make_coffee(d))

            # Thêm hiệu ứng hover
            btn.bind("<Enter>", lambda event, button=btn: on_hover(event, button))
            btn.bind("<Leave>", lambda event, button=btn: on_leave(event, button))

            btn.pack(pady=10)

        action_frame = tk.Frame(menu_tab)
        action_frame.pack(pady=20)

        # Nút "View Report"
        tk.Button(action_frame, text="View Report", font=("Arial", 12, "bold"), bg="blue", fg="white", width=20,
                  height=2, command=view_report).grid(row=0, column=0, padx=10)

        # Nút "Refill Resources"
        tk.Button(action_frame, text="Refill Resources", font=("Arial", 12, "bold"), bg="orange", fg="white", width=20,
                  height=2, command=refill_resources).grid(row=0, column=1, padx=10)

    # Tạo cửa sổ Tkinter
    root = tk.Tk()
    root.title("Coffee Machine")
    root.state('zoomed')  # Toàn màn hình (Windows)

    notebook = ttk.Notebook(root)
    notebook.pack(fill='both', expand=True)


    menu_tab = tk.Frame(notebook)
    notebook.add(menu_tab, text="Menu")


    payment_tab = tk.Frame(notebook)
    notebook.add(payment_tab, text="Payment")

    notebook.select(menu_tab)
    play_music()
    # Nút tắt nhạc
    stop_button = tk.Button(root, text="Stop Music", command=stop_music, font=("Arial", 16), bg="red", fg="white")
    stop_button.pack(pady=20)
    # Gọi hàm thiết lập nội dung cho menu_tab
    setup_menu_tab()

    root.mainloop()
