<?php
	$servername = "localhost";
	$username = "user";
	$password = "password";
	$database_name = "userstable";
	$conn = new mysqli($servername,$username,$password,$database_name);

	if($conn->connect_error){
		die("Connection failed: " .$conn->connect_error);
	}
	else{
		$username = $_POST["username"];
		$password = $_POST["password"];
		$repassword = $_POST["repassword"];
		$email = $_POST["email"];
		$query = "SELECT * FROM users WHERE Username = '$username' or Email = '$email'";
		$result = $conn->query($query);

		if($result->num_rows > 0){
			setcookie('user_already_exists','true');
			header('Location: register.php');
		}	
		else{
			if(isset($_COOKIE['user_already_exists'])){
				setcookie('user_already_exists','true',time()-3600);
			}
			if(strcmp($repassword,$password) != 0){
				echo "Passwords don't match";
				setcookie('registration_sub','false');
				header('Location: register.php');
			}
			else{
				if(isset($_COOKIE['registration_sub'])){
					setcookie('registration_sub', "", time() - 3600);
				}	
				$_POST['registration_sub'] = true;
				$query = "INSERT INTO users VALUES ('$username','$email','$password')";
				if($conn->query($query) == TRUE){
					echo "Query successful";
					header('Location: index.php');
				} else{
					echo "Error: ".$query."<br>".$conn->error;
				}
			}
		}
	}
?>
