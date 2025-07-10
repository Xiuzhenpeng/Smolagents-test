import requests
import base64
import json

class Swarmui:
    def __init__(self, prompt:str, session_id):
        self.url = "118.191.0.226:23091"
        self.session_url = f"http://{self.url}/API/GetNewSession"
        self.get_image_url = f"http://{self.url}/API/GenerateText2Image"
        self.prompt_data = {
                "prompt": prompt,
                "negativeprompt": "",
                "model": "flux1-dev-fp8",
                "images": "1",
                "seed": "-1",
                "steps": "20",
                "cfgscale": "1",
                "width": "1024",
                "height": "1024",
                "sampler": "euler",
                "scheduler": "simple",
                "fluxguidancescale": "3.5",
                "session_id": session_id,
            }
        self.image_path = None
        self.image_url = None

    @staticmethod
    def get_new_sessions(url:str):
        response = requests.post(f"http://{url}/API/GetNewSession", json={})
        return response.json()['session_id']

    def generate_image_url(self):
        headers = {
        "Content-Type": "application/json",
        }
        response = requests.post(self.get_image_url, headers=headers, data=json.dumps(self.prompt_data))
        result = response.json()
        image_path = result["images"][0]
        image_url = f"http://{self.url}/{image_path}"
        self.image_path = image_path
        self.image_url = image_url
        return image_url
    
    def get_image_b64(self):
        image_url = self.get_image_url()
        f = requests.get(image_url)
        image_b64 = base64.b64encode(f.content).decode("utf-8")
        return image_b64

def generate_image(prompt: str) -> str:
    # init
    swarmui_url = "118.191.0.226:23091"
    session_id = Swarmui.get_new_sessions(swarmui_url)

    swarmui = Swarmui(prompt, session_id)
    image_b64 = swarmui.generate_image_url()

    print(f"Generated image ({len(image_b64)} chars)")
    return image_b64

def call_swarmui_api(prompt: str) -> str:
    # init
    swarmui_url = "118.191.0.226:23091"
    session_id = Swarmui.get_new_sessions(swarmui_url)

    swarmui = Swarmui(prompt, session_id)
    image_url = swarmui.generate_image_url()

    print(f"Generated image ({len(image_url)} chars)")
    return image_url