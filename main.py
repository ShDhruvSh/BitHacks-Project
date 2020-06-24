from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import time
reportCount = 0
imageName = ""

class CameraWindow(Screen):
    def onCameraClick(self, *args):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        imageName = "IMG_"+timestr+".png"
        camera.export_to_png(imageName)
    pass


class ConfirmPhotoWindow(Screen):
    def getPhoto(self):
        plate_image = self.ids['plate_image']
        plate_image.source = 'PlatePhotos/'+imageName

    pass


class InfoWindow(Screen):
    '''
    def recordData(self, plate):
        infoFile = open('*/dictionary.json', 'r')
        for CopPlates in infoFile:
            if(CopPlates == plate):
                return "cop-id", "name", "official-infractions", "reported-infractions"
            else:
                infoFile = open('*/dictionary.json', 'a')
                infoFile.truncate(2)
                infoFile.write();
    '''
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
