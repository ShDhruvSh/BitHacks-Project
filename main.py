import itertools

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition, SlideTransition
from kivy.uix.popup import Popup
import time
import json
import os

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
    plateNumber = "00000001"

    def getImage(self):
        plate_image = self.ids['plate_image']
        plate_image.source = imageName

    def replaceImage(self):
        plate_image = self.ids['plate_image']
        plate_image.source = ""

    def isNewPlate(self):
        plateNumber = "00000001"
        documentedPlateFlag = False

        with open("CopDictionary.json", 'r+') as file:
            data = json.load(file)

        for PlateNums in data:
            if PlateNums == plateNumber:
                documentedPlateFlag = True
            else:
                continue

        return not documentedPlateFlag

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
                             pos_hint={'x': 0.9, 'y': 0.9},
                             font_size=12)
        layout.add_widget(popupLabel)
        layout.add_widget(popupButton)

        popupWindow = Popup(title="ERROR: VERIFY IMAGE",
                            #"ERROR 404 YOUR COMPUTER IS CORRUPTED INSTALL ANTIVIRUS IMMEDIATELY",
                            content=layout,
                            size_hint=(None, None),
                            size=(250, 250))
        popupButton.bind(on_press=popupWindow.dismiss)

        if len(str(plateImage.source)) > 0:
            if self.isNewPlate():
                self.parent.current = "third"
            else:
                self.parent.current = "fourth"
            self.replaceImage()
        else:
            self.parent.current = "second"
            self.replaceImage()
            popupWindow.open()


class EnterInfoWindow(Screen):
    def clearNameText(self):
        nameLabel = self.ids['name-label']
        if nameLabel.text == "Input name here":
            nameLabel.text = ""
        nameLabel.foreground_color = (1, 1, 1, 1)

    def clearIdText(self):
        idLabel = self.ids['id-label']
        if idLabel.text == "Input badge number here":
            idLabel.text = ""
        idLabel.foreground_color = (1, 1, 1, 1)

    def clearData(self):
        nameLabel = self.ids['name-label']
        idLabel = self.ids['id-label']
        offInfracLabel = self.ids['off-infrac-label']
        repInfracLabel = self.ids['rep-infrac-label']

        self.addNewInfo(nameLabel.text, idLabel.text)

        nameLabel.text = "Input name here"
        idLabel.text = "Input id here"
        offInfracLabel.text = "0"
        repInfracLabel.text = "0"
        nameLabel.foreground_color = (0, 0, 0, 0.4)
        nameLabel.foreground_color = (0, 0, 0, 0.4)

    def addNewInfo(self, copName, copID):
        obj = ConfirmPhotoWindow()
        with open("CopDictionary.json", 'rb+') as file:
            # data = json.load(file)
            # newDictionary = {plateNumber: {"cop-id": 103, "name": "anotherCop", "official-infractions": 0, "reported-infractions": 0}}
            # data.update(newDictionary)
            file.seek(-1, os.SEEK_END)
            file.truncate()

        with open("CopDictionary.json", 'a+') as file:
            # data = json.load(file)
            appendString = ", \"" + obj.plateNumber + "\" : {\"cop-id\":" + copID + ", \"name\": \"" + copName + "\", \"official-infractions\": 0, \"reported-infractions\": 0}}"
            file.write(appendString)
            # data.append(appendString)
            # json.dump(data, file)

    pass


class InfoWindow(Screen):
    def getData(self):
        obj = ConfirmPhotoWindow()
        nameLabel = self.ids['name-label']
        idLabel = self.ids['id-label']
        offInfracLabel = self.ids['off-infrac-label']
        repInfracLabel = self.ids['rep-infrac-label']

        with open("CopDictionary.json", 'r+') as file:
            data = json.load(file)

        # plateNumber = "00000000"
        # documentedPlateFlag = False
        for PlateNums in data:
            if PlateNums == obj.plateNumber:
                nameLabel.text = "Name: " + str(data[PlateNums]["name"])
                idLabel.text = str(data[PlateNums]["cop-id"])
                offInfracLabel.text = str(data[PlateNums]["official-infractions"])
                repInfracLabel.text = str(data[PlateNums]["reported-infractions"])
                # documentedPlateFlag = True

    '''
        if documentedPlateFlag == False:
            with open("CopDictionary.json", 'rb+') as file:
                #data = json.load(file)
                # newDictionary = {plateNumber: {"cop-id": 103, "name": "anotherCop", "official-infractions": 0, "reported-infractions": 0}}
                # data.update(newDictionary)
                file.seek(-1, os.SEEK_END)
                file.truncate()

            with open("CopDictionary.json", 'a+') as file:
                #data = json.load(file)
                appendString = ", \"" + plateNumber + "\" : {\"cop-id\": 103, \"name\": \"anotherCop\", \"official-infractions\": 0, \"reported-infractions\": 0}}"
                file.write(appendString)
                #data.append(appendString)
                #json.dump(data, file)
    '''

    def clearData(self):
        nameLabel = self.ids['name-label']
        idLabel = self.ids['id-label']
        offInfracLabel = self.ids['off-infrac-label']
        repInfracLabel = self.ids['rep-infrac-label']

        nameLabel.text = "Name: "
        idLabel.text = ""
        offInfracLabel.text = ""
        repInfracLabel.text = ""

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
        obj = ConfirmPhotoWindow()
        if report.text != "" and report.text != "Type out cop's infraction here":
            with open("CopDictionary.json", "r+") as file:
                data = json.load(file)
                data[obj.plateNumber]["reported-infractions"] += 1
                # reportDictionary = {"reported-infractions": (data[obj.plateNumber]["reported-infractions"]+1)}
                # data[obj.plateNumber].update(reportDictionary)

                file.seek(0)  # go back to beginning of file
                json.dump(data, file)
                file.truncate()

                dictionary = {
                    obj.plateNumber: {
                        str(data[obj.plateNumber]["reported-infractions"]): report.text
                    }
                }

            #    json.dump(data, file)
            #    file.truncate()

            # Serializing json
            #json_object = json.dumps(dictionary, indent=4)

            # Writing to reports.json
            with open("reports.json", "r+") as file:
                data = json.load(file)
            #    file.write(json_object)
                plateThere = False
                for PlateNums in data:
                    if (PlateNums == obj.plateNumber):
                        plateThere = True

                if not plateThere:
                    data.update(dictionary)
                else:
                    data[obj.plateNumber].update(dictionary[obj.plateNumber])

                file.seek(0)  # go back to beginning of file
                file.truncate()
                json.dump(data, file)

            report.text = "Type out cop's infraction here"
            report.foreground_color = (0, 0, 0, 0.4)

            self.parent.current = "sixth"
        elif report.text == "" or report.text == "Type out cop's infraction here":
            self.parent.current = "fifth"

    def clearText(self):
        report = self.ids['report']
        if report.text == "Type out cop's infraction here":
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
