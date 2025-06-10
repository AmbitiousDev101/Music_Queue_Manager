def time_to_seconds(time_str):
    """Convert time string to seconds"""
    parts = time_str.split(":")
    if len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
    elif len(parts) == 2:
        minutes, seconds = map(int, parts)
        hours = 0
    else:
        raise ValueError("Invalid time format")
    return hours * 3600 + minutes * 60 + seconds

def seconds_to_time_format(seconds):
    """Convert seconds to time string"""
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours}:{minutes:02}:{seconds:02}" if hours else f"{minutes}:{seconds:02}"

class Song:
    def __init__(self, name, artist, dur):
        self.name = name
        self.artist = artist
        self.duration = dur

    def get_name(self): return self.name
    def get_artist(self): return self.artist
    def get_duration(self): return self.duration
    
    def __str__(self):
        return f"{self.name}\n   Artists: {self.artist}\n   Duration: {seconds_to_time_format(self.duration)}"

class MusicQueue:
    def __init__(self):
        self.items = []
        self.length = 0

    def enqueue_b(self, item):
        self.items.append(item)
        self.length += item.get_duration()

    def enqueue_f(self, item):
        self.items.insert(0, item)
        self.length += item.get_duration()
            
    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue is empty")
        popped = self.items.pop(0)
        self.length -= popped.get_duration()
        return popped
    
    def peek(self):
        if self.is_empty():
            raise Exception("Queue is empty")
        return self.items[0]
           
    def is_empty(self): return len(self.items) == 0
    def size(self): return len(self.items)
    def clear(self):
        self.items = []
        self.length = 0

    def __str__(self):
        str_exp = f"\nQUEUE LENGTH: {seconds_to_time_format(self.length)}\nSONGS QUEUED: {self.size()}\n"  
        for i, item in enumerate(self.items, 1):
            str_exp += f"{i}. {item}\n"
        return str_exp.strip('\n')