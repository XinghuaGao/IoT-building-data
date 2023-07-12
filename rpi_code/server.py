
import requests

# Server URL
server_url = "http://192.168.0.6/data_collection/"

def get_latest_entry(rpi_id, room_id):
    """
    Get the latest entry in local database of given Raspberry Pi and room.
    
    Args:
    rpi_id (str): ID of the Raspberry Pi.
    room_id (str): ID of the room.

    Returns:
    str: Date and time of last inserted row.
    """
    row_data = {"rpi_id": rpi_id, "room_id": room_id}
    url = server_url + "get_latest_entry.php"
    
    try:
        response = requests.post(url, params=row_data)
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Exception: {e}")
        return None

def sendFile(file_name):
    """
    Send a file to the central server.
    
    Args:
    file_name (str): Name of the file to send.
    """
    url = server_url + "file_receive.php"
    
    try:
        with open(file_name, 'rb') as f:
            files = {'file': f}
            response = requests.post(url, files=files)
            if response.text == "1":
                print("Error uploading file\n")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
