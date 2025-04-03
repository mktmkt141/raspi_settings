from smartcard.System import readers as get_readers
from smartcard.Exceptions import NoCardException
import time
from my_requests import update_status  # サーバー通信用の関数をインポート

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
        time.sleep(1)  # 次のチェックまで10秒待機
