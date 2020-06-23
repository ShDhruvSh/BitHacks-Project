from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import time
reportCount = 0


class CameraWindow(Screen):
    def onCameraClick(self, *args):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        camera.export_to_png("PlatePhotos/IMG_{}.png".format(timestr))
    pass


class InfoWindow(Screen):
    def addReport(self):
        reportCount += 1
    pass


class ReportWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("screens.kv")


class CopReporter(App):
    def build(self):
        return kv

class ThankYouScreen(ScreenManager):
    pass

if __name__ == "__main__":
    CopReporter().run()
