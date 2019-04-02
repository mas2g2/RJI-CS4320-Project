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
                $email = $_POST["email"];
		setcookie("Username",$username);
		$query = "select Password from users where Username='$username'";
		if($conn->query($query) == TRUE){
			if(isset($_COOKIE['no_user'])){
				setcookie('no_user','true',time()-3600);
			}
			echo "Query successful";
			$results = $conn->query($query);
			if($results->num_rows > 0){
				echo 'You got results';
				
				$value = "";
				while($row = $results->fetch_assoc()){
					echo $row["Password"];
					$value = $row["Password"];
				}
				echo $value;
				$msg = "Your password is : " . $value;
				$msg = wordwrap($msg,70);
				mail($email,"Reset Password",$msg);
				header('Location: index.php');	
			} else{
				echo "No results";
				setcookie('no_user','true');
				header('Location: reset_password.php');
				#header('Location : reset_password.php');
			}
		} else{
				echo "Query failed";	
		}
	}
?>
