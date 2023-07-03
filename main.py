'''
    - Leggere 1 file
        - Header
            - Nome (128bit)
            - Path (256bit)
            - Numero Pixels (64bit)
    - Caricamento file
    - Scaricamento file
    - Convertire mp4 -> files
'''
from ImageParser import imageParser

PATH = "toUpload/"

t = imageParser(PATH)
t.generateImages()