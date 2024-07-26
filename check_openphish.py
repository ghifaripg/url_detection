import requests
import ssl
import socket

def check_google_safe_browsing(api_key, url):
    api_url = 'https://safebrowsing.googleapis.com/v4/threatMatches:find?key=' + api_key
    data = {
        "client": {
            "clientId": "cspfinal",
            "clientVersion": "1.0"
        },
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [
                {"url": url}
            ]
        }
    }
    
    try:
        response = requests.post(api_url, json=data)
        response.raise_for_status()  # Raise an error for bad status codes

        if response.status_code == 200:
            result = response.json()
            if result.get('matches'):
                print(f"The URL '{url}' is listed as unsafe.")
                for match in result['matches']:
                    print(f"- Threat Type: {match['threatType']}")
                    print(f"- Platform Type: {match['platformType']}")
                    print(f"- Threat Entry: {match['threat']['url']}")
            else:
                print(f"The URL '{url}' is safe according to Google Safe Browsing.")
        else:
            print(f"Failed to fetch data: {response.status_code}")
            print(response.text)  # Print response text for debugging
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

def check_ssl_certificate(url):
    try:
        hostname = url.split('//')[1].split('/')[0]
        context = ssl.create_default_context()
        with socket.create_connection((hostname, 443)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                print(f"SSL certificate for {url} is valid.")
                return True
    except Exception as e:
        print(f"SSL certificate validation failed for {url}: {e}")
        return False

if __name__ == '__main__':
    api_key = 'AIzaSyB68uOVxxc7g51PzbiDdTG4eD-cLOZQ-fM'
    test_url = 'https://pdfcoffee.com/'
    
    print(f"Checking URL: {test_url}")
    
    # Check Google Safe Browsing
    check_google_safe_browsing(api_key, test_url)
    
    # Check SSL certificate validity
    ssl_check_result = check_ssl_certificate(test_url)
    if not ssl_check_result:
        print(f"The URL '{test_url}' has SSL certificate issues.")
    else:
        print(f"The URL '{test_url}' has a valid SSL certificate.")
