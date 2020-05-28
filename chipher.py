import argparse
import random

#Входная функция для шифрования
def crypt(text, xKey, yKey):
    # Создаем список из нашей строки
    text = textTransform(text, len(xKey) * len(yKey))

    # Перебирая список шифруем каждый его элемент
    result = ''
    for item in text: 
        result += encryption(item, xKey, yKey)

    setChiphertextInFile(result)

    return result

#Входная функция для дешифрования
def decrypt(ciphertext, xKey, yKey):
    # Создаем список из нашей строки
    ciphertext = textTransform(ciphertext, len(xKey) * len(yKey))

    # Перебирая список дешифруем каждый его элемент
    result = ''
    for item in ciphertext: 
        result += decryption(item, xKey, yKey)

    setDecryptTextInFile(result)

    return result

# Дешифрующая функция
def decryption(text, xKey, yKey):

    # Сортируем ключи
    xKeySorted = sorted(xKey)
    yKeySorted = sorted(yKey)

    # Создаем матрицу по отсортированным ключам(такую как создавали на последнем шаге во время шифрования)
    matrix = createMatrix(xKeySorted, yKeySorted, False)

    # Наполняем ее элементами
    i = 0        
    for x in matrix:
        matrix[x] = text[i:i+1]
        i = i + 1   

    # Создаем матрицу для чтения
    matrixForRead = createMatrix(yKey, xKey)
    text = ''

    # По ключу из матрицы для чтения находим значения в заполненной ранее матрице
    # и записываем его в переменную
    for x in matrixForRead:
        text += ''.join(matrix[x])

    return text

# Шифрующая функция
def encryption(text, xKey, yKey):

    # Создаем матрицу из ключей
    matrix = createMatrix(yKey, xKey)
    ciphertext = ''

    # Записываем нашу строку по символьно для каждого ключа (ПД => А)
    i = 0        
    for x in matrix:
        matrix[x] = text[i:i+1]
        i = i + 1

    #Сортируем значение ключей по алфавиту 
    xKey = sorted(xKey)
    yKey = sorted(yKey)

    # Создаем матрицу по которой будем считывать наш шифр
    matrixForRead = createMatrix(xKey, yKey, False)

    # По ключу из матрицы для чтения находим значения в заполненной ранее матрице
    # и записываем его в переменную
    for x in matrixForRead:
        ciphertext += ''.join(matrix[x])

    return ciphertext

# Создание матрицы 
# переменная flag показывает для каких целей создается матрица, True - для записи, False для чтения(с отсортированными ключами)
def createMatrix(key1, key2, flag = True):
    matrix = {}
    if flag:  
        for y in key1:
            for x in key2:
                matrix[y+x] = ''
    else:  
        for y in key1:
            for x in key2:
                matrix[x+y] = ''         
    return matrix

# Преобразование текста
def textTransform(text, sizeMatrix):
    # Удаляем ис строки пробелы
    text =  ''.join([x for x in text if x != ' '])

    # Если строка не заполняет полностью матрицу
    # то мы заполняем пустоты буквой "о"
    if(len(text) % sizeMatrix != 0):
        # Находим разницу для того, чтобы узнать сколько символов "о" нужно дописать
        difference = sizeMatrix - len(text) % sizeMatrix
        text = text + ''.join((difference * 'о'))

    textList = []
    starting = 0
    before = sizeMatrix

    # Заполняем список разделенными значениями нашей строки
    # кол-во сиволом в элементе списка равно размерности матрицы 
    for item in range(round(len(text)/sizeMatrix)):
        textList.append(text[starting:before])
        starting = starting + sizeMatrix
        before = before + sizeMatrix

    return textList

# Получение открытого текста из файла
def getTextFromFile(path_file):
    try:
        # Открываем файл
        open_file = open(path_file)
        # Читаем файл и удаляем различные символы преноса строк и возврата каретки
        data = open_file.read().splitlines()
        # Закрываем файл
        open_file.close()
        # Соединяем значения в полученном списке в одну строку
        return (''.join(data)).lower()
    # Исключение на случай если файла не существует    
    except FileNotFoundError:
        print("Файла не существует")
        exit()

# Записываем ключи в файл
def setKeyInFile(keys):
    open_file = open('./keys.key', 'w')
    for key in keys:
        open_file.write(key + ": " + keys.get(key) + "\n\r")

    open_file.close()

# Записываем Шифрованный текст в файл
def setChiphertextInFile(text):
    open_file = open('./chiphertext.crypt', 'w')

    open_file.write(text)

    open_file.close()    

# Записываем расшифрованый текст в файл
def setDecryptTextInFile(text):
    open_file = open("./decryptText.txt", 'w')    

    open_file.write(text)

    open_file.close() 

# Генерируем ключ
def generateKey():
    alphabet = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    xKey = ''
    yKey = ''

    # Длинна рандомного ключа составляет от 5 до 15 символов(длинна выбирается тоже рандомно)
    randomLenX = random.randint(5, 15)
    for char in range(0, randomLenX):
        xKey += alphabet[random.randint(0, 32)]

    randomLenY = random.randint(5, 15)
    for char in range(0, randomLenY):
        yKey += alphabet[random.randint(0, 32)]

    keys = {
        'xKey' : xKey,
        'yKey' : yKey
    }

    setKeyInFile(keys)

    return keys

# Функция, которая првоеряет были ли введены ключи через параметры CLI или их нужно сгенерировать рандомно
def keyCryptValidate(key1, key2):
    keys = {}
    if(key1 == None or key2 == None):
        keys = generateKey()
    else: 
        keys['xKey'] = arg.key1
        keys['yKey'] = arg.key2

    return keys    

# Функция, которая првоеряет были ли введены ключи через параметры CLI, если ключи отсутствуют просим их ввести(работает только для дешифрования)
def keyDecryptValidate(key1, key2):
    keys = {}
    if(key1 == None or key2 == None):
        print("Введите ключи, которые указаны в файле \"keys.key\"(он находится в папка с шифрующей программой)")
    else: 
        keys['xKey'] = arg.key1
        keys['yKey'] = arg.key2

    return keys      

# Создаем парсер командной строки
parser = argparse.ArgumentParser(
        description='Шифрование матричным алгоритмом', 
        usage="python3 chipher.py crypt path_file [--key1] [--key2] | python3 chipher.py decrypt path_file --key1 --key2",   
    )

# Добавляем аргументы которые нужно парсить 
parser.add_argument("action", help="Действия: crypt - зашифровать, decrypt - расшифровать")
parser.add_argument('path_file', help="Путь до файла с открытм/закрытым текстом")
parser.add_argument("-k1", "--key1", help="первый ключ для матрицы(xKey)") # xKey
parser.add_argument("-k2", "--key2", help="второй ключ для матрицы(yKey)") # yKey

# Парсим аргументы командной строки
# Если аргументы пустые то выдается стандартная ошибка пакетя для парсинга аргументов
# И подсказка для использования
try:
    arg = parser.parse_args()
except BaseException:
    parser.print_help()
    exit()


# Взависимости от параметра action производим действия
if arg.action == "crypt":
    # Получаем ключи для шифрования
    keys = keyCryptValidate(arg.key1, arg.key2)
    # Получаем тест для шифрования
    text = getTextFromFile(arg.path_file)
    # Шифруем открытый текст
    print(crypt(text, keys.get('xKey'), keys.get('yKey')))
elif arg.action == "decrypt":
    # Получаем ключи для дешифрования
    keys = keyDecryptValidate(arg.key1, arg.key2)
    # Получаем закрытй текст
    text = getTextFromFile(arg.path_file)
    # Дешифруем текс
    print(decrypt(text, keys.get('xKey'), keys.get('yKey')))
else: 
    print("Аргумента не существует")
    parser.print_help()
