import cv2
import os
from skimage.metrics import structural_similarity 
import cv2

UPLOAD_FOLDER = 'static/images/'

conversion_table = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
                    5: '5', 6: '6', 7: '7',
                    8: '8', 9: '9', 10: 'a', 11: 'b', 12: 'c',
                    13: 'd', 14: 'e', 15: 'f'}

def decimalToHexadecimal(decimal):
    hexadecimal = ''
    while(decimal > 0):
        remainder = decimal % 16
        hexadecimal = conversion_table[remainder] + hexadecimal
        decimal = decimal // 16
    return hexadecimal

def binaryToDecimal(binary):   
    decimal,i=0,0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal
     
def bintohexa(binary):
  decimal = binaryToDecimal(binary)
  return decimalToHexadecimal(decimal)

def dhash(img):
  image = cv2.resize(img, (16,16), interpolation = cv2.INTER_CUBIC)
  dhash_str = ''
  for i in range(image.shape[0]):
    for j in range(image.shape[1]-1):
      if image[i, j] > image[i, j + 1]:
        dhash_str = dhash_str + '1'
      else:
        dhash_str = dhash_str + '0'
  result = ''
  for i in range(0, image.shape[0]*(image.shape[1]-1), 1):
    result += ''.join('%x' % int(dhash_str[i: i + 1], 2))
  return result

def camphash(hash_b1, hash_b2):
  n = 0
  for i in range(len(hash_b1)):
    if hash_b1[i] == hash_b2[i]:
      pass
    else:
      n = n + 1
  return n

def add_image_paths_from_directory(directory):
  images = []
  for filename in os.listdir(directory):
      f = os.path.join(directory, filename)
      # checking if it is a file
      if os.path.isfile(f):
          images.append(f)
  return images

def grayscale_images(images):
  grayscale = []
  for img in images:
    image = cv2.imread(img)
    image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayscale.append(image_grayscale)
  return grayscale

def compute_hash(images):
  hashes = []
  for img in grayscale_images(images):
    hashes.append(bintohexa(int(dhash(img))))
  return hashes
 
def orb_sim(images, file):
    f = grayscale_images([file])[0]
    gs_images = grayscale_images(images)
    max_similarity_val = -1
    max_similarity_img = -1
    for i in range (0,len(gs_images)):
      orb = cv2.ORB_create()

      # detect keypoints and descriptors
      kp_a, desc_a = orb.detectAndCompute(gs_images[i], None)
      kp_b, desc_b = orb.detectAndCompute(f, None)

      # define the bruteforce matcher object
      bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

      #perform matches. 
      matches = bf.match(desc_a, desc_b)
      #Look for similar regions with distance < 60. .
      matches = sorted(matches, key = lambda x:x.distance)    
      similar_regions = [i for i in matches if i.distance < 60]  
      if len(matches)==0:
         return -1
      similarity = len(similar_regions) / len(matches)
      if similarity>=max_similarity_val:
        max_similarity_val = similarity
        max_similarity_img = i
    return {
          "Image":max_similarity_img,
          "Value":max_similarity_val
        }