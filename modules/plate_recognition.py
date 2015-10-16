import os
import subprocess


class AutomaticPlateRecognition():
    """A class that can be used to retrieve a numberplate out of the target image using the openalpr library.
    It has 1 method that requires a image path and it will return a number plate with the correct dashes
    """

    def get_plate(self, file):
        """Returns numberplate of given image
        :param file: image_path like static/img/test4.jpg
        :type file: string
        :return:
            If numberplate not found:
                return 'error'
            Else
                return the numberplate with correct hyphens
        """
        # alpr.exe is run and given the path to the image that should be read. the output is made up of several
        # possible plates and the program's confidence in the accuracy. This output gets assigned to plate.
        plate = str(subprocess.Popen([os.path.join(os.getcwd(), 'libs\openalpr_32\\alpr.exe'), '-c', 'eu', file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE).communicate())

        if "found" in plate:
            return "error"  # the alpr.exe returns "no license plates found" if there are no plates recognised.
                            # the word found is not in the return if plates are found, hence the error for the word "found".
        else:
            # the first result from "plate" is the one with the highest accuracy and is split from the rest.
            number_plate = list(str(plate).split('-')[1].split('\\t')[0].replace(' ', ''))
            number_plate.insert(2, '-')

            if number_plate[3] == "V":
                number_plate.insert(6, '-')
            else:
                number_plate.insert(5, '-')
            number_plate = ''.join(number_plate)
            # This checks the sequence of the plate (xx-xx-xx or xx-xxx-x etc) and puts a hyphen in the correct places.

            return number_plate
