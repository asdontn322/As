# ButterTerm: Cosmic Edition (Single File)
import os, subprocess, time
from datetime import datetime, timedelta
import psutil
from textual.app import App, ComposeResult
from textual.widgets import Static, Input
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.binding import Binding

class TopBar(Static):
    def on_mount(self): self.set_interval(1, self.refresh)
    def refresh(self): self.update(f"🧠 ButterTerm | {datetime.now().strftime('%H:%M:%S')} | ⬆️ {timedelta(seconds=int(time.time() - psutil.boot_time()))}")

class AsciiLogo(Static):
    def on_mount(self): self.update(r"""
██████╗ ██╗   ██╗████████╗████████╗███████╗██████╗ ███╗   ███╗
██╔══██╗██║   ██║╚══██╔══╝╚══██╔══╝██╔════╝██╔══██╗████╗ ████║
██████╔╝██║   ██║   ██║      ██║   █████╗  ██████╔╝██╔████╔██║
██╔═══╝ ██║   ██║   ██║      ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║
██║     ╚██████╔╝   ██║      ██║   ███████╗██║  ██║██║ ╚═╝ ██║
╚═╝      ╚═════╝    ╚═╝      ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝
""")

class SystemStats(Static):
    def on_mount(self): self.set_interval(1, self.refresh)
    def refresh(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        net = psutil.net_io_counters()
        temp = psutil.sensors_temperatures().get("k10temp", [{}])[0].get("current", 0)
        self.update(f"🧠 CPU: {cpu}%\n💾 RAM: {ram}%\n🌡️ Temp: {temp}°C\n📡 ↓ {net.bytes_recv//1024}KB ↑ {net.bytes_sent//1024}KB")

class ShellInput(Input): pass

class ButterTerm(App):
    BINDINGS = [Binding("ctrl+l", "clear_output", "Clear"), Binding("ctrl+s", "save_output", "Save"), Binding("ctrl+t", "toggle_theme", "Theme")]
    output_text = reactive("")
    theme_index = reactive(0)
    themes = ["obsidian", "cyber"]

    def compose(self) -> ComposeResult:
        yield TopBar()
        with Horizontal(): yield AsciiLogo(); yield SystemStats()
        yield Static(id="output")
        yield ShellInput(placeholder="Type command...")

    def on_mount(self):
        self.output = self.query_one("#output", Static)
        self.input = self.query_one(ShellInput)
        self.history, self.history_index = [], -1
        self.set_theme("obsidian")

    def on_input_submitted(self, msg: Input.Submitted):
        cmd = msg.value.strip()
        if not cmd: return
        self.history.append(cmd); self.history_index = len(self.history)
        try: result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        except Exception as e: output = f"Error: {e}"
        else: output = result.stdout + result.stderr
        self.output_text += f"\n$ {cmd}\n{output}"
        self.output.update(self.output_text)
        self.input.value = ""

    def on_key(self, event):
        if event.key == "up" and self.history:
            self.history_index = max(0, self.history_index - 1)
            self.input.value = self.history[self.history_index]
        elif event.key == "down" and self.history:
            self.history_index = min(len(self.history) - 1, self.history_index + 1)
            self.input.value = self.history[self.history_index]

    def action_clear_output(self): self.output_text = ""; self.output.update("")
    def action_save_output(self):
        os.makedirs("logs", exist_ok=True)
        with open(f"logs/output_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt", "w") as f:
            f.write(self.output_text)

    def action_toggle_theme(self):
        self.theme_index = (self.theme_index + 1) % len(self.themes)
        self.set_theme(self.themes[self.theme_index])

    def set_theme(self, theme: str):
        if theme == "obsidian":
            self.stylesheet = """
TopBar { background: black; color: cyan; }
AsciiLogo { background: #111; color: #444; }
SystemStats { background: #0c0c0c; color: lime; }
ShellInput { background: #060606; color: #ff79c6; }
#output { background: #101010; color: white; }
"""
        else:
            self.stylesheet = """
TopBar { background: #002244; color: #00ffff; }
AsciiLogo { background: #001122; color: #66ccff; }
SystemStats { background: #002244; color: #00ffcc; }
ShellInput { background: #001122; color: #ccff00; }
#output { background: #000022; color: #f0f0f0; }
"""
        self.reload_css(self.stylesheet)

if __name__ == "__main__":
    ButterTerm().run()
