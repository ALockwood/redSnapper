import bettercam
import re

# Primary Class for managing the "camera" and capturing frames

class Snapper():
    MIN_DIMENSION = 10
    MIN_FPS = 1

    def __init__(self, detectionBoxWidth: int = 800, detectionBoxHeight: int = 600, targetFps: int = 30):
        # Validate input
        if detectionBoxWidth <= Snapper.MIN_DIMENSION or detectionBoxHeight <= Snapper.MIN_DIMENSION or targetFps < Snapper.MIN_FPS:
            print(f"Detection box width and height must be greater than {Snapper.MIN_DIMENSION} and target FPS must be greater than {Snapper.MIN_FPS}")
            raise ValueError("Invalid input values")
        
        if detectionBoxWidth % 2 != 0 or detectionBoxHeight % 2 != 0:
            print("Detection box width and height must even numbers")
            raise ValueError("Invalid input values")

        # Find primary device and monitor
        for screen in self.get_device_info_list():
            if bool(screen['Primary']) == True:
                self.monitorId = screen['Output']
                self.gpuId = screen['Device']
                self.HRes = int(screen['ResX'])
                self.VRes = int(screen['ResY'])
                break

        if detectionBoxWidth > self.HRes or detectionBoxHeight > self.VRes:
            print("Detection box width and height must be less than the screen resolution")
            raise ValueError("Invalid configuration")

        self.target_fps = targetFps
        self.detectionX = detectionBoxWidth
        self.detectionY = detectionBoxHeight
        self.detectionBox = self.define_capture_box()

        self.cam = bettercam.create(device_idx=self.monitorId, output_idx=self.gpuId, output_color="BGR", max_buffer_len=512)
        self.cam.start(region=self.detectionBox, target_fps=self.target_fps)
        print("📸 Snapper initialized, capture started...")

    # Gets the latest frame (if changed since last call) from the buffer
    def snap(self):
        return self.cam.get_latest_frame()

    # Sets up the area to be captured by bettercam
    def define_capture_box(self):
        left, top = (self.HRes - self.detectionX) // 2, (self.VRes - self.detectionY) // 2
        right, bottom = left + self.detectionX, top + self.detectionY
        return (left, top, right, bottom)

    # A prety hacky way of getting info about the primary monitor and graphics card info
    # It's parsed out from the output of bettercam.output_info()
    # TODO: Maybe put up a PR to add a util in bettercam that returns this in a better format?
    def get_device_info_list(self):
        oplist = []
        outputs = bettercam.output_info().split('\n')

        for op in outputs:
            if op == '':
                continue

            op = op.strip().replace(", ", ",")
            device_str, info_str = op.split(': ', 1)
            info_dict = {}

            for devpart in device_str.split(' '):
                match = re.match(r'(\w+)\[(\d+)\]', devpart)
                if match:
                    key = match.group(1)
                    info_dict[key] = int(match.group(2))

            infopairs = info_str.replace('Rot', 'Rotation').split(' ')
            for pair in infopairs:
                key, value = pair.split(':')
                if key == 'Res':
                    value = value.strip('()')
                    info_dict['ResX'] = value.split(',')[0]
                    info_dict['ResY'] = value.split(',')[1]
                else:
                    info_dict[key] = value
        
            oplist.append(info_dict)
        return oplist

    # Clean shutdown of bettercam camera
    def Quit(self):
        self.cam.release