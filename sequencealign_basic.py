import numpy as np


def main():
    print('Hello, World!\n')
    x, y = generate_input()
    print(x+"\n"+y+"\n")
    sequenceAlignment(x, y)


def sequenceAlignment(X, Y):
    alpha_dict = {'AA': 0, 'AC': 110, 'AG': 48, 'AT': 94, 'CA': 110, 'CC': 0, 'CG': 118, 'CT': 48, 'GA': 48, 'GC': 118,
                  'GG': 0, 'GT': 110, 'TA': 98, 'TC': 48, 'TG': 110, 'TT': 0}
    delta = 30
    m = len(X)
    n = len(Y)
    A = np.zeros((m + 1, n + 1))

    for i in range(0, m + 1):
        A[i][0] = delta * i

    for j in range(0, n + 1):
        A[0][j] = delta * j

    for j in range(1, n+1):
        for i in range(1, m+1):
            alphapair = 0
            try:
                alphapair = X[i-1] + Y[j-1]
            except:
                print("An error occurred with (i = " + str(i) + ", j = " + str(j) + ")")
            match_xy = alpha_dict.get(alphapair) + A[i-1][j-1]
            unmatchX = delta + A[i-1][j]
            unmatchY = delta + A[i][j-1]
            a_im1_jm1 = A[i-1][j-1]
            a_im1_j = A[i - 1][j]
            a_i_jm1 = A[i][j - 1]
            A[i][j] = min(alpha_dict.get(alphapair) + A[i - 1][j - 1], delta + A[i - 1][j], delta + A[i][j - 1])

    print(A)
    print("A[m][n] = " + str(A[m][n])+"\n")

    x_matching = y_matching = ""
    i = m - 1; j = n - 1
    while i >= 0 and j >= 0:
        alphapair = X[i] + Y[j]
        if A[i][j] == A[i-1][j-1] + alpha_dict.get(alphapair):
            # print("x["+str(i)+"] and y["+str(j)+"] aligned")
            x_matching = x_matching + X[i]
            y_matching = y_matching + Y[j]
            i = i - 1; j = j - 1
        elif A[i][j] == A[i-1][j] + delta:
            # print("gap on y["+str(j)+"]")
            x_matching = x_matching + X[i]
            y_matching = y_matching + '_'
            i = i - 1
        else:
            # print("gap on x[" + str(i) + "]")
            x_matching = x_matching + '_'
            y_matching = y_matching + Y[j]
            j = j - 1

    while i >= 0 or j >= 0:
        if j > 0:
            x_matching = x_matching + '_'
            y_matching = y_matching + Y[j]
            j = j - 1
        else:
            x_matching = x_matching + X[i]
            y_matching = y_matching + '_'
            i = i - 1

    x_rev_matching = x_matching[::-1]
    y_rev_matching = y_matching[::-1]
    print(x_rev_matching)
    print(y_rev_matching)

    # print("Found magic val?")
    # if 1296 in A:
    #     print(True)
    # else:
    #     print(False)


def generate_input():
    all_inputs = read_inputs()
    x_str = all_inputs[0]

    y_idx = 0
    idx = 0
    for i in range(1, len(all_inputs)):
        if type(all_inputs[i]) == int:
            idx = all_inputs[i] + 1
            base = x_str
            x_str = base[0:idx] + base + base[idx:]
        else:
            y_idx = i
            break

    y_str = all_inputs[y_idx]

    for i in range(y_idx + 1, len(all_inputs)):
        idx = all_inputs[i]+1
        base = y_str
        y_str = base[0:idx] + base + base[idx:]

    return x_str, y_str


def read_inputs():
    file = open("input.txt", 'r')
    mixed_list = []
    while True:
        next_line = file.readline().strip()
        if not next_line:
            break
        if next_line.isnumeric():
            mixed_list.append(int(next_line))
        else:
            mixed_list.append(next_line)
    file.close()

    return mixed_list


if __name__ == '__main__':
    main()
