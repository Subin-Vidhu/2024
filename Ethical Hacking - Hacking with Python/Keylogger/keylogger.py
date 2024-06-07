import keyboard

keys = keyboard.record(until='ESC')

input('Press enter to stop recording')
keyboard.play(keys, speed_factor=1)