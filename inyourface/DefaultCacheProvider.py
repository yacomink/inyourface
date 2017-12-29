import os, sqlite3
class CacheProvider(object):

    def __init__(self, cache_dir):
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)
        conn = sqlite3.connect(cache_dir + 'faces.db')
        self.cache_connection = conn
        c = conn.cursor()

        # Create table
        c.execute('''CREATE TABLE IF NOT EXISTS faces
                     (facesum char(32) PRIMARY KEY, face_data text)''')
        self.cache_connection.commit()

    def get(self, key):
        c = self.cache_connection.cursor()
        c.execute("select face_data FROM faces WHERE facesum = ?", (key,))
        res = c.fetchone()
        return res[0] if res else None

    def set(self, key, value):
        c = self.cache_connection.cursor()
        c.execute('REPLACE INTO faces (facesum, face_data) VALUES (?,?)', (key, value))
        self.cache_connection.commit()

    def close(self):
        self.cache_connection.close()        