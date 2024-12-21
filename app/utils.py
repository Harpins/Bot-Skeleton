import requests
from urllib.parse import urljoin
from datetime import datetime

BASE_URL = "http://195.133.75.198:8000/"

# Поиск по ID


def get_by_id(something_list, id):
    filtered_something = [
        something for something in something_list if something["id"] == id
    ]
    if filtered_something:
        return filtered_something[0]
    return filtered_something


# Реквесты


def register_user(params):
    requests.post(f"{BASE_URL}users/", json=params, timeout=10)


def get_response(url, params=None, timeout=10):
    response = requests.get(url=url, params=params, timeout=timeout)
    response.raise_for_status()
    return response


def register_booking(params):
    requests.post(f"{BASE_URL}bookings/", json=params, timeout=10)


# Клиенты и юзеры


def get_all_users():
    url = urljoin(BASE_URL, "api/users")
    return get_response(url).json()


def check_client(client_tg_id=0, client_phone_number=""):
    users = get_all_users()
    clients = get_clients(users)
    filtered_clients = [
        client
        for client in clients
        if client["telegram_id"] == client_tg_id
        or client["phone_number"] == client_phone_number
    ]
    if filtered_clients:
        return filtered_clients[0]
    return filtered_clients


def get_clients(users):
    return [user for user in users if user["role"] == "client"]


def make_client_template(client_tg_id, client_phone_number, client_name):
    return {
        "username": client_name,
        "role": "client",
        "phone_number": client_phone_number,
        "telegram_id": client_tg_id,
    }


# Специалисты


def get_specialists():
    url = urljoin(BASE_URL, "api/specialists")
    return get_response(url).json()


def filter_specialists(specialists, salon, procedure):
    return [
        specialist
        for specialist in specialists
        if (salon in specialist["salons"] and procedure in specialist["procedures"])
    ]


def get_specialist_by_id(specialists, id):
    filtered_specialist = [
        specialist for specialist in specialists if specialist["id"] == id
    ]
    if filtered_specialist:
        return filtered_specialist[0]
    return filtered_specialist


# Салоны


def get_salons():
    url = urljoin(BASE_URL, "api/salons")
    return get_response(url).json()


def get_salon_by_id(salons, id):
    filtered_salon = [salon for salon in salons if salon["id"] == id]
    if filtered_salon:
        return filtered_salon[0]
    return filtered_salon


# Процедуры


def get_procedures():
    url = urljoin(BASE_URL, "api/procedures")
    return get_response(url).json()


def get_procedure_by_id(procedures, id):
    filtered_procedure = [
        procedure for procedure in procedures if procedure["id"] == id
    ]
    if filtered_procedure:
        return filtered_procedure[0]
    return filtered_procedure


# Доступные записи


def get_availabilities():
    url = urljoin(BASE_URL, "api/availabilities")
    return get_response(url).json()


def filter_availabilities(availabilities, specialist, salon):
    found_availabilities = []
    for availability in availabilities:
        if (
            availability["specialist"] == specialist and availability["salon"] == salon
        ) and not availability["is_booked"]:
            found_availabilities.append(availability)
    return found_availabilities


# Время


def format_time_to_string(time: datetime):
    return time.strftime("%Y-%m-%dT%H:%M:%SZ")


def get_occupied_time_intervals(found_availabilities):
    occupied_time_intervals = []
    for availability in found_availabilities:
        str_start_time = availability["start_time"]
        str_end_time = availability["end_time"]

        start_time = datetime.fromisoformat(str_start_time.replace("Z", "+00:00"))
        end_time = datetime.fromisoformat(str_end_time.replace("Z", "+00:00"))

        occupied_time_intervals.append((start_time, end_time))
    return occupied_time_intervals


def get_free_time_intervals(occupied_time_intervals):
    str_start_time = "2024-01-01T14:00:00Z"
    str_end_time = "2024-12-31T14:00:00Z"
    start_time = datetime.fromisoformat(str_start_time.replace("Z", "+00:00"))
    end_time = datetime.fromisoformat(str_end_time.replace("Z", "+00:00"))
    free_time_intervals = []
    if occupied_time_intervals[0][0] > start_time:
        free_time_intervals.append((free_time_intervals, occupied_time_intervals[0][0]))
    for i in range(1, len(occupied_time_intervals)):
        if occupied_time_intervals[i][0] > occupied_time_intervals[i - 1][1]:
            free_time_intervals.append(
                (free_time_intervals[i - 1][1], free_time_intervals[i][0])
            )
    if occupied_time_intervals[-1][1] < end_time:
        free_time_intervals.append(
            (occupied_time_intervals[-1][1], occupied_time_intervals)
        )
    return free_time_intervals
