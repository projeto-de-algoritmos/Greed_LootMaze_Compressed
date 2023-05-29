import os
from PIL import Image
from collections import Counter
from queue import PriorityQueue
import bitarray

from src.config import MAP_ASSETS_DIR
from src.config import SPRITES_DIR

class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq


def calc_freq(filename):
    img = Image.open(filename)
    pixels = img.load()

    counter = Counter()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            pixel = pixels[i, j]
            counter[pixel] += 1

    return counter


def build_tree(counter):
    q = PriorityQueue()
    for symbol, freq in counter.items():
        q.put(Node(freq, symbol))

    while q.qsize() > 1:
        l = q.get()
        r = q.get()
        node = Node(l.freq + r.freq, None, l, r)
        q.put(node)

    return q.get()


def build_codes(node, binary_string='', coding={}):
    if node is None:
        return
    if node.symbol is not None:
        coding[node.symbol] = binary_string
        return
    build_codes(node.left, binary_string + '0', coding)
    build_codes(node.right, binary_string + '1', coding)
    return coding


def huffman_encode(filename, output):
    """
    Encodes an image using Huffman coding and saves the result to a file.

    Args:
        filename (str): The name of the image file to encode.
        output (str): The name of the file to save the encoded image to.

    Usage:
        >>> huffman_encode('input.png', 'output.bin')

    """
    freq = calc_freq(filename)
    root = build_tree(freq)
    codes = build_codes(root)

    img = Image.open(filename)
    pixels = img.load()

    with open(output, 'wb') as file:
        bits = bitarray.bitarray()
        for i in range(img.size[0]):
            for j in range(img.size[1]):
                pixel = pixels[i, j]
                bits.extend(codes[pixel])
        bits.tofile(file)

def huffman_decode(filename, output, root, size):
    """
    Decodes an image using Huffman coding and saves the result to a file.

    Args:
        filename (str): The name of the file to decode.
        output (str): The name of the file to save the decoded image to.
        root (Node): The root node of the Huffman tree.
        size (tuple): The size of the image to decode.

    Usage:
        >>> huffman_decode('output.bin', 'decoded.png', root, (32, 32))

    """
    with open(filename, 'rb') as file:
        bits = bitarray.bitarray()
        bits.fromfile(file)
        bits = bits.to01()

    img = Image.new('RGBA', size)
    pixels = img.load()

    i = j = pos = 0
    while pos < len(bits):
        node = root
        while node.symbol is None:
            if bits[pos] == '0':
                node = node.left
            else:
                node = node.right
            pos += 1
        pixels[i, j] = node.symbol

        j += 1
        if j == size[0]:
            i += 1
            j = 0

    img.save(output)

def compress_map_assets():
    """
    Compress every png map from the map assets folder using huffman_encode
    """
    print("Compressing map assets...")
    for map_name in os.listdir(MAP_ASSETS_DIR):
        if map_name.endswith(".png"):
            print("Compressing map: {}".format(map_name))
            huffman_encode(os.path.join(MAP_ASSETS_DIR, map_name), os.path.join(MAP_ASSETS_DIR, map_name.replace(".png", ".bin")))


if __name__ == '__main__':
    compress_map_assets()