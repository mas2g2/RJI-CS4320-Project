<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>Welcome to My Web Page</title>
		<link rel="stylesheet" type="text/css" href="mystyle.css">	
	</head>
	<body>
		<div class="content">
			<form action="action_reg.php" method="POST">
				<div class="container">
					<p>Please fill in this form to create an account<p>
					<input type="text" placeholder="Enter Email" name="email" required>
					<input type="text" placeholder="Enter Username" name="username" required>
					<input type="password" placeholder="Enter Password" name="password" required>
					<input type="password" placeholder="Re-enter Password" name="repassword" required>
					<?php
						if(isset($_COOKIE['registration_sub'])){
							echo '<p class="reg_failed">Passwords must match</p>';
						}
						if(isset($_COOKIE['user_already_exists'])){
							echo '<p class="reg_failed">User already exists</p>';
						}	
					?>
					<p>By creating an account you agree to our Terms and Privacy</p>
					<button type="submit" class="register">Register</button>
					<p>Already have an account? <a href="index.php">Sign In</a></p>
				</div>
			</form>
		</div>
	</body>
</html>
