from smolagents import CodeAgent, InferenceClientModel, LiteLLMModel, tool, GradioUI
from smolagents import Tool
from utils.swarmui_flux_t2i import call_swarmui_api


# 假设我们有一个获取最高评分餐饮服务的函数
@tool
def catering_service_tool(query: str) -> str:
    """
    This tool returns the highest-rated catering service in Gotham City.
    
    Args:
        query: A search term for finding catering services.
    """
   # 示例餐饮服务及评分列表
    services = {
        "Gotham Catering Co.": 4.9,
        "Wayne Manor Catering": 4.8,
        "Gotham City Events": 4.7,
    }
    
    # 查找评分最高的餐饮服务（模拟搜索查询过滤）
    best_service = max(services, key=services.get)
    
    return best_service

@tool
def generate_image_with_flux1(prompt: str) -> str:
    """
    This tool generates an image based on a given text prompt using the flux1.dev model.

    Args:
        prompt: A descriptive natural language prompt that specifies the desired content and style of the image.
                For example: "A futuristic city skyline at sunset with flying cars".
    
    Returns:
        A URL string pointing to the generated image hosted on a server or storage service.
    """

    image_url = call_swarmui_api(prompt)
    return image_url

model = LiteLLMModel(
    model_id="deepseek/deepseek-chat",
    api_base="https://api.deepseek.com",
    # api_key=os.environ["sk-31b706fc72bc4793983bc76237ebb569"],
    api_key="sk-31b706fc72bc4793983bc76237ebb569",
)

class GenerateImage(Tool):
    name = "image_generate_tool"
    description = "This tool generates an image based on a given text prompt using the flux1.dev model."
    inputs = {'prompt': {"type": "string", "description": """A descriptive natural language prompt that specifies the desired content and style of the image.
                                                            For example: "A futuristic city skyline at sunset with flying cars."""}}
    output_type = "str"

    def __init__(self, **hub_kwargs) -> None:

        super().__init__()

        self.stable_diffusion = self.default_stable_diffusion_checkpoint

        self.hub_kwargs = hub_kwargs

    def forward(self, image, prompt):
        image_url = call_swarmui_api(prompt)

agent = CodeAgent(tools=[generate_image_with_flux1], model=model)


# result = agent.run(
#     "扩充这段提示词，翻译成英文，并生成一张图片。一辆车停在山顶上"
# )
# print(result)   # Output: Gotham Catering Co.

ui = GradioUI(agent)
ui.launch()