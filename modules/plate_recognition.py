import os
import subprocess


class AutomaticPlateRecognition():
    plate = ''

    def get_plate(self, file):
        plate = str(subprocess.Popen([os.path.join(os.getcwd(), 'libs\openalpr_32\\alpr.exe'), '-c', 'eu', file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).communicate())

        if "found" in plate:
            return "error"
        else:
            number_plate = list(str(plate).split('-')[1].split('\\t')[0].replace(' ', ''))
            number_plate.insert(2, '-')
            if number_plate[3] == "V":
                number_plate.insert(6, '-')
            else:
                number_plate.insert(5, '-')
            number_plate = ''.join(number_plate)

            return number_plate

