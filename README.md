# Weather reminder

Weather reminder service and API, you can create a subscription with a suitable notification period(hours) and add your desired cities.

## Getting Started

1. For using this app, you need to fill personal data, such as:
 - "EMAIL_FROM", "EMAIL_HOST_USER" and EMAIL_HOST_PASSWORD - from who will be sent notification messages;

2. For getting access token, register on service "http://'your domain name'/accounts/signup/", or login "http://'your domain name'/accounts/login/"
3. Use this token to put in http request header like: "{'Authorization': f'Bearer {token}'}";
4. To create subscription use POST method: "http://'your domain name'/api/subscription/", with "period_notifications"(in hours) data header;
5. To add city to subscription you need to use POST on: "http://'your domain name'/api/subscription/<subscription_id>/cities/" with city name data header;
6. You can check your subscription list using GET method on: "http://'your domain name'/api/subscription/" or 
    view a specific subscription: "http://'your domain name'/api/subscription/<subscription_id>";
7. To check cities in specific subscription GET on "http://'your domain name'/api/subscription/<subscription_id>/cities/";
8. To get weather for all cities on subscription GET on "http://'your domain name'/api/subscription/<subscription_id>/get_weather/"
9. To check weather on specific city use GET on "http://'your domain name'/api/subscription/<subscription_id>/get_weather/<city_name>/

To run app, use: 
"docker compose up"

### Prerequisites

- Docker
