import pymysql
from config import db_name, password, host, user
import datetime






class My_Database:
    def __init__(self):
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=db_name,
            cursorclass=pymysql.cursors.DictCursor
        )

    def __del__(self):
        self.connection.close()


    def get_all_tables(self):
        insert_query = f"SELECT * FROM INFORMATION_SCHEMA.TABLES"
        with self.connection.cursor() as cursor:
            cursor.execute(insert_query)
            self.connection.commit()
            result = cursor.fetchall()
            dict_table = {}
            for table in result:
                if table['TABLE_SCHEMA'] == db_name:
                    dict_table[table['TABLE_SCHEMA']] = table['TABLE_NAME']
            return dict_table

    def insert_one_user(self, tg_id, tg_nickname):
        insert_query = f"""select tg_id from user"""
        with self.connection.cursor() as cursor:
            cursor.execute(insert_query)
            if any(d['tg_id'] == tg_id for d in cursor.fetchall()):
                return 'Already in table'
            else:
                insert_query = f"""insert into user (tg_id, tg_nickname) values
                                            ('{tg_id}','{tg_nickname}')"""
                cursor.execute(insert_query)
                self.connection.commit()
                return 'Inserted'


    def get_info_user(self, tg_id):
        insert_query = f"""select id, tg_id, tg_nickname from user where tg_id = {tg_id}"""
        with self.connection.cursor() as cursor:
            cursor.execute(insert_query)
            result = cursor.fetchall()
            return result[0]

    def insert_reminder(self, id_user, token, text, date_rim):
        insert_query = f"""insert into list_reminder (`id_user`,`token`, `text`, `date_rim`, `status`) values
                                                            ('{id_user}','{token}','{text}', '{date_rim}', 'wait')"""
        with self.connection.cursor() as cursor:
            cursor.execute(insert_query)
            self.connection.commit()
            return 'Inserted'

    def get_info_reminder(self, token):
        insert_query = f"""select id, id_user, token, text, date_rim, status from list_reminder where token = '{token}'"""
        with self.connection.cursor() as cursor:
            cursor.execute(insert_query)
            result = cursor.fetchall()
            return result[0]

    def get_all_reminder(self, tg_id):
        insert_query = f"""select lr.id_user, lr.token, lr.text, lr.date_rim, lr.status from list_reminder lr
                            join user u on lr.id_user = u.id
                            where u.tg_id = '{tg_id}' and lr.status = 'wait'"""
        with self.connection.cursor() as cursor:
            cursor.execute(insert_query)
            result = cursor.fetchall()
            dict_reminder = {}
            count_reminder = 1
            for reminder in result:
                dict_reminder[count_reminder] = reminder
                count_reminder += 1

            return dict_reminder

    def deactivate_reminder(self, token):
        query = f"update list_reminder set status = 'deactivate' where token = '{token}'"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def activate_reminder(self, token):
        query = f"update list_reminder set status = 'wait' where token = '{token}'"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def delete_reminder(self, token):
        query = f'update list_reminder set status ="delete" where token = "{token}"'
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def restore_reminder(self, token):
        query = f'update list_reminder set status = "wait" where token = "{token}"'
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

    def get_all_reminder_for_send(self):
        query = f"""select tg_id, text, date_rim, token from list_reminder lr
                    join user u on u.id = lr.id_user
                    where lr.status = 'wait'"""
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchall()
            dict_reminder = {}
            count_reminder = 1
            for reminder in result:
                dict_reminder[count_reminder] = reminder
                count_reminder += 1

            return dict_reminder

    def set_status_reminder(self, token, status):
        query = f"update list_reminder set status = '{status}' where token = '{token}'"
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

# db = My_Database()
# print(db.set_status_reminder('5QZ33W8HUS8E1NJA6E0H4', 'qwe'))