from typing import Generator
import time
import pynvim
import json
import sseclient
import requests
import threading


class Model:
    def __init__(self) -> None:
        self.stop = threading.Event()

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
            yield text

@pynvim.plugin
class VimLocalAI(object):
    def __init__(self, nvim):
        self.nvim: pynvim.api.Nvim = nvim
        self.model = Model()
        self.update_setting()
        self.stop = threading.Event()
        self.is_running = threading.Event()
        self.current_buffer = None
        self.last_buffer = None

    def update_setting(self):
        self.settings = self.nvim.vars.get("vim_localai_settings")
        self.model.update_settings(self.settings)

    def completions(self, buffer):
        self.update_setting()
        self.current_buffer = buffer
        self.last_buffer = self.current_buffer[:]
        if self.is_running.is_set():
            self.nvim.out_write(f"有一个续写操作在执行\n")
            return
        self.is_running.set()
        self.nvim.out_write(f"续写中……\n")
        for text in self.model.completions("\n".join(self.current_buffer)):
            if self.stop.is_set():
                self.stop.clear()
                break
            for t in text:
                if t == "\n":
                    self.current_buffer.append("")
                else:
                    self.current_buffer[-1] += t
        self.is_running.clear()
        self.nvim.out_write(f"续写结束。\n")

    @pynvim.command('AICompletions', nargs='*', range='')
    def completions_command(self, args, range_):
        buffer = self.nvim.current.buffer
        self.completions(buffer)

    def stop_completions(self):
        self.stop.set()

    @pynvim.command('AIStopCompletions', nargs='*', range='')
    def stop_completions_command(self, args, range_):
        self.stop_completions()

    def clear_completions_output(self):
        if self.current_buffer is None:
            self.current_buffer = self.nvim.current.buffer

        if self.last_buffer is None:
            self.last_buffer = self.current_buffer[:]
        # 停止续写
        if self.is_running.is_set():
            self.stop_completions()
            for i in range(50):
                self.nvim.out_write(f"停止运行中的续写……{i*0.1}s\n") # 必须加这个不然会卡住，不知道为什么。
                if not self.is_running.is_set():
                    break
                time.sleep(0.1)
            if self.is_running.is_set():
                self.nvim.out_write(f"失败。续写未停止\n")
                raise RuntimeError("续写操作正在进行中，无法继续执行新的操作")

        self.current_buffer[:] = self.last_buffer

    @pynvim.command('AIClearCompletions', nargs='*', range='')
    def clear_completions_output_command(self, args, range_):
        try:
            self.clear_completions_output()
        except RuntimeError:
            return

    @pynvim.command('AIReCompletions', nargs='*', range='')
    def recompletions(self, args, range_):
        self.nvim.out_write(f"重新生成中……\n")

        try:
            self.clear_completions_output()
        except RuntimeError:
            return

        self.completions(self.current_buffer)
