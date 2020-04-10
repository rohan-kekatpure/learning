import json
from copy import deepcopy
from struct import pack, unpack
from subprocess import check_call
import warnings

FSPY_CMD = '/Applications/fSpy.app/Contents/MacOS/fSpy'

def extract_project(file_obj, return_image_data=False):
    """
    Extracts state from a binary object representing an FSPY project.
    The state is returned as a state vector.

    The extraction is based on the FSPY file format which can be found at
    https://github.com/stuffmatic/fSpy/blob/develop/project_file_format.md

    The argument to this function is a file_object or a file_id, which
    is obtained after the open() call, prior to read. So it is
    recommended to invoke this function within a `with open(fname, 'rb') as f:`
    block. Note that the file obj must be opened in binary mode.

    Set `return_image_data` to `True` if embedded image data is needed
    (potentially multiple MBs)
    """
    project_id = unpack('<I', file_obj.read(4))[0]
    if project_id != 2037412710:
        warnings.warn('fSpy project_id != 2037412710, likely a result of bad parsing')

    project_version = unpack('<I', file_obj.read(4))[0]
    if project_version != 1:
        warnings.warn('fSpy project_version != 1, likely a result of bad parsing')

    state_string_size = unpack('<I', file_obj.read(4))[0]
    image_buffer_size = unpack('<I', file_obj.read(4))[0]

    if image_buffer_size == 0:
        warnings.warn('fSpy image_buffer_size == 0, fSpy project with no image data')

    file_obj.seek(16)
    state = json.loads(file_obj.read(state_string_size).decode('utf-8'))

    project_info = {
        'project': project_id,
        'project_version': project_version,
        'state_string_size': state_string_size,
        'image_buffer_size': image_buffer_size,
        'state': state,
        'image_data': None
    }

    if return_image_data:
        image_data = file_obj.read(image_buffer_size)
        project_info['image_data'] = image_data

    return project_info


def _get_file_id():
    s = 'fspy'
    file_id = 0x00
    shift = 24
    for c in reversed(s):
        file_id |= ord(c) << shift
        shift -= 8
    return file_id


def extract_project_from_templates():
    with open('./project_template_1vp.fspy', 'rb') as f, \
         open('./peoject_state_1vp.json', 'w') as g:
        state_1vp = extract_project(f)
        json.dump(state_1vp, g, indent=2)

    with open('./project_template_2vp.fspy', 'rb') as f, \
         open('./project_state_2vp.json', 'w') as g:
        state_2vp = extract_project(f)
        json.dump(state_2vp, g, indent=2)

def _create_fspy_binary(state_dct, img_data, outfile_name):
    s = json.dumps(state_dct, indent=0)
    s = s.replace('\n', '')
    state_str = s.encode('utf-8')

    file_id = ('I', _get_file_id())
    version = ('I', 1)
    state_size = ('I', len(state_str))
    img_buf_size = ('I', len(img_data))  # len() of a byte string is its size.
    state_info = ('{}s'.format(state_size[1]), state_str)
    img_info = ('{}s'.format(img_buf_size[1]), img_data)

    items = [file_id, version, state_size, img_buf_size, state_info, img_info]

    fmt_str = '<'
    values = []
    for fmt, val in items:
        fmt_str += fmt
        values.append(val)

    byte_str = pack(fmt_str, *values)

    with open(outfile_name, 'wb') as f:
        f.write(byte_str)


def _create_state_1vp(vp):
    with open('state_templete_1vp.json') as f:
        tmpl = json.load(f)

    state = deepcopy(tmpl)
    line = vp[0]
    vp1 = state['controlPointsStateBase']['firstVanishingPoint']
    vp1['lineSegments'] = line
    return state


def _create_state_2vp(vp):
    with open('state_templete_2vp.json') as f:
        tmpl = json.load(f)

    state = deepcopy(tmpl)
    line_1, line_2 = vp
    vp1 = state['controlPointsStateBase']['firstVanishingPoint']
    vp2 = state['controlPointsState2VP']['secondVanishingPoint']
    vp1['lineSegments'] = line_1
    vp2['lineSegments'] = line_2
    return state

def solve(img_path, scene, vanishing_segments, mode, create_fspy_binary=True):
    vp = vanishing_segments
    if mode == '1vp':
        state = _create_state_1vp(vp)
    elif mode == '2vp':
        state = _create_state_2vp(vp)
    else:
        raise ValueError('Invalid mode `{}`'.format(mode))

    # Compute camera parameters by invoking fspy commandline
    state_filename = '_pre_state.json'
    with open(state_filename, 'w') as f:
        json.dump(state, f, indent=2)

    camera_param_filename = '_camera_params.json'
    img_width = scene['img_size']['width']
    img_height = scene['img_size']['height']
    cmd_list = [
        FSPY_CMD,
        '-w', str(img_width),
        '-h', str(img_height),
        '-s', state_filename,
        '-o', camera_param_filename
    ]
    print(' '.join(cmd_list))
    check_call(cmd_list)
    with open(camera_param_filename) as f:
        solver_result = json.load(f)

    cparams = solver_result['cameraParameters']
    state['cameraParameters'] = cparams
    with open('_post_state.json', 'w') as f:
        json.dump(state, f, indent=2)

    if create_fspy_binary:
        with open(img_path, 'rb') as f:
            img_data = f.read()
        _create_fspy_binary(state, img_data, '_project.fspy')

    return cparams
