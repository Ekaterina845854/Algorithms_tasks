from PIL import Image
import numpy as np

class BitArray:
    def __init__(self, length):
        self.length = length
        self.array = [0] * ((length + 31) // 32)

    def set(self, i):
        if 0 <= i < self.length:
            self.array[i // 32] |= (1 << (i % 32))

    def __getitem__(self, i):
        if 0 <= i < self.length:
            return (self.array[i // 32] >> (i % 32)) & 1

    def __len__(self):
        return self.length

def dhash(image, hash_size=9):
    image = image.convert('L')
    image = image.resize((hash_size, hash_size))
    pixels = np.array(image)

    hash_length = 2 * ((hash_size - 1) **2) 
    bit_array = BitArray(hash_length)

    index = 0
    for row in range(hash_size):
        for col in range(hash_size - 1):
            if pixels[row][col] < pixels[row][col + 1]:
                bit_array.set(index)
            index += 1

    for col in range(hash_size):
        for row in range(hash_size - 1):
            if pixels[row][col] < pixels[row + 1][col]:
                bit_array.set(index)
            index += 1

    return bit_array

def hamming_distance(hash1, hash2):

    distance = 0
    for i in range(hash1.length):
        if hash1[i] != hash2[i]:
            distance += 1
    return distance

def are_images_similar(image_path1, image_path2, threshold):
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)

    hash1 = dhash(image1)
    hash2 = dhash(image2)

    distance = hamming_distance(hash1, hash2)
    
    if distance == threshold:
        return True, "same"
    if distance < threshold:
        return True, "similar"
    else:
        return False, distance

if __name__ == "__main__":
    imagepath1 = "D:\Infotecs\i.jpg"
    imagepath2 = "D:\Infotecs\i.jpg"
    print(are_images_similar(imagepath1, imagepath2, 10))

    