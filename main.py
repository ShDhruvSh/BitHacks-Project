from kivy.app import App
from kivy.lang import Builder
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.popup import Popup
import time
import json

plateNumber = ""
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

    def showPopup(self):
        plateImage = self.ids['plate_image']
        submitPhoto = self.ids['submit-photo']
        show = P()

        popupWindow = Popup(title = "ERROR 404 YOUR COMPUTER IS CORRUPTED INSTALL ANTIVIRUS IMMEDIATELY", content = show, size_hint = (0.5, 0.5))

        if len(str(plateImage.source)) > 0:
            self.parent.current = "third"
            self.replaceImage()
        else:
            self.parent.current = "second"
            self.replaceImage()
            popupWindow.open()
    pass



class InfoWindow(Screen):
    def getData(self):
        nameLabel = self.ids['name-label']
        idLabel = self.ids['id-label']
        offInfracLabel = self.ids['off-infrac-label']
        repInfracLabel = self.ids['rep-infrac-label']

        with open("CopDictionary.json",) as read_file:
            data = json.load(read_file)

        global plateNumber
        plateNumber = "00000000"
        for PlateNums in data:
            if PlateNums == plateNumber:
                nameLabel.text = "Name: " + str(data[PlateNums]["name"])
                idLabel.text = str(data[PlateNums]["cop-id"])
                offInfracLabel.text = str(data[PlateNums]["official-infractions"])
                repInfracLabel.text = str(data[PlateNums]["reported-infractions"])

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
        global reportCount
        reportCount += 1

    def clearText(self):
        report = self.ids['report']
        report.text = ""
        report.foreground_color = (0, 0, 0, 1)
    pass


class EndWindow(Screen):
    pass


class WindowManager(ScreenManager):
    pass


class P(FloatLayout):
    pass


kv = Builder.load_file("screens.kv")


class CopReporter(App):
    def build(self):
        return kv



if __name__ == "__main__":
    CopReporter().run()
