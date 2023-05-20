import cv2
import os

DATABASE_FOLDER = 'static/images/database'
RESULT_FOLDER = 'static/result/'

def add_image_paths_from_directory(directory):
  images = []
  for filename in os.listdir(directory):
      f = os.path.join(directory, filename)
      images.append(f)
  return images

def grayscale_images(images):
  grayscale = []
  for img in images:
    image = cv2.imread(img)
    image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    grayscale.append(image_grayscale)
  return grayscale
     
def orb_sim(images, file):
    max_similarity_val = -1
    max_similarity_img = -1
    for i in range (0,len(images)):
      orb = cv2.ORB_create()

      # detect keypoints and descriptors
      kp_a, desc_a = orb.detectAndCompute(images[i], None)
      kp_b, desc_b = orb.detectAndCompute(file, None)

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

def convert_tiff(image, name):
    tiff_image = cv2.imread(image)
    quality = 80 
    params = [int(cv2.IMWRITE_JPEG_QUALITY), quality]
    cv2.imwrite(RESULT_FOLDER + name + '.jpg', tiff_image, params)
  
