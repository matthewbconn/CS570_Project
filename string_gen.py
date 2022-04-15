import numpy as np
import sys

def main():
    f = open("input.txt","w")
    np.random.seed(5)

    linecount = 7
    arr = np.random.rand(linecount)
    x_base = "TGCAGACT"
    y_base = "CCATTAGC"
    s = x_base
    t = y_base
    for i in range(linecount):
        s = s + "\n" + str(int(1024*arr[i]) % len(s))
        t = t + "\n" + str(int(1024*arr[i]) % len(s))
    both = s + "\n" + t
    f.write(both)
    #print(both)
    f.close()


if __name__ == '__main__':
    main()
