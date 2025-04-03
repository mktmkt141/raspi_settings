import requests  # 追加
URL = "http://192.168.20.50:5000/api/v1/auth/scan"

def update_status(idm):
    """取得した IDm をサーバーに送信し、ステータスを更新する"""
    if not idm:
        print("IDm が取得できませんでした。")
        return
    
    data = {"idm": idm}
    
    try:
        response = requests.post(URL, json=data)
        if response.status_code == 200:
            response_data = response.json()
            print(f"レスポンスデータ: {response_data}")  # ここでレスポンスを表示
            print(f"✅ ICカード {response_data['user']['idm']} のステータスが {response_data['user']['status']} に更新されました。")
        else:
            print(f"❌ ステータス更新に失敗しました: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"🚨 リクエストエラー: {e}")

