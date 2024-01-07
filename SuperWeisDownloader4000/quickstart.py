from pydrive2.auth import GoogleAuth

gauth = GoogleAuth()


def google_authenticate():
    """
    This function authenticates the application to Google to enable the use of Google Drive API v2 via PyDrive2

     Related documentation:
    | `PyDrive2 docs <https://docs.iterative.ai/PyDrive2/>`_
    """
    gauth.LoadCredentialsFile("mycreds.txt")

    if gauth.credentials is None:

        gauth.settings.update({'get_refresh_token': True})
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        # Potentiel exception handling omkring mycreds.txt existing
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")
