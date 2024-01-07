from pydrive2.drive import GoogleDrive
from quickstart import gauth

drive = GoogleDrive(gauth)


def upload_file(filepath, title, folder_name, subfolder_name, twitch_id):
    """
    Uploads a Twitch Clip to Google Drive

    :param filepath: The path to the file that is going to be uploaded
    :param title: Name of the file to be uploaded
    :param folder_name: Name of the folder. Should be the name of a Twitch broadcaster.
    :param subfolder_name: Name of the subfolder. Should be the date the Twitch Clip was created.
    :param twitch_id: The id of the Twitch Clip
    """
    folder_id = get_id_of_folder(folder_name)
    if folder_id is None:
        folder_id = create_folder(folder_name)

    subfolder_id = get_id_of_folder(subfolder_name, folder_id)
    if subfolder_id is None:
        subfolder_id = create_subfolder(subfolder_name, folder_id)

    file = drive.CreateFile({'title': title + '.mp4', 'parents': [{'id': subfolder_id}],
                             'properties': [{'key': 'TwitchID', 'value': twitch_id}]})
    file.SetContentFile(filepath)
    file.Upload()
    print('title: %s, mimeType: %s' % (file['title'], file['mimeType']))


def create_folder(folder_name):
    """
    Creates a folder in Google Drive

    :param folder_name: The name given to the created folder
    :return: Returns the id of the newly created folder
    """
    new_folder = drive.CreateFile({'title': str(folder_name), 'mimeType': 'application/vnd.google-apps.folder'})
    new_folder.Upload()
    return new_folder['id']


def create_subfolder(folder_name, parent_folder_id):
    """
    Creates a subfolder in Google Drive

    :param folder_name: The name given to the created folder.
    :param parent_folder_id: The id of the Google Drive folder in which the folder will be created.
    :return: Returns the id of the newly created folder.
    """
    new_folder = drive.CreateFile({'title': str(folder_name), 'mimeType': 'application/vnd.google-apps.folder',
                                   'parents': [{'kind': 'drive#fileLink', 'id': parent_folder_id}]})
    new_folder.Upload()
    return new_folder['id']


def get_id_of_folder(folder_name, parent_directory_id=None):
    """
    Get the id of the folder with the name matching ``folder_name``

    :rtype: None | str
    :param folder_name: Name of the folder whose id is wanted
    :param str parent_directory_id: Optional; The id of the folder in which the folder is placed. Defaults to None
    :return: Returns the id of the folder if it exists otherwise returns None
    """
    if parent_directory_id is None:
        query = {'q': "'root' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"}
    else:
        query = {'q': f"'{parent_directory_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false"}

    folder_list = drive.ListFile(query).GetList()

    for folder in folder_list:
        if folder['title'] == str(folder_name):
            return folder['id']

    return None


def check_file_exists(twitch_id, folder_name, subfolder_name):
    """
    Checks if a file with the given ``twitch_id`` exists in Google Drive

    :param twitch_id: The id of the Twitch Clip
    :param folder_name: Name of the folder. Should be the name of a Twitch broadcaster.
    :param subfolder_name: Name of the subfolder. Should be the date the Twitch Clip was created.
    :return: Returns True if the file exists otherwise returns False
    """
    folder_id = get_id_of_folder(folder_name)
    if folder_id is None:
        print("No clips have been downloaded from this streamer")
        return False

    subfolder_id = get_id_of_folder(subfolder_name, folder_id)
    if subfolder_id is None:
        print("No clips have been downloaded from this date " + str(subfolder_name))
        return False

    query = {'q': f"'{subfolder_id}' in parents and trashed = false"}

    file_list = drive.ListFile(query).GetList()

    for file in file_list:
        if file['properties'][0]['value'] == twitch_id:
            print("Clip already exists")
            return True

    return False

