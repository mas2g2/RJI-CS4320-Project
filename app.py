from flask import Flask, url_for, render_template, request, redirect
import mysql.connector
app = Flask(__name__)

# TODO set up read_db_config
mydb = mysql.connector.connect(
  host="ec2-3-17-206-109.us-east-2.compute.amazonaws.com",
  user="adminUser",
  passwd="password123",
  database="rjiDB"
)

mycursor = mydb.cursor()

@app.route('/')
def home():
    user_id = request.cookies.get('loggedInUser')
    if user_id:
        return render_template('home.html')
    else:
        return render_template("login.html") 
    
    
@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/login/', methods=["GET","POST"])
def login_page():

    try: 
	       
        if request.method == "POST":
            
            # handle login request
            if request.form['action'] == "loginMeIn":
                
                attempted_username = request.form['username']
                attempted_password = request.form['password']
                
                userCredentialsQuery = "SELECT * FROM User WHERE username='"+ attempted_username +"' AND password='"+ attempted_password +"'"
                
                mycursor.execute(userCredentialsQuery)

                userCredentialsQueryResult = mycursor.fetchone()
                
                if not userCredentialsQueryResult:
                    
                    error = 'Invalid username or password. Please try again!'
                    return render_template('login.html', error = error)
                    
                else:
                    
                    response = redirect("http://3.17.206.109")
                    response.set_cookie('loggedInUser', userCredentialsQueryResult[1])
                    
                    return response
                    
                
            # handle register user request
            elif request.form['action'] == "signMeUp":
                
                attempted_first_name = request.form['first_name']
                attempted_last_name = request.form['last_name']
                attempted_email = request.form['email']
                attempted_username = request.form['username']
                attempted_password = request.form['password']
		          
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
                    mydb.commit()
                    
                except Error as e:
                    error = 'Failed to create account'
                    return render_template('login.html', error = error)
                
                # if successful, then redirect to homepage
                response = redirect("http://3.17.206.109")
                response.set_cookie('loggedInUser', attempted_username)
                return response

        return redirect("http://3.17.206.109")

    except Exception as e:

        response = redirect("http://3.17.206.109")
        response.set_cookie('exception', e)

        return response
		
# USE CASE 1
# input: folder of images or single image file
# output: new record created in database and file saved to server
# The user needs to submit an image into the system from the system homepage, since we are implementing our project as a web application we would need to use a form HTML element which will collect the image. This file is then submitted to the ‘/rating/’ route via POST method. The python flask backend verifies it has received a post request and reads the files submitted to the form, if any exist. The submitted photos are appended with a random integer at the end to avoid files with the same name and the photos are moved to specified storage on the server. Photo records are then saved to the database that take the filename and filepath inputs.

# USE CASE 2
# input: image or image folder
# output: json array with technical and aesthetic rating of each picture
# These .jpg photos are then submitted to the neural network image assessment system. The rating system outputs a json array that contains the technical and aesthetic rating of each photo. These ratings are then added to the Photo records in the database and a JSON array that contains the file path, filename, and ratings of each file is passed to the ‘/photoGallery/’ template. For this task, the system will require: HTML, Python, MySQL, an image, a web server.
@app.route('/rating/', methods=["GET","POST"])
def rating_photos():

    try:
	
        if request.method == "POST":
            
            filedata = form['upload']
            
            # TODO move files to temp storage on server
            # TODO upload photo records to db
            # TODO pass photos to ranking system
            # TODO update photo records to db with ranking system's output json
            # TODO pass photo data in json array format to html template
            # TODO rediretct to photo display gallery
            
            
            
        # USE CASE 3
        # USE CASE 4
        return redirect('/photoGallery/')

    except Exception as e:

        return redirect('/')

# USE CASE 3
# images will have the option to click a link button that will have the attribute 'download' that will download a given picture upon mousedown
# input: mousedown
# output: download to client's machine
# The photo gallery template will dynamically load the images that are passed to it from the json object created on the backend after receiving the photo ratings. In the case of a large number of files being submitted, batches of files are loaded to the page via AJAX. The photos are displayed in a grid fashion. From here, the user will be be able to download images. A user can click an image to view more details about it or click each photo’s download button to download individually. The user also has the option to select all the photos to download via a checkbox. For this task the system will require: JavaScript, HTML, Python, an image, and a web server
@app.route('/photoGallery/')
def photo_gallery():
    user_id = request.cookies.get('loggedInUser')
    if user_id:
        return render_template("photoGallery.html")
    else:
        return redirect("/login/") 


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
    
    

