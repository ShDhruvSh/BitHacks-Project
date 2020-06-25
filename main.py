from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import time
import random
import json

reportCount = 0
imageName = ""

class CameraWindow(Screen):
    def onCameraClick(self, *args):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        global imageName
        imageName = "IMG_"+timestr+".png"
        camera.export_to_png(imageName)
    pass


class ConfirmPhotoWindow(Screen):
    def getImage(self):
        plate_image = self.ids['plate_image']
        plate_image.source = imageName

    def replaceImage(self):
        plate_image = self.ids['plate_image']
        plate_image.source = ""
    pass



class InfoWindow(Screen):
    def getData(self):
        nameLabel = self.ids['name-label']
        idLabel = self.ids['id-label']
        offInfracLabel = self.ids['off-infrac-label']
        repInfracLabel = self.ids['rep-infrac-label']
        with open("CopDictionary.json",) as read_file:
            data = json.load(read_file)
        nameLabel.text = "Name: "+str(data["00000000"]["name"])
        idLabel.text = str(data["00000000"]["cop-id"])
        offInfracLabel.text = str(data["00000000"]["official-infractions"])
        repInfracLabel.text = str(data["00000000"]["reported-infractions"])
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
