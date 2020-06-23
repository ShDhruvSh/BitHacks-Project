from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
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
        self.reportCount += 1
    pass


class ReportWindow(Screen):
    def submitReport(self):
        report = self.ids['report']
        report.text = "Type out cop's infraction here"
        report.foreground_color = (0, 0, 0, 0.4)

    def clearText(self):
        report = self.ids['report']
        report.text = ""
        report.foreground_color = (0, 0, 0, 1)
    pass


class EndWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


kv = Builder.load_file("screens.kv")


class CopReporter(App):
    def build(self):
        return kv


if __name__ == "__main__":
    CopReporter().run()
