import pychromecast
from gtts import gTTS
import os
import time

DEVICE_NAME = "GoogleHome"  # 実際に見つかったデバイス名に変更
TTS_FILE = "/home/pi/sounds/test_message.mp3"
TTS_URL = "http://192.168.10.74:8000/test_message.mp3"  # IPを実際のものに変更

# Google Homeに接続
chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[DEVICE_NAME])
if not chromecasts:
    print(f"デバイス '{DEVICE_NAME}' が見つかりません。")
    exit(1)

cast = chromecasts[0]
cast.wait()
mc = cast.media_controller

# TTS音声を生成
tts = gTTS(text="こんにちは、テストです", lang="ja")
tts.save(TTS_FILE)
print("TTS音声を生成しました。")

# HTTPサーバーが動いているか確認
print("Google Home でTTS音声を再生します...")
mc.play_media(TTS_URL, "audio/mp3")
mc.block_until_active()
mc.play()
