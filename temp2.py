from langchain.chat_models import AzureChatOpenAI  
from deepagents import create_deep_agent
import os

# Set your Azure OpenAI credentials
os.environ["AZURE_OPENAI_API_KEY"] = "your-azure-openai-key"
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://your-resource-name.openai.azure.com/"
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"] = "your-deployment-name"  # This should match your deployment name on Azure

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

# Create an instance of AzureChatOpenAI
model = AzureChatOpenAI(
    openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
    openai_api_base=os.environ["AZURE_OPENAI_ENDPOINT"],
    deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    openai_api_type="azure",
    openai_api_version="2023-05-15"  # or the version that matches your Azure deployment
)

instruction = "You are an expert log analyzer. Analyze log files and provide insights."

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
