# Python code to convert an image to ASCII image.
import sys, random, argparse
import numpy as np
import math
import text_to_image
import random


from PIL import Image

# gray scale level values from:
# http://paulbourke.net/dataformats/asciiart/

# 10 levels of gray
gscale2 = '17398888888'[::-1]


def getAverageL(image):

    """
    Given PIL Image, return average value of grayscale value
    """
    # get image as numpy array
    im = np.array(image)

    # get shape
    w, h = im.shape

    # get average
    return np.average(im.reshape(w * h))


def covertImageToAscii(fileName, cols, scale, moreLevels):
    """
    Given Image and dims (rows, cols) returns an m*n list of Images
    """
    # declare globals
    global gscale1, gscale2

    # open image and convert to grayscale
    image = Image.open(fileName).convert('L')

    # store dimensions
    W, H = image.size[0], image.size[1]
    print("input image dims: %d x %d" % (W, H))

    # compute width of tile
    w = W / cols

    # compute tile height based on aspect ratio and scale
    h = w / scale

    # compute number of rows
    rows = int(H / h)

    print("cols: %d, rows: %d" % (cols, rows))
    print("tile dims: %d x %d" % (w, h))

    # check if image size is too small
    if cols > W or rows > H:
        print("Image too small for specified cols!")
        exit(0)

    # ascii image is a list of character strings
    aimg = []
    # generate list of dimensions
    for j in range(rows):
        y1 = int(j * h)
        y2 = int((j + 1) * h)
        # print(y1)

        # correct last tile
        if j == rows - 1:
            y2 = H

        # append an empty string
        aimg.append("")

        for i in range(cols):

            # crop image to tile
            x1 = int(i * w)
            x2 = int((i + 1) * w)

            # correct last tile
            if i == cols - 1:
                x2 = W

            # crop image to extract tile
            img = image.crop((x1, y1, x2, y2))

            # get average luminance
            avg = int(getAverageL(img))

            # look up ascii char
            if moreLevels:
                gsval = gscale1[int((avg * 69) / 255)]
            else:
                gsval = gscale2[int((avg * 9) / 255)]

            # append ascii char to string
            aimg[j] += gsval

        # return txt image
    return aimg

def is_Prime(n):
    """
    Miller-Rabin primality test.

    A return value of False means n is certainly not prime. A return value of
    True means n is very likely a prime.
    """
    if n != int(n):
        return False
    n = int(n)
    # Miller-Rabin test for prime
    if n == 0 or n == 1 or n == 4 or n == 6 or n == 8 or n == 9:
        return False

    if n == 2 or n == 3 or n == 5 or n == 7:
        return True
    s = 0
    d = n - 1
    while d % 2 == 0:
        d >>= 1
        s += 1
    assert (2 ** s * d == n - 1)

    def trial_composite(a):
        if pow(a, d, n) == 1:
            return False
        for i in range(s):
            if pow(a, 2 ** i * d, n) == n - 1:
                return False
        return True

    for i in range(8):  # number of trials
        a = random.randrange(2, n)
        if trial_composite(a):
            return False

    return True


def mutate(num):


    pos = [random.randint(1,len(num)-1) for _ in range(103)]

    for i in pos:
        num = num[:i-1]+str(random.randint(0,9))+num[i:]

    print(pos)
    print("<<<===== mutated =====>>>")
    return num


def find_prime(num):

    print("<<<=======>>>")
    prime = 1
    found_prime = False

    maybe_prime = mutate(num)

    while found_prime == False :

        found_prime = is_Prime(int(maybe_prime))

        if found_prime :
            prime = maybe_prime
        else:
            maybe_prime = mutate(num)
        print(maybe_prime)
        return maybe_prime

    return prime


# main() function
def main():
    # create parser
    descStr = "This program converts an image into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)
    # add expected arguments
    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--asciiout', dest='outFile', required=False)
    parser.add_argument('--primeout', dest='primefile', required=False)
    parser.add_argument('--cols', dest='cols', required=False)
    parser.add_argument('--morelevels', dest='moreLevels', action='store_true')

    # parse args
    args = parser.parse_args()

    imgFile = args.imgFile

    # set output file
    outFile = args.outFile or 'out.txt'


    # set scale default as 0.43 which suits
    # a Courier font
    scale = 0.43
    if args.scale:
        scale = float(args.scale)

    # set cols
    cols = 80
    if args.cols:
        cols = int(args.cols)

    print('generating ASCII art...')
    # convert image to ascii txt
    aimg = covertImageToAscii(imgFile, cols, scale, args.moreLevels)
    print(len(aimg[0]))

    # open file
    with open(outFile, 'w+') as f:

        # write to file
        for row in aimg:
            f.write(row + '\n')

    # cleanup
    f.close()

    encoded_image_path = text_to_image.encode_file(outFile, "output_image.png")
    print("ASCII art written to %s" % outFile)

    with open(outFile,"r") as file:

        number = file.read().replace("\n", "")

    #finding the prime.

    next_prime = find_prime(number)

    size = len(aimg[0])

    string = [next_prime[i:i + size] for i in range(0, len(next_prime), size)]

    prime_file = args.primefile or "prime_file.txt"

    with open(prime_file, 'w+') as f:

        for row in string:
            f.write(row + '\n')


# call main
if __name__ == '__main__':
    main()

    # print(mutate("234567898765456898765678976545678765456765467654"))

    # k = "ad12sfasdfakdjfnakjdfnkjn"
    # print(k[4:])
    # k = k[:3]+"5"+k[4:]
    # print(k)

    # print(nextprime(int(number)))