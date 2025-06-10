from ytmusicapi import YTMusic
from structures import MusicQueue, Song, time_to_seconds, seconds_to_time_format
from database import init_db, add_song_to_history, get_history
import os

NO_OF_RESULTS = 5

def clear():
    """
    Input: None
    Returns: None
    Working:
    This function clears terminal screen
    """
    if os.name == "posix":
        os.system('clear')
    else:
        os.system('cls')

def extract_artists(song_info):
    """
    Input: Data of the song as originally retrieved (dictionary format)
    Returns: All artists involved in the song as a string or "NA" if no artist info is available.
    Working:
    This function makes sure that all artists involved in a song show up in the final 
    representation.
    """
    artists = song_info.get('artists', []) #this will give an empty list if artists not in dictionary
    
    if not artists:  # if the list from before is empty
        return "NA"
    else:
        artist_names = [artist['name'] for artist in artists]  #since it is a list of dictionaries
        single_string=", ".join(artist_names)
        return single_string  


def song_search(query):
    """
    Input: Search query
    Returns: Top 5 results from the retrieved data
    Working:
    This function invokes the search method on YTMusic object with required arguments
    and returns the top "NO_OF_RESULTS" results.
    """
    try:
        ytmusic = YTMusic()  
        results = ytmusic.search(query, filter="songs")  
        return results[:NO_OF_RESULTS]  # it will return top 5 results, as NO_OF_RESULTS=5
    except Exception as e:
        raise Exception(f"Error occurred while searching for songs: {e}")


def filter_info(results):
    """
    Input: Search results in a JSON like format
    Returns: List of Song Objects
    Working:
    This function is supposed to extract the required information from the JSON,
    create Song objects and append them to a list. If an error occurs, raise an
    exception.
    """
    songs = []  #the thing it will return
    
    try:
        for song in results:
            title = song['title']  
            artist = extract_artists(song)  
            duration = time_to_seconds(song['duration'])  # time to secondss
            songs.append(Song(title, artist, duration))    
        return songs
    except Exception as fault:
        raise Exception(f"The following error occured: {fault}")

def print_song_results(results):
    """
    Input: List containing "Song" objects
    Returns: None
    Working:
    This function is reponsible for printing the song results with a serial number beside them.
    """
    print("RESULTS:")
    for i in range(len(results)):
        print(f"{i+1}. {results[i]}")  #will give a format like for example "1. song object"

def search():
    """
    Input: None
    Return: A Song object representing the song the user wants to add into the Queue, or None if the user wants to go back
    Working:
    1. This function takes search query from the user
    2. Searches for the song using songSearch function
    3. Filters the information using filterInfo function
    4. Prints the song results using printSongResults function
    5. Asks for user choice
    6. Returns the chosen song information
    7. If the user wants to go back, it returns None
    """
    while True:
        clear()
        query = input("Enter the song name: ")
        results = song_search(query)  
        songs = filter_info(results)
        
        print_song_results(songs)  
        
        while True:  
            choice = input("\nEnter a number (1-5) to add to the queue, '0' to search again, or 'q' to go back: ")

            if choice == 'q':  
                return None
            elif choice == '0': 
                break  # this will break only this inner while loop, lettig him search again from the outer while loop
            else:
                int_choice = int(choice)
                if int_choice>=1 and int_choice<=len(songs):  # Ensure it's a valid selection
                    return songs[int_choice-1]  # since index begins with 0, subtract one
                else:
                    print("Invalid input.")

def main():
    """Main application loop"""
    init_db()  # Initialize SQLite database
    queue = MusicQueue()
    clear()
    print("MUSIC QUEUE PLAYER\n")
    
    while True:
        print(f"Currently playing: {queue.peek() if not queue.is_empty() else 'None'}\n")
        print("""Options:
        1. Add Song
        2. Play Next Song
        3. Show Queue
        4. Clear Queue
        5. Show History
        6. Quit""")
        
        choice = input("\nEnter choice (1-6): ")
        
        if choice == '1':
            song = search()
            if song:
                place = input("Add to: 1. Top | 2. End: ")
                queue.enqueue_f(song) if place == '1' else queue.enqueue_b(song)
                print(f"Added: {song.get_name()}")
                input("\nPress Enter to continue...")
        
        elif choice == '2':
            clear()
            if not queue.is_empty():
                current_song = queue.dequeue()
                add_song_to_history(current_song)  # Add to SQLite history
                print(f"Now playing: {current_song}")
            else:
                print("Queue is empty!")
            input("\nPress Enter to continue...")
        
        elif choice == '3':
            clear()
            print(queue)
            input("\nPress Enter to continue...")
        
        elif choice == '4':
            queue.clear()
            print("Queue cleared!")
            input("\nPress Enter to continue...")
        
        elif choice == '5':
            clear()
            print("\nRECENTLY PLAYED:")
            for idx, (title, artist, duration, played_at) in enumerate(get_history(), 1):
                print(f"{idx}. {title} - {artist} ({seconds_to_time_format(duration)}) - {played_at}")
            input("\nPress Enter to continue...")
        
        elif choice == '6':
            break
        
        clear()
    
    print("Thanks for listening!")

if __name__ == "__main__":
    main()