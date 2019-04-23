## For Use Case 1, uploading/submitting images to the server:

Input: folder of images or image file(s)

Output: new record created in database and file saved to server

The user needs to submit an image, image folder, or multiple images into the system from the system homepage. We check for logged-in user. Since we are implementing our project as a web application we use two form HTML elements which will collect the image file(s) and/or an image folder. These files are then submitted to the ‘/rating/’ route via POST method. The python flask back-end verifies it has received a post request and reads the files submitted to the form, if any exist. We check for a good file name. Before the files are uploaded in full, all the user's previously uploaded files are deleted from the database and server. Photo records are then saved to the database that take the filename and filepath inputs. Files of type .JPG are converted to .jpg files.

    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION
     def rating_photos():

    // TODO set interval action that will check how old a photo is and delete old ones
    try:
        user_id = request.cookies.get('loggedInUser')
        if user_id:
            if request.method == "POST":

                // delete user's previous photos from server
                userPhotosQuery = "SELECT * FROM Photo WHERE user_id="+ user_id
                mycursor.execute(userPhotosQuery)
                userPhotosQueryResults = mycursor.fetchall()
                for photo in userPhotosQueryResults:
                    removeCmd = "rm " + photo[1]
                    subprocess_cmd(removeCmd)

                // delete all photo records previously in the database for this user
                sql = "DELETE FROM Photo WHERE user_id = " + user_id
                mycursor.execute(sql)
                mydb.commit()

                // check if the post request has the file part
                if 'file[]' not in request.files:

                    return redirect(request.url)

                filePathList = list()

                // TODO handle files with same name
                uploaded_files = request.files.getlist("file[]")
                if uploaded_files is None:
                    return redirect('/')
                for file in uploaded_files:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        absoluteFilepath = app.config['UPLOAD_FOLDER'] + filename
                        file.save(absoluteFilepath)
                        try:
                            user_id = request.cookies.get('loggedInUser')
                            sql = "INSERT INTO Photo (filepath, user_id) VALUES (%s, %s)"
                            val = (absoluteFilepath, user_id)
                            mycursor.execute(sql, val)
                            mydb.commit()
                            filePathList.append(absoluteFilepath)

                        except Exception as e:
                            print(e);
                            error = 'Unable to Upload Photos'
                            return render_template('home.html', error = error)

                # convert all files to lower-case .jpg
                #
                userPhotosQuery = "SELECT * FROM Photo WHERE user_id="+ user_id
                mycursor.execute(userPhotosQuery)
                userPhotosQueryResults = mycursor.fetchall()



                for photo in userPhotosQueryResults:
                    originalFileName = photo[1]
                    if originalFileName[-3:] == "JPG":
                        # change file type to jpg
                        # this assumes 3 char at end are file type
                        im = Image.open(photo[1])
                        filename = photo[1]
                        filename = filename[:-3]
                        filename += "jpg"
                        rgb_im = im.convert('RGB')
                        rgb_im.save(filename)
                        os.remove(photo[1])

                        # update record in database to jpg
                        sql = "UPDATE Photo SET filepath = '" + filename + "' WHERE filepath LIKE '" + photo[1] + "'"
                        mycursor.execute(sql)
                        mydb.commit()
                    elif originalFileName != "jpg":
                        pass
           
System requirements include: Flask, Python, HTML

## For Use Case 2, rating images:

 input: image or image folder

 output: photo records are updated in the database with the aesthetic rating

These .jpg photos are submitted to the neural network image assessment system after the user uploads the image to the server through the home page and a box comes up with the options to upload a folder of images or a set of image files and the option to Rate Photos. When the user clicks Rate Photos the image(s) will be uploaded and run through the rating system. The rating system will update existing photo records in the database with the aesthetic rating of each photo. A json array of all the Photo records for the logged-in user will be passed to the ‘/photoGallery/’ template. In the '/photoGallery/', the user will be able to see the images that were uploaded. To check the rating for every image, the user will click a button underneath each image, the button is labeled with the text 'More Information'.


               userPhotosQuery = "SELECT * FROM Photo WHERE user_id="+ user_id
                mycursor.execute(userPhotosQuery)
                userPhotosQueryResults = mycursor.fetchall()
                for photo in userPhotosQueryResults:
                    print(photo[1])
                    myCommand = "cd image-quality-assessment; ./predict --docker-image nima-cpu --base-model-name   MobileNet --weights-file /home/ubuntu/image-quality-assessment/models/MobileNet/weights_mobilenet_aesthetic_0.07.hdf5 --image-source " + photo[1]
                    print(myCommand)
                    subprocess_cmd(myCommand)

                return redirect('/photoGallery/')
        else:
            return redirect('/login/')



    except Exception as e:

        print(e);
        return redirect('/')


For this task, the system will require: HTML, Python, MySQL, an image or a folder, a web server and Flask.
The system will also require the following code for performing predictions, this code can be found in the repository idealo/image-quality-assessment in the directory src/evaluater/predict.py:

         def predict(model, data_generator):
    return model.predict_generator(data_generator, workers=8, use_multiprocessing=True, verbose=1)


    def main(base_model_name, weights_file, image_source, predictions_file, img_format='jpg'):
    print(weights_file)
    # load samples
    if os.path.isfile(image_source):
        image_dir, samples = image_file_to_json(image_source)
    else:
        image_dir = image_source
        samples = image_dir_to_json(image_dir, img_type='jpg')

    # build model and load weights
    nima = Nima(base_model_name, weights=None)
    nima.build()
    nima.nima_model.load_weights(weights_file)

    # initialize data generator
    data_generator = TestDataGenerator(samples, image_dir, 64, 10, nima.preprocessing_function(),
                                       img_format=img_format)

    # get predictions

    predictions = predict(nima.nima_model, data_generator)

    # calc mean scores and add to samples
    for i, sample in enumerate(samples):
        sample['mean_score_prediction'] = calc_mean_score(predictions[i])

    myJson = json.loads(json.dumps(samples, indent=2))
    #print(myJson)
    #print("hello")
    # TODO set up read_db_config


    for photo in myJson:
        print(photo['image_id'])
        sql = "UPDATE Photo SET aesthetic_rating = " + str(photo['mean_score_prediction']) + " WHERE filepath LIKE '%" + photo['image_id'] + "%'"
        mycursor.execute(sql)
        mydb.commit()


## For Use Case 3, download images:
Every Image will have a download button around it which will  allow the user to download the image

input: mousedown

output: download to client's machine

The photo gallery template will dynamically load the images that are passed to it from the json array created on the back-end after receiving the photo ratings. In the case of a large number of files being submitted, we dynamically load the photos to the display as the user scrolls down, via lazy loading. The photos are displayed in a grid fashion. From here, the user will be be able to download images. A user can click an image's button to view more details about it or click each photo to download individually. 
   
    @app.route('/photoGallery/')
    def photo_gallery():
    user_id = request.cookies.get('loggedInUser')
    if user_id:
    // run each file individually, batch too slow        

        userPhotosQuery = "SELECT * FROM Photo WHERE user_id="+ user_id
        mycursor.execute(userPhotosQuery)
        userPhotosQueryResults = mycursor.fetchall()


        

        return render_template("photoGallery.html", userPhotos =userPhotosQueryResults)
    else:
        return redirect("/login/")


     <div class="container-fluid prevwebpage" id="graphicstage">

     {% if userPhotos %}
        {% set count = 1 %}
        {% for photo_row in userPhotos | batch(4, '&nbsp;')  | sort(attribute='Rating')%}
        <div class="row showcaserow  wow fadeIn">
            {% for photo in photo_row %}
            {% if photo['Rating'] > imgr %}
            <div class="col-md-3">
                <a class="download" href="{{'../' + photo['relativePath']}}" download="{{'../' + photo['relativePath']}}"><p class="center"><img src="{{'../' + photo['relativePath']}}" alt="Image: {{ '../' + photo['relativePath']}}" class="img-responsive centerimg previewborder"></p></a><br>
                <p class="center"><button type="button" class="btn btn-primary btn-lg" data-toggle="modal" data-target="#img{{count}}">
                  More Information
                </button></p>

                <div class="modal fade" id="img{{count}}" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
                  <div class="modal-dialog" role="document">
                    <div class="modal-content">
                      <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                        <h4 class="modal-title center pmodal" id="myModalLabel">Image Submited by [USERNAME]</h4>
                      </div>
                      <div class="modal-body">
                        <p class="pmodal">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vel justo sit amet arcu auctor hendrerit. Vestibulum ornare eget libero eget lacinia. Suspendisse potenti. Suspendisse aliquam libero non lectus accumsan, et luctus quam pretium. Etiam suscipit erat eget erat mattis.</p>
                          <p class="pmodal">Category: [CATEGORY]</p>
                          <p class="pmodal">Rating: {{photo['Rating']}}</p>
                      </div>
                      <div class="modal-footer">
                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                      </div>
                    </div>
                  </div>
                </div>
            </div>
            {% endif %}
            {% set count = count + 1 %}
            {% endfor %}
        </div>
        {% endfor %}
    {% endif %} 

For this task the system will require: JavaScript, HTML, Python, an image or an image folder, and a web server


        
As the system currently works, after each image is rated, the image file path and the rating are stored in the database, and the user will be directed to the photo gallery web page, but the images that were uploaded to the server will not be displayed. With the rating.

## For Use Case 4 filtering and sorting through images based on rating:
Detects which fashion to filter/sort, such as descending/ascending rating, rating zone, etc.

 input: filter options

 output: updates displayed photo order

The user will be able to filter the images based on their ratings. Specifically, the user can filter the displayed results by selecting a minimum rating. Photos that are below the threshold are hidden from the display. For this task the system will require HTML and JavaScript.

              <form action="/getRating/" method="POST">
                  <input type="radio" name="imgrating" id="imgr0" value="0" checked> 0    
                  <input type="radio" name="imgrating" id="imgr1" value="1"> 1
                  <input type="radio" name="imgrating" id="imgr2" value="2"> 2
                  <input type="radio" name="imgrating" id="imgr3" value="3"> 3
                  <input type="radio" name="imgrating" id="imgr4" value="4"> 4
                  <input type="radio" name="imgrating" id="imgr5" value="5"> 5
                  <input type="radio" name="imgrating" id="imgr6" value="6"> 6
                  <input type="radio" name="imgrating" id="imgr7" value="7"> 7
                  <input type="radio" name="imgrating" id="imgr8" value="8"> 8
                  <input type="radio" name="imgrating" id="imgr9" value="9"> 9
                  <input type="radio" name="imgrating" id="imgr10" value="10"> 10
                    <input class="btn downloadbtn" type="submit" value="Submit">
                </form>



    {% if userPhotos %}
        {% set count = 1 %}
        {% for photo_row in userPhotos | batch(4, '&nbsp;')  | sort(attribute='Rating')%}
        <div class="row showcaserow  wow fadeIn">
            {% for photo in photo_row %}
            {% if photo['Rating'] > imgr %}
            <div class="col-md-3">
                <a class="download" href="{{'../' + photo['relativePath']}}" download="{{'../' + photo['relativePath']}}"><p class="center"><img src="{{'../' + photo['relativePath']}}" alt="Image: {{ '../' + photo['relativePath']}}" class="img-responsive centerimg previewborder"></p></a><br>
                <p class="center"><button type="button" class="btn btn-primary btn-lg" data-toggle="modal" data-target="#img{{count}}">
                  More Information
                </button></p>

                <div class="modal fade" id="img{{count}}" tabindex="-1" role="dialog" aria-labelledby="myModalLabel">
                  <div class="modal-dialog" role="document">
                    <div class="modal-content">
                      <div class="modal-header">
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                        <h4 class="modal-title center pmodal" id="myModalLabel">Image Submited by [USERNAME]</h4>
                      </div>
                      <div class="modal-body">
                        <p class="pmodal">Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec vel justo sit amet arcu auctor hendrerit. Vestibulum ornare eget libero eget lacinia. Suspendisse potenti. Suspendisse aliquam libero non lectus accumsan, et luctus quam pretium. Etiam suscipit erat eget erat mattis.</p>
                          <p class="pmodal">Category: [CATEGORY]</p>
                          <p class="pmodal">Rating: {{photo['Rating']}}</p>
                      </div>
                      <div class="modal-footer">
                        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
                      </div>
                    </div>
                  </div>
                </div>
            </div>
            {% endif %}
            {% set count = count + 1 %}
            {% endfor %}
        </div>
        {% endfor %}
    {% endif %}

