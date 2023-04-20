from flask import Flask, render_template, request
import cv2
import os
from tabulate import tabulate

app = Flask(__name__) 
app.config['UPLOAD_FOLDER'] = 'static/images/'

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

def compute_hash(grayscale_images):
  hashes = []
  for img in grayscale_images:
    hashes.append(bintohexa(int(dhash(img))))
  return hashes

def calculate_hashes(images, file):
    gs_images = grayscale_images(images)
    hashes = compute_hash(gs_images)
    gs_image = grayscale_images([file])
    if file in images:
       return 0
    hashes.append(compute_hash(gs_image)[0])
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
       os.remove(app.config['UPLOAD_FOLDER']+file)
    return hashes
 
@app.route('/') 
def home():  
    return render_template("index.html")
  
@app.route('/result', methods=['GET','POST']) 
def result():  
    if request.method == 'POST':
        files = request.files.getlist("multi-file-inp")
        images = []
        for file in files:
            file.save(app.config['UPLOAD_FOLDER']+file.filename)
            images.append(app.config['UPLOAD_FOLDER']+file.filename)
        print(images)
        single_file = request.files.getlist("single-file-inp")
        print(single_file)
        single_file[0].save(app.config['UPLOAD_FOLDER']+single_file[0].filename)
        print("here",single_file[0].filename)
        result = calculate_hashes(images, app.config['UPLOAD_FOLDER']+single_file[0].filename)
        if(result == 0):
            print("here")
            return render_template("hashes.html", result="The image to be compared belongs to the database!!")
        else:
            print(result)
            result = tabulate(result, tablefmt='html')
            print(result)
            return render_template("hashes.html", result=result)

if __name__ =='__main__':  
    app.run(debug = True)