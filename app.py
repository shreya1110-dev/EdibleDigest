from flask import Flask, render_template, request
import modules
import os

app = Flask(__name__) 

database_images = modules.add_image_paths_from_directory(modules.DATABASE_FOLDER)

@app.route('/') 
def home():  
    return render_template("index.html", title="Home")
  
@app.route('/result', methods=['GET','POST']) 
def result():  
    if request.method == 'POST':
        for file in os.listdir(modules.RESULT_FOLDER):
            os.remove(modules.RESULT_FOLDER + file)
        file = request.files.getlist("single-file-inp")
        if file[0].filename == '':
            return render_template("index.html", empty="No image uploaded", title="Results")
        file[0].save(modules.RESULT_FOLDER+file[0].filename)
        grayscale_file = modules.grayscale_images([modules.RESULT_FOLDER+file[0].filename])
        database_gs_images = modules.grayscale_images(database_images)
        orb_result = modules.orb_sim(database_gs_images, grayscale_file[0])
        similarity = orb_result['Value']
        modules.convert_tiff(database_images[orb_result['Image']], 'left')
        modules.convert_tiff(modules.RESULT_FOLDER+file[0].filename, 'right')
        print(orb_result['Value'])
        if(orb_result != -1):
            return render_template("hashes.html", similarity=similarity, title="Results", left_image_name = database_images[orb_result['Image']].split('/')[-1], right_image_name = file[0].filename)

if __name__ =='__main__':  
    app.run(debug = True)