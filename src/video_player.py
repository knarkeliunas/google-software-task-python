"""A video player class."""

from .video_library import VideoLibrary
import random as rnd
import numpy as np

class VideoPlayer:
    """A class used to represent a Video Player."""

    def __init__(self):
        self._video_library = VideoLibrary()
        self.isPlaying = False
        self.isPaused = False
        self.Video_Playing_id = "None"
        self.playlist_id = 0
        self.playlist_list = []
        self.video_flags = np.empty((0,2), str)

    def Video_Name(self, video_id):
        """Converts id to title"""
        video = self._video_library.get_video(video_id)
        return video.title

    def is_video_flagged(self, video_id):
        """Checks if video is flagged, also returns the reason"""
        is_flagged = False
        i = 0
        for flag in self.video_flags[:,0]:
            if video_id == flag:
                return True, self.video_flags[i,1]
            i += 1
        return False, "Not Flagged"

    def number_of_videos(self):
        num_videos = len(self._video_library.get_all_videos())
        print(f"{num_videos} videos in the library")

    def show_all_videos(self):
        """Returns all videos."""
        videos = self._video_library.get_all_videos()
        print("Here's a list of all available videos:")

        temp_list = []
        for video in videos:
            # Convoluted way to display tags in required format
            tags = "["
            for tag in video.tags:
                tags = tags + tag + " "
            tags += "]"

            if tags != "[]":
                tags = tags[0:len(tags)-2] + "]"

            # Check if video is flagged
            flagged = self.is_video_flagged(video.video_id)
            if flagged[0]:
                flag = f' - FLAGGED (reason: {flagged[1]})'
            else:
                flag = ''

            # Put all videos in a list for sorting
            temp_list += [f"{video.title} ({video.video_id}) {tags}{flag}"]

        # Sort the list and display
        sorted_list = sorted(temp_list)
        for element in sorted_list:
            print(element)



    def play_video(self, video_id):
        """Plays the respective video.

        Args:
            video_id: The video_id to be played.
        """
        video = self._video_library.get_video(video_id)


        flag = self.is_video_flagged(video_id)
        if flag[0]:
            print(f"Cannot play video: Video is currently flagged (reason: {flag[1]})")
            return

        # Use try function for when inevitably it throws an error
        try:
            temp = video.title
            if self.isPlaying == False:
                print(f'Playing video: {video.title}')
                self.isPlaying = True
                self.isPaused = False
                self.Video_Playing_id = video_id
            else:
                print(f'Stopping video: {self.Video_Name(self.Video_Playing_id)}')
                print(f'Playing video: {video.title}')
                self.Video_Playing_id = video_id
                self.isPaused = False
        except:
            print('Cannot play video: Video does not exist')

    def stop_video(self):
        """Stops the current video."""

        # Check if video is playing and then simply change the global variables
        if self.isPlaying == True:
            print(f'Stopping video: {self.Video_Name(self.Video_Playing_id)}')
            self.isPlaying = False
            self.isPaused = False
            self.Video_Playing_id = 'None'
        else:
            print('Cannot stop video: No video is currently playing')

    def play_random_video(self):
        """Plays a random video from the video library."""
        videos = self._video_library.get_all_videos()

        # Check if all videos are flagged
        if len(self.video_flags[:,0]) == len(videos):
            print("No videos available")
            return

        # Choose random video and check if it's flagged
        loop = True
        while loop == True:
            video = rnd.choice(videos)
            if len(self.video_flags[:,0]) == 0:
                loop = False
            if video.video_id not in self.video_flags[:,0]:
                loop == False
        # call play_video function and parse a randomly picked id
        self.play_video(video.video_id)

    def pause_video(self):
        """Pauses the current video."""

        # Check if a video is playing or already paused
        if self.isPlaying == False:
            print("Cannot pause video: No video is currently playing")
        elif self.isPaused == True:
            print(f"Video already paused: {self.Video_Name(self.Video_Playing_id)}")
        else:
            print(f"Pausing video: {self.Video_Name(self.Video_Playing_id)}")
            self.isPaused = True

    def continue_video(self):
        """Resumes playing the current video."""
        if self.isPlaying == True:
            if self.isPaused == True:
                print(f"Continuing video: {self.Video_Name(self.Video_Playing_id)}")
            else:
                print("Cannot continue video: Video is not paused")
        else:
            print("Cannot continue video: No video is currently playing")

    def show_playing(self):
        """Displays video currently playing."""
        if self.isPlaying:
            video = self._video_library.get_video(self.Video_Playing_id)

            # Do the tag shenangians from show_all_videos
            tags = "["
            for tag in video.tags:
                tags = tags + tag + " "
            tags += "]"

            if tags != "[]":
                tags = tags[0:len(tags)-2] + "]"

            if self.isPaused:
                print(f"Currently playing: {video.title} ({video.video_id}) {tags} - PAUSED")
            else:
                print(f"Currently playing: {video.title} ({video.video_id}) {tags}")
        else:
            print("No video is currently playing")



    ''' PART 2'''

    def create_playlist(self, playlist_name):
        """Creates a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        # Create a global list of lists and work with that
        for playlist in self.playlist_list:
            if playlist_name.casefold() == playlist[1].casefold():
                print("Cannot create playlist: A playlist with the same name already exists")
                return

        # Add id in case I need it later (I didn't but I can't remove it due to how other parts work)
        self.playlist_list.append([self.playlist_id, playlist_name])
        self.playlist_id += 1
        print(f"Successfully created new playlist: {playlist_name}")

    def add_to_playlist(self, playlist_name, video_id):
        """Adds a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be added.
        """

        # Check if video is flagged
        flag = self.is_video_flagged(video_id)
        if flag[0]:
            print(f"Cannot add video to {playlist_name}: Video is currently flagged (reason: {flag[1]})")
            return

        # Check if playlist exists
        playlist_exists = False
        temp_id = 0
        for playlist in self.playlist_list:
            if playlist_name.casefold() != playlist[1].casefold():
                temp_id += 1
                pass
            else:
                playlist_exists = True
                break

        # Return if didn't find playlist
        if playlist_exists == False:
            print(f"Cannot add video to {playlist_name}: Playlist does not exist")
            return

        # Check if video exists
        videos = self._video_library.get_all_videos()
        video_id_list = []

        for video in videos:
            video_id_list += [video.video_id]

        if video_id not in video_id_list:
            print(f"Cannot add video to {playlist_name}: Video does not exist")
            return

        # Check if video is already on the playlist
        if video_id in self.playlist_list[temp_id]:
            print(f"Cannot add video to {playlist_name}: Video already added")
            return

        # If everything checks out, add to playlist
        self.playlist_list[temp_id].append(video_id)
        video = self._video_library.get_video(video_id)
        print(f"Added video to {playlist_name}: {video.title}")

    def show_all_playlists(self):
        """Display all playlists."""
        if len(self.playlist_list) == 0:
            print("No playlists exist yet")
        else:
            # Put all playlist names in a list
            playlist_names = []
            for playlist in self.playlist_list:
                playlist_names += [playlist[1]]

            # Sort the list alphabetically
            sorted_list = sorted(playlist_names)

            print("Showing all playlists:")
            for playlist in sorted_list:
                print(playlist)

    def find_playlist_index(self, playlist_name):
        """Returns location of playlist in the global list"""
        index = 0
        for playlist in self.playlist_list:
            if playlist_name.casefold() != playlist[1].casefold():
                index += 1
                pass
            else:
                break
        return index

    def show_playlist(self, playlist_name):
        """Display all videos in a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        # Check if playlist exists
        playlist_exists = False
        temp_id = 0
        for playlist in self.playlist_list:
            if playlist_name.casefold() != playlist[1].casefold():
                temp_id += 1
                pass
            else:
                playlist_exists = True
                break

        # Return if didn't find playlist
        if playlist_exists == False:
            print(f"Cannot show playlist {playlist_name}: Playlist does not exist")
            return

        # Grab the playlist and display items in it
        playlist = self.playlist_list[self.find_playlist_index(playlist_name)]
        print(f"Showing playlist: {playlist_name}")
        if len(playlist) == 2:
            print("No videos here yet")
        else:
            i = 0
            for element in playlist:
                # First two elements are id and name, so skip them
                if i <=1:
                    pass
                else:
                    video = self._video_library.get_video(element)

                    # Tag nonsense again
                    tags = "["
                    for tag in video.tags:
                        tags = tags + tag + " "
                    tags += "]"

                    if tags != "[]":
                        tags = tags[0:len(tags)-2] + "]"

                    # Check if video is flagged
                    flagged = self.is_video_flagged(video.video_id)
                    if flagged[0]:
                        flag = f' - FLAGGED (reason: {flagged[1]})'
                    else:
                        flag = ''
                    print(f"{video.title} ({video.video_id}) {tags}{flag}")
                i += 1

    def remove_from_playlist(self, playlist_name, video_id):
        """Removes a video to a playlist with a given name.

        Args:
            playlist_name: The playlist name.
            video_id: The video_id to be removed.
        """

        playlist_index = self.find_playlist_index(playlist_name)

        # Check if playlist exists
        playlist_exists = False
        temp_id = 0
        for playlist in self.playlist_list:
            if playlist_name.casefold() != playlist[1].casefold():
                temp_id += 1
                pass
            else:
                playlist_exists = True
                break

        if playlist_exists == False:
            print(f"Cannot remove video from {playlist_name}: Playlist does not exist")
            return

        # Check if video exists
        videos = self._video_library.get_all_videos()
        video_id_list = []

        for video in videos:
            video_id_list += [video.video_id]

        if video_id not in video_id_list:
            print(f"Cannot remove video from {playlist_name}: Video does not exist")
            return

        # Check if video is in playlist
        if video_id not in playlist:
            print(f"Cannot remove video from {playlist_name}: Video is not in playlist")
            return
        video = self._video_library.get_video(video_id)
        self.playlist_list[playlist_index].remove(video_id)
        print(f"Removed video from {playlist_name}: {video.title}")

    def clear_playlist(self, playlist_name):
        """Removes all videos from a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """

        # Check if playlist exists
        playlist_exists = False
        temp_id = 0
        for playlist in self.playlist_list:
            if playlist_name.casefold() != playlist[1].casefold():
                temp_id += 1
                pass
            else:
                playlist_exists = True
                break

        if playlist_exists == False:
            print(f"Cannot clear playlist {playlist_name}: Playlist does not exist")
        else:
            playlist_index = self.find_playlist_index(playlist_name)
            playlist = self.playlist_list[playlist_index]
            self.playlist_list[playlist_index] = playlist[0:2]
            print(f"Successfully removed all videos from {playlist_name}")

    def delete_playlist(self, playlist_name):
        """Deletes a playlist with a given name.

        Args:
            playlist_name: The playlist name.
        """
        # Check if playlist exists
        playlist_exists = False
        temp_id = 0
        for playlist in self.playlist_list:
            if playlist_name.casefold() != playlist[1].casefold():
                temp_id += 1
                pass
            else:
                playlist_exists = True
                break

        if playlist_exists == False:
            print(f"Cannot delete playlist {playlist_name}: Playlist does not exist")
        else:
            playlist_index = self.find_playlist_index(playlist_name)
            self.playlist_list.pop(playlist_index)
            print(f"Deleted playlist: {playlist_name}")

    def search_videos(self, search_term):
        """Display all the videos whose titles contain the search_term.

        Args:
            search_term: The query to be used in search.
        """


        # Grab video title one by one and check if the search string is in it.
        # If there is, save the location on videos.txt
        videos = self._video_library.get_all_videos()
        index = 0
        search_hits_indexes = []
        for video in videos:
            if video.title.casefold().find(search_term.casefold()) != -1:
                search_hits_indexes += [index]
            index += 1

        if len(search_hits_indexes) == 0:
            print(f"No search results for {search_term}:")
            return


        print(f"Here are the results for {search_term}:")
        temp_list = np.array([])
        for index in search_hits_indexes:
            video = videos[index]

            # Check if video is flagged
            flag = self.is_video_flagged(video.video_id)
            if flag[0]:
                continue

            # Convoluted way to display tags in required format
            tags = "["
            for tag in video.tags:
                tags = tags + tag + " "
            tags += "]"

            if tags != "[]":
                tags = tags[0:len(tags)-2] + "]"
            temp_list = np.append(temp_list, f"{video.title} ({video.video_id}) {tags}")

        # Use numpy.argsort for parallel sorting
        idx = np.argsort(temp_list)
        strings = np.array(temp_list)[idx]
        indexes = np.array(search_hits_indexes)[idx]
        numbers = range(len(indexes))
        i = 0
        for n in numbers:
            print(f"{n+1}) {strings[i]}")
            i += 1

        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        try:
            selection = int(input())
            # Indexes already sorted, so just play the selection-1 element from indexes array
            self.play_video(videos[indexes[selection-1]].video_id)
        except:
            return



    def search_videos_tag(self, video_tag):
        """Display all videos whose tags contains the provided tag.

        Args:
            video_tag: The video tag to be used in search.
        """

        # Literally identical code to last part except changed the way how to search for tags
        videos = self._video_library.get_all_videos()
        index = 0
        search_hits_indexes = []
        for video in videos:
            for tag in video.tags:
                if tag == video_tag:
                    search_hits_indexes += [index]
            index += 1

        # No changes past here
        if len(search_hits_indexes) == 0:
            print(f"No search results for {video_tag}:")
            return


        print(f"Here are the results for {video_tag}:")
        temp_list = np.array([])
        for index in search_hits_indexes:
            video = videos[index]

            # Check if video is flagged
            flag = self.is_video_flagged(video.video_id)
            if flag[0]:
                continue

            # Convoluted way to display tags in required format
            tags = "["
            for tag in video.tags:
                tags = tags + tag + " "
            tags += "]"

            if tags != "[]":
                tags = tags[0:len(tags)-2] + "]"
            temp_list = np.append(temp_list, f"{video.title} ({video.video_id}) {tags}")

        # Use numpy.argsort for parallel sorting
        idx = np.argsort(temp_list)
        strings = np.array(temp_list)[idx]
        indexes = np.array(search_hits_indexes)[idx]
        numbers = range(len(indexes))
        i = 0
        for n in numbers:
            print(f"{n+1}) {strings[i]}")
            i += 1

        print("Would you like to play any of the above? If yes, specify the number of the video.")
        print("If your answer is not a valid number, we will assume it's a no.")
        try:
            selection = int(input())
            # Indexes already sorted, so just play the selection-1 element from indexes array
            self.play_video(videos[indexes[selection-1]].video_id)
        except:
            return

    def flag_video(self, video_id, flag_reason="Not supplied"):
        """Mark a video as flagged.

        Args:
            video_id: The video_id to be flagged.
            flag_reason: Reason for flagging the video.
        """
        # Check if video exists
        video_exists = False
        videos = self._video_library.get_all_videos()
        for video in videos:
            if video.video_id == video_id:
                video_exists = True
        if video_exists == False:
            print("Cannot flag video: Video does not exist")
            return

        # Check if video is flagged
        if video_id in self.video_flags[:,0]:
            print("Cannot flag video: Video is already flagged")
            return

        # If pass checks, flag video
        video = self._video_library.get_video(video_id)
        self.video_flags = np.append(self.video_flags, [[video_id,flag_reason]], axis = 0)

        # Stop video if it's playing
        if self.isPlaying == True:
            if  self.Video_Playing_id == video.video_id:
                print(f"Stopping video: {video.title}")
                self.isPlaying = False
                self.Video_Playing_id = "None"
                print(f"Successfully flagged video: {video.title} (reason: {flag_reason})")
            else:
                print(f"Successfully flagged video: {video.title} (reason: {flag_reason})")
        else:
            print(f"Successfully flagged video: {video.title} (reason: {flag_reason})")

    def allow_video(self, video_id):
        """Removes a flag from a video.

        Args:
            video_id: The video_id to be allowed again.
        """

        # Check if video exists
        video_exists = False
        videos = self._video_library.get_all_videos()
        for video in videos:
            if video.video_id == video_id:
                video_exists = True
        if video_exists == False:
            print("Cannot remove flag from video: Video does not exist")
            return

        # Check if video is in the flagged list
        if video_id not in self.video_flags[:,0]:
            print("Cannot remove flag from video: Video is not flagged")
            return

        i = 0
        for video in self.video_flags[:,0]:
            if video_id == video:
                np.delete(self.video_flags, i, axis=0)
                print(f"Successfully removed flag from video: {self._video_library.get_video(video_id).title}")
            i += 1


