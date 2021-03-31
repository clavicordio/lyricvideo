from operator import itemgetter

class LyricsParser:
    def __init__(self, text_path, separator='`'):
        self.lines_list = LyricsParser.parse_lyric_text(text_path, separator)

    def find_lyrics_time(self, timecode_seconds):
        ret_lines = []
        for sec_start, sec_end, lyric_line in self.lines_list:
            if sec_start <= timecode_seconds < sec_end:
                ret_lines.append((sec_start, sec_end, lyric_line))

        return ret_lines

    @staticmethod
    def parse_lyric_text(text_path, separator='`'):
        lines_list = []
        with open(text_path, 'r') as fp:
            for line in fp:
                lyric_line, time_start, time_end = line.split(separator)
                lyric_line = lyric_line.replace('\\n', '\n')
                m, s, ms = time_start.split(':')
                sec_start = int(m) * 60. + int(s) + int(ms) / 100.
                m, s, ms = time_end.split(':')
                sec_end = int(m) * 60. + int(s) + int(ms) / 100.
                assert sec_end > sec_start

                lines_list.append((sec_start, sec_end, lyric_line))

        lines_list.sort(key=itemgetter(0))
        return lines_list


