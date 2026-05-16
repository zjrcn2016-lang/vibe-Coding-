from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
# ================= 配置 =================
API_KEY = "977abc8921f94ddfb5a04a8a5eb9e8df.eXbUL6z8BkdTdBX4"
BASE_URL = "https://open.bigmodel.cn/api/paas/v4/"

# ================= 创建模型 =================
llm = ChatOpenAI(
    model="glm-4",
    api_key=API_KEY,
    base_url=BASE_URL,
    temperature=0.1,
    timeout=30
    #... other params

)

@tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"

agent = create_agent(llm, tools=[search, get_weather])

# 测试搜索功能
print("测试: 搜索功能")
print("=" * 30)

# 直接测试工具
print("直接调用工具:")
search_result = search.invoke({"query": "Python最新版本"})
print(f"search('Python最新版本') = {search_result}")

print()
print("=" * 30)
print("使用Agent调用工具:")

# 调用 Agent
result = agent.invoke(
    {"messages": [{"role": "user", "content": "Python最新版本是什么？"}]}
)

# 打印结果类型
print(f"结果类型: {type(result)}")
print("测试完成！")