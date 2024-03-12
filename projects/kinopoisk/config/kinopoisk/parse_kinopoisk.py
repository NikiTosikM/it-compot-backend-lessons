import os
import pickle
from datetime import datetime
from urllib.parse import urlparse

import requests
from django.core.files.base import ContentFile
from django.db import transaction
from requests.exceptions import InvalidURL

from kinopoisk.models import MoviePerson, Genre, Movie


def parse_date(iso_str):
    if iso_str:
        return datetime.strptime(iso_str.split('T')[0], "%Y-%m-%d").date()
    return None


def download_image(image_url):
    try:
        response = requests.get(image_url)
    except InvalidURL:
        try:
            response = requests.get(image_url.replace('https:https:', 'https:'))
        except InvalidURL:
            return None
    if response.status_code == 200:
        image_content = ContentFile(response.content)
        filename = os.path.basename(urlparse(image_url).path)+'.png'
        return image_content, filename
    else:
        return None


def parse_and_save_movie_data(data):
    with open('persons_data.pkl', 'rb') as file:
        person_data = pickle.load(file)

    if 'docs' not in data:
        return

    with transaction.atomic():
        person_objs = {}
        for person in person_data:
            if not person.get('name'):
                continue
            photo_content, filename = download_image(person['photo']) if person.get('photo') else (None, None)
            person_obj, _ = MoviePerson.objects.update_or_create(
                id=person['id'],
                defaults={
                    'name': person['name'],
                    'photo': None
                }
            )
            if photo_content and filename:
                person_obj.photo.save(filename, photo_content, save=True)
            person_objs[person['id']] = person_obj

        for item in data['docs']:
            genre_objs = []
            for genre in item.get('genres', []):
                genre_obj, _ = Genre.objects.get_or_create(name=genre['name'])
                genre_objs.append(genre_obj)

            poster_content, poster_filename = download_image(item.get('poster', {}).get('url')) if item.get('poster',
                                                                                                            {}).get(
                'url') else (None, None)
            movie, created = Movie.objects.get_or_create(
                title=item.get('name', 'Unknown'),
                defaults={
                    'description': item.get('description', ''),
                    'release_date': datetime.strptime(str(item.get('year', '1900')), '%Y').date() if item.get(
                        'year') else None,
                    'rating': item.get('rating', {}).get('kp'),
                    'duration': item.get('movieLength', 0),
                    'budget': item.get('budget', {}).get('value', 0),
                    'poster': None
                }
            )
            if poster_content and poster_filename:
                movie.poster.save(poster_filename, poster_content, save=True)

            if genre_objs:
                movie.genres.set(genre_objs)

            actors = [person_objs[person_id] for person_id in person_objs if any(
                person['id'] == person_id and person['profession'] in ['актеры', 'actor'] for person in
                item.get('persons', []))]
            directors = [person_objs[person_id] for person_id in person_objs if any(
                person['id'] == person_id and person['profession'] in ['режиссеры', 'director'] for person in
                item.get('persons', []))]

            if actors:
                movie.actors.set(actors)

            if directors:
                movie.directors.set(directors)

            movie.save()


def fetch_movies_data():
    filename = 'movies_data.pkl'
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            data = pickle.load(file)
    else:
        url = "https://api.kinopoisk.dev/v1.4/movie?page=1&limit=250&selectFields=id&selectFields=name&selectFields=description&selectFields=shortDescription&selectFields=type&selectFields=isSeries&selectFields=status&selectFields=year&selectFields=releaseYears&selectFields=rating&selectFields=ageRating&selectFields=budget&selectFields=movieLength&selectFields=genres&selectFields=countries&selectFields=poster&selectFields=persons&rating.kp=8-10&lists=top250"
        headers = {
            "accept": "application/json",
            "X-API-KEY": "NJA1FE1-MX4MACW-PZXT4YJ-APPQ6J9"
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            with open(filename, 'wb') as file:
                pickle.dump(data, file)
        else:
            data = None
    return data


def fetch_persons_data(person_ids):
    """Получение данных о персонах по их ID."""
    base_url = "https://api.kinopoisk.dev/v1.4/person"
    select_fields = [
        "id", "name", "photo", "sex", "growth", "birthday"
    ]
    select_fields_param = "&selectFields=".join(select_fields)
    ids_param = "&".join([f"id={id}" for id in person_ids])
    url = f"{base_url}?page=1&limit=250&selectFields={select_fields_param}&{ids_param}"
    headers = {
        "accept": "application/json",
        "X-API-KEY": "NJA1FE1-MX4MACW-PZXT4YJ-APPQ6J9"  # Используйте свой API-ключ
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()  # Возвращает данные в формате JSON
    else:
        print(f"Error: {response.status_code}")
        return None


def save_persons_data_to_pickle(data, filename='persons_data.pkl'):
    """Сохранение данных о персонах в файл pickle."""
    with open(filename, 'wb') as file:
        pickle.dump(data, file)


def fetch_and_save_persons_data_from_movies(movies_data):
    person_ids = set()
    for movie in movies_data['docs']:
        for person in movie.get('persons', []):
            person_ids.add(person['id'])

    # Инициализируем список для сбора данных о всех персонах
    all_persons_data = []

    # Разбиваем список ID на части по 100 элементов
    chunk_size = 100
    for i in range(0, len(person_ids), chunk_size):
        chunk = list(person_ids)[i:i + chunk_size]
        # Выполняем запрос для каждой порции ID
        chunk_data = fetch_persons_data(chunk)
        if chunk_data and chunk_data.get('docs'):
            # Добавляем полученные данные о персонах в общий список
            all_persons_data.extend(chunk_data['docs'])

    # Сохраняем собранные данные о всех персонах в файл pickle
    if all_persons_data:
        save_persons_data_to_pickle(all_persons_data)
