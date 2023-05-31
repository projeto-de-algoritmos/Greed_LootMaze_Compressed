import pickle
import os
from PIL import Image
from collections import Counter
from queue import PriorityQueue
import bitarray
import numpy as np
import heapq
from PIL import Image

from src.config import MAP_ASSETS_DIR
from src.config import SPRITES_DIR


import heapq
import pickle
from collections import defaultdict
from PIL import Image

# RGB color to char mapping
color_to_char_map = {
    (0, 0, 0): '0',  # black
    (255, 255, 255): '1',  # white
    (0, 0, 255): '2',  # blue
    (0, 255, 0): '3'   # green
}

# Char to RGB color mapping
char_to_color_map = {v: k for k, v in color_to_char_map.items()}

# Huffman tree node class
class Node:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(string):
    frequency = defaultdict(int)
    for char in string:
        frequency[char] += 1

    heap = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)

        merged = Node(None, node1.freq + node2.freq, node1, node2)
        heapq.heappush(heap, merged)

    return heap[0]

def build_huffman_dict(node, binary_string='', huffman_dict={}):
    if node is None:
        return

    if node.char is not None:
        huffman_dict[node.char] = binary_string
        return

    build_huffman_dict(node.left, binary_string + '0', huffman_dict)
    build_huffman_dict(node.right, binary_string + '1', huffman_dict)

    return huffman_dict

def image_to_string(image_path):
    image = Image.open(image_path)
    pixels = list(image.getdata())
    image_string = ''.join(color_to_char_map[pixel[:3]] for pixel in pixels)

    root = build_huffman_tree(image_string)
    huffman_dict = build_huffman_dict(root)

    encoded_string = ''.join(huffman_dict[char] for char in image_string)

    return encoded_string, huffman_dict

def string_to_image(image_string, huffman_dict, output_path):
    reverse_huffman_dict = {v: k for k, v in huffman_dict.items()}

    decoded_string = ''
    temp = ''
    for bit in image_string:
        temp += bit
        if temp in reverse_huffman_dict:
            decoded_string += reverse_huffman_dict[temp]
            temp = ''

    pixels = [char_to_color_map[char] for char in decoded_string]
    image = Image.new('RGB', (32, 32))
    image.putdata(pixels)
    image.save(output_path)


def compress_map_assets():
    """
    Compress every png map from the map assets folder using huffman_encode
    """
    print("Compressing map assets...")
    for map_name in os.listdir(MAP_ASSETS_DIR):
        if map_name.endswith(".png"):
            print("Compressing map: {}".format(map_name))
            
            # Convert image to Huffman encoded string
            image_string, huffman_dict = image_to_string(os.path.join(MAP_ASSETS_DIR, map_name))

            # Save the huffman dictionary for later use
            with open(
                os.path.join(MAP_ASSETS_DIR, f"huffman_dict_{map_name.replace('.png', '')}.pkl"), 'wb'
            ) as f:
                pickle.dump(huffman_dict, f)

            # Save the compressed string
            with open(os.path.join(MAP_ASSETS_DIR, f"compressed_{map_name.replace('.png', '')}"), 'wb') as f:
                f.write(image_string.encode('utf-8'))
                

def decompress_map(map_name):
    """
    Decompress a map using the huffman dictionary
    """
    print("Decompressing map: {}".format(map_name))
    with open(
        os.path.join(MAP_ASSETS_DIR, f"huffman_dict_{map_name.replace('.png', '')}.pkl"), 'rb'
    ) as f:
        huffman_dict = pickle.load(f)

    with open(os.path.join(MAP_ASSETS_DIR, f"compressed_{map_name.replace('.png', '')}"), 'rb') as f:
        compressed_string = f.read()

    string_to_image(compressed_string.decode('utf-8'), huffman_dict, os.path.join(MAP_ASSETS_DIR, f'a_decompressed_{map_name}'))



if __name__ == '__main__':
    #compress_map_assets()
    decompress_map('map_2.png')