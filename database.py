import sqlite3
from datetime import datetime

def init_db():
    """Initialize the SQLite database"""
    conn = sqlite3.connect('music_history.db')
    cursor = conn.cursor()
    file=open("schema.sql",'r')
    schema=file.read()
    cursor.executescript(schema)
    file.close()
    conn.commit()
    conn.close()

def add_song_to_history(song):
    """Add a played song to history"""
    conn = sqlite3.connect('music_history.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO history (title, artist, duration)
    VALUES (?, ?, ?)
    ''', (song.get_name(), song.get_artist(), song.get_duration()))
    
    conn.commit()
    conn.close()

def get_history(limit=20):
    """Retrieve playback history"""
    conn = sqlite3.connect('music_history.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT title, artist, duration, played_at 
    FROM history 
    ORDER BY played_at DESC 
    LIMIT ?
    ''', (limit,))
    
    history = cursor.fetchall()
    conn.close()
    return history