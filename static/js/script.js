document.getElementById('urlForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const url = document.getElementById('url').value;
    fetch('/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `url=${encodeURIComponent(url)}`
    })
    .then(response => response.json())
    .then(data => {
        const resultElement = document.getElementById('result-text');
        resultElement.textContent = 'Processing...';

        setTimeout(() => {
            resultElement.textContent = `The URL is ${data.prediction}.`;
            document.getElementById('result').classList.add('show');
            document.getElementById('result-anchor').scrollIntoView({ behavior: 'smooth', block: 'start' });

            const safeImage = document.getElementById('safephoto');
            const maliciousImage = document.getElementById('maliciousphoto');
            if (data.prediction === 'safe') {
                safeImage.style.display = 'block';
                maliciousImage.style.display = 'none';
            } else {
                safeImage.style.display = 'none';
                maliciousImage.style.display = 'block';
            }
        }, 2000);
    })
    .catch(error => {
        console.error('Error fetching prediction:', error);
        const resultElement = document.getElementById('result-text');
        resultElement.textContent = 'Error fetching prediction. Please try again later.';
    });
});

document.addEventListener('DOMContentLoaded', function() {
    let sections = document.querySelectorAll('.section');
    let currentSection = 0;
    let isScrolling = false;
    const offset = 10; 

    function scrollToSection(index) {
        const sectionTop = sections[index].offsetTop - offset;
        window.scrollTo({
            top: sectionTop,
            behavior: 'smooth'
        });
    }

    window.addEventListener('wheel', function(event) {
        if (isScrolling) return;

        if (event.deltaY > 0) {
            currentSection = Math.min(sections.length - 1, currentSection + 1);
        } else {
            currentSection = Math.max(0, currentSection - 1);
        }
        scrollToSection(currentSection);

        isScrolling = true;
        setTimeout(() => {
            isScrolling = false;
        }, 1000);
    });

    document.getElementById('checkButton').addEventListener('click', function() {
        window.location.hash = 'section2';
    });
});


