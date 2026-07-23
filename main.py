#!/usr/bin/env python3
"""
日志监控 + AI 辅助告警系统主入口
将各模块串联：日志采集 → 规则+统计异常检测 → AI增强 → 微信通知 → Dashboard记录
"""
import os
import threading
from collector.log_watcher import LogWatcher
from analyzer import Analyzer
from notifier import notify
from ai_helper.llm_client import LLMClient
from web.app import app, add_alert
from datetime import datetime 

LOG_FILE = os.getenv("LOG_FILE", "test.log")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
PUSHPLUS_TOKEN = os.getenv("PUSHPLUS_TOKEN")

analyzer = Analyzer()
ai_client = LLMClient(api_key=DEEPSEEK_API_KEY) if DEEPSEEK_API_KEY else None

def on_new_log(line: str):
    result = analyzer.analyze(line)
    if not result.get("alert"):
        return
    # === 添加时间戳 ===
    result["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if ai_client:
        try:
            ai_result = ai_client.analyze_log(line)
            result["ai_reason"] = ai_result.get("possible_cause", "")
            result["ai_suggestion"] = ai_result.get("suggestion", "")
        except Exception as e:
            result["ai_reason"] = "AI分析异常"
            result["ai_suggestion"] = f"错误: {str(e)}"
    try:
        notify(result, pushplus_token=PUSHPLUS_TOKEN)
    except Exception as e:
        print(f"[通知异常] {e}")
    add_alert(result)

def main():
    watcher = LogWatcher(LOG_FILE, on_new_log)
    watcher_thread = threading.Thread(target=watcher.start, daemon=True)
    watcher_thread.start()
    print(f"[系统启动] 监听日志文件: {LOG_FILE}")

    print("[系统启动] Dashboard: http://localhost:5000")
    app.run(host="0.0.0.0", port=5000, debug=False)

if __name__ == "__main__":
    main()