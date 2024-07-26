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

// Uncomment the line below for debugging purposes, but remove it in production
// echo "Connected successfully";

?>
