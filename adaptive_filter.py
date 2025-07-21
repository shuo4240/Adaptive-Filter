import flet as ft
import numpy as np
import matplotlib.pyplot as plt
import padasip as pa
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def main(page: ft.Page):
    
    page.window_width = 600
    page.window_height = 900

    coeff_fields = []

    # 根據 n 產生係數欄位
    def generate_coeff_fields(n):
        coeff_fields.clear()
        for i in range(n):
            coeff_fields.append(
                # 隨機設置參數，介於-2~2間
                ft.TextField(label=f"Coefficient {i+1}", width=150, value=str(np.round(np.random.uniform(-2, 2), 2))) 
            )

    def refresh_page():
        page.controls.clear()
        page.add(
            select_filter,
            n_field,
            mu_field,
            update_coeffs_btn,
            *coeff_fields,
            slider,
            ft.Row([
                ft.Container(content=icon_speak, width=30, height=30, bgcolor=ft.colors.BLUE, border_radius=15),
                ft.Container(content=t, width=480, height=30, bgcolor=ft.colors.WHITE),
                ft.Container(content=icon_mircophone, width=30, height=30, bgcolor=ft.colors.BLUE, border_radius=15),
            ]),
            plot_btn,
            difference_btn,
        )

    def update_coeffs(e):
        try:
            n = int(n_field.value)
            generate_coeff_fields(n)
            refresh_page()
        except ValueError:
            print("Invalid n value")

    # 選擇濾波器
    select_filter = ft.Dropdown(
        label="Adaptive Filter",
        hint_text="Choose an adaptive filter",
        options=[
            ft.dropdown.Option("LMS"),
            ft.dropdown.Option("RLS"),
            ft.dropdown.Option("NLMS"),
        ],
        autofocus=True,
        width=250,
    )

    n_field = ft.TextField(label="n (Dimension of input vector):", width=240, value="4")
    mu_field = ft.TextField(label="mu (Adaptation step size):", width=240, value="0.01")
    update_coeffs_btn = ft.FilledButton(text="Update Coefficient Fields", on_click=update_coeffs)

    generate_coeff_fields(int(n_field.value))

    # 單一濾波器模擬&繪圖
    def plot_click(e):
        n = int(n_field.value)
        mu = float(mu_field.value)

        # 500個樣本
        N = 500

        # 代表噪音
        v = np.random.normal(0, 0.1*(slider.value+1), N)

        # 隨機輸入向量
        x = np.random.normal(0, 1, (N, n))

        # 根據係數組合出目標信號 d
        coeffs = [float(c.value) for c in coeff_fields]
        d = np.dot(x, coeffs) + v

        # 根據選擇建立對應濾波器
        f = None
        if select_filter.value == "LMS":
            f = pa.filters.FilterLMS(n=n, mu=mu, w="random")
        elif select_filter.value == "RLS":
            f = pa.filters.FilterRLS(n=n, mu=mu)
        elif select_filter.value == "NLMS":
            f = pa.filters.FilterNLMS(n=n, mu=mu, w="random")

        # 執行濾波器學習
        y, e, w = f.run(d, x)

        # 顯示圖表
        root = tk.Tk()
        root.title("Filter Plot")

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7))
        ax1.set_title("Adaptation Process")
        ax1.set_xlabel("Sample Indexs")
        ax1.plot(d, "b", label="d : Target")
        ax1.plot(y, "g", label="y : Output")
        ax1.legend()

        plt.subplots_adjust(hspace=0.5)

        ax2.set_title("Filter Error")
        ax2.set_xlabel("Sample Indexs")
        ax2.plot(10 * np.log10(e ** 2), "r", label="Error (dB)")
        ax2.legend()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        root.mainloop()

    plot_btn = ft.FilledButton(text="Show Filter Plot", on_click=plot_click)

    # 三種濾波器比較並推薦最佳者
    def difference_click(e):
        n = int(n_field.value)
        mu = float(mu_field.value)

        # 500個樣本
        N = 500

        # 代表噪音
        v = np.random.normal(0, 0.1*(slider.value+1), N)

        # 隨機輸入向量
        x = np.random.normal(0, 1, (N, n))

        # 根據係數組合出目標信號 d
        coeffs = [float(c.value) for c in coeff_fields]
        d = np.dot(x, coeffs) + v

        # 建立三種濾波器
        f1 = pa.filters.FilterLMS(n=n, mu=mu, w="random")
        f2 = pa.filters.FilterRLS(n=n, mu=mu)
        f3 = pa.filters.FilterNLMS(n=n, mu=mu, w="random")

        # 執行三種濾波器
        y1, e1, _ = f1.run(d, x)
        y2, e2, _ = f2.run(d, x)
        y3, e3, _ = f3.run(d, x)

        # 計算平均誤差
        avg_error_lms = np.mean(e1 ** 2)
        avg_error_rls = np.mean(e2 ** 2)
        avg_error_nlms = np.mean(e3 ** 2)

        # 找到最小誤差的濾波器
        min_error = min(avg_error_lms, avg_error_rls, avg_error_nlms)
        if min_error == avg_error_lms:
            recommended_filter = "LMS"
        elif min_error == avg_error_rls:
            recommended_filter = "RLS"
        else:
            recommended_filter = "NLMS"

        # 顯示比較圖
        root = tk.Tk()
        root.title("Filter Comparison")

        fig, ax = plt.subplots(figsize=(10, 7))
        ax.set_title("Compare Filter Error")
        ax.set_xlabel("Sample Indexs")
        ax.plot(10 * np.log10(e1 ** 2), "r", label="LMS Error (dB)")
        ax.plot(10 * np.log10(e2 ** 2), "g", label="RLS Error (dB)")
        ax.plot(10 * np.log10(e3 ** 2), "b", label="NLMS Error (dB)")
        ax.legend()

        recommendation_label = tk.Label(root, text=f"Recommended Filter: {recommended_filter}", font=("Arial", 14))
        recommendation_label.pack()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        root.mainloop()

    difference_btn = ft.FilledButton(text="Show Three Filter Error", on_click=difference_click, style=ft.ButtonStyle(bgcolor=ft.colors.RED,))

    # 模擬聲源與接收音源的遠近
    icon_speak = ft.Draggable(group="voice", content=ft.Icon(name="RECORD_VOICE_OVER", size=20, color=ft.colors.WHITE))
    icon_mircophone = ft.Draggable(group="voice", content=ft.Icon(name="KEYBOARD_VOICE_ROUNDED", size=20, color=ft.colors.WHITE))

    def slider_change(e):
        t.value = f"The sound source is {5 - e.control.value} m away from the microphone"
        page.update()

    t = ft.Text()
    slider = ft.Slider(min=0, max=5, divisions=5, on_change=slider_change)

    refresh_page()

ft.app(target=main)
