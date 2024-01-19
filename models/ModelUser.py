from .entities.User import User

class ModelUser():
    @classmethod
    def login(self,db, user):
        try:
            cursor=db.connection.cursor()
            sql="""SELECT id, username, password FROM users
                    WHERE username = '{}'""".format(user.username)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                user=User(row[0],row[1],User.password_checker(row[2], user.password))
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def register(self, db, user, password):
        try:
            
            conn=db.connection

            cursor = conn.cursor()

            # Ejecutar una sentencia INSERT
            cursor.execute(f"INSERT INTO users (username, password) VALUES ('{user}', '{password}')")

            # Confirmar la transacción y cerrar la conexión
            conn.commit()
            cursor.close()
            
        except Exception as ex:
            raise Exception(ex)

        
    @classmethod
    def get_by_id(self,db,id):
        try:
            cursor=db.connection.cursor()
            sql="""SELECT id, username FROM users
                    WHERE id = '{}'""".format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                return User(row[0],row[1],None)
                
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
        
    
    @classmethod
    def create_post(self, db, posts, user, hora_actual):
        try:
            
            conn=db.connection

            cursor = conn.cursor()

            # Ejecutar una sentencia INSERT
            cursor.execute(f"INSERT INTO posts (post, user, hora_publicacion) VALUES ('{posts}', '{user}', '{hora_actual}')")

            # Confirmar la transacción y cerrar la conexión
            conn.commit()
            cursor.close()
            
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def create_admin_post(self, db, posts, user, hora_actual):
        try:
            
            conn=db.connection

            cursor = conn.cursor()

            # Ejecutar una sentencia INSERT
            cursor.execute(f"INSERT INTO admin (post, user, hora_publicacion) VALUES ('{posts}', '{user}', '{hora_actual}')")

            # Confirmar la transacción y cerrar la conexión
            conn.commit()
            cursor.close()
            
        except Exception as ex:
            raise Exception(ex)
        
    
    @classmethod
    def get_admin_post(self, db):
        try:
            conn=db.connection

            cursor = conn.cursor()
            cursor.execute(f"SELECT id, post, user, hora_publicacion FROM admin")
            row = cursor.fetchall()
            cursor.close()
            return row
            
            
        except Exception as ex:
            raise Exception(ex)
        
    
    @classmethod
    def get_post(self, db):
        try:
            conn=db.connection

            cursor = conn.cursor()
            cursor.execute(f"SELECT id, post, user, hora_publicacion FROM posts")
            row = cursor.fetchall()
            cursor.close()
            return row
            
            
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_post(self, db, id):
        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM posts WHERE id = %s", (id,))
        db.connection.commit()
        cursor.close()

        cursor = db.connection.cursor()
        cursor.execute("DELETE FROM admin WHERE id = %s", (id,))
        db.connection.commit()
        cursor.close()