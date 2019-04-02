<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>Welcome to My Web Page</title>
		<link rel="stylesheet" type="text/css" href="mystyle.css">
	</head>
	<body>
		<div class="content">
		<form action="action_page.php" method="POST">
			<div class='container'>
				<h1>Welcome</h1>
				<input type="text" placeholder="Enter Username" name="username" required>
				<input type="password" placeholder="Enter Password" name="password" required>
				<?php
					if(isset($_COOKIE['access_denied'])){
                        			echo '<p class="reg_failed">Login failed</p>';	
					}
				?>
				<button type="submit">Login</button>
				<p><input type="checkbox" name="remember">Remember Me</p>
				
				<p class="password">Forgot <a href="reset_password.php">password?</a>
				</p>
				
				<p class="register"><a href="register.php">Register</a></p>
			</div>
		</form>
		</div>
	</body>
</html>
