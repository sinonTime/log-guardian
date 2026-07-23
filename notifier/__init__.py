from .wechat_notifier import send_alert_to_wechat

def notify(alert_info: dict, pushplus_token: str = None):

    if not alert_info.get("alert"):
        return  

    line = alert_info.get("line", "未知日志")
    engine = alert_info.get("engine", "unknown")
    ai_reason = alert_info.get("ai_reason", "")
    ai_suggestion = alert_info.get("ai_suggestion", "")

    title = f"[{engine.upper()}] 日志告警"
    content = f"""
## 🚨 日志告警

- **触发引擎**: {engine}
- **告警时间**: {alert_info.get('time', 'N/A')}

### 日志内容"""