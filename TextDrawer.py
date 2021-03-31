from PIL import Image, ImageFont, ImageDraw
from LyricFileParser import LyricsParser

class TextDrawer:
    def __init__(self, canvas_size = (640, 480),
                        font_rgba = (255, 255, 255, 255),
                        outline_rgba = (0, 0, 0, 255),
                        outline_thickness = 3,
                        font_path = "fonts/DiaryOfAn8BitMage-lYDD.ttf",
                        font_size = 26,
                        line_width_char = 30,
                        line_spacing = 4
                 ):

        self.canvas_size = canvas_size
        self.font_rgba = font_rgba
        self.outline_rgba = outline_rgba
        self.outline_thickness = outline_thickness
        self.background_rgba = (0,0,0,0)
        self.font_path = font_path
        self.font_size = font_size
        self.line_width_char = line_width_char
        self.line_spacing = line_spacing
        self.bbox = None

    @staticmethod
    def outline_coordinates(xy, thickness):
        x, y = xy
        for x_delta in range(-thickness, thickness+1):
            for y_delta in range(-thickness, thickness+1):
                yield x+x_delta, y+y_delta


    def calculate_y_shift(self, frame_cur, frame_start, frame_end, speed=1., offset_step=2):
        if speed > 0:
            speed_sign = 1.
        else:
            speed_sign = -1.
        bb_size = self.bbox[1] - self.bbox[0]
        boundaries_1 = sorted([frame_start, frame_start + int(bb_size / abs(speed))])
        boundaries_2 = sorted([frame_start + int(bb_size / speed), frame_end - int(bb_size / abs(speed))])

        if boundaries_1[0] <= frame_cur <= boundaries_1[1]:
            retval = int ( (frame_cur - frame_start) * speed - bb_size * speed_sign )
        elif boundaries_2[0] < frame_cur < boundaries_2[1]:
            retval = 0
        else:
            retval = int ( bb_size * speed_sign - (frame_end - frame_cur) * speed )

        retval = retval // offset_step
        retval *= offset_step

        return retval

    def figure_out_bounding_box(self, lyric_parsed, y0=None):
        if y0 is None:
            y0 = self.canvas_size[1] / 2
        usr_font = ImageFont.truetype(self.font_path, size=self.font_size)
        max_font_height = max([usr_font.getsize(text)[1] for _,_,text in lyric_parsed])
        max_number_of_lines = max([len(text.split('\n')) for _,_,text in lyric_parsed])
        bbox_size = max_font_height*max_number_of_lines + self.line_spacing*(max_number_of_lines-1)

        self.bbox = y0-2*self.outline_thickness, y0+bbox_size+2*self.outline_thickness


    def draw_text_with_offset_in_box(self, text, x=None, y=None, y_offset=0, anchor='ma', align='center'):
        if y is None:
            y = self.canvas_size[1] / 2

        usr_image = self.draw_text_on_canvas(text, x, y+y_offset, anchor, align)
        usr_draw = ImageDraw.Draw(usr_image)
        assert self.bbox is not None
        usr_draw.rectangle([(0, 0),(self.canvas_size[0], self.bbox[0])], fill=(0,0,0,0), outline=(0,0,0,0))
        usr_draw.rectangle([(0, self.bbox[1]), (self.canvas_size[0], self.canvas_size[1])], fill=(0, 0, 0, 0), outline=(0, 0, 0, 0))

        return usr_image


    def draw_text_on_canvas(self, text, x=None, y=None, anchor='ma', align='center'):
        if x is None:
            x = self.canvas_size[0] / 2

        if y is None:
            y = self.canvas_size[1] / 2

        usr_image = Image.new("RGBA", self.canvas_size, self.background_rgba)
        usr_font = ImageFont.truetype(self.font_path, size=self.font_size)
        usr_draw = ImageDraw.Draw(usr_image)
        usr_draw.fontmode = "1"

        # Draw the outline
        outline_xy_list = TextDrawer.outline_coordinates((x,y), self.outline_thickness)
        for outline_xy in outline_xy_list:
            usr_draw.text(outline_xy, text, fill=self.outline_rgba, anchor=anchor, align=align, font=usr_font, spacing=self.line_spacing)

        usr_draw.text((x,y), text, fill=self.font_rgba, anchor=anchor, align=align, font=usr_font, spacing=self.line_spacing)
        usr_draw.text((x,y), text, fill=self.font_rgba, anchor=anchor, align=align, font=usr_font, spacing=self.line_spacing)

        return usr_image


if __name__ == "__main__":
    canvas_size = 640, 480
    text_drawer = TextDrawer(canvas_size=canvas_size)
    text_drawer.figure_out_bounding_box(LyricsParser.parse_lyric_text("daily journey.txt"))
    usr_image = text_drawer.draw_text_with_offset_in_box("Deep down in the ocean", y_offset=-10)

    k = 0
    usr_image.show()





