import subprocess


class Recognition:
    result = ''

    def get_number_plate(self, image_path):
        result = subprocess.Popen(['./libs/openalpr_32/alpr.exe', '-c', 'eu', image_path],
                                  stdout=subprocess.PIPE).communicate()
        number_plate = list(str(result).split('-')[1].split('\\t')[0].replace(' ', ''))
        number_plate.insert(2, '-')
        if number_plate[2] == "V":
            number_plate.insert(6, '-')
        else:
            number_plate.insert(5, '-')
        number_plate = ''.join(number_plate)
        return number_plate
