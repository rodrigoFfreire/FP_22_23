matrix = ((0, 1, 1, 1), (1, 0, 1, 1), (1, 1, 0, 1), (1, 1, 1, 0))


matrix_temp = ()
for l in range(len(matrix)):
    if matrix[l][l] == 0:
        for j in range(l + 1, len(matrix)):
            if matrix[j][l] != 0 and j == len(matrix) - 1:
                print(matrix[l], matrix[j])
                matrix_temp = matrix[l:j] + (matrix[l], )
                matrix = matrix[:l] + (matrix[j], ) + matrix_temp[1:]
                break
            if matrix[j][l] != 0 and j != len(matrix) - 1:
                print(matrix[l], matrix[j])
                matrix_temp = matrix[l:j] + (matrix[l], ) + matrix[j + 1:]
                matrix = matrix[:l] + (matrix[j], ) + matrix_temp[1:]
                break
