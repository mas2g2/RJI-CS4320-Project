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
		

@app.route('/rating/', methods=["GET","POST"])
def rating_photos():

    try:
	
        if request.method == "POST":
            
            filedata = form['upload']
            # TODO give photos to ranking system
            # TODO upload photos to db
            # TODO rediretct to photo display gallery
            # Pass photo data in json form to html page
        return redirect('/photoGallery/')

    except Exception as e:

        return redirect('/')

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


with app.test_request_context():
    url_for('static', filename='styles/mystyle.css')
    url_for('static', filename='styles/stylesheet.css')
    url_for('static', filename='scripts/myScript.js')
    url_for('static', filename='styles/bootstrap.min.css')



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
    
    

