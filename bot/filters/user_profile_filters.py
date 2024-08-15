from requests import get

from lexicon.errors import RegisterDialogErrors as Errors


def age_filter(age: str) -> int:
    if all(ch.isdigit() for ch in age) and 12 <= int(age) <= 99:
        return int(age)
    raise ValueError(Errors.invalid_age)


def username_filter(username: str) -> str:
    if isinstance(username, str):
        return username
    raise ValueError(Errors.invalid_username)


def description_filter(description: str) -> str:
    if isinstance(description, str) and len(description) > 99:
        return description
    raise ValueError(Errors.invalid_description)


def city_filter(city: str) -> str:
    if isinstance(city, str):
        city = city.title()
        url = (f'https://nominatim.openstreetmap.org/search?featureType=city&'
               f'city={city}&format=json&accept-language=ru-Ru&email=example@gmail.com')
        response = get(url)
        if response.json():
            info = response.json()[0]['display_name'].split(', ')
            if info[0] == city:
                return info[0]
        raise ValueError(Errors.invalid_city)
