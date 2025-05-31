import psycopg2

class Database:
    def __init__(self, dbname, user, password, host="localhost", port="5432"):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.conn = None
        self.cur = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)
            self.cur = self.conn.cursor()
            print("Conexión a la base de datos exitosa.")
        except psycopg2.OperationalError as e:
            print(f"Error al conectar a la base de datos: {e}")
            self.conn = None
            self.cur = None

    def disconnect(self):
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("Conexión a la base de datos cerrada.")

    def create_user(self, username, password):
        if not self.conn:
            print("No hay conexión a la base de datos.")
            return False
        try:
            # Verificar si el usuario ya existe
            self.cur.execute("SELECT id FROM usuarios WHERE username = %s", (username,))
            if self.cur.fetchone() is not None:
                print("El usuario ya existe.")
                return False
                
            self.cur.execute("INSERT INTO usuarios (username, password) VALUES (%s, %s)", (username, password))
            self.conn.commit()
            print(f"Usuario {username} creado exitosamente.")
            return True
        except psycopg2.Error as e:
            print(f"Error al crear usuario: {e}")
            self.conn.rollback()
            return False

    def login_user(self, username, password):
        if not self.conn:
            print("No hay conexión a la base de datos.")
            return False
        try:
            self.cur.execute("SELECT password FROM usuarios WHERE username = %s", (username,))
            result = self.cur.fetchone()
            if result is not None and result[0] == password:
                print(f"Inicio de sesión exitoso para el usuario {username}.")
                return True
            else:
                print("Usuario o contraseña incorrectos.")
                return False
        except psycopg2.Error as e:
            print(f"Error al iniciar sesión: {e}")
            return False

# Ejemplo de uso (esto se eliminará o adaptará al integrarlo con el juego)
# if __name__ == "__main__":
#     db = Database(dbname="your_db_name", user="postgres", password="root")
#     db.connect()
#     db.create_user("test_user", "test_password")
#     db.login_user("test_user", "test_password")
#     db.login_user("wrong_user", "wrong_password")
#     db.disconnect() 