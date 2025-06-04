
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivy.uix.filechooser import FileChooserListView
from kivy.core.audio import SoundLoader
from kivy.uix.video import Video
from plyer import filechooser
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
import os
import shutil

KV = '''
Screen:
    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        MDLabel:
            text: 'Secret Calculator'
            halign: 'center'
            font_style: 'H4'

        MDTextField:
            id: input_field
            hint_text: 'Enter expression or secret code'
            halign: 'right'
            size_hint_y: None
            height: '60dp'
            font_size: '24sp'

        MDRaisedButton:
            text: 'Enter'
            pos_hint: {'center_x': 0.5}
            on_release: app.evaluate_expression()

        MDLabel:
            id: result_label
            text: ''
            halign: 'center'
            theme_text_color: 'Secondary'
'''

class SecretCalculatorApp(MDApp):
    def build(self):
        self.title = "Secret Calculator"
        return Builder.load_string(KV)

    def evaluate_expression(self):
        user_input = self.root.ids.input_field.text.strip()

        if user_input == "7777":
            self.open_music_player()
        elif user_input == "8888":
            self.open_video_player()
        elif user_input == "9999":
            self.request_pin()
        else:
            try:
                result = str(eval(user_input.replace("^", "**")))
                self.root.ids.result_label.text = result
            except:
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
        if pin == "1234":  # Default access PIN
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
