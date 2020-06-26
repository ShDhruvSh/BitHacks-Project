import tensorflow as tf
import itertools
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import time
import json
import os
import OpenCV_PlateFinder
import Use_Model
from kivy.uix.textinput import TextInput

prediction = Use_Model.predictionMethods()

#plateNumber = prediction.returnDigits()
plateNumber = "00000001"
imageName = ""


class CameraWindow(Screen):
    def onCameraClick(self, *args):
        camera = self.ids['camera']
        timestr = time.strftime("%Y%m%d_%H%M%S")
        global imageName
        imageName = "IMG_" + timestr + ".png"
        camera.export_to_png(imageName)
        print("IMAGE: " + imageName)
        OpenCV_PlateFinder.scan_plate(imageName)
        global plateNumber
        plateNumber = prediction.returnDigits()
        print(plateNumber)

    pass


class ConfirmPhotoWindow(Screen):
    #plateNumber = "00000001"

    floatLayout = FloatLayout()

    def getImage(self):
        plateImage = self.ids['plate-image']
        plateImage.source = imageName
        plate0 = self.ids['plate0']
        plate1 = self.ids['plate1']
        plate2 = self.ids['plate2']
        plate3 = self.ids['plate3']
        plate4 = self.ids['plate4']
        plate5 = self.ids['plate5']
        plate6 = self.ids['plate6']
        plate7 = self.ids['plate7']

#        length = len(self.plateNumber) - 1
        length = len(plateNumber) - 1
        print (plateNumber)
        print (length)

        if length < float(plate7.text):
            plate7.size_hint = 0.005, 0.005
            plate7.size = 0, 0
        if length < float(plate6.text):
            plate6.size_hint = 0.005, 0.005
            plate6.size = 0, 0
        if length < float(plate5.text):
            plate5.size_hint = 0.005, 0.005
            plate5.size = 0, 0
        if length < float(plate4.text):
            plate4.size_hint = 0.005, 0.005
            plate4.size = 0, 0
        if length < float(plate3.text):
            plate3.size_hint = 0.005, 0.005
            plate3.size = 0, 0
        if length < float(plate2.text):
            plate2.size_hint = 0.005, 0.005
            plate2.size = 0, 0
        if length < float(plate1.text):
            plate1.size_hint = 0.005, 0.005
            plate1.size = 0, 0
        if length < float(plate0.text):
            plate0.size_hint = 0.005, 0.005
            plate0.size = 0, 0

        if length >= float(plate7.text):
#            plate7.text = self.plateNumber[7]
            plate7.text = plateNumber[7]
        else:
            plate7.text = ""
        if length >= float(plate6.text):
#            plate6.text = self.plateNumber[6]
            plate6.text = plateNumber[6]
        else:
            plate6.text = ""
        if length >= float(plate5.text):
#            plate5.text = self.plateNumber[5]
            plate5.text = plateNumber[5]
        else:
            plate5.text = ""
        if length >= float(plate4.text):
#            plate4.text = self.plateNumber[4]
            plate4.text = plateNumber[4]
        else:
            plate4.text = ""
        if length >= float(plate3.text):
#            plate3.text = self.plateNumber[3]
            plate3.text = plateNumber[3]
        else:
            plate3.text = ""
        if length >= float(plate2.text):
#            plate2.text = self.plateNumber[2]
            plate2.text = plateNumber[2]
        else:
            plate2.text = ""
        if length >= float(plate1.text):
#            plate1.text = self.plateNumber[1]
            plate1.text = plateNumber[1]
        else:
            plate1.text = ""
        if length >= float(plate0.text):
#            plate0.text = self.plateNumber[0]
            plate0.text = plateNumber[0]
        else:
            plate0.text = ""

    def replaceImage(self):
        plate_image = self.ids['plate-image']
        plate_image.source = ""

    def isNewPlate(self):
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
        plateImage = self.ids['plate-image']
        plate0 = self.ids['plate0']
        plate1 = self.ids['plate1']
        plate2 = self.ids['plate2']
        plate3 = self.ids['plate3']
        plate4 = self.ids['plate4']
        plate5 = self.ids['plate5']
        plate6 = self.ids['plate6']
        plate7 = self.ids['plate7']
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
                            # "ERROR 404 YOUR COMPUTER IS CORRUPTED INSTALL ANTIVIRUS IMMEDIATELY",
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
#            self.plateNumber =
            global plateNumber
            plateNumber = plate0.text + plate1.text + plate2.text + plate3.text + plate4.text + \
                               plate5.text + plate6.text + plate7.text
            print (plateNumber)

        else:
            self.parent.current = "second"
            self.replaceImage()
            popupWindow.open()

    pass


class EnterInfoWindow(Screen):
    def clearNameText(self):
        nameLabel = self.ids['name-label']
        if nameLabel.text == "Input name here":
            nameLabel.text = ""
        nameLabel.foreground_color = (1, 1, 1, 1)
        print(plateNumber)

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

        if nameLabel.text != "Input name here" and idLabel.text != "Input badge number here" \
                and nameLabel.text!= "" and idLabel.text != "":
            self.parent.current = "fourth"
            self.addNewInfo(nameLabel.text, idLabel.text)
            nameLabel.text = "Input name here"
            idLabel.text = "Input badge number here"
            offInfracLabel.text = "0"
            repInfracLabel.text = "0"
            nameLabel.foreground_color = (0, 0, 0, 0.4)
            nameLabel.foreground_color = (0, 0, 0, 0.4)
        else:
            self.parent.current = "third"


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
            appendString = ", \"" + plateNumber + "\" : {\"cop-id\":" + copID + ", \"name\": \"" + copName + "\", \"official-infractions\": 0, \"reported-infractions\": 0}}"
            file.write(appendString)
            # data.append(appendString)
            # json.dump(data, file)

    pass


class InfoWindow(Screen):
    def getData(self):
        #obj = ConfirmPhotoWindow()
        nameLabel = self.ids['name-label']
        idLabel = self.ids['id-label']
        offInfracLabel = self.ids['off-infrac-label']
        repInfracLabel = self.ids['rep-infrac-label']

        with open("CopDictionary.json", 'r+') as file:
            data = json.load(file)

        # plateNumber = "00000000"
        # documentedPlateFlag = False
        for PlateNums in data:
            if PlateNums == plateNumber:
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
                data[plateNumber]["reported-infractions"] += 1
                # reportDictionary = {"reported-infractions": (data[obj.plateNumber]["reported-infractions"]+1)}
                # data[obj.plateNumber].update(reportDictionary)

                file.seek(0)  # go back to beginning of file
                json.dump(data, file)
                file.truncate()

                dictionary = {
                    plateNumber: {
                        str(data[plateNumber]["reported-infractions"]): report.text
                    }
                }

            #    json.dump(data, file)
            #    file.truncate()

            # Serializing json
            # json_object = json.dumps(dictionary, indent=4)

            # Writing to reports.json
            with open("reports.json", "r+") as file:
                data = json.load(file)
                #    file.write(json_object)
                plateThere = False
                for PlateNums in data:
                    if (PlateNums == plateNumber):
                        plateThere = True

                if not plateThere:
                    data.update(dictionary)
                else:
                    data[plateNumber].update(dictionary[plateNumber])

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
