from langchain.chat_models import init_chat_model
from deepagents import create_deep_agent
import os


def read_log_file(file_path: str) -> str:
    """
    Reads the content of a local log file and returns its text.
    """
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
        return content
    except FileNotFoundError:
        return f"File not found: {file_path}"
    except Exception as e:
        return f"Error reading file: {str(e)}"


# Make sure your Anthropic API key is set in your environment!
model = init_chat_model("claude-sonnet-4-5-20250929")
instruction="You are an expert log analyzer. Analyze log files and provide insights."

agent = create_deep_agent(
    model=model,
    system_prompt=instruction,
    tools=[read_log_file],
)

file_path = "logs/app_server.log"
result = agent.invoke({
    "messages": [
        {"role": "user", "content": f"Analyze the file: {file_path}"}
    ]
})
print(result)
