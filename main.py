import os
from smolagents import CodeAgent, DuckDuckGoSearchTool, InferenceClientModel, OpenAIServerModel, LiteLLMModel

model = LiteLLMModel(
    model_id="deepseek/deepseek-chat",
    api_base="https://api.deepseek.com",
    # api_key=os.environ["sk-31b706fc72bc4793983bc76237ebb569"],
    api_key="sk-31b706fc72bc4793983bc76237ebb569",
)

agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)

agent.run("Search for the best music recommendations for a party at the Wayne's mansion.")