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

##### 2-1. Appの追加
Slack Appの[追加ページ](https://api.slack.com/apps?new_app=1)にアクセスします。

`App Name` にアプリの名前を記入し、`Development Slack Workspace`にjvn-botを追加する  
ワークスペースを選択した後、`Create App`と表示されているボタンをクリックします。

##### 2-2. Slashコマンドの追加
`Create App`ボタンをクリックすると、`Basic Information`にジャンプされます。  
そのページの、`Slash Commands`ボタンをクリックします。

<img src="https://i.imgur.com/8H6EmAW.png" width="400px"/>

その後、スラッシュコマンド一覧が現れるので、`Create New Command` をクリックします。

<img src="https://i.imgur.com/0nRy6Dd.png" width="400px"/>

コマンド、サーバのURL、説明等を記入し、`Save`ボタンをクリックします。  
登録が必要なスラッシュコマンドは以下の通りです。

`server.example.com`は自身のサーバのアドレスに変更してください。

| Command | Request URL                      | 
|:-------:|:---------------------------------| 
| add  |  https://server.example.com/add   | 
| info |  https://server.example.com/info  | 
| del  |  https://server.example.com/del   | 

<img src="https://i.imgur.com/JSDYPc7.png" width="700px"/>

### 2-3. Botの追加

画面左にある、`Bot Users`をクリックし、`Add Bot User`をクリック。

<img src="https://i.imgur.com/tKcPvb0.png" width="200px"/>
<img src="https://i.imgur.com/8Nt0uqR.png" width="400px"/>

さらにジャンプするので、その先でも`Add Bot User`をクリックします。
<img src="https://i.imgur.com/uQJ62Dc.png" width="400px"/>

### 2-3. 認証情報の取得

画面左にある、`Basic Information`をクリックします。

<img src="https://i.imgur.com/tKcPvb0.png" width="200px"/>


### 3. 設定の作成
`src/settings.py`を作成し、以下の内容を書き込む。

```py
SLASH_CMD_TOKEN = '<SLACK VERIFICATION TOKEN>'
CLIENT_TOKEN = '<BOT USER OAUTH ACCESS TOKEN>'
ALERT_CHANNEL = '<CHANNEL USING WHEN THIS SERVICE CRASHED>'
```

## 起動

```sh
cd src
sh run.sh
```
