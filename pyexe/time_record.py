#!/usr/bin/python3
# For recording data(or just comments along time)
# Works like a stopwatch with comment function
import time
import sys
from pygame import mixer

time_zero = time.time()
mixer.init()
mixer.music.load('./you_suffer.mp3')

while True:
    sys.stdout.write("\r")
    time_past = time.time() - time_zero
    sys.stdout.write(str(time_past))
    sys.stdout.flush()
    print(int(time_past))
    if not int(time_past) % 720:
        mixer.music.play()
        mixer.music.play()
    # ready, _, _ = select.select([sys.stdin], [], [])
    # print(ready)
    # comment = input("Leave a comment here:")
    # print(str(time.time() - time_zero))
    # print(comment)
    
    time.sleep(1)