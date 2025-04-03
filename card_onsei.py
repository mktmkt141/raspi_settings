from smartcard.System import readers as get_readers
from smartcard.Exceptions import NoCardException
import time
import pychromecast
from gtts import gTTS
import os
from my_requests import update_status  # サーバー通信用の関数

# Google Home の設定
DEVICE_NAME = "GoogleHome"  # 設定したGoogle Homeの名前
TTS_FILE = "/home/pi/sounds/test_message.mp3"  # TTSの音声ファイル
TTS_URL = "http://192.168.10.74:8000/test_message.mp3"  # TTS用のMP3を置くHTTPサーバーのURL

# Google Homeに接続
chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[DEVICE_NAME])
if not chromecasts:
    print(f"デバイス '{DEVICE_NAME}' が見つかりません。")
    exit(1)

cast = chromecasts[0]
cast.wait()
mc = cast.media_controller

def generate_tts_message(text):
    """TTSの音声ファイルを作成する"""
    tts = gTTS(text=text, lang="ja")
    tts.save(TTS_FILE)
    print("TTS音声を生成しました。")

def play_tts():
    """Google Home でTTS音声を再生する"""
    print("Google Home でTTS音声を再生します...")
    mc.play_media(TTS_URL, "audio/mp3")
    mc.block_until_active()
    mc.play()

def get_idm():
    """ICカードリーダーから IDm を取得する"""
    readers = get_readers()
    if not readers:
        print("カードリーダーが見つかりません。")
        return None

    conn = readers[0].createConnection()

    while True:
        try:
            print("カードをかざしてください...")
            conn.connect()  # カードが挿入されるまで待機
            send_data = [0xFF, 0xCA, 0x00, 0x00, 0x00]
            recv_data, sw1, sw2 = conn.transmit(send_data)
            idm = " ".join(format(byte, "02X") for byte in recv_data)  # スペース区切り
            print(f"取得した IDm: {idm}")
            
            # TTS音声を生成して再生
            generate_tts_message("カードを検出しました")
            play_tts()
            
            return idm
        except NoCardException:
            time.sleep(1)  # カードがない場合、1秒待機して再試行
        except Exception as e:
            print(f"エラー: {e}")
            return None

if __name__ == "__main__":
    while True:
        idm = get_idm()  # IDm を取得
        if idm:  
            update_status(idm)  # サーバーに送信
        time.sleep(10)  # 次のチェックまで10秒待機
