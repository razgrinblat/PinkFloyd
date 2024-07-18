class Album:
    def __init__(self):
        self.albums = []
        # A list of Albums that each album contains a dict of AlbumName, published year and list of song
        # each song contains a dict of songName, composer, duration and lyrics

    def handle_song(self,line: str) -> dict:
        song_info = line[1:].split('::')
        song_name = song_info[0]
        composer = song_info[1]
        duration = song_info[2]
        lyrics = song_info[3]
        song = {
            'name': song_name,
            'composer': composer,
            'duration': duration,
            'lyrics': lyrics
        }
        return song

    def handle_album(self, line: str) -> dict:
        album_info = line[1:].split('::')
        album_name = album_info[0]
        album_year = album_info[1]
        album = {
            'name': album_name,
            'year': album_year,
            'songs': []
        }
        return album


    def parse_file(self,database_file):
        """
        function to parse the DB.txt file into the albums list
        :param database_file: the path to the .txt database
        :return:  A list of album dictionaries, each containing song information.
        """
        # Opening the database file for reading with UTF-8 encoding
        with open(database_file, 'r', encoding='utf-8') as file:
            current_album = None
            for line in file:
                line = line.strip() # Removing leading/trailing whitespace from the line
                if line.startswith('#'):
                    # Line represents a new album
                    current_album = self.handle_album(line)
                    self.albums.append(current_album)
                    current_song = None
                elif line.startswith('*'):
                    # Line represents a new song
                    current_song = self.handle_song(line)
                    current_album['songs'].append(current_song)
                else:
                    # Line represents lyrics for the current song
                    if current_song:
                        current_song['lyrics'] += f'\n{line}' # Append the lyrics to the current song's lyrics
            return self.albums   # Return the list of parsed albums



