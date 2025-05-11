### ラズパイを用いたカード認識

## 使用したもの
・Google Home<br>
・ラズパイ<br>
・sony rc-s300(カードリーダー)<br>

## 概要
card_onsei.py→カード情報を読み取り、バックエンドに送り、音声を出すためのファイル<br>
cardread.py→カード情報を出力するためのファイル。(出力した情報をユーザー登録の際に用いる)<br>
my_requests.py→カード番号をバックエンドに渡すためのファイル。<br>
/home/pi/sounds/test_message.mp3→音声を発生させるためのサーバ<br>

## 手順
1.ラズパイにssh接続を行う<br>

2.githubにクローンする<br>

3.仮想環境をアクティブにする<br>
`source ~/felica_project/venv/bin/activate`<br>

4.MP3サーバを起動する
まず、音声サーバを作成する。<br>
`mkdir -p /home/pi/sounds`<br>
`python3 -m http.server 8000`　<br>

5.アクティブにした状態で、以下のコマンドを実行する<br>
`cd felica_project`<br>
`python3 cardread.py` →カードの情報を読み取る(ここで読み取った情報を使ってユーザー登録を行う)<br>
`python3 card_onsei.py` →カードの情報を読み取り、バックエンドの情報と照合し、照合出来たらスピーカーで音声を出力する。<br>
