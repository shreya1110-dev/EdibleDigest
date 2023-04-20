from flask import Flask, render_template, request
import modules
from tabulate import tabulate

app = Flask(__name__) 

@app.route('/') 
def home():  
    return render_template("index.html", title="Home")
  
@app.route('/result', methods=['GET','POST']) 
def result():  
    if request.method == 'POST':
        files = request.files.getlist("multi-file-inp")
        images = []
        for file in files:
            file.save(modules.UPLOAD_FOLDER+file.filename)
            images.append(modules.UPLOAD_FOLDER+file.filename)
        single_file = request.files.getlist("single-file-inp")
        single_file[0].save(modules.UPLOAD_FOLDER+single_file[0].filename)
        modules.add_image_paths_from_directory(modules.UPLOAD_FOLDER)
        result = modules.calculate_hashes(images, modules.UPLOAD_FOLDER+single_file[0].filename)
        if(result == 0):
            return render_template("hashes.html", result="The image to be compared belongs to the database!!", title="Results")
        else:
            result = tabulate(result, tablefmt='html')
            return render_template("hashes.html", result=result, title="Results")

if __name__ =='__main__':  
    app.run(debug = True)