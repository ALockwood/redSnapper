import libs.snapper as snp
import libs.keymon as km
from PIL import Image
import threading
import os

# Constants
FILENAME_PREFIX = "capture"
CAPTURE_SUB_DIRECTORY = "rs_caps"

# Globals
localCam : snp.Snapper = None
keyWatcher : km.KeyMon = None
image_counter : int = 0


def save_image(arr):
    global image_counter
    im = Image.fromarray(arr)
    image_counter += 1
    im.save(f"{CAPTURE_SUB_DIRECTORY}/{FILENAME_PREFIX}_{image_counter}.jpg")

# Should be used as a callback, starts capturing
def start_capture():
    localCam.start_snapping()

# Should be used as a callback, stops capturing
def stop_capture():
    global image_counter
    print(f"💾  Saved {image_counter} images so far")
    localCam.stop_snapping()

# Cleanup & exit code
def exit():
    global image_counter
    keyWatcher.stop()
    localCam.Quit()
    print(f"Capture operation complete with {image_counter} images saved! 👍🚀")

# Check for subdirectory in current dir and create if it doesn't exist
def mk_subdir():
    if not os.path.exists(CAPTURE_SUB_DIRECTORY):
        os.makedirs(CAPTURE_SUB_DIRECTORY)
    print(f"📂  Capture directory: {os.getcwd()}\\{CAPTURE_SUB_DIRECTORY}")

def main():
    global localCam, keyWatcher
    localCam = snp.Snapper(detectionBoxWidth=1024, detectionBoxHeight=1024, targetFps=3)
    mk_subdir()
    keyWatcher = km.KeyMon(start_callback=start_capture, stop_callback=stop_capture)
    
    # Wait for hotkeys to be pressed
    while not keyWatcher.do_exit:
        if localCam.saveSnap:
            arr = localCam.snap()
            if arr is not None:
                threading.Thread(target=save_image, args=(arr,)).start()
    
    # Nothing to do but say goodbye...
    exit()


if __name__ == "__main__":
    main()
