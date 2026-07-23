import requests
import json
import os

def send_alert_to_wechat(title: str, content: str, token: str = None):
    if token is None:
        token = os.getenv("f1a40c10fc38461da12c757f65929a77")
        if not token:
            raise ValueError("请在环境变量 PUSHPLUS_TOKEN 中设置 PushPlus 的 Token")

    url = "http://www.pushplus.plus/send"
    headers = {"Content-Type": "application/json"}
    payload = {
        "token": token,
        "title": title,
        "content": content,
        "template": "markdown" 
    }
    try:
        resp = requests.post(url, data=json.dumps(payload), headers=headers, timeout=10)
        resp.raise_for_status()
        result = resp.json()
        if result.get("code") == 200:
            print(f"✅ 微信推送成功: {title}")
        else:
            print(f"⚠️ 微信推送失败: {result.get('msg')}")
    except Exception as e:
        print(f"❌ 微信推送异常: {e}")