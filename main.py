import itertools

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.popup import Popup
import Factory
import time
import json

#plateNumber = ""
imageName = ""


class CameraWindow(Screen):
    def onCameraClick(self, *args):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        global imageName
        imageName = "IMG_" + timestr + ".png"
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
        layout = FloatLayout()
        popupLabel = Label(text="Error: Please click "
                                "\n\"Verify Image\" before "
                                "\nsubmitting photo!",
                           size_hint=(0.8, 1),
                           pos_hint={'x': 0.1, 'y': 0},
                           halign='center',
                           valign='middle',
                           text_size=self.size)
        popupButton = Button(text="X",
                             background_normal='',
                             background_color=(1, 0, 0, 1),
                             size_hint=(0.1, 0.05),
                             pos_hint={'x': 0.9, 'y': 0.95})
        layout.add_widget(popupLabel)
        layout.add_widget(popupButton)

        popupWindow = Popup(title="ERROR 404 YOUR COMPUTER IS CORRUPTED INSTALL ANTIVIRUS IMMEDIATELY",
                            content=layout,
                            size_hint=(None, None),
                            size=(250, 250))
        popupButton.bind(on_press=popupWindow.dismiss)

        if len(str(plateImage.source)) > 0:
            self.parent.current = "third"
            self.replaceImage()
        else:
            self.parent.current = "second"
            self.replaceImage()
            popupWindow.open()

    pass


class InfoWindow(Screen):
    plateNumber = "00000000"
    def getData(self):
        nameLabel = self.ids['name-label']
        idLabel = self.ids['id-label']
        offInfracLabel = self.ids['off-infrac-label']
        repInfracLabel = self.ids['rep-infrac-label']

        with open("CopDictionary.json", ) as read_file:
            data = json.load(read_file)

        for PlateNums in data:
            if PlateNums == plateNumber:
                nameLabel.text = "Name: " + str(data[PlateNums]["name"])
                idLabel.text = str(data[PlateNums]["cop-id"])
                offInfracLabel.text = str(data[PlateNums]["official-infractions"])
                repInfracLabel.text = str(data[PlateNums]["reported-infractions"])
            #else
                #plateNumber + ": {\"cop-id\": 1001, \"name\": \"anotherCop\", \"official-infractions\": 0, \"reported-infractions\": 0}"

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
        obj = InfoWindow()
        with open("CopDictionary.json", "r+") as file:
            data = json.load(file)
            data[obj.plateNumber]["reported-infractions"] += 1
            #reportDictionary = {"reported-infractions": (data[obj.plateNumber]["reported-infractions"]+1)}
            #data[obj.plateNumber].update(reportDictionary)

            file.seek(0)  # go back to beginning of file
            json.dump(data, file)
            file.truncate()
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


class P(Popup):
    def dismissPopup(self):
        exitButton = self.ids['exit-button']
        exitButton.on_press = lambda *args: self.popup_exit.dismiss()

    pass


kv = Builder.load_file("screens.kv")


class CopReporter(App):
    def build(self):
        return kv


if __name__ == "__main__":
    CopReporter().run()
