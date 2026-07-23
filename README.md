# 🔍 LogGuardian - 轻量级日志监控 + AI 辅助告警系统

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![DeepSeek](https://img.shields.io/badge/DeepSeek-API-orange)
![Docker](https://img.shields.io/badge/Docker-ready-brightgreen)

---

## 📖 简介

LogGuardian 是一个**端到端的日志监控与智能告警系统**，专为中小型服务设计。它通过实时采集日志文件，结合**规则引擎 + 统计异常检测**双引擎分析，并引入**DeepSeek 大模型**进行根因分析和排查建议，最后通过**微信推送**通知运维人员，同时提供**Web Dashboard**可视化展示。

**项目亮点**：
- 双引擎告警：规则引擎（快、准、可解释）+ 统计异常（发现未知模式）
- AI 增强运维：调用 DeepSeek API 对异常日志进行语义分析，输出结构化 JSON 建议
- 工程化：Docker 容器化部署，使用 `.env` 管理配置
- 实时 Dashboard：Flask + Chart.js 展示告警趋势与详情

---

## 🧱 系统架构（数据流）

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  日志文件    │────>│  collector   │────>│   analyzer      │
│ (test.log)  │     │ (watchdog)   │     │ (规则+Z-score)  │
└─────────────┘     └──────────────┘     └────────┬──────────┘
                                                   │  alert=True?
                                                   ▼
                                          ┌─────────────────┐
                                          │   ai_helper     │
                                          │  (DeepSeek LLM) │
                                          └────────┬─────────┘
                                                   │  possible_cause + suggestion
                                                   ▼
                                          ┌─────────────────┐
                                          │   notifier      │
                                          │ (PushPlus微信)  │
                                          └────────┬─────────┘
                                                   │
                                                   ▼
                                          ┌─────────────────┐
                                          │ web / Dashboard │
                                          │ (Flask + Chart) │
                                          └─────────────────┘
```

- **collector**：使用 `watchdog` 实时监听日志文件变化，增量读取。
- **analyzer**：规则引擎（正则匹配 ERROR/5xx/timeout） + 滑动窗口 Z-score 统计异常检测。
- **ai_helper**：调用 DeepSeek API，输出 JSON 格式的可能原因和排查建议。
- **notifier**：通过 PushPlus 推送到个人微信。
- **web**：Flask 提供 RESTful API，前端 Chart.js 展示告警趋势，表格展示详情。

---

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| **日志采集** | 实时监控文件变化，增量读取，支持日志轮转 |
| **规则引擎** | 基于正则匹配 ERROR、5xx、timeout 等关键词，毫秒级响应 |
| **统计异常检测** | 滑动窗口 Z-score，发现突发错误流量或模式偏移 |
| **AI 根因分析** | DeepSeek API 分析异常日志，输出结构化诊断与建议 |
| **微信推送** | 通过 PushPlus 将告警消息（含 AI 建议）推送到个人微信 |
| **Web Dashboard** | 实时告警列表、趋势折线图、统计卡片，每 3 秒自动刷新 |
| **容器化部署** | Docker + docker-compose 一键构建运行 |

---

## 🛠 技术栈

- **语言**：Python 3.10+
- **日志采集**：watchdog
- **Web 框架**：Flask
- **前端图表**：Chart.js（CDN）
- **大模型**：DeepSeek Chat API（兼容 OpenAI SDK）
- **消息推送**：PushPlus（微信）
- **配置管理**：python-dotenv
- **容器化**：Docker, docker-compose

---

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/your-username/log-guardian.git
cd log-guardian
```

### 2. 创建虚拟环境并安装依赖

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate

pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件（与 `docker-compose.yml` 同级）：

```
DEEPSEEK_API_KEY=sk-你的DeepSeek密钥
PUSHPLUS_TOKEN=你的PushPlus Token
LOG_FILE=test.log
```

> **注意**：
> - DeepSeek API Key 在 [platform.deepseek.com](https://platform.deepseek.com/) 注册获取。
> - PushPlus Token 在 [pushplus.plus](https://www.pushplus.plus/) 获取。

### 4. 运行测试

```bash
python main.py
```

打开浏览器访问 `http://localhost:5000` 查看 Dashboard。

### 5. 模拟日志产生（新终端）

```bash
echo "ERROR: database connection timeout" >> test.log
```

观察主终端输出，您将看到：
```
[采集到新日志] ERROR: database connection timeout
[分析结果] {'alert': True, 'engine': 'rule', ...}
[AI分析] 可能原因: ...
[通知] 微信推送已发送
```

微信将收到包含 AI 建议的告警消息。

---

## 🐳 Docker 部署

### 1. 构建并启动

```bash
docker compose up --build
```

### 2. 配置环境变量

确保 `.env` 文件已正确设置，或通过 shell 传入：

```bash
DEEPSEEK_API_KEY=sk-xxx PUSHPLUS_TOKEN=xxx docker compose up
```

### 3. 访问 Dashboard

浏览器打开 `http://localhost:5000`。

> **注意**：容器内的日志文件路径默认挂载了宿主机的 `/var/log/nginx`。如需监控其他文件，请修改 `docker-compose.yml` 中的 volumes。

---

## 📁 项目结构

```
log-guardian/
├── collector/
│   ├── __init__.py
│   └── log_watcher.py          # watchdog 日志文件监听
├── analyzer/
│   ├── __init__.py              # Analyzer 类，组合规则+统计引擎
│   ├── rule_engine.py           # 规则引擎（正则匹配）
│   └── anomaly_detector.py      # 滑动窗口 Z-score 异常检测
├── notifier/
│   ├── __init__.py              # 统一通知接口
│   └── wechat_notifier.py       # PushPlus 微信推送
├── ai_helper/
│   ├── __init__.py
│   └── llm_client.py            # DeepSeek API 调用与 Prompt 设计
├── web/
│   ├── __init__.py
│   ├── app.py                   # Flask 服务 + REST API
│   └── templates/
│       └── index.html           # Dashboard 前端页面
├── main.py                      # 系统主入口，串联所有模块
├── requirements.txt             # Python 依赖
├── .env                         # 环境变量（Git 忽略）
├── Dockerfile                   # 容器构建文件
├── docker-compose.yml           # 多容器编排
└── README.md                    # 项目文档
```

---

## 💡 关键设计亮点

### 1. 双引擎告警
- **规则引擎**：快速、确定、可解释，覆盖已知异常模式。
- **统计异常**：基于滑动窗口 Z-score，检测规则无法覆盖的突发错误，提高发现未知问题的能力。
- 两者并行工作，任一引擎触发即告警，降低漏报风险。

### 2. AI Prompt 工程
- 设计严格格式的提示词，要求模型输出固定的 JSON 字段（`possible_cause`, `suggestion`）。
- 使用 `temperature=0.1` 降低输出随机性。
- 处理模型可能返回的 Markdown 代码块（` ```json `），提高解析成功率。

### 3. Windows 兼容性
- 原始 watchdog 在 Windows 下可能因文件系统事件丢失而不触发，通过 `os.path.abspath` 统一路径，并保留轮询模式作为备选，确保跨平台稳定。

### 4. 配置管理
- 使用 `python-dotenv` 从 `.env` 文件加载敏感信息，避免硬编码密钥。
- 环境变量支持灵活切换日志文件路径、API Key 等。

### 5. 异常处理
- 每个模块都包裹了 try-except 防止单点故障导致系统崩溃。
- AI 分析失败时自动降级，不影响告警主流程。

---

## 📸 演示效果

<table>
  <tr>
    <td><b>Web Dashboard</b></td>
    <td><b>微信推送</b></td>
  </tr>
  <tr>
    <td><img src="screenshots/dashboard.png" width="400"/></td>
    <td><img src="screenshots/wechat.png" width="300"/></td>
  </tr>
</table>

> *截图展示告警趋势图、告警列表及微信推送的 AI 建议内容。*

---

## 🔮 扩展思路

- **持久化存储**：将告警存入 SQLite / PostgreSQL，支持历史查询。
- **多通道通知**：增加企业微信、钉钉、邮件等。
- **告警聚合**：相同错误合并，减少重复推送。
- **更丰富的异常检测**：引入 Isolation Forest、Prophet 等模型。
- **日志文件自动发现**：监听目录下所有 `.log` 文件。
- **集成 Prometheus**：暴露指标供 Prometheus 拉取。

---

## 📄 License

MIT License

---

## 👨‍💻 作者

[Your Name] – [your-email@example.com]
欢迎 Star、Issue、PR！