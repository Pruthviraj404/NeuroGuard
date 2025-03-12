import pygame
import time

pygame.mixer.init()

try:
    shutter_sound = pygame.mixer.Sound(r"D:\Neuroguard\audio\shuttereffect.wav")
    shutter_sound.play()
    time.sleep(2)  # Wait to hear sound
except pygame.error as e:
    print(f"Error: {e}")
