"""
LangChain 入门示例
对比 baby-agent.py 学习
"""
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate

# ================= 配置 =================
API_KEY = "977abc8921f94ddfb5a04a8a5eb9e8df.eXbUL6z8BkdTdBX4"
BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"

# ================= 创建模型 =================
llm = init_chat_modelv2(
    model="glm-4",
    api_key=API_KEY,
    base_url=BASE_URL,
    temperature=0
)

# ================= 定义工具 =================
@tool
def calculator(expression: str) -> str:
    """执行数学计算"""
    try:
        return str(eval(expression))
    except Exception as e:
        return f"计算失败: {e}"

tools = [calculator]

# ================= 提示词 =================
system_prompt = """
你是简易AI智能体，严格遵守规则：
1. 需要计算就输出：
Action: calculator
Action Input: 数学算式
2. 算出最终结果后输出：
Final Answer: 你的答案
"""

# ================= 简单循环（不用 LangChain Agent） =================
def simple_agent(user_input: str):
    """
    模拟 baby-agent.py 的方式
    直接用 LLM + 工具，不用复杂 API
    """
    messages = [
        ("system", system_prompt),
        ("user", user_input)
    ]
    
    for _ in range(5):
        # 1. 调用 LLM
        ai_msg = llm.invoke(messages)
        ai_text = ai_msg.content
        print(f"AI: {ai_text}\n")
        
        # 2. 检查是否结束
        if "Final Answer:" in ai_text:
            return ai_text.split("Final Answer:")[-1].strip()
        
        # 3. 解析工具调用
        if "Action:" in ai_text and "Action Input:" in ai_text:
            # 简单解析
            action = ai_text.split("Action:")[1].split("Action Input:")[0].strip()
            input_param = ai_text.split("Action Input:")[1].strip()
            
            print(f"调用工具: {action}, 参数: {input_param}")
            
            # 执行工具
            if action == "calculator":
                result = calculator(input_param)
                print(f"工具结果: {result}\n")
                
                # 添加到消息
                messages.append(("assistant", ai_text))
                messages.append(("user", f"Observation: {result}"))
    
    return "没有找到答案"

# ================= 主程序 =================
if __name__ == "__main__":
    print("=" * 50)
    print("LangChain 入门 - 对比 baby-agent.py")
    print("=" * 50)
    
    # 测试
    question = "计算 258 * 36 + 1590"
    print(f"问题: {question}\n")
    
    answer = simple_agent(question)
    print(f"\n最终答案: {answer}")