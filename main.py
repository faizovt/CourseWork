import cv2

class CopyrightDetector():
    def __init__(self, file_name=None):
        self.file_name = None
        self.resolution = 64 # Разрешение изображения QxQp

    def set_file_name(self, file_name):
        self.file_name = file_name

    def __calcimagehash(self, file_name):
        image = cv2.imread(file_name, 0)  # Прочитаем картинку
        resized = cv2.resize(image, (self.resolution, self.resolution), interpolation=cv2.INTER_AREA)  # Уменьшим картинку
        avg = resized.mean()  # Среднее значение пикселя
        ret, threshold_image = cv2.threshold(resized, avg, 255, 0)  # Бинаризация по порогу

        # Рассчитаем хэш
        _hash = ""
        for x in range(self.resolution):
            for y in range(self.resolution):
                val = threshold_image[x, y]
                if val == 255:
                    _hash = _hash + "1"
                else:
                    _hash = _hash + "0"
        return _hash

    def __comparehash(self, hash1, hash2):
        l = len(hash1)
        i = 0
        count = 0
        while i < l:
            if hash1[i] != hash2[i]:
                count = count + 1
            i = i + 1
        similarity = 1 - count / (self.resolution * self.resolution)
        if similarity >= 0.82:
            return 'Images are equal'
        else:
            return 'Images are different'

    def result(self):
        currentHash = self.__calcimagehash(self.file_name)
        count = 0
        for z in range(1, 13):
            tmpHash = self.__calcimagehash(file_name='daVinci/File' + str(z) + '.jpg')
            result = self.__comparehash(currentHash, tmpHash)
            if result == 'Images are equal':
                count += 1
        if count > 0:
            return 'Yes'
        else:
            return 'No'

Object = CopyrightDetector()
Object.set_file_name('File10.jpg')
print(Object.result())