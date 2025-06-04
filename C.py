from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivy.uix.gridlayout import GridLayout
from kivy.core.audio import SoundLoader
from kivy.uix.video import Video
from plyer import filechooser
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import os
import shutil

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        MDLabel:
            text: 'Secret Calculator'
            halign: 'center'
            font_style: 'H4'

        MDTextField:
            id: solution
            hint_text: 'Enter expression or secret code'
            halign: 'right'
            size_hint_y: None
            height: '60dp'
            font_size: '24sp'
            readonly: True

        GridLayout:
            id: button_grid
            cols: 4
            spacing: 10
            padding: 10
            size_hint_y: None
            height: self.minimum_height

        MDLabel:
            id: result_label
            text: ''
            halign: 'center'
            theme_text_color: 'Secondary'
'''

class SecretCalculatorApp(MDApp):
    def build(self):
        self.title = "Secret Calculator"
        self.operators = ['+', '-', '*', '/', '**', '.', '%']
        self.last_was_operator = None
        self.last_button = None
        screen = Builder.load_string(KV)

        # Define button layout
        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            ["0", ".", "C", "+"],
            ["(", ")", "^", "="]
        ]

        # Add buttons to the grid
        button_grid = screen.ids.button_grid
        for row in buttons:
            h_layout = GridLayout(cols=4, spacing=10, size_hint_y=None, height='60dp')
            for label in row:
                button = MDRaisedButton(
                    text=label,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    size_hint=(1, None),
                    height='60dp'
                )
                button.bind(on_press=self.on_button_press)
                h_layout.add_widget(button)
            button_grid.add_widget(h_layout)

        return screen

    def on_button_press(self, instance):
        text = instance.text
        if text == "C":
            self.root.ids.solution.text = ""
            self.root.ids.result_label.text = ""
        elif text == "=":
            self.calculate_result()
        else:
            self.root.ids.solution.text += text

    def calculate_result(self):
        expr = self.root.ids.solution.text.strip()
        if expr == "7777":
            self.root.ids.solution.text = ""
            self.open_music_player()
        elif expr == "8888":
            self.root.ids.solution.text = ""
            self.open_video_player()
        elif expr == "9999":
            self.root.ids.solution.text = ""
            self.request_pin()
        else:
            try:
                result = str(eval(expr.replace("^", "**")))
                self.root.ids.result_label.text = result
            except Exception:
                self.root.ids.result_label.text = "Invalid Expression"

    def open_music_player(self):
        file_path = filechooser.open_file(title="Select Music", filters=[("*.mp3", "*.mp3")])
        if file_path:
            sound = SoundLoader.load(file_path[0])
            if sound:
                sound.play()
                self.root.ids.result_label.text = "Playing Music..."

    def open_video_player(self):
        file_path = filechooser.open_file(title="Select Video", filters=[("*.mp4", "*.mp4")])
        if file_path:
            self.root.ids.result_label.text = f"Play: {os.path.basename(file_path[0])}"
            os.system(f"am start -a android.intent.action.VIEW -d file://{file_path[0]} -t video/mp4")

    def request_pin(self):
        self.pin_dialog = MDDialog(
            title="Enter Access PIN",
            type="custom",
            content_cls=MDTextField(hint_text="Enter PIN", password=True, id="pin_input"),
            buttons=[
                MDFlatButton(text="Cancel", on_release=self.close_dialog),
                MDFlatButton(text="Unlock", on_release=self.validate_pin)
            ]
        )
        self.pin_dialog.open()

    def close_dialog(self, *args):
        self.pin_dialog.dismiss()

    def validate_pin(self, *args):
        pin = self.pin_dialog.content_cls.text
        if pin == "1234":
            self.pin_dialog.dismiss()
            self.file_locker()
        else:
            self.root.ids.result_label.text = "Incorrect PIN"
            self.pin_dialog.dismiss()

    def file_locker(self):
        file_path = filechooser.open_file(title="Select File to Lock/Unlock")
        if file_path:
            original_path = file_path[0]
            dir_name = os.path.dirname(original_path)
            base_name = os.path.basename(original_path)
            if base_name.startswith("."):
                new_name = base_name[1:]  # Unlock
            else:
                new_name = "." + base_name  # Lock
            new_path = os.path.join(dir_name, new_name)
            shutil.move(original_path, new_path)
            self.root.ids.result_label.text = f"File {'unlocked' if base_name.startswith('.') else 'locked'}: {new_name}"

if __name__ == '__main__':
    SecretCalculatorApp().run()
