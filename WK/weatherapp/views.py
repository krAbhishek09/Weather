from django.shortcuts import render
from django.contrib import messages
import requests

import datetime

def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'

    # Replace with your actual API keys
    API_KEY_WEATHER = '678562c2a35984e3b7656c776c9267cc'
    API_KEY_SEARCH = 'your_search_api_key'
    SEARCH_ENGINE_ID = 'your_search_engine_id'

    weather_url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY_WEATHER}'
    params = {'units': 'metric'}

    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    search_type = 'image'
    search_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY_SEARCH}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={search_type}&imgSize=xlarge"

    try:
        # Fetching image
        search_response = requests.get(search_url).json()
        search_items = search_response.get("items", [])
        if search_items:
            image_url = search_items[0]['link']
        else:
            image_url = ''

        # Fetching weather data
        weather_response = requests.get(weather_url, params=params).json()
        description = weather_response['weather'][0]['description']
        icon = weather_response['weather'][0]['icon']
        temp = weather_response['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })
        

    except KeyError:
        exception_occurred = True
        messages.error(request, 'Entered data is not available to API')
        day = datetime.date.today()
        return render(request, 'weatherapp/index.html', {
            'description': 'clear sky',
            'icon': '01d',
            'temp': 25,
            'day': day,
            'city': 'indore',
            'exception_occurred': exception_occurred
        })
