from flask import Flask, url_for, render_template, request, redirect
import mysql.connector
import subprocess
import piexif
import os
import re
import json
import time
import exifread
from PIL import Image
from werkzeug.utils import secure_filename
from flask_mysqldb import MySQL
import PIL.ExifTags
app = Flask(__name__)
# app.config.from_envvar('YOURAPPLICATION_SETTINGS')
# app.config.from_pyfile("/home/ubuntu/init.py", silent=True)

UPLOAD_FOLDER = '/home/ubuntu/static/img/tmp/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

f = open("init.txt", "r")
host = f.readline().rstrip()
user = f.readline().rstrip()
password = f.readline().rstrip()
db = f.readline().rstrip()
f.close()


app.config['MYSQL_HOST'] = host
app.config['MYSQL_USER'] = user
app.config['MYSQL_PASSWORD'] = password
app.config['MYSQL_DB'] = db

mysql = MySQL(app)

@app.route('/')
def home():
    user_id = request.cookies.get('loggedInUser')
    if user_id:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))
    
    
@app.route('/aboutthissite/')
def aboutthissite():
    return render_template('aboutthissite.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login/', methods=["GET","POST"])
def login_page():

    try: 
        # TODO set up read_db_config
        # mydb = mysql.connector.connect(
        #   host="ec2-3-14-73-158.us-east-2.compute.amazonaws.com",
        #   user="adminUser",
        #   passwd="password123",
        #   database="rjiDB"
        # )
        # mycursor = mydb.cursor()
        mycursor = mysql.connection.cursor()
	       
        if request.method == "POST":
            validString = re.compile("^[A-Za-z0-9]*$")
            
            # handle login request
            if request.form['action'] == "loginMeIn":
                
                attempted_username = request.form['username']
                attempted_password = request.form['password']

                if not validString.match(attempted_password):
                    error = 'Invalid password. Please try again!'
                    return render_template('login.html', error = error)

                if not validString.match(attempted_username):
                    error = 'Invalid username. Please try again!'
                    return render_template('login.html', error = error)

                
                userCredentialsQuery = "SELECT * FROM User WHERE username='"+ attempted_username +"' AND password='"+ attempted_password +"'"
                
                mycursor.execute(userCredentialsQuery)

                userCredentialsQueryResult = mycursor.fetchone()
                
                if not userCredentialsQueryResult:
                    
                    error = 'Invalid username or password. Please try again!'
                    return render_template('login.html', error = error)
                    
                else:
                    response = redirect("/")
                    response.set_cookie('loggedInUser', str(userCredentialsQueryResult[0]))
                    
                    return response
                    
                
            # handle register user request
            elif request.form['action'] == "signMeUp":

                validString = re.compile("^[A-Za-z0-9']*$")
                
                attempted_first_name = request.form['first_name']
                attempted_last_name = request.form['last_name']
                attempted_email = request.form['email']
                attempted_username = request.form['username']
                attempted_password = request.form['password']

                if not validString.match(attempted_first_name):
                    error = 'Invalid characters in first name. Please try again!'
                    return render_template('login.html', error = error)
                
                if not validString.match(attempted_last_name):
                    error = 'Invalid characters in last name. Please try again!'
                    return render_template('login.html', error = error)
                
                if not validString.match(attempted_username):
                    error = 'Invalid username. Please try again!'
                    return render_template('login.html', error = error)
                
                if not validString.match(attempted_password):
                    error = 'Invalid password. Please try again!'
                    return render_template('login.html', error = error)
		          
                # check for invalid username
                # TODO do regex check
                userQuery = "SELECT * FROM User WHERE username='"+ attempted_username +"'"
                mycursor.execute(userQuery)
                userQueryResult = mycursor.fetchone()
                if userQueryResult:
                    
                    error = 'Username Taken. Please try again!'
                    return render_template('login.html', error = error)
                    
                # check for invalid email
                # TODO do regex check
                emailQuery = "SELECT * FROM User WHERE email='"+ attempted_email +"'"
                mycursor.execute(emailQuery)
                emailQueryResult = mycursor.fetchone()
                if emailQueryResult:
                    
                    error = 'This email already has an account!'
                    return render_template('login.html', error = error)
                
                try:
                    sql = "INSERT INTO User (username, password, email, first_name, last_name) VALUES (%s, %s, %s, %s, %s)"
                    val = (attempted_username, attempted_password, attempted_email, attempted_first_name, attempted_last_name)
                    mycursor.execute(sql, val)
                    mysql.connection.commit()
                    
                    userCredentialsQuery = "SELECT * FROM User WHERE username='"+ attempted_username +"' AND password='"+ attempted_password +"'"
                    mycursor.execute(userCredentialsQuery)
                    userCredentialsQueryResult = mycursor.fetchone()
                    
                except Exception as e:
                    print(e)
                    error = 'Failed to create account'
                    return render_template('login.html', error = error)
                
                # if successful, then redirect to homepage
                response = redirect("/")
                response.set_cookie('loggedInUser', userCredentialsQueryResult[0])
                return response

        return redirect(url_for('login'))

    except Exception as e:

        response = redirect(url_for('login'))
        response.set_cookie('exception', e)

        return response
    finally:
        mycursor.close()
		
# USE CASE 1
# input: folder of images or single image file
# output: new record created in database and file saved to server
# The user needs to submit an image into the system from the system homepage, since we are implementing our project as a web application we would need to use a form HTML element which will collect the image. This file is then submitted to the ‘/rating/’ route via POST method. The python flask backend verifies it has received a post request and reads the files submitted to the form, if any exist. The submitted photos are appended with a random integer at the end to avoid files with the same name and the photos are moved to specified storage on the server. Photo records are then saved to the database that take the filename and filepath inputs.

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# USE CASE 2
# input: image or image folder
# output: json array with technical and aesthetic rating of each picture
# These .jpg photos are then submitted to the neural network image assessment system. The rating system outputs a json array that contains the technical and aesthetic rating of each photo. These ratings are then added to the Photo records in the database and a JSON array that contains the file path, filename, and ratings of each file is passed to the ‘/photoGallery/’ template. For this task, the system will require: HTML, Python, MySQL, an image, a web server.
@app.route('/rating/', methods=["GET","POST"])
def rating_photos():

    # TODO set interval action that will check how old a photo is and delete old ones
    try:
        # TODO set up read_db_config
        # mydb = mysql.connector.connect(
        #   host="ec2-3-14-73-158.us-east-2.compute.amazonaws.com",
        #   user="adminUser",
        #   passwd="password123",
        #   database="rjiDB"
        # )
        # mycursor = mydb.cursor()
        mycursor = mysql.connection.cursor()
        
        user_id = request.cookies.get('loggedInUser')
        if user_id:
            if request.method == "POST":

                # delete user's previous photos from server
                userPhotosQuery = "SELECT * FROM Photo WHERE user_id="+ user_id
                mycursor.execute(userPhotosQuery)
                userPhotosQueryResults = mycursor.fetchall()
                for photo in userPhotosQueryResults:
                    removeCmd = "rm " + photo[1]
                    subprocess_cmd(removeCmd)
                
                # delete all photo records previously in the database for this user
                sql = "DELETE FROM Photo WHERE user_id = " + user_id
                mycursor.execute(sql)
                mysql.connection.commit()

                # check if the post request has the file part
                if 'file[]' not in request.files:

                    return redirect(request.url)

                filePathList = list()

                # TODO handle files with same name
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
                            mysql.connection.commit()
                            filePathList.append(absoluteFilepath)

                        except Exception as e:
                            print(e)
                            error = 'Unable to Upload Photos'
                            return redirect(url_for('/'), error=error)
                            #return render_template('home.html', error = error)

                uploaded_directory = request.files.getlist("directory[]")
                if uploaded_directory is None:
                    return redirect('/')  
                for file in uploaded_directory:
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        absoluteFilepath = app.config['UPLOAD_FOLDER'] + filename
                        file.save(absoluteFilepath)
                        try:
                            user_id = request.cookies.get('loggedInUser')
                            sql = "INSERT INTO Photo (filepath, user_id) VALUES (%s, %s)"
                            val = (absoluteFilepath, user_id)
                            mycursor.execute(sql, val)
                            mysql.connection.commit()
                            filePathList.append(absoluteFilepath)

                        except Exception as e:
                            print(e)
                            error = 'Unable to Upload Photos'
                            return redirect(url_for('/'), error=error)
                            # return render_template('home.html', error = error)
                        
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
                        mysql.connection.commit()
                    elif originalFileName != "jpg":
                        pass

                userPhotosQuery = "SELECT * FROM Photo WHERE user_id="+ user_id
                mycursor.execute(userPhotosQuery)
                userPhotosQueryResults = mycursor.fetchall()  

                for photo in userPhotosQueryResults:
                    referencePath = photo[1].replace('/home/ubuntu/','')
                    print(referencePath)
                    f = open(referencePath, 'rb')
                    # Return Exif tags
                    tags = exifread.process_file(f)
                    print(tags)
        
                userPhotosQuery = "SELECT * FROM Photo WHERE user_id="+ user_id
                mycursor.execute(userPhotosQuery)
                userPhotosQueryResults = mycursor.fetchall()
                for photo in userPhotosQueryResults:
                    print(photo[1])
                    myCommand = "cd image-quality-assessment; ./predict --docker-image nima-cpu --base-model-name MobileNet --weights-file /home/ubuntu/image-quality-assessment/models/MobileNet/weights_mobilenet_aesthetic_0.07.hdf5 --image-source " + photo[1]
                    print(myCommand)
                    subprocess_cmd(myCommand)
                    
                return redirect('/photoGallery/')
        else:
            return redirect('/login/')
	
        

    except Exception as e:
        print(e); 
        return redirect('/')
    
    finally:
        mycursor.close()
    
# help on this code from https://stackoverflow.com/questions/17742789/running-multiple-bash-commands-with-subprocess
def subprocess_cmd(command):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True)
    proc_stdout = process.communicate()[0].strip()
    print(proc_stdout)
    
# USE CASE 3
# images will have the option to click a link button that will have the attribute 'download' that will download a given picture upon mousedown
# input: mousedown
# output: download to client's machine
# The photo gallery template will dynamically load the images that are passed to it from the json object created on the backend after receiving the photo ratings. In the case of a large number of files being submitted, batches of files are loaded to the page via AJAX. The photos are displayed in a grid fashion. From here, the user will be be able to download images. A user can click an image to view more details about it or click each photo’s download button to download individually. The user also has the option to select all the photos to download via a checkbox. For this task the system will require: JavaScript, HTML, Python, an image, and a web server
@app.route('/photoGallery/')
def photo_gallery():
    
    try:
        # TODO set up read_db_config
        # mydb = mysql.connector.connect(
        #   host="ec2-3-14-73-158.us-east-2.compute.amazonaws.com",
        #   user="adminUser",
        #   passwd="password123",
        #   database="rjiDB"
        # )
        # mycursor = mydb.cursor()
        mycursor = mysql.connection.cursor()
        
        user_id = request.cookies.get('loggedInUser')
        if user_id: 

            # run each file individually, batch too slow
            #subprocess_cmd('cd image-quality-assessment; ./predict --docker-image nima-cpu --base-model-name MobileNet --weights-file /home/ubuntu/image-quality-assessment/models/MobileNet/weights_mobilenet_aesthetic_0.07.hdf5 --image-source /tmp/images')
            #subprocess.run("cd image-quality-assessment && pwd")

            userPhotosQuery = "SELECT * FROM Photo WHERE user_id=" + user_id
            mycursor.execute(userPhotosQuery)
            userPhotosQueryResults = mycursor.fetchall()

            relativePath, Rating = [], []
            for photo in userPhotosQueryResults:
                referencePath = photo[1].replace('/home/ubuntu/','')
                # {key:value mapping}

                relativePath.append(referencePath)
                Rating.append(photo[2])

            photoArray = [{"Rating": t, "relativePath": s} for t, s in zip(Rating, relativePath)]

            userPhotos = json.loads(json.dumps(photoArray))

            print(userPhotos)

            for photo in userPhotos:
                print(photo['Rating'])

            # add tags
    #        for photo in userPhotosQueryResults:
    #            exif_dict = piexif.load(photo[1])
    #            print(exif_dict['Exif'])
    #            for ifd in ("0th", "Exif", "GPS", "1st"):
    #                for tag in exif_dict[ifd]:
    #                    print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])

            return render_template("photoGallery.html", userPhotos = userPhotos, imgr = 0)
        else:
            return redirect("/login/") 
    
    except Exception as e:
        print(e)
        return redirect('/')

    finally:
        mycursor.close()


@app.route('/getRating/', methods=["GET","POST"])
def get_Rating():
    try:
        # if request.form['imgrating']:
        #option = request.form['options']
        imgr = request.form['imgrating']

        # TODO set up read_db_config
        # mydb = mysql.connector.connect(
        # host="ec2-3-14-73-158.us-east-2.compute.amazonaws.com",
        # user="adminUser",
        # passwd="password123",
        # database="rjiDB"
        # )
        # mycursor = mydb.cursor()
        mycursor = mysql.connection.cursor()
        
        user_id = request.cookies.get('loggedInUser')
        if user_id: 

            # run each file individually, batch too slow
            #subprocess_cmd('cd image-quality-assessment; ./predict --docker-image nima-cpu --base-model-name MobileNet --weights-file /home/ubuntu/image-quality-assessment/models/MobileNet/weights_mobilenet_aesthetic_0.07.hdf5 --image-source /tmp/images')
            #subprocess.run("cd image-quality-assessment && pwd")

            userPhotosQuery = "SELECT * FROM Photo WHERE user_id=" + user_id
            mycursor.execute(userPhotosQuery)
            userPhotosQueryResults = mycursor.fetchall()

            relativePath, Rating = [], []
            for photo in userPhotosQueryResults:
                referencePath = photo[1].replace('/home/ubuntu/','')
                # {key:value mapping}

                relativePath.append(referencePath)
                Rating.append(photo[2])

            photoArray = [{"Rating": t, "relativePath": s} for t, s in zip(Rating, relativePath)]

            userPhotos = json.loads(json.dumps(photoArray))

            print(userPhotos)

            # add tags
    #        for photo in userPhotosQueryResults:
    #            exif_dict = piexif.load(photo[1])
    #            print(exif_dict['Exif'])
    #            for ifd in ("0th", "Exif", "GPS", "1st"):
    #                for tag in exif_dict[ifd]:
    #                    print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])

            return render_template("photoGallery.html", userPhotos = userPhotos, imgr = float(imgr))
        else:
            return redirect("/login/") 
    
    except Exception as e:
        print(e)
        return redirect('/')

    finally:
        mycursor.close()

@app.route('/logout/')
def logout():
    response = redirect("/login/")
    response.set_cookie('loggedInUser', '', expires=0)
    return response


# USE CASE 4
# will detect which fashion to filter/sort
# ex.) descending/ascending rating, rating zone, etc.
# input: filter options
# output: updates displayed photo order
# The user will be able to filter the images based on their ratings. The user can sort by aesthetic and technical ratings in descending and ascending order. Additionally, the user can filter the displayed results by selecting an image rating range 1-10 on both measures. For this task the system will require HTML and JavaScript.
with app.test_request_context():
    url_for('static', filename='styles/mystyle.css')
    url_for('static', filename='styles/stylesheet.css')
    url_for('static', filename='scripts/myScript.js')   # USE CASE 4
    url_for('static', filename='styles/bootstrap.min.css')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
    
    

