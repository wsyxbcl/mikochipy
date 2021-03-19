import math

import numpy as np


def matrix_separator(matrix, col_ref, row_ref, slope):
    """
    Separate given matrix by arbitrary line, which passes x0(col0, row0) with slope
    """
    m = matrix.shape[0]
    n = matrix.shape[1]
    grid = np.indices((m, n))
    indices_row = grid[0]
    indices_column = grid[1]

    # define the arbitrary line
    gen_mask = lambda cols, rows, s, col0, row0: s * (cols - col0) + (rows - row0) 
    # create the mask
    mask = gen_mask(indices_row, indices_column, s=slope, col0=col_ref, row0=row_ref)

    matrix_left = matrix * (mask < 0)
    matrix_middle = matrix * (mask == 0)
    matrix_right = matrix * (mask > 0)
    return matrix_left, matrix_middle, matrix_right

if __name__ == '__main__':
    matrix = np.random.rand(8, 6)
    x0 = (4, 3)
    angle = math.pi / 3
    slope = math.tan(angle)

    matrix_left, matrix_middle, matrix_right = matrix_separator(matrix, x0[0], x0[1], slope)
    print(matrix_left)
    print(matrix_right)