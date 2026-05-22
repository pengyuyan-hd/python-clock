import tkinter as tk
import math
from time import strftime, localtime
from datetime import datetime


class AnalogClock:
    def __init__(self, root):
        self.root = root
        self.root.title("动态时钟")
        self.root.resizable(False, False)
        self.root.configure(bg="#1a1a2e")

        self.size = 400
        self.center = self.size // 2
        self.radius = self.size // 2 - 20

        self.canvas = tk.Canvas(
            root, width=self.size, height=self.size,
            bg="#1a1a2e", highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=(20, 0))

        self.digital_label = tk.Label(
            root, font=("Consolas", 28, "bold"),
            fg="#e94560", bg="#1a1a2e"
        )
        self.digital_label.pack(pady=(10, 5))

        self.date_label = tk.Label(
            root, font=("Microsoft YaHei", 12),
            fg="#8888aa", bg="#1a1a2e"
        )
        self.date_label.pack(pady=(0, 20))

        self.hands: dict[str, int | None] = {"hour": None, "minute": None, "second": None, "center": None}
        self.tick_ids: list[int] = []

        self.draw_face()
        self.update()

    def draw_face(self):
        r = self.radius
        cx = cy = self.center

        # Outer ring
        self.canvas.create_oval(
            cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8,
            outline="#e94560", width=3
        )
        self.canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r,
            outline="#0f3460", width=2
        )

        # Hour markers and numbers
        for i in range(12):
            angle = math.radians(i * 30 - 90)
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)

            # Tick marks
            inner_r = r - 10
            outer_r = r - 25
            if i % 3 == 0:
                inner_r = r - 8
                outer_r = r - 30

            x1 = cx + inner_r * cos_a
            y1 = cy + inner_r * sin_a
            x2 = cx + outer_r * cos_a
            y2 = cy + outer_r * sin_a
            tid = self.canvas.create_line(x1, y1, x2, y2, fill="#e94560", width=2 if i % 3 == 0 else 1)
            self.tick_ids.append(tid)

            # Numbers
            num_r = r - 45
            nx = cx + num_r * cos_a
            ny = cy + num_r * sin_a
            num = 12 if i == 0 else i
            self.canvas.create_text(
                nx, ny, text=str(num),
                fill="#ffffff", font=("Consolas", 16, "bold")
            )

        # Minute ticks
        for i in range(60):
            if i % 5 == 0:
                continue
            angle = math.radians(i * 6 - 90)
            x1 = cx + (r - 10) * math.cos(angle)
            y1 = cy + (r - 10) * math.sin(angle)
            x2 = cx + (r - 16) * math.cos(angle)
            y2 = cy + (r - 16) * math.sin(angle)
            tid = self.canvas.create_line(x1, y1, x2, y2, fill="#555577", width=1)
            self.tick_ids.append(tid)

    def draw_hand(self, angle, length, width, color, tag):
        cx, cy = self.center, self.center
        rad = math.radians(angle - 90)
        x = cx + length * math.cos(rad)
        y = cy + length * math.sin(rad)

        if self.hands.get(tag):
            self.canvas.delete(self.hands[tag])

        hid = self.canvas.create_line(cx, cy, x, y, fill=color, width=width, capstyle=tk.ROUND, tags=tag)
        self.hands[tag] = hid

    def update(self):
        now = datetime.now()
        h = now.hour % 12
        m = now.minute
        s = now.second
        ms = now.microsecond / 1_000_000

        # Angles with smooth second hand
        sec_angle = (s + ms) * 6
        min_angle = m * 6 + (s + ms) / 10
        hour_angle = h * 30 + m / 2 + s / 120

        self.draw_hand(hour_angle, self.radius * 0.48, 6, "#e94560", "hour")
        self.draw_hand(min_angle, self.radius * 0.72, 4, "#16c79a", "minute")
        self.draw_hand(sec_angle, self.radius * 0.82, 1.5, "#ffffff", "second")

        # Center dot
        cx, cy = self.center, self.center
        if self.hands.get("center"):
            self.canvas.delete(self.hands["center"])
        dot = self.canvas.create_oval(
            cx - 6, cy - 6, cx + 6, cy + 6,
            fill="#e94560", outline="#ffffff", width=2
        )
        self.hands["center"] = dot

        # Digital display
        time_str = now.strftime("%H:%M:%S")
        self.digital_label.config(text=time_str)

        # Date display (Chinese)
        weekdays = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
        wd = weekdays[now.weekday()]
        date_str = now.strftime(f"%Y年%m月%d日 {wd}")
        self.date_label.config(text=date_str)

        self.root.after(50, self.update)


if __name__ == "__main__":
    root = tk.Tk()
    AnalogClock(root)
    root.mainloop()
