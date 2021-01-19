"""
Script to take in renders from folders and organize them into a cleaner format
https://www.spriters-resource.com/nintendo_switch/supersmashbrosultimate/
Folder structure by default:
    Nintendo Switch - Super Smash Bros Ultimate - {Character}/Super Smash Bros Ultimate/Fighter Portraits/{Character}

Desire is to grab the portraits for each character organize them in the following way:
    Square render
        Character (1)
        ...
        Character (8)
    Body render
    Full render
    Diamond render

"""
import os