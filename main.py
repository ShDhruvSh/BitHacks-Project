import time
from kivy.app import App
from kivy.uix.camera import Camera
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.lang import Builder

kv = Builder.load_file("screens.kv")

class PlateCamera(BoxLayout):
    # Take the current frame of the video as the photo graph
    def onCameraClick(self, *args):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("PlatePhotos/IMG_{}.png".format(timestr))

class CameraExample(App):

    def build(self):
        # return the root widget
        return PlateCamera()


# Start the Camera App
if __name__ == '__main__':
    CameraExample().run()
