import json
import struct
from pathlib import Path
from IPython import embed

def _get_file_id():
    s = 'fspy'
    file_id = 0x00
    shift = 24
    for c in reversed(s):
        file_id |= ord(c) << shift
        shift -= 8
    return file_id


with open('saved_state_cp.json', 'rb') as f:
    s = json.load(f)
    s = json.dumps(s, indent=0)
    s = s.replace('\n', '')
    state_str = s.encode('utf-8')


img_pth = Path('img/room4.jpg')
with img_pth.open('rb') as f:
    img_buf = f.read()

file_id = ('I', _get_file_id())
version = ('I', 1)
state_size = ('I', len(state_str))
img_buf_size = ('I', img_pth.stat().st_size)
state_info = ('{}s'.format(state_size[1]), state_str)
img_info = ('{}s'.format(img_buf_size[1]), img_buf)

items = [file_id, version, state_size, img_buf_size, state_info, img_info]

fmt_str = '<'
values = []
for fmt, val in items:
    fmt_str += fmt
    values.append(val)

byte_str = struct.pack(fmt_str, *values)

with open('scene.fspy', 'wb') as f:
    f.write(byte_str)

