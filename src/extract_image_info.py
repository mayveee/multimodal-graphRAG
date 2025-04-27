import io
import exifread
import requests
from api.geocoding_api import call_reverse_geocoding_api

def extract_image_info(image_bytes: bytes) -> dict:
    # 정보 1 메타데이터
    metadata = extract_metadata(image_bytes)

    # 정보 2 라벨링
    
    return {
        "DateTime": metadata.get("DateTime"),
        "시": metadata.get("시"),
        "구": metadata.get("구"),
        "동": metadata.get("동"),
        "로": metadata.get("로")
    }

def extract_metadata(image_bytes: bytes) -> dict:
    """
    exifread를 사용하여 이미지 bytes에서 메타데이터 추출
    """
    metadata = {
        "DateTime": None,
        "Latitude": None,
        "Longitude": None,
        "시": None,
        "구": None,
        "동": None,
        "로": None
    }
    f = io.BytesIO(image_bytes)
    tags = exifread.process_file(f, details=False)

    # 메타데이터가 없는 사진
    if not tags:
        return metadata
    
    # 찍은 날짜 추출
    date_time = tags.get('EXIF DateTimeOriginal') or tags.get('Image DateTime')
    metadata["DateTime"] = str(date_time)

    # GPS 데이터 추출
    lat, lon = None, None
    gps_latitude = tags.get('GPS GPSLatitude')
    gps_latitude_ref = tags.get('GPS GPSLatitudeRef')
    gps_longitude = tags.get('GPS GPSLongitude')
    gps_longitude_ref = tags.get('GPS GPSLongitudeRef')

    if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
        lat = _convert_GPS_to_degrees(gps_latitude)
        if gps_latitude_ref.values[0] != 'N':
            lat = -lat

        lon = _convert_GPS_to_degrees(gps_longitude)
        if gps_longitude_ref.values[0] != 'E':
            lon = -lon

    metadata["Latitude"] = lat
    metadata["Longitude"] = lon

    # GPS를 실제 주소로 변환
    if lat is not None and lon is not None:
        location_info = _reverse_geocode(lat, lon)
        metadata.update(location_info)

    return metadata

def _convert_GPS_to_degrees(value):
    """
    GPS 좌표를 degrees(float)로 변환
    """
    d, m, s = [float(x.num) / float(x.den) for x in value.values]
    return d + (m / 60.0) + (s / 3600.0)

def _reverse_geocode(lat, lon)-> dict:
    """
    위도, 경도를 받아서 행정구역 주소를 반환
    """
    address_info = {
        "시": None,
        "구": None,
        "동": None,
        "로": None
    }
    if(lat is None and lon is None):
        return address_info
    
    api_data = call_reverse_geocoding_api(lat, lon)
    if api_data:
        address = api_data.get('address', {})
        address_info.update({
            "시": address.get('city') or address.get('town') or address.get('village'),
            "구": address.get('borough') or address.get('county'),
            "동": address.get('quarter') or address.get('suburb'),
            "로": address.get('road')
        })
    return address_info
