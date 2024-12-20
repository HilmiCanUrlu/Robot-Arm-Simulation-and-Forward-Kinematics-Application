import math
import tkinter as tk
from tkinter import messagebox
from tkinter.colorchooser import askcolor
import time

def calculate_angles_and_draw(target_x, target_y):
    try:
        # Kullanıcıdan alınan uzunluklar
        L1 = length_slider_L1.get()
        L2 = length_slider_L2.get()

        # Uygunluk kontrolü
        distance = math.sqrt(target_x**2 + target_y**2)
        if distance > (L1 + L2) or distance < abs(L1 - L2):
            messagebox.showerror("Hata", "Hedef noktaya ulaşmak mümkün değil. Kol uzunluklarını veya hedef konumunu kontrol edin.")
            return

        # İleri kinematik hesaplama
        r = (target_x**2 + target_y**2 - L1**2 - L2**2) / (2 * L1 * L2)
        theta2 = math.acos(r)
        k1 = L1 + L2 * math.cos(theta2)
        k2 = L2 * math.sin(theta2)
        theta1 = math.atan2(target_y, target_x) - math.atan2(k2, k1)

        # Sonuçları göster
        result_label.config(text=f"Theta1: {math.degrees(theta1):.2f}°\nTheta2: {math.degrees(theta2):.2f}°")

        # Hedef uzaklık göstergesi
        distance_label.config(text=f"Hedef Uzaklığı: {distance:.2f}")

        # Robot kolu çiz
        animate_robot_arm(L1, L2, theta1, theta2, target_x, target_y)

    except ValueError:
        messagebox.showerror("Hata", "Lütfen geçerli değerler girin.")

def draw_robot_arm(L1, L2, theta1, theta2, target_x, target_y):
    # Canvas temizle
    canvas.delete("all")

    # Eksenleri çiz
    center_x = 300  # Center of the canvas
    center_y = 300  # Center of the canvas
    scale = scale_slider.get()

    # X ve Y eksenlerini çiz
    canvas.create_line(0, center_y, 600, center_y, fill="gray", dash=(2, 2))  # X ekseni
    canvas.create_line(center_x, 0, center_x, 600, fill="gray", dash=(2, 2))  # Y ekseni

    # Eksen üzerinde gösterilecek sayıları çiz
    for i in range(0, 600, 50):
        canvas.create_text(i, center_y + 10, text=f"{(i - center_x) / scale:.0f}", fill="black", font=("Arial", 8))
        canvas.create_text(center_x + 10, i, text=f"{(center_y - i) / scale:.0f}", fill="black", font=("Arial", 8))

    # İlk bağlantı ucu (0, 0)'dan itibaren çiz
    x1 = L1 * math.cos(theta1)
    y1 = L1 * math.sin(theta1)

    # İkinci bağlantı ucu
    x2 = x1 + L2 * math.cos(theta1 + theta2)
    y2 = y1 + L2 * math.sin(theta1 + theta2)

    # Başlangıç ve ölçekli koordinatlar
    start_x = center_x
    start_y = center_y

    joint_x1 = center_x + x1 * scale
    joint_y1 = center_y - y1 * scale

    end_x = center_x + x2 * scale
    end_y = center_y - y2 * scale

    # Kolun ilk parçasını çiz
    canvas.create_line(start_x, start_y, joint_x1, joint_y1, fill=arm1_color.get(), width=4)

    # Kolun ikinci parçasını çiz
    canvas.create_line(joint_x1, joint_y1, end_x, end_y, fill=arm2_color.get(), width=4)

    # Eklem noktalarını göster
    canvas.create_oval(joint_x1 - 3, joint_y1 - 3, joint_x1 + 3, joint_y1 + 3, fill="black")
    canvas.create_oval(end_x - 3, end_y - 3, end_x + 3, end_y + 3, fill="black")

    # Hedef noktayı göster
    target_x_canvas = center_x + target_x * scale
    target_y_canvas = center_y - target_y * scale
    canvas.create_oval(target_x_canvas - 3, target_y_canvas - 3, target_x_canvas + 3, target_y_canvas + 3, outline="green", width=2)
    canvas.create_text(target_x_canvas + 10, target_y_canvas, text="Hedef", fill="green", font=("Arial", 10, "bold"))
    
    
  # Sonuçları göster
    result_label.config(text=f"Theta1: {math.degrees(theta1):.2f}°\nTheta2: {math.degrees(theta2):.2f}°")
    
    # Kolun menzilini göster (Yeşil çember)
    max_reach = L1 + L2
    canvas.create_oval(center_x - max_reach * scale, center_y - max_reach * scale,
                       center_x + max_reach * scale, center_y + max_reach * scale,
                       outline="green", width=2, dash=(4, 4))  # Menzil çemberi (yeşil, kesikli çizgi)


def animate_robot_arm(L1, L2, theta1, theta2, target_x, target_y):
    steps = 20
    for i in range(1, steps + 1):
        interim_theta1 = theta1 * i / steps
        interim_theta2 = theta2 * i / steps
        draw_robot_arm(L1, L2, interim_theta1, interim_theta2, target_x, target_y)
        root.update()
        time.sleep(1 / speed_slider.get())  # Speed control
    draw_robot_arm(L1, L2, theta1, theta2, target_x, target_y)

def on_canvas_click(event):
    center_x = 300
    center_y = 300
    scale = scale_slider.get()
    target_x = (event.x - center_x) / scale
    target_y = (center_y - event.y) / scale
    target_label.config(text=f"Hedef: ({target_x:.2f}, {target_y:.2f})")
    manual_target_x.set(f"{target_x:.2f}")
    manual_target_y.set(f"{target_y:.2f}")
    calculate_angles_and_draw(target_x, target_y)

def apply_manual_target():
    try:
        target_x = float(manual_target_x.get())
        target_y = float(manual_target_y.get())
        calculate_angles_and_draw(target_x, target_y)
    except ValueError:
        messagebox.showerror("Hata", "Geçerli bir hedef konumu girin.")

def reset_simulation():
    length_slider_L1.set(10)
    length_slider_L2.set(10)
    manual_target_x.set("0.00")
    manual_target_y.set("0.00")
    result_label.config(text="Sonuç: -")
    distance_label.config(text="Hedef Uzaklığı: 0.00")
    canvas.delete("all")

def choose_arm1_color():
    color_code = askcolor(title="Kol 1 Rengi Seç")[1]
    if color_code:
        arm1_color.set(color_code)

def choose_arm2_color():
    color_code = askcolor(title="Kol 2 Rengi Seç")[1]
    if color_code:
        arm2_color.set(color_code)

# Tkinter ana pencere oluşturma
root = tk.Tk()
root.title("Robot Kol Simülasyonu")
root.geometry("1000x600")  # Pencere boyutunu biraz daha büyük yapalım

# PanedWindow oluşturma (solda kayar menü, sağda simülasyon alanı)
paned_window = tk.PanedWindow(root, orient="horizontal")
paned_window.pack(fill=tk.BOTH, expand=True)

# Sol panel (ayarlar)
left_panel = tk.Frame(paned_window, width=250, bg="#f4f4f9", relief="solid", borderwidth=2)
left_panel.pack_propagate(False)  # Bu panel boyutlandırmayı içerik üzerine yapmasın
paned_window.add(left_panel)

# Sağ panel (simülasyon)
right_panel = tk.Frame(paned_window, bg="white")
right_panel.pack(fill=tk.BOTH, expand=True)
paned_window.add(right_panel)

# Başlık
tk.Label(left_panel, text="Robot Kol Simülasyonu", font=("Arial", 16, "bold"), bg="#f4f4f9").pack(pady=10)

# Kol uzunluğu kaydırıcıları
tk.Label(left_panel, text="Kol Uzunluğu L1:", font=("Arial", 10), bg="#f4f4f9").pack()
length_slider_L1 = tk.Scale(left_panel, from_=1, to=100, orient="horizontal")
length_slider_L1.set(10)
length_slider_L1.pack(pady=5)

tk.Label(left_panel, text="Kol Uzunluğu L2:", font=("Arial", 10), bg="#f4f4f9").pack()
length_slider_L2 = tk.Scale(left_panel, from_=1, to=100, orient="horizontal")
length_slider_L2.set(10)
length_slider_L2.pack(pady=5)

# Çizim ölçeği kaydırıcısı
tk.Label(left_panel, text="Çizim Ölçeği:", font=("Arial", 10), bg="#f4f4f9").pack()
scale_slider = tk.Scale(left_panel, from_=1, to=50, orient="horizontal")
scale_slider.set(5)
scale_slider.pack(pady=5)

# Animasyon hızı kaydırıcısı
tk.Label(left_panel, text="Animasyon Hızı:", font=("Arial", 10), bg="#f4f4f9").pack()
speed_slider = tk.Scale(left_panel, from_=1, to=100, orient="horizontal")
speed_slider.set(50)
speed_slider.pack(pady=5)

# Renk seçim butonları
arm1_color = tk.StringVar(value="#0000FF")  # Başlangıçta mavi
arm2_color = tk.StringVar(value="#FF0000")  # Başlangıçta kırmızı

tk.Button(left_panel, text="Kol 1 Rengini Seç", command=choose_arm1_color).pack(pady=5)
tk.Button(left_panel, text="Kol 2 Rengini Seç", command=choose_arm2_color).pack(pady=5)

# Hedef koordinatları manuel girme
tk.Label(left_panel, text="Manuel Hedef Koordinatları:", font=("Arial", 10), bg="#f4f4f9").pack(pady=5)
manual_target_x = tk.StringVar(value="0.00")
tk.Entry(left_panel, textvariable=manual_target_x).pack(pady=5)

manual_target_y = tk.StringVar(value="0.00")
tk.Entry(left_panel, textvariable=manual_target_y).pack(pady=5)

tk.Button(left_panel, text="Hedefi Uygula", command=apply_manual_target).pack(pady=5)

# Reset butonu
tk.Button(left_panel, text="Simülasyonu Sıfırla", command=reset_simulation).pack(pady=5)

# Sonuç ve mesafe etiketleri
result_label = tk.Label(left_panel, text="Sonuç: -", font=("Arial", 12), bg="#f4f4f9")
result_label.pack(pady=5)

distance_label = tk.Label(left_panel, text="Hedef Uzaklığı: 0.00", font=("Arial", 12), bg="#f4f4f9")
distance_label.pack(pady=5)

# Hedef etiket
target_label = tk.Label(left_panel, text="Hedef: (0.00, 0.00)", font=("Arial", 10), bg="#f4f4f9")
target_label.pack(pady=5)

# Canvas (robot kolunun çizileceği alan)
canvas = tk.Canvas(right_panel, width=600, height=600, bg="white")
canvas.pack()

canvas.bind("<Button-1>", on_canvas_click)

root.mainloop()
