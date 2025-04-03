from smartcard.System import readers
from smartcard.Exceptions import NoCardException

def read_felica_lite_idm():
    try:
        # カードリーダーの取得
        reader_list = readers()
        if not reader_list:
            print("カードリーダーが見つかりません")
            return
        
        print("利用可能なカードリーダー:", reader_list)

        # 最初のリーダーを使用
        reader = reader_list[0]
        connection = reader.createConnection()

        # 接続
        connection.connect()

        # Felica Lite-SカードのIDmを読み取るためのコマンド
        GET_IDM_APDU = [0xFF, 0xCA, 0x00, 0x00, 0x00]

        # コマンドを送信してIDmを取得
        response, sw1, sw2 = connection.transmit(GET_IDM_APDU)

        # ステータスコードが正常な場合、IDmを表示
        if sw1 == 0x90 and sw2 == 0x00:
            # 2桁ごとにスペースを入れる
            idm_hex = ' '.join(format(byte, '02X') for byte in response)
            print("Felica Lite-SカードのIDm:", idm_hex)
        else:
            print("Felica Lite-SカードのIDmを取得できませんでした")

        # 接続を解除
        connection.disconnect()

    except NoCardException:
        print("カードが読み込めませんでした")

if __name__ == "__main__":
    read_felica_lite_idm()
