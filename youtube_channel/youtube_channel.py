"""
Complete Lab 3 and update the following information:

Author: Douglas London
Date: 5/14/2026
"""

class YouTubeChannel:
    def __init__(self, name: str = "", video_count: int = 0) -> None:
        """
        name: the channel title
        video_count: number of videos uploaded to this channel
        """
        self._name = name
        self.__video_count = video_count

    def __str__(self) -> str:
        return f"Channel: {self._name}, Videos: {self.__video_count}"

    # Get the channel name
    def get_name(self) -> str:
        return self._name

    # Set the channel name
    def set_name(self, name: str) -> None:
        self._name = name

    # Get the video count
    def get_video_count(self) -> int:
        return self.__video_count

    # Set the video count, ignoring negative values
    def set_video_count(self, video_count: int) -> None:
        if video_count >= 0:
            self.__video_count = video_count


def main() -> None:
    channel = YouTubeChannel("UVUCS1410", 150)
    print(channel)

    # Print current values using getters
    print("Name via getter:", channel.get_name())
    print("Video count via getter:", channel.get_video_count())

    # Modify values using setters and print updated channel
    channel.set_name("dogo1017")
    channel.set_video_count(200)
    print("After setters:", channel)

    # Reflection Q1: single underscore is directly accessible outside the class
    print("Direct _name access:", channel._name)

    # Reflection Q2: double underscore raises AttributeError outside the class
    try:
        print(channel.__video_count)
    except AttributeError as e:
        print("AttributeError:", e)

    # Access __video_count using name mangling syntax
    print("Via name mangling:", channel._YouTubeChannel__video_count)

    # Verify setter ignores negative values
    channel.set_video_count(-50)
    print("After trying to set -50:", channel.get_video_count())


if __name__ == "__main__":
    main()