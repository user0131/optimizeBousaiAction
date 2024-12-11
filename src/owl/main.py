import pygame
import random
import sys
from pathlib import Path
# 仮想の町を想定
"""
町役場が１つ。地区Aと地区Bがある。地区Aと地区Bにはそれぞれ警察署と消防署が1つずつある。各地区の警察と消防のリソースは2組。
市役所は、地区Aに存在する。地区A(ふもと)には徒歩で5分、地区B(山)には徒歩で30分前後かかる。
隣町へは、10km離れている。成人であれば1時間で着く
避難所は、市役所の近くの町の中心部に１つある。

地区Aには50人(内未成年8人、成人30人、老人12人)、地区Bには10人(子供1人、老人9人)の住民が住んでいる。

夕方、5時に震度7の地震が発生。役場は勤務が終わるタイミングだった。幸い1人も負傷者はいない。
役場には、移動のための広報車が1つ、人数は5人、電話・LINEは通じない状況。
住民への広報をするためのスピーカーが１つある。


目的は、住民の被害を最小限に食い止めること。
あなたは、市役所で、情報を収集させたり、外部へ連絡させたり広報させたりする人。

(
隠しイベント:
発生する2次災害:地区Ｂでの土砂崩れ(1時間後)
1時間半後に修理業者が来て電話・LINEが通じるようになる。外部への連絡も可能
住民・警察・消防からの連絡は多数（避難、負傷者等）

)

メインクエスト:
情報収集
住民への対応・広報・負傷者指示・避難指示
(可能であれば)外部への連絡
"""



# フォントファイルのパスを指定
font_path = Path(__file__).parent.parent / "NotoSansJP-Regular.otf"

# Pygame を初期化
pygame.init()

# 画面設定
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("町役場防災ゲーム")
clock = pygame.time.Clock()

# 色設定
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (200, 200, 200)


# フォント読み込み
font = pygame.font.Font(str(font_path), 36)
button_font = pygame.font.Font(str(font_path), 24)  # ボタン用フォントを小さめに

# リソース設定
resources = {
    "職員": 5,
    "広報車": 1,
    "スピーカー": 1
}

time_elapsed = 0

def draw_background():
    """役場の一室を描画"""
    screen.fill(GRAY)

    # 部屋の枠
    pygame.draw.rect(screen, WHITE, (50, 50, 700, 500))

    # 各リソースの表示
    resources_text = font.render(f"職員: {resources['職員']} | 広報車: {resources['広報車']} | スピーカー: {resources['スピーカー']}", True, BLACK)
    screen.blit(resources_text, (60, 20))

    # 時間の表示
    global time_elapsed
    time_text = font.render(f"時間: {time_elapsed // 60}分", True, BLACK)
    screen.blit(time_text, (600, 20))

def draw_buttons():
    """アクションボタンの描画"""
    # ボタン: 情報収集
    pygame.draw.rect(screen, BLACK, (100, 500, 150, 50))
    collect_info_text = button_font.render("情報収集", True, WHITE)
    screen.blit(collect_info_text, (110, 515))

    # ボタン: 広報車で避難指示
    pygame.draw.rect(screen, BLACK, (300, 500, 200, 50))
    use_car_text = button_font.render("広報車で避難", True, WHITE)
    screen.blit(use_car_text, (310, 515))

    # ボタン: スピーカーで避難指示
    pygame.draw.rect(screen, BLACK, (550, 500, 200, 50))
    use_speaker_text = button_font.render("スピーカーで避難", True, WHITE)
    screen.blit(use_speaker_text, (560, 515))


def handle_click(x, y):
    """クリックイベントの処理"""
    global resources

    if 100 <= x <= 250 and 500 <= y <= 550:
        if resources["職員"] > 0:
            resources["職員"] -= 1
            print("情報収集を実施しました。")
        else:
            print("職員が足りません。")

    elif 300 <= x <= 500 and 500 <= y <= 550:
        if resources["広報車"] > 0:
            resources["広報車"] -= 1
            print("広報車で避難指示を行いました。")
        else:
            print("広報車が利用できません。")

    elif 550 <= x <= 750 and 500 <= y <= 550:
        if resources["スピーカー"] > 0:
            resources["スピーカー"] -= 1
            print("スピーカーで避難指示を行いました。")
        else:
            print("スピーカーが利用できません。")

# メインゲームループ
running = True
while running:
    delta_time = clock.tick(30) / 1000  # フレーム間の経過時間を秒単位で計算
    time_elapsed += delta_time * 180  # 3倍速で進行

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            handle_click(x, y)

    # 背景とUIの描画
    draw_background()
    draw_buttons()

    # 画面更新
    pygame.display.flip()

pygame.quit()
sys.exit()
