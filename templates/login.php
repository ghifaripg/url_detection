<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Malicious URL Detection</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css">
    <link rel="stylesheet" href="static/css/style.css"> 

</head>
<body>
    <header class="header">
        <div class="container">
            <div class="row justify-content-between align-items-center">
                <div class="col-auto">
                    <div class="logo">URL Detection</div>
                </div>
                <div class="col-auto">
                    <nav class="nav-links">
                        <a href="">Home</a>
                        <a href="#history">History</a>
                        <a href="">Account</a>
                    </nav>
                </div>
                <div class="col-auto signin_button" id="signin_button">
                    <a href="/login">
                        <button class="Btn">
                            <div class="sign">
                                <svg viewBox="0 0 512 512">
                                    <path d="M377.9 105.9L500.7 228.7c7.2 7.2 11.3 17.1 11.3 27.3s-4.1 20.1-11.3 27.3L377.9 406.1c-6.4 6.4-15 9.9-24 9.9c-18.7 0-33.9-15.2-33.9-33.9l0-62.1-128 0c-17.7 0-32-14.3-32-32l0-64c0-17.7 14.3-32 32-32l128 0 0-62.1c0-18.7 15.2-33.9 33.9-33.9c9 0 17.6 3.6 24 9.9zM160 96L96 96c-17.7 0-32 14.3-32 32l0 256c0 17.7 14.3 32 32 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32l-64 0c-53 0-96-43-96-96L0 128C0 75 43 32 96 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32z"></path>
                                </svg>
                            </div>
                            <div class="text">Sign In</div>
                        </button>
                    </a>
                </div>
                <div class="col-auto signout_button" id="signout_button" style="display: none;">
                    <a href="/logout">
                        <button class="Btn">
                            <div class="sign">
                                <svg viewBox="0 0 512 512">
                                    <path d="M377.9 105.9L500.7 228.7c7.2 7.2 11.3 17.1 11.3 27.3s-4.1 20.1-11.3 27.3L377.9 406.1c-6.4 6.4-15 9.9-24 9.9c-18.7 0-33.9-15.2-33.9-33.9l0-62.1-128 0c-17.7 0-32-14.3-32-32l0-64c0-17.7 14.3-32 32-32l128 0 0-62.1c0-18.7 15.2-33.9 33.9-33.9c9 0 17.6 3.6 24 9.9zM160 96L96 96c-17.7 0-32 14.3-32 32l0 256c0 17.7 14.3 32 32 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32l-64 0c-53 0-96-43-96-96L0 128C0 75 43 32 96 32l64 0c17.7 0 32 14.3 32 32s-14.3 32-32 32z"></path>
                                </svg>
                            </div>
                            <div class="text">Sign Out</div>
                        </button>
                    </a>
                </div>
            </div>
        </div>
    </header>

    <div class="container">
        <h1 class="animate__animated animate__fadeInDown">Malicious URL Detection</h1>
        {% if username %}
        <h1>Welcome, {{ username }}</h1>
        {% else %}
        <h1>Welcome, Guest</h1>
        <h4>Sign In to Save Your Searching History</h4>
        {% endif %}

        <form id="urlForm" class="form animate__animated animate__fadeInUp">
            <div style="position: relative;">
                <input type="text" id="url" name="url" class="input" placeholder="Enter URL">
                <div class="input-border"></div>
            </div>
            <button type="submit" class="btn btn-primary mt-3">Check</button>
        </form>
        
        <!-- Result Box -->
        <div id="result" class="mt-4 p-3 bg-light rounded" style="display: none;">
            <h3>Detection Result:</h3>
            <p id="result-text"></p>
        </div>
    </div>

    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="/static/js/script.js"></script>
    <script>
        $(document).ready(function() {
            // Check if user is authenticated (replace with your actual logic)
            const isAuthenticated = {{ username|tojson|safe }} !== null; // Check if username is defined

            if (isAuthenticated) {
                $('#signin_button').hide();
                $('#signout_button').show();
            } else {
                $('#signin_button').show();
                $('#signout_button').hide();
            }

            // Example function to simulate result display
            $('#urlForm').submit(function(event) {
                event.preventDefault();
                $('#result-text').text('URL is safe.');
                $('#result').fadeIn();
            });
        });
    </script>
</body>
</html>
