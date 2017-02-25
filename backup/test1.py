#import Tkinter as tk
from PIL import Image, ImageGrab

#root = tk.Tk()
last_image = None

def grab_it():
    global last_image
    im = ImageGrab.grab(bbox=(0,0,1980,1980))
    # Only want to save images if its a new image and is actually an image.
    # Not sure if you can compare Images this way, though - check the PIL docs.
    if im != last_image and im:
        last_image = im
        print ("aaaa")
        im.save('filename1.png')
    # This will inject your function call into Tkinter's mainloop.

grab_it() # Starts off the process