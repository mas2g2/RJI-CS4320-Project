<?php
	$username = "user";
        $password = "password";
        $database_name = "userstable";
        $conn = new mysqli($servername,$username,$password,$database_name);

        if($conn->connect_error){
                die("Connection failed: " .$conn->connect_error);
        }
	$username = $_POST["username"];
	$password = $_POST["password"];
	$query = "SELECT * FROM users WHERE Username = '$username' and Password = '$password'";
	if($conn->query($query) == TRUE){
		$results = $conn->query($query);
		if($results->num_rows > 0){
			echo "Access Granted";
			if(isset($_COOKIE['access_denied'])){
				setcookie('access_denied','true',time()-3600);
			}
		} else{
			echo "Access Denied";
			setcookie('access_denied','true');
			header('Location: index.php');
		}
	} else{
		echo "Error: " . $query . "<br>" . $conn->error;
	}	
?>
