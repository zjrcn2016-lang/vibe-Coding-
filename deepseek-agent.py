from openai import OpenAI
import os
import re

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/"
MODEL_NAME = "deepseek-chat"

if not DEEPSEEK_API_KEY:
    print("请设置环境变量 DEEPSEEK_API_KEY")
    print("PowerShell: $env:DEEPSEEK_API_KEY='你的密钥'")
    exit(1)

client = OpenAI(‘’
    api_key=DEEPSEEK_API_KEY,
    base_url=DEEPSEEK_API_URL
)

def calculator(expression: str):
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算出错：{str(e)}"

tools_map = {
    "计算器": calculator
}

system_prompt = """
你是简易AI智能体，严格遵守规则：
1. 需要计算就输出：
行动：计算器
参数：数学算式
2. 算出最终结果后输出：
最终答案：你的结果
禁止多余话术，只按上面格式输出。
"""

def run_agent(user_input: str):
    print(f"用户提问：{user_input}\n")
    msg_list = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    for _ in range(5):
        resp = client.chat.completions.create(
            model=MODEL_NAME,
            messages=msg_list,
            temperature=0
        )
        ai_text = resp.choices[0].message.content.strip()
        print(f"AI思考内容：{ai_text}\n")

        if "最终答案：" in ai_text:
            res = ai_text.split("最终答案：")[-1].strip()
            print(f"[OK] 完成，结果：{res}")
            return res

        act_match = re.search(r"行动：(.+)", ai_text)
        arg_match = re.search(r"参数：(.+)", ai_text)
        if act_match and arg_match:
            act_name = act_match.group(1).strip()
            args_text = arg_match.group(1).strip()
            print(f"[TOOL] 调用工具：{act_name}")
            tool_result = tools_map[act_name](args_text)
            print(f"工具返回：{tool_result}\n")

            msg_list.append({"role": "assistant", "content": ai_text})
            msg_list.append({"role": "user", "content": f"工具返回结果：{tool_result}，继续处理"})

if __name__ == "__main__":
    run_agent("计算 258 * 36 + 1590")