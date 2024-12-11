from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# テスト用のフォントパスとテキスト
font_path = Path(__file__).parent.parent / "NotoSansJP-Regular.otf"
text_to_draw = "警報: 大雨による避難勧告が発令されました。"

# Pillowでのテキスト描画テスト
image = Image.new("RGB", (600, 100), (255, 255, 255))  # 白背景
draw = ImageDraw.Draw(image)

try:
    # フォントを読み込む (Pathオブジェクトをstrに変換)
    font = ImageFont.truetype(str(font_path), 16)

    # テキストを描画
    draw.text((10, 10), text_to_draw, font=font, fill="black")
    print("描画成功: テキストが正しく描画されました。")

except FileNotFoundError:
    print(f"フォントファイルが見つかりません: {font_path}")

except OSError as e:
    print(f"フォント読み込みエラー: {e}")

except Exception as e:
    print(f"描画エラー: {e}")