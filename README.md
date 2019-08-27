# jvn-bot
JVN iPediaを利用して、脆弱性情報収集を行うSlackBot。

## インストール

### 1. 必要なパッケージのインストール
Ubuntu 18.04の場合、以下のコマンドでインストールできる。

```sh
sudo apt update
sudo apt upgrade

sudo apt install python3 python3-pip

git clone https://github.com/akakou/jvn-bot/
cd jvn-bot
pip3 install -r requirements.txt
```

### 2. Slack側の設定
TODO

### 3. 設定の作成
`src/settings.py`を作成し、以下の内容を書き込む。

```py
SLASH_CMD_TOKEN = '<SLACK Verification Token>'
CLIENT_TOKEN = '<BOT USER OAUTH ACCESS TOKEN>'
ALERT_CHANNEL = '<CHANNEL USING WHEN THIS SERVICE CRASHED>'
```

## 起動

```sh
cd src
sh run.sh
```