import snapper as snap
from PIL import Image
import threading

def save_image(arr, i):
    im = Image.fromarray(arr)
    im.save(f"test_{i}.jpeg")

def test():
    si = snap.Snapper(detectionBoxWidth=1024, detectionBoxHeight=1024, targetFps=3)
    #print(si.get_device_info_list())
    i = 0
    loop = True
    while loop:
        arr = si.snap()
        if arr is not None:
            threading.Thread(target=save_image, args=(arr, i)).start()
        i += 1
        if i == 10:
            loop = False

    si.Quit()


if __name__ == "__main__":
    test()
