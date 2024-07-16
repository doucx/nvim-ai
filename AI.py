from typing import Generator
import pynvim
import json
import sseclient
import requests


class Model:
    def __init__(self, settings) -> None:
        self.update_settings(settings)

    def get_stream(self, url, data) -> Generator:
        headers = {
            "Content-Type": "application/json"
        }
        stream_response = requests.post(url, headers=headers, json=data, verify=False, stream=True)
        client = sseclient.SSEClient(stream_response)

        for event in client.events():
            payload = json.loads(event.data)
            text = payload['choices'][0]['text']
            yield text

    def update_settings(self, settings) -> None:
        self.settings = settings

    def completions(self, prompt) -> Generator:
        # 用设置与提示词进行续写
        json_data = self.settings["completions"]
        json_data["prompt"] = prompt
        json_data["stream"] = True
        stream = self.get_stream(self.settings["urls"]["completions"], json_data)
        for text in stream:
            # 可能的后续操作
            # 比如stop_token之类的
            yield text

@pynvim.plugin
class VimLocalAI(object):
    def __init__(self, nvim):
        self.nvim : pynvim.api.Nvim = nvim
        self.settings = self.nvim.vars.get("vim_localai_settings")
        self.model = Model(self.settings)
        self.stop = False
        self.running = False

    @pynvim.command('AICompletions', nargs='*', range='')
    def completions(self, args, range):
        self.settings = self.nvim.vars.get("vim_localai_settings")
        self.model.update_settings(self.settings)
        if self.running:
            self.nvim.out_write(f"有一个续写操作在执行\n")
            return
        self.running = True
        self.nvim.out_write(f"续写中……\n")
        buffer = self.nvim.current.buffer
        for text in self.model.completions("\n".join(buffer)):
            if self.stop:
                self.stop = False
                break
            for t in text:
                if t == "\n":
                    buffer.append("")
                else:
                    buffer[-1] += t
        self.running = False
        self.nvim.out_write(f"续写结束。\n")

    @pynvim.command('StopAICompletions', nargs='*', range='')
    def stop_completions(self, args, range):
        self.stop = True
