<?php
$servername = "localhost"; // Change this to your MySQL server hostname if it's different
$database = "csp"; // Change this to your database name
$username = "root"; // Change this to your MySQL username
$password = ""; // Change this to your MySQL password if you have one set

// Create connection
$conn = mysqli_connect($servername, $username, $password, $database);

// Check connection
if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
}

// Retrieve form data
$username = $_POST["newUsername"];
$email = $_POST["newEmail"];
$password = $_POST["newPass"];
$confirmPassword = $_POST["confirmPass"];

// Validate if passwords match
if ($password !== $confirmPassword) {
    die("Passwords do not match");
}

// Hash the password
$hashedPassword = password_hash($password, PASSWORD_DEFAULT);

// Prepare SQL query
$query_sql = "INSERT INTO users (Username, Email, Password) 
              VALUES ('$username', '$email', '$hashedPassword')";

// Execute SQL query
if (mysqli_query($conn, $query_sql)) {
    echo "<script>alert('Sign up successful'); window.location.href = 'index.html';</script>"; // Redirect with JavaScript after successful sign-up
} else {
    echo "Failed : " . mysqli_error($conn);
}
?>
