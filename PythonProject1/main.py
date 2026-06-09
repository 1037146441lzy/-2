from openai import OpenAI
import json

from tools import get_weather
from tools import get_current_time


# =========================
# DashScope配置
# =========================

client = OpenAI(
    api_key="sk-de872eec95a341d993c603e45347f310",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

# =========================
# 工具定义(Function Calling)
# =========================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询某个城市天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前时间",
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
    }
]

# =========================
# Tool映射
# =========================

available_functions = {
    "get_weather": get_weather,
    "get_current_time": get_current_time
}

# =========================
# 上下文记忆
# =========================

messages = [
    {
        "role": "system",
        "content":
        """
        你是一个智能Agent。

        你的能力：
        1. 查询天气
        2. 查询时间
        3. 记住用户上下文

        如果用户问天气，
        自动调用get_weather。

        如果用户问时间，
        自动调用get_current_time。
        """
    }
]

print("=" * 60)
print("智能Agent启动成功")
print("输入 exit 退出")
print("=" * 60)

while True:

    user_input = input("\n用户：")

    if user_input.lower() == "exit":
        break

    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = client.chat.completions.create(
        model="qwen-plus",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    response_message = response.choices[0].message

    # =========================
    # 判断是否需要调用工具
    # =========================

    if response_message.tool_calls:

        messages.append(response_message)

        for tool_call in response_message.tool_calls:

            function_name = tool_call.function.name

            function_to_call = available_functions[function_name]

            arguments = json.loads(
                tool_call.function.arguments
            )

            # Tool 1
            if function_name == "get_weather":

                function_response = function_to_call(
                    city=arguments.get("city")
                )

            # Tool 2
            elif function_name == "get_current_time":

                function_response = function_to_call()

            else:
                function_response = "未知工具"

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": str(function_response)
                }
            )

        second_response = client.chat.completions.create(
            model="qwen-plus",
            messages=messages
        )

        assistant_reply = second_response.choices[0].message.content

        print("\nAgent：")
        print(assistant_reply)

        messages.append(
            {
                "role": "assistant",
                "content": assistant_reply
            }
        )

    else:

        assistant_reply = response_message.content

        print("\nAgent：")
        print(assistant_reply)

        messages.append(
            {
                "role": "assistant",
                "content": assistant_reply
            }
        )