"""
Create an html page where you can write an username of twitter use and it'll
create a map with there friends locations
"""
import folium
import json
import requests
from flask import Flask, render_template, request
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderUnavailable

app = Flask('Friends_map', template_folder='mysite/templates')


@app.route('/')
def route():
    """
    Html page with place to write an username and submit button
    """
    return render_template('form.html')


@app.route('/map')
def route_map():
    """
    Html page with map
    """
    user = request.args.get('user')
    return create_map(get_friends_locations(get_friends_inform(user)))


def get_friends_inform(user_name):
    """
    Get json object data about friends by user name
    :param user_name: str
    :return: information about friends of this account
    """
    url = 'https://api.twitter.com/2/users/by/username/' + user_name
    headers = {'authorization': '<API token>'}
    user_inform = json.loads(requests.get(url, headers=headers).text)
    user_id = user_inform["data"]["id"]
    friends_url = "https://api.twitter.com/2/users/" + user_id + "/following"
    friends_inform = json.loads(requests.get(friends_url,
                                             headers=headers,
                                             params={
                                                 'user.fields': 'location'}) \
                                .text)
    return friends_inform


def get_coordinates(friend_location):
    """
    Get coordinates from names of locations
    :param friend_location: location where friend lives
    :return: tuple of coordinates
    >>> get_coordinates("Ukraine")
    (49.4871968, 31.2718321)
    """
    try:
        geolocator = Nominatim(user_agent="geopyLab")
        location = geolocator.geocode(friend_location)
        while location is None:
            if len(friend_location.split(", ")) > 1:
                friend_location = friend_location[-1]
                location = geolocator.geocode(friend_location)
            else:
                break
        if location is not None:
            coordinates = (location.latitude, location.longitude)
            return coordinates
    except TimeoutError:
        return None
    except GeocoderUnavailable:
        return None


def get_friends_locations(friends_json):
    """
    Create a list of tuple with coordinates of friends location and it's name
    :param friends_json: information about friends
    :return: list of tuple with coordinates of friends location and it's name
    """
    name_and_location = []
    for friend in friends_json['data']:
        if "location" in friend:
            coordinates = get_coordinates(friend['location'])
            if coordinates is None:
                continue
            name_and_location.append((coordinates, friend["name"]))
    return name_and_location


def create_map(name_and_location):
    """
    Create map
    :param name_and_location: list of tuple with coordinates and friends' name
    :return: map
    """
    map = folium.Map(location=list((0.0000, 0.0000)),
                     zoom_start=2)
    friends_locations = folium.FeatureGroup(name='Friends')
    for friend in name_and_location:
        friends_locations.add_child(folium.Marker(
            location=list(friend[0]),
            popup=friend[1],
            icon=folium.Icon()))
    map.add_child(friends_locations)
    return map.get_root().render()


if __name__ == '__main__':
    app.run(port=8080)
