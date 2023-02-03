from PIL import Image
import cv2

_max_frame_id = 100

class FrameFeederGif:
    def __init__(self, gif_path, speed=1.0, scale=1.0):
        self.gif_capture = Image.open(gif_path)
        self.scale = scale
        self.frame_id = 0
        self.new_video_frame_id = 0.0
        self.speed = speed

        self.frame = None

    def read_frame(self):
        width, height = self.gif_capture.size
        if self.scale == 1.:
            self.frame = self.gif_capture. \
                convert("RGB").convert("RGBA")
        else:
            self.frame = self.gif_capture.resize((int(width * self.scale), int(height * self.scale)), Image.NEAREST). \
                convert("RGB").convert("RGBA")
        try:
            self.gif_capture.seek(self.gif_capture.tell()+1)
        except EOFError:
            self.gif_capture.seek(0)

        self.frame_id += 1

    def fix_too_big_frame_ids(self):
        if min(self.frame_id, self.new_video_frame_id) > _max_frame_id:
            self.frame_id -= _max_frame_id
            self.new_video_frame_id -= _max_frame_id

    def pop_frame(self):
        self.fix_too_big_frame_ids()
        while True:
            if self.frame_id < int(self.new_video_frame_id):
                # capture frame
                self.read_frame()
                continue

            if self.frame_id == int(self.new_video_frame_id):
                self.read_frame()
                self.new_video_frame_id += self.speed
                return self.frame

            if self.frame_id > int(self.new_video_frame_id):
                self.new_video_frame_id += self.speed
                return self.frame


if __name__ == "__main__":
    frame_reader = FrameFeederGif("data\Coast_sunset.gif", speed=1)
    while True:
        print('frame_id: {} real: {}'.format(frame_reader.frame_id, frame_reader.new_video_frame_id))
        cv2.imshow('frame', frame_reader.pop_frame())

        if cv2.waitKey(16) & 0xFF == ord('q'):
            break








