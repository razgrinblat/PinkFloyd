

database_file = "Pink_Floyd_DB.txt"
albums = []
def parse_file(database_file):
    with open(database_file,'r',encoding= 'utf-8') as f:
        current_album = None
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                album_info = line[1:].split('::')
                album_name = album_info[0]
                album_year = album_info[1]
                current_album = {
                    'name' : album_name,
                    'year' : album_year,
                    'songs' : []
                }
                albums.append(current_album)
                current_song = None
            elif line.startswith('*'):
                song_info = line[1:].split('::')
                song_name = song_info[0]
                composer = song_info[1]
                duration = song_info[2]
                lyrics = song_info[3]
                current_song = {
                    'name' : song_name,
                    'composer' : composer,
                    'duration' : duration,
                    'lyrics' : lyrics
                }
                current_album['songs'].append(current_song)
            else:
                if current_song:
                    current_song['lyrics'] += f'\n{line}'
        return albums



