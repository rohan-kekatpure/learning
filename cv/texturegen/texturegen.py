import argparse
from sklearn.neighbors import KDTree
import numpy as np
import cv2
from aarwild_utils.img import pad_border


def _process_args():
    desc = 'Texture synthesis script.'
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument('--input-image', dest='input_image', action='store',
                        help='Input image path', required=True)

    parser.add_argument('--output-width', dest='output_width', action='store',
                        help='Width of output image', required=True, type=int)

    parser.add_argument('--output-height', dest='output_height', action='store',
                        help='Height of output image', required=True, type=int)

    parser.add_argument('--kchild', dest='ksize_child', action='store',
                        help='Kernel size for child level', required=True, type=int)

    parser.add_argument('--kparent', dest='ksize_parent', action='store',
                        help='Kernel size for parent level', required=True, type=int)

    parser.add_argument('--output-dir', dest='output_dir', action='store',
                        help='Output directory to store images', required=True)

    parser.add_argument('--pyr-levels', dest='pyr_levels', action='store',
                        help='Number of pyramid levels', required=True, type=int)

    args = parser.parse_args()
    return args


def get_neighbourhood(pyramid, lvl, coord, ksize, mode):
    R, C = coord
    if mode == 'parent':
        R //= 2
        C //= 2

    # TODO: Pad with 'reflection' to guarantee tiling
    #  being lazy for now and tiling with white
    pad_thickness = ksize // 2
    pad_color = (255, 255, 255)
    img_padded = pad_border(pyramid[lvl], pad_thickness, pad_color)

    # get neighbourhood
    r1, r2 = R, R + ksize
    c1, c2 = C, C + ksize
    nbhd = img_padded[r1:r2, c1:c2].reshape(-1, 3)

    # If mode is child then return only the causal half of the
    # neighbourhood which is already determined. Dont fully
    # understand why.
    if mode == 'child':
        nbhd = nbhd[0: int(np.floor(ksize * ksize / 2)), :]

    return nbhd


def get_pyramid_neighbourhood(pyr, lvl, coord, ksize_child, ksize_parent):
    nbhd_child = get_neighbourhood(pyr, lvl, coord, ksize_child, mode='child')
    if lvl > 0:
        nbhd_parent = get_neighbourhood(pyr, lvl - 1, coord, ksize_parent, mode='parent')
    else:
        # For images with no long-range features, random init gives better results
        # For wood-grain images with long-range features, a zero-init gives better
        # results. There is probably some smart parameter choosing involved here.
        nbhd_parent = np.random.normal(size=(ksize_parent ** 2, 3))  # Use this for distressed iron etc
        # nbhd_parent = np.zeros((kparent ** 2, 3))  # Use this for wood etc

    pyr_nbhd = np.concatenate((nbhd_child, nbhd_parent), axis=0)
    return pyr_nbhd


# TODO: Write an exhaustive version of this function to guarantee
#  tileability. It will need to be written in C++ for efficiency
def get_match_VQ(output_pyr, input_pyr, kdtree, lvl, coord, ksize_child, ksize_parent, k):
    nbhd = get_pyramid_neighbourhood(output_pyr.pyramid, lvl, coord, ksize_child, ksize_parent)
    _, ind = kdtree.query([nbhd.reshape(-1)], k=k)
    row, col = np.unravel_index(ind[0, 0], input_pyr.pyramid[lvl].shape[:2])
    return row, col


def get_match_exhaustive():
    pass


def build_kdtree(pyr, lvl, ksize_child, ksize_parent):
    rows, cols = pyr[lvl].shape[:2]
    samples = []
    for r in range(rows):
        for c in range(cols):
            nbhd = get_pyramid_neighbourhood(pyr, lvl, [r, c], ksize_child, ksize_parent)
            samples.append(nbhd.reshape(-1))
    return KDTree(samples), len(samples)


class Pyramid:
    def __init__(self, input_img, n_levels):
        self.n_levels = n_levels
        self._build(input_img)

    def _build(self, img):
        level_img = img.copy()
        self.pyramid = [level_img]
        for i in range(self.n_levels):
            level_img = cv2.pyrDown(level_img)
            self.pyramid.insert(0, level_img)


def texturegen(input_image, output_width, output_height,
               ksize_child, ksize_parent, output_dir, n_levels):
    input_img = cv2.imread(input_image)
    input_img = input_img.astype(float) / 255.0
    if input_img.ndim == 2:
        input_img = cv2.cvtColor(input_img, cv2.COLOR_GRAY2BGR)

    input_img = input_img[:, :, :3]
    output_img = np.zeros((output_height, output_width, 3), dtype=np.float)

    # build pyramids for input and output
    input_pyrs = Pyramid(input_img, n_levels=n_levels)
    output_pyrs = Pyramid(output_img, n_levels=n_levels)

    # Seed completely random output image
    # TODO: can this be improved by sampling from input image? Paper suggests so.
    output_pyrs.pyramid[0] = np.random.normal(size=output_pyrs.pyramid[0].shape)

    for lvl in range(0, n_levels + 1):
        kdtree, n_samples = build_kdtree(input_pyrs.pyramid, lvl, ksize_child, ksize_parent)
        
        rows, cols = output_pyrs.pyramid[lvl].shape[:2]      
        for r in range(rows):
            for c in range(cols):
                mi, mj = get_match_VQ(output_pyrs, input_pyrs, kdtree, lvl, [r, c],
                                      ksize_child, ksize_parent, k=n_samples)
                output_pyrs.pyramid[lvl][r, c] = input_pyrs.pyramid[lvl][mi, mj]

            print('Level -> {}/{}, row -> {}/{}'.format(lvl, output_pyrs.n_levels, r, rows))

        outfile_name = '{}/pyr_level_{}.jpg'.format(output_dir, lvl)
        plvl_img = (output_pyrs.pyramid[lvl] * 255.0).astype(np.uint8)
        cv2.imwrite(outfile_name, plvl_img)


def main():
    args = _process_args()
    texturegen(
        args.input_image,
        args.output_width,
        args.output_height,
        args.ksize_child,
        args.ksize_parent,
        args.output_dir,
        args.pyr_levels
    )

    # Example invocation
    '''python texturegen.py --input-image=images/ex9.jpg 
                            --output-width=256 
                            --output-height=128 
                            --kchild=5 
                            --kparent=3 
                            --output-dir=output 
                            --pyr-levels=4
    '''


if __name__ == '__main__':
    main()
