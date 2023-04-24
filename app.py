from flask import Flask, render_template, request
import modules
import pathlib
import os

app = Flask(__name__) 

@app.route('/') 
def home():  
    return render_template("index.html", title="Home")
  
@app.route('/result', methods=['GET','POST']) 
def result():  
    if request.method == 'POST':
        for file in os.listdir('./static/images'):
            os.remove('./static/images/'+file)
        files = request.files.getlist("multi-file-inp")
        images = []
        for file in files:
            if file.filename!='':
                file.save(modules.UPLOAD_FOLDER+file.filename)
                images.append(modules.UPLOAD_FOLDER+file.filename)
        single_file = request.files.getlist("single-file-inp")
        if len(os.listdir(modules.UPLOAD_FOLDER))==0:
            return render_template("hashes.html",empty="No images uploaded for comparison")
        single_file[0].save(modules.UPLOAD_FOLDER+single_file[0].filename)
        modules.add_image_paths_from_directory(modules.UPLOAD_FOLDER)
        orb_result = modules.orb_sim(images, modules.UPLOAD_FOLDER+single_file[0].filename)
        if(orb_result != -1):
            result = modules.compute_hash([images[orb_result["Image"]], modules.UPLOAD_FOLDER+single_file[0].filename])
            if(result == 0):
                return render_template("hashes.html", result="The image to be compared belongs to the database!!", title="Results")
            else:
                return render_template("hashes.html", image_name=images[orb_result['Image']].split('/')[-1], image=images[orb_result['Image']], similarity=orb_result['Value'], title="Results", type=pathlib.Path(images[orb_result['Image']]).suffix)

if __name__ =='__main__':  
    app.run(debug = True)