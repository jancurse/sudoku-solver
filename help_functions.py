def find_block(i, j):
    """
    :return: all coordinates of fields in the same block as (i,j)
    """
    I, J = int(i / 3), int(j / 3)
    block = []
    for ii in range(3):
        for jj in range(3):
            block.append((3 * I + ii, 3 * J + jj))
    return block

def to_small_square(i,j):
    """
    :return: Given coordinate (i,j) of a field, returns (ii,jj), where
    (i,j) is the jj-th number in the ii-th small square counting in lexicographic order
    """
    I, J = int(i / 3), int(j / 3)
    ii = 3*I+J
    jj = 3*(i - 3*I)+(j-3*J)
    return ii, jj

def to_big_square(ii,jj):
    """
    :return: Gives coordinates (i,j) of the jj-th field in the ii-th small square
    """
    I, II = int(ii/3), int(jj/3)
    J, JJ = ii % 3, int(jj % 3)

    i = 3*I + II
    j = 3*J + JJ
    return i, j
