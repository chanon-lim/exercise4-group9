# INIAD Forum
Google Authenticationなどの認証を利用したフォーラムWebアプリ

https://iniad-forum.onrender.com

![image](https://github.com/chanon-lim/exercise4-group9/assets/85671768/86146f54-8971-4dd9-b1eb-f18c53c5e6e5)


# Installation

必要なライブラリをインストールしてください
```bash
source venv/bin/activate
pip install -r requirements.txt
```
　

その後、DjangoのSECRET_KEY変数を.envに移動してください
1. .envファイルをルートディレクトリーに作成する
2. .envファイルに
```
SECRET_KEY = 'ここにSECRET_KEYの値を入力する'
```
3. 以下のコマンドを実行
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
