import tkinter as tk
from PIL import Image, ImageDraw, ImageFont, ImageTk
from pathlib import Path
import random

# 仮想の町設定
TOWN_INFO = {
    "地区1": {"住民": 200},
    "地区2": {"住民": 50},
}

font_path = Path(__file__).parent.parent / "NotoSansJP-Regular.otf"


# 情報を追加する関数
def information_provider():
    # 新しい情報を追加
    provided_info.append("警報: 大雨による避難勧告が発令されました。")
    provided_info.append("情報: 避難所1が開設されました。")

def available_deliver_way(employees_at_city_hall, usable_tels, phone_lines_available, usable_cars, usable_smartphones, smartphones_available, usable_pcs, pcs_available, internet_available):
    deliver_way = []

    if employees_at_city_hall > 0:
        deliver_way.append("足")

        if ( usable_tels >0 or usable_smartphones >0 )and phone_lines_available > 0:
            deliver_way.append("電話")

        if usable_cars > 0:
            deliver_way.append("車")

        if usable_smartphones >0 and internet_available and smartphones_available > 0:
            deliver_way.append("LINE")

        if usable_pcs >0 and internet_available and pcs_available > 0:
            deliver_way.append("ネット掲示板")

    return deliver_way

# # Example usage:
# available_methods = available_deliver_way(
#     employees_at_city_hall=5,
#     phone_lines_available=3,
#     usable_cars=2,
#     smartphones_available=1,
#     pcs_available=0,
#     internet_available=True
# )
# print(available_methods)

def available_imformation_destination():
    # 伝達可能な伝達先を記述
    # 伝達が可能なのは警察, 消防, 国・県, 避難所, 物資供給班, 土木班, 住民, ライフライン業者
    # 各伝達先に対して、事前に了解を結んでいるすべての伝達方法の情報も記述
    print(f"現在のリソース: {resources}")

delivery_data = {
    "警察1-A": {"足": (15, 3, 10, 20), "車": (6, 2, 3, 10)},
    "警察1-B": {"足": (30, 10, 15, 45), "車": (10, 3, 5, 15)},
    "警察1-C": {"足": (22.5, 4.5, 15, 30), "車": (12.5, 2.5, 10, 15)},
    "警察2-A": {"足": (30, 7.5, 20, 50), "車": (17.5, 4.5, 10, 25)},
    "消防1-A": {"足": (22.5, 4.5, 15, 30), "車": (10, 2.5, 5, 15)},
    "消防1-B": {"足": (7.5, 1.5, 5, 10), "車": (4, 1, 3, 5)},
    "避難所1-A": {"足": (22.5, 4.5, 15, 30), "車": (10, 2.5, 5, 15)},
    "避難所1-B": {"足": (7.5, 1.5, 5, 10), "車": (4, 1, 3, 5)},
    "避難所1-C": {"足": (22.5, 4.5, 15, 30), "車": (10, 2.5, 5, 15)},
    "避難所1-D": {"足": (30, 10, 15, 45), "車": (10, 2.5, 5, 15)},
    "避難所2-A": {"足": (35, 7.5, 20, 50), "車": (17.5, 4.5, 10, 25)},
    "避難所2-B": {"足": (35, 7.5, 20, 50), "車": (17.5, 4.5, 10, 25)},
}

# 配達時間を計算する共通関数
def calculate_time(mean, stddev, min_time, max_time):
    time = random.gauss(mean, stddev)
    return max(min_time, min(max_time, time))

# 配達時間を計算するメイン関数
def calculate_delivering_time(destination, deliver_way):
    if deliver_way in ["電話", "ネット掲示板", "LINE"]:
        return 0  # 配達不要
    if destination in delivery_data and deliver_way in delivery_data[destination]:
        mean, stddev, min_time, max_time = delivery_data[destination][deliver_way]
        return calculate_time(mean, stddev, min_time, max_time)
    return 999  # 不明な場合

# # 使用例
# print(calculate_delivering_time("警察1-A", "足"))
# print(calculate_delivering_time("避難所2-B", "車"))
# print(calculate_delivering_time("不明な場所", "足"))

    
def calculate_notice_time(deliver_way):
    if deliver_way in ["足", "車", "電話"]:
        notice_time = random.gauss(2, 0.5)  
        return max(1, min(3, notice_time)) 
    elif deliver_way in ["ネット掲示板", "LINE"]:
        if deliver_way == "ネット掲示板":
            notice_time = random.gauss(2, 7)
            return max(1, min(30, notice_time))  
        else:
            notice_time = random.gauss(2, 2)
            return max(1, min(30, notice_time))  
    else:
        return 999

def calculate_delivering_prepare_time(deliver_way):
    if deliver_way == "足":
        prepare_time = 0 
        return prepare_time    
    if deliver_way == "車":
        prepare_time = 3
        return prepare_time 
    if deliver_way == "電話":
        prepare_time = 1   
    if deliver_way == "LINE":
        prepare_time = random.gauss(1, 0.5)
        return max(1, min(3, prepare_time))     
    if deliver_way == "ネット掲示板":
        prepare_time = random.gauss(2, 0.5)
        return max(1, min(3, prepare_time))      
    else:
        return 999
    
# 配送手段ごとのリソース割り当てデータ
resource_data = {
    "足": {
        "human_resource": 1,
        "car_resource": 0,
        "tel_resource": 0,
        "smart_phone_resource": 0,
        "PC_resource": 0,
    },
    "車": {
        "human_resource": 1,
        "car_resource": 1,
        "tel_resource": 0,
        "smart_phone_resource": 0,
        "PC_resource": 0,
    },
    "電話": {
        "human_resource": 1,
        "car_resource": 0,
        "tel_resource": 1,
        "smart_phone_resource": 0,
        "PC_resource": 0,
    },
    "LINE": {
        "human_resource": 1,
        "car_resource": 0,
        "tel_resource": 0,
        "smart_phone_resource": 1,
        "PC_resource": 0,
    },
    "ネット掲示板": {
        "human_resource": 1,
        "car_resource": 0,
        "tel_resource": 0,
        "smart_phone_resource": 0,
        "PC_resource": 1,
    },
}

# 配送手段に応じたリソースを取得する関数
def deliver_resource(deliver_way):
    default_resource = {
        "human_resource": 999,
        "car_resource": 999,
        "tel_resource": 999,
        "smart_phone_resource": 999,
        "PC_resource": 999,
    }
    return resource_data.get(deliver_way, default_resource)

# # 使用例
# print(deliver_resource("足"))  # 正常ケース
# print(deliver_resource("車"))  # 正常ケース
# print(deliver_resource("不明な手段"))  # 未知のケース

###################################################


resources = {
    "職員": 10,
    "車": 3,
    "スピーカー": 1,
    "電話": 3,
    "スマホ": 10,
    "PC": 10,
}

# 情報を追加する関数
def information_provider():
    provided_info.append("警報: 大雨による避難勧告が発令されました。")
    provided_info.append("情報: 避難所1が開設されました。")


# メインアプリケーションクラス
time_elapsed = 0
tel_communication_restored = False
internet_communication_restored = False
provided_info = []
sent_history = []

class DisasterGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("市役所防災ゲーム")
        self.root.geometry("600x600")

        self.time_elapsed = 0  # タイマーの初期値

        # フォントを設定
        font_path = Path(__file__).parent.parent  / "NotoSansJP-Regular.otf"
        try:
            self.japanese_font = ImageFont.truetype(str(font_path), 16)
        except IOError:
            print(f"フォントが見つからないため、デフォルトフォントを使用します。")
            self.japanese_font = ImageFont.truetype("arial.ttf", 16)

        self.setup_ui()
        self.update_timer()

    def setup_ui(self):
        # リソースパネル
        self.resource_label = tk.Label(self.root, bg="lightblue", anchor="w")
        self.resource_label.pack(fill="x", padx=10, pady=5)

        # タイマーパネル
        self.timer_label = tk.Label(self.root, bg="lightgray", anchor="w")
        self.timer_label.pack(fill="x", padx=10, pady=5)

        # 情報ログ
        self.info_frame = tk.Frame(self.root, bg="lightgreen", padx=5, pady=5)
        self.info_frame.pack(fill="x", padx=10, pady=5)

        self.info_canvas = tk.Canvas(self.info_frame, height=100, bg="lightgreen", highlightthickness=0)
        self.info_canvas.pack(fill="both", expand=True)

        # 入力パネル
        self.interaction_frame = tk.Frame(self.root, bg="lightyellow", padx=5, pady=5)
        self.interaction_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(self.interaction_frame, text="伝達先:", bg="lightyellow").grid(row=0, column=0, sticky="w")
        self.target_entry = tk.Entry(self.interaction_frame, font=("Noto Sans JP", 12))
        self.target_entry.grid(row=0, column=1, sticky="ew", padx=5)

        tk.Label(self.interaction_frame, text="伝達手段:", bg="lightyellow").grid(row=1, column=0, sticky="w")
        self.method_entry = tk.Entry(self.interaction_frame, font=("Noto Sans JP", 12))
        self.method_entry.grid(row=1, column=1, sticky="ew", padx=5)

        tk.Label(self.interaction_frame, text="伝達内容:", bg="lightyellow").grid(row=2, column=0, sticky="w")
        self.content_entry = tk.Entry(self.interaction_frame, font=("Noto Sans JP", 12))
        self.content_entry.grid(row=2, column=1, sticky="ew", padx=5)

        self.send_button = tk.Button(self.interaction_frame, text="送信", command=self.send_message)
        self.send_button.grid(row=3, column=1, sticky="e", pady=5)        

        # 送信履歴
        self.history_frame = tk.Frame(self.root, bg="lightgray", padx=5, pady=5)
        self.history_frame.pack(fill="x", padx=10, pady=5)

        self.history_canvas = tk.Canvas(self.history_frame, height=100, bg="lightgray", highlightthickness=0)
        self.history_canvas.pack(fill="both", expand=True)

    def render_text_with_pillow(self, canvas, text, font, bg_color):
        # Pillowで描画
        width, height = 600, 100
        image = Image.new("RGB", (width, height), bg_color)
        draw = ImageDraw.Draw(image)
        draw.text((10, 10), text, font=font, fill="black")

        # Tkinterで表示
        photo_image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, anchor="nw", image=photo_image)
        canvas.image = photo_image  # メモリ保持

    def update_ui(self):
        # リソースパネル
        resource_text = f"職員: {resources['職員']} | 車: {resources['車']} | 電話: {resources['電話']} | スマホ: {resources['スマホ']} | PC: {resources['PC']}"
        print(resource_text)
        self.resource_label.config(
            text=resource_text,
            font=("Noto Sans JP", 12)
            )

        # タイマーパネル
        timer_text = f"経過時間: {self.time_elapsed} 秒"
        self.timer_label.config(text=timer_text)

        # 情報ログ
        info_text = "\n".join(provided_info[-5:])
        self.render_text_with_pillow(self.info_canvas, info_text, self.japanese_font, "lightgreen")

        # 送信履歴
        history_text = "\n".join(sent_history[-5:])
        self.render_text_with_pillow(self.history_canvas, history_text, self.japanese_font, "lightgray")

    def update_timer(self):
        self.time_elapsed += 1
        if self.time_elapsed % 5 == 0:
            information_provider()
        self.update_ui()
        self.root.after(1000, self.update_timer)

    def send_message(self):
        target = self.target_entry.get()
        method = self.method_entry.get()
        content = self.content_entry.get()
        if target and method and content:
            sent_message = f"伝達先: {target}, 伝達手段: {method}, 伝達内容: {content}"
            sent_history.append(sent_message)
            provided_info.append(sent_message)
            self.target_entry.delete(0, tk.END)
            self.method_entry.delete(0, tk.END)
            self.content_entry.delete(0, tk.END)
        self.update_ui()


if __name__ == "__main__":
    root = tk.Tk()
    app = DisasterGameApp(root)
    root.mainloop()
