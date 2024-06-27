import bettercam
import re

class Snapper():
    def __init__(self, detectionBoxWidth: int = 800, detectionBoxHeight: int = 600, targetFps: int = 30):
        # Find primary device and monitor
        for screen in self.get_device_info_list():
            if bool(screen['Primary']) == True:
                self.monitorId = screen['Output']
                self.gpuId = screen['Device']
                self.HRes = int(screen['ResX'])
                self.VRes = int(screen['ResY'])
                break

        self.target_fps = targetFps
        self.detectionX = detectionBoxWidth
        self.detectionY = detectionBoxHeight

        self.cam = bettercam.create(device_idx=self.monitorId, output_idx=self.gpuId, output_color="BGR", max_buffer_len=512)
        self.cam.start(region=self.define_capture_box(), target_fps=self.target_fps)


    def snap(self):
        return self.cam.get_latest_frame()


    def define_capture_box(self):
        left, top = (self.HRes - self.detectionX) // 2, (self.VRes - self.detectionY) // 2
        right, bottom = left + self.detectionX, top + self.detectionY
        return (left, top, right, bottom)


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

    def Quit(self):
        self.cam.release