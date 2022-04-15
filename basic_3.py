import time
import psutil
import sys

alpha_dict = {'AA': 0, 'AC': 110, 'AG': 48, 'AT': 94,
              'CA': 110, 'CC': 0, 'CG': 118, 'CT': 48,
              'GA': 48, 'GC': 118, 'GG': 0, 'GT': 110,
              'TA': 94, 'TC': 48, 'TG': 110, 'TT': 0}
delta = 30

def main():
    num_args = len(sys.argv)
    outpath = "output_default.txt"
    if num_args < 2:
        return ("Error, insufficient args. Expecting <input.txt> <output.txt>")
    if num_args == 3:
        outpath = str(sys.argv[2])

    inpath = str(sys.argv[1])
    x, y = generate_input(inpath)
    # print(x+"\n"+y+"\n")
    x_al, y_al, score,tdif, kb_used = sequenceAlignment(x, y)

    f = open(outpath,"w")
    s = score + "\n" + x_al + "\n" + y_al + "\n" + tdif + "\n" + kb_used
    f.write(s)
    # print(s) # delete/comment me before submission
    f.close()


def sequenceAlignment(X, Y):
    tstart = time.time()

    m = len(X)
    n = len(Y)
    A = [[0 for i in range(n+1)] for j in range(m+1)] # np.zeros((m + 1, n + 1)) #

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
            # these are just used for debugging; the next 6 lines could be deleted and everything works fine
            match_xy = alpha_dict.get(alphapair) + A[i-1][j-1]
            unmatchX = delta + A[i-1][j]
            unmatchY = delta + A[i][j-1]
            a_im1_jm1 = A[i-1][j-1]
            a_im1_j = A[i - 1][j]
            a_i_jm1 = A[i][j - 1]
            A[i][j] = min(alpha_dict.get(alphapair) + A[i - 1][j - 1], delta + A[i - 1][j], delta + A[i][j - 1])

    # print(A)
    # print("A[m-1][n] = " + str(A[m-1][n])+"\n")
    # print("A[m][n-1] = " + str(A[m][n-1])+"\n")
    # print("A[m][n] = " + str(A[m][n])+"\n")

    #print(str(sys.getsizeof(A)/(2**10)) + " KB used for A[m][n]")
    i = m
    j = n

    alphapair = "" # also for debugging

    # top = 30
    # bot = 15
    # line = "     "
    # for c in range(bot,top):
    #     line = line + "   j=" + str(c) + ""
    # print(line)
    # for a in range(bot, top):
    #     line = "i = " + str(a)
    #     for b in range(bot, top):
    #         line = line + "  " + str(A[a][b])
    #     print(line)

    x_align = ""
    y_align = ""
    while i != 0 and j != 0:
        alphapair = X[i-1] + Y[j-1]
        if A[i][j] == (A[i - 1][j - 1] + alpha_dict.get(alphapair)):
            x_align = X[i-1] + x_align
            y_align = Y[j-1] + y_align
            i = i - 1
            j = j - 1

        elif A[i][j] == (A[i][j-1] + delta):
            x_align = '_' + x_align
            y_align = Y[j-1] + y_align
            j = j - 1

        elif A[i][j] == (A[i - 1][j] + delta):
            x_align = X[i-1] + x_align
            y_align = '_' + y_align
            i = i - 1

        else:
            print("Error! at (i = " + str(i) + ", j = " + str(j) + ")")

    while i != 0: # gaps on y's
        x_align = X[i - 1] + x_align
        y_align = '_' + y_align
        i = i - 1

    while j != 0: # gaps on x's
        x_align = '_' + x_align
        y_align = Y[j - 1] + y_align
        j = j - 1

    xlen = len(x_align)
    x_out = x_align[0:50] + " " + x_align[xlen - 50:xlen]
    #print(x_out)
    ylen = len(y_align)
    y_out = y_align[0:50] + " " + y_align[ylen-50:ylen]
    #print(y_out)
    score = str(A[m][n])
    #print(str(A[m][n]))
    tfin = time.time()
    tdif = str(1.0*(tfin - tstart)*1000)

    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed= int(memory_info.rss/1024)

    return x_align,y_align,score,tdif,str(memory_consumed)
    # return x_out, y_out, score, tdif, str(memory_consumed)

def generate_input(inpath):
    all_inputs = read_inputs(inpath)
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


def read_inputs(inpath):
    file = open(inpath, 'r')
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