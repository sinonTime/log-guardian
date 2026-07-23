import os
import json
from openai import OpenAI

class LLMClient:
    def __init__(self, api_key: str = None, model: str = "deepseek-v4-flash"):
        self.api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
        if not self.api_key:
            raise ValueError("API Key 未提供，请设置环境变量 DEEPSEEK_API_KEY 或传入参数")
        
        self.client = OpenAI(
            api_key=self.api_key,
            base_url="https://api.deepseek.com"
        )
        self.model = model

    def analyze_log(self, log_text: str) -> dict:
        prompt = f"""你是一位经验丰富的运维专家。以下是一条系统日志，请分析可能的错误原因和排查建议。
请输出 **严格的 JSON 格式**，不要包含任何其他文字、注释或代码块标记。JSON 应包含两个字段：
- "possible_cause": 简短的可能原因（字符串，中文）
- "suggestion": 具体的排查建议（字符串，可包含命令，中文）

确保所有字符串内容都已正确转义，且 JSON 是合法的。
日志内容：
{log_text}"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你只输出 JSON，不输出任何其他内容。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1, 
                max_tokens=500
            )
            content = response.choices[0].message.content.strip()
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()

            result = json.loads(content)
            return result
        except json.JSONDecodeError as e:
            return {
            "possible_cause": "JSON 解析错误",
            "suggestion": f"模型返回的内容无法解析：{str(e)}"
        }
        except Exception as e:
            return {"possible_cause": "分析失败", "suggestion": f"其他错误：{str(e)}"}