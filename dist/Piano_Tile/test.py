import PySimpleGUI as sg
import pygame

class Music:

    def __init__(self, file):
        self.sound = file

    def play(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(self.sound)
        pygame.mixer.music.play()

    def volchange(volume):
        pygame.mixer.music.set_volume(volume)  # The set_volume range is from 0.00 to 1.00 (every 0.01)

    def isplaying():
        return pygame.mixer.music.get_busy()

layout = [
    [ 
     sg.Slider(key = 'volume', range=(0, 100), 
     orientation='h', size=(10, 15), default_value= 100, 
     enable_events = True)] # <--- enable slider moved event
]
window = sg.Window('Help me', layout)

while True:
    event, values = window.read()
    if event == 'Play':
        path = "D:\Project\IE221\Final Project\Piano Tiles\Musics\Dango Daikazoku.mp3"
        music = Music(path)
        music.play()
    if Music.isplaying():
        Music.volchange(float(values['volume'] / 100))