from kivy.app import App
from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
import cv2
from kivy.graphics.texture import Texture

class MyImageViewerApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        
        # Load button
        self.load_button = Button(text="Load Image", size_hint=(1, 0.1))
        self.load_button.bind(on_press=self.load_image)
        
        # Image to display
        self.image = Image(size_hint=(1, 0.8))
        
        # Add button and image to layout
        self.layout.add_widget(self.load_button)
        self.layout.add_widget(self.image)
        
        return self.layout

    def load_image(self, instance):
        layout = BoxLayout(orientation="vertical")
        filechooser = FileChooserIconView(filters=['*.jpg', '*.jpeg', '*.png'])
        confirm_button = Button(text="Select", size_hint=(1, 0.1))
        
        layout.add_widget(filechooser)
        layout.add_widget(confirm_button)
        
        popup = Popup(title="Select an Image", content=layout, size_hint=(0.8, 0.8))
        
        def on_select(instance):
            if filechooser.selection:
                self.display_image(filechooser.selection[0])
                popup.dismiss()
        
        confirm_button.bind(on_press=on_select)
        popup.open()

    def display_image(self, image_path):
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to load image: {image_path}")
            return
        
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (400, 400))
        
        texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='rgb')
        texture.blit_buffer(image.tobytes(), colorfmt='rgb', bufferfmt='ubyte')
        texture.flip_vertical()
        
        self.image.texture = texture

if __name__ == "__main__":
    MyImageViewerApp().run()
