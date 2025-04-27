import requests

def call_reverse_geocoding_api(lat: float, lon: float) -> dict | None:
    """
    OpenStreetMap Nominatim API 호출
    """
    url = 'https://nominatim.openstreetmap.org/reverse'
    params = {
        'lat': lat,
        'lon': lon,
        'format': 'json',
        'addressdetails': 1
    }
    headers = {
        'User-Agent': 'MyImageBot/1.0'
    }
    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        print(f"Reverse geocoding API call error: {e}")
        return None
