from datetime import datetime
from buzhug import Base

class Dao:
    def __init__(self, dbname):
        self.db = Base(dbname).open()
        self.db.set_string_format(unicode, 'utf-8')

    def regist_admin(self, data):
        return self.db.insert(
            generation  = data.get('generation'),
            dept        = data.get('dept'),
            name_sei    = data.get('name_sei'),
            name_mei    = data.get('name_mei'),
            mail        = data.get('mail'),
            account     = data.get('account'),
            passwd      = data.get('crypt_passwd'),
            add_dt      = datetime.now()
        )

    def get_admins(self):
        result = self.db.select()
        return result

    def close(self):
        self.db.close()

    def __del__(self):
        self.db.close()
