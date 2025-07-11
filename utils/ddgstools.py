from smolagents import Tool
from duckduckgo_search import DDGS

class DuckDuckGoImageSearchTool(Tool):
    name = "image_search"
    description = """Performs a DuckDuckGo image search based on your query and returns the top image results."""
    inputs = {
        "keywords": {"type": "string", "description": "The search keywords for images."},
        "region": {"type": "string", "description": "The region code, e.g., 'us-en', 'uk-en'.", "default": "us-en", "nullable": True,},
        "safesearch": {"type": "string", "description": "on, moderate, or off.", "default": "moderate", "nullable": True,},
        "timelimit": {"type": "string", "description": "Day, Week, Month, Year", "optional": True, "nullable": True,},
        "size": {"type": "string", "description": "Small, Medium, Large, Wallpaper", "optional": True, "nullable": True,},
        "color": {"type": "string", "description": "color, Monochrome, Red, Orange, Yellow, etc.", "optional": True, "nullable": True,},
        "type_image": {"type": "string", "description": "photo, clipart, gif, transparent, line", "optional": True, "nullable": True,},
        "layout": {"type": "string", "description": "Square, Tall, Wide", "optional": True, "nullable": True,},
        "license_image": {"type": "string", "description": "any, Public, Share, ShareCommercially, Modify, ModifyCommercially", "optional": True, "nullable": True,},
        "max_results": {"type": "integer", "description": "Maximum number of image results", "optional": True, "nullable": True,}
    }
    output_type = "string"

    def __init__(self, **kwargs):
        super().__init__()
        try:
            from duckduckgo_search import DDGS
        except ImportError as e:
            raise ImportError(
                "You must install package `duckduckgo_search` to run this tool: run `pip install duckduckgo-search`."
            ) from e
        self.ddgs = DDGS(**kwargs)

    def forward(self, keywords: str, region: str = "us-en", safesearch: str = "moderate",
                timelimit: str = None, size: str = None, color: str = None,
                type_image: str = None, layout: str = None, license_image: str = None,
                max_results: int = 5) -> str:
        results = self.ddgs.images(
            keywords=keywords,
            region=region,
            safesearch=safesearch,
            timelimit=timelimit,
            size=size,
            color=color,
            type_image=type_image,
            layout=layout,
            license_image=license_image,
            max_results=max_results
        )

        if not results:
            raise Exception("No image results found for the query.")

        # Format results into markdown-style output
        postprocessed = [
            f"![{item['title']}]({item['image']})\nSource: [{item['source']}]({item['url']})"
            for item in results
        ]
        return "## Image Search Results\n\n" + "\n\n".join(postprocessed)
    
if __name__ == "__main__":
    results = DDGS().images(
    keywords="butterfly",
    region="wt-wt",
    safesearch="off",
    size=None,
    color="Monochrome",
    type_image=None,
    layout=None,
    license_image=None,
    max_results=100,
    )
    print(results)
