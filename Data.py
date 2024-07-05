
albums = []


def handle_album(line: str) -> dict:
    album_info = line[1:].split('::')
    album_name = album_info[0]
    album_year = album_info[1]
    album = {
        'name': album_name,
        'year': album_year,
        'songs': []
    }
    return album


def handle_song(line: str) -> dict:
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


def parse_file(database_file):
    with open(database_file, 'r', encoding='utf-8') as file:
        current_album = None
        for line in file:
            line = line.strip()
            if line.startswith('#'):
                current_album = handle_album(line)
                albums.append(current_album)
                current_song = None
            elif line.startswith('*'):
                current_song = handle_song(line)
                current_album['songs'].append(current_song)
            else:
                if current_song:
                    current_song['lyrics'] += f'\n{line}'
        return albums
