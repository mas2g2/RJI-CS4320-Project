<!DOCTYPE html>
<html>
	<head>
		<meta charset="UTF-8">
		<title>Welcome to My Web Page</title>
		<link rel="stylesheet" type="text/css" href="mystyle.css">	
	</head>
	<body>
		<div class="content">
			<form action="action_pass.php" method="POST">
				<div class="container">
					<p>Please fill out this form to reset your password</p>
					<input type="text" placeholder="Enter Username" name="username" required>
					<input type="text" placeholder="Enter Email" name="email" required>
					<?php
						if(isset($_COOKIE['no_user'])){
                                                        echo '<p class="reg_failed">No user with this email or username</p>';
                                                }
					?>
					<button type="submit">Reset Password</button>
					<p><a href="index.php">Cancel</a><p>
				</div>
			</form>
		</div>
	</body>
</html>
