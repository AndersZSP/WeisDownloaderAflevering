from twitchAPI.twitch import Twitch
from twitchAPI.helper import limit

#TWITCH_SECRET and TWITCH_SECRET_ID are placeholders, as to not share the private developer tokens we have been granted
# by Twitch.tv

async def check_user(name):
    """
    Makes a request to the Twitch Helix API to check if a user with the name passed to the function exists.

     Related documentation:
    | `Helix docs <https://dev.twitch.tv/docs/api/reference/#get-users>`_
    | `TwitchAPI docs <https://pytwitchapi.dev/en/stable/modules/twitchAPI.twitch.html#twitchAPI.twitch.Twitch.get_users>`_

    :param name: The name of the user whose existence needs to be verified
    :return: Returns a boolean based on whether the user exists
    """
    twitch = await Twitch("TWITCH_SECRET_ID", "TWITCH_SECRET")
    generator = twitch.get_users(logins=name)
    user = [user async for user in generator]

    if len(user) == 1:
        return True

    return False


async def get_user_id(name):
    """
    Makes a request to the Twitch Helix API to get the user who matches the name passed as a parameter.

     Related documentation:
    | `Helix docs <https://dev.twitch.tv/docs/api/reference/#get-users>`_
    | `TwitchAPI docs <https://pytwitchapi.dev/en/stable/modules/twitchAPI.twitch.html#twitchAPI.twitch.Twitch.get_users>`_

    :param name: The name of the Twitch user
    :return: Returns the id of the user
    """
    twitch = await Twitch("TWITCH_SECRET_ID", "TWITCH_SECRET")
    generator = twitch.get_users(logins=name)
    user_list = [user async for user in generator]
    user = user_list[0]

    return user.id


async def get_clip(broadcaster_id):
    """
    Makes a request to the Twitch Helix API to get the first 5 clips of a single broadcaster.

    This function was primarily used in the beginning for testing purposes and isn't currently being used
    anywhere in the program.

     Related documentation:
    | `Helix docs <https://dev.twitch.tv/docs/api/reference/#get-clips>`_
    | `TwitchAPI docs <https://pytwitchapi.dev/en/stable/modules/twitchAPI.twitch.html#twitchAPI.twitch.Twitch.get_clips>`_

    :param broadcaster_id: The id used to identify the Twitch broadcaster the clips should come from
    :return: returns a list of 5 clips from the broadcaster whose id is passed as a parameter to the function
    """
    twitch = await Twitch("TWITCH_SECRET_ID", "TWITCH_SECRET")
    generator = limit(twitch.get_clips(broadcaster_id=broadcaster_id, first=5), 5)
    clips = [clip async for clip in generator]

    return clips


async def get_clips_by_dates(broadcaster_id, start_date, end_date):
    """
    Makes a request to the Twitch Helix API to get all clips from a specific Twitch broadcaster within
    the date range defined by ``start_date`` and ``end_date``

     Related documentation:
    | `Helix docs <https://dev.twitch.tv/docs/api/reference/#get-clips>`_
    | `TwitchAPI docs <https://pytwitchapi.dev/en/stable/modules/twitchAPI.twitch.html#twitchAPI.twitch.Twitch.get_clips>`_

    :param broadcaster_id: The id used to identify the Twitch broadcaster the clips should come from
    :param start_date: The date that defines the lower boundary of when the clips are created
    :param end_date: The date that defines the upper boundary of when the clips are created
    :return:
    """
    twitch = await Twitch("TWITCH_SECRET_ID", "TWITCH_SECRET")
    generator = twitch.get_clips(broadcaster_id=broadcaster_id, started_at=start_date, ended_at=end_date)
    clips = [clip async for clip in generator]

    return clips
