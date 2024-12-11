### Python Installation

Install Python dependencies using Poetry:

```sh
poetry install
```

Activate the virtual environment:

```sh
source .venv/bin/activate
```

## もし.venvがでなかったら
```sh
poetry config --local virtualenvs.in-project true
poetry env remove python
poetry install  
```


## Run Application
```
python src/owl/main.py
```

## 文字化けが発生する場合
# ロケールを: ja_JP.UTF-8に設定
```
export LANG=ja_JP.UTF-8
```
# フォントがインストールされているか確認
```
fc-list | grep "Noto"
sudo apt update
sudo apt install fonts-noto-cjk
```

## 日本語文字が入力できない場合
# IMEの設定
```
sudo apt update
sudo apt install -y ibus ibus-mozc
```

# ibus-daemonを再起動して変更を反映
```
ibus-daemon -drx
```
# 入力メソッドの設定
```
ibus-daemon -drx
or
ibus-setup
```
2 「入力メソッド」タブで「日本語（Mozc）」を選択して追加