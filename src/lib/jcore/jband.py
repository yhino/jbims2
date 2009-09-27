import os
from datetime import datetime
from buzhug import Base

class Dao:
    DELIMITER = ''

    def __init__(self, dbname):
        self.db = Base(dbname).open()
        self.db.set_string_format(unicode, 'utf-8')

    def get_band_list(self):
        result = self.db.select()
        return result

    def get_band_by_id(self, id):
        result = self.db[int(id)]
        return result

    def regist_band(self, data):
        # formatting data.
        member_str = self.DELIMITER.join(data['member'])
        part_str = self.DELIMITER.join(data['part'])
        music_name_str = self.DELIMITER.join(data['music_name'].split("\r\n"))
        comment_str = self.DELIMITER.join(data['comment'].split("\r\n"))
        
        id = self.db.insert(
            band_name = data['band_name'],
            genre = data['genre'],
            leader_name = data['leader_name'],
            leader_mail = data['leader_mail'],
            passwd = data['passwd'],
            member_num = int(data['member_num']),
            member = member_str,
            part = part_str,
            comment = comment_str,
            music_name = music_name_str,
            music_time = '',
            music_genre = '',
            music_comp = '',
            stage_setting = '',
            stage_info = '',
            live_entry = False,
            add_dt = datetime.now()
        )
        return id 

    def regist_liveinfo(self, id, ver, data):
        old_data = self.get_band_by_id(id)
        
        if old_data.__version__ != int(ver):
            return False
        self.db.update(
            old_data,
            band_name = data['band_name'],
            genre = data['genre'],
            member = data['member'],
            part = data['part'],
            comment = data['comment'],
            music_name = data['music_name'],
            music_time = data['music_time'],
            music_genre = data['music_genre'],
            music_comp = data['music_comp'],
            upd_dt = datetime.now()
        )
        return True

    def entry_live(self, id, ver, data):
        old_data = self.get_band_by_id(id)

        if old_data.__version__ != int(ver):
            return False
        self.db.update(
            old_data,
            stage_setting = data['stage_setting'],
            stage_info = data['s_supplement'],
            live_entry = True,
            upd_dt = datetime.now()
        )
        return True

    def reset_live_entry(self, id, ver):
        old_data = self.get_band_by_id(id)

        if old_data.__version__ != int(ver):
            return False
        self.db.update(
            old_data,
            music_time = '',
            music_genre = '',
            music_comp = '',
            stage_setting = '',
            stage_info = '',
            live_entry = False,
            upd_dt = datetime.now()
        )
        return True

    def edit_band(self, id, ver, data):
        old_data = self.get_band_by_id(id)

        if old_data.__version__ != int(ver):
            return False
        self.db.update(
            old_data,
            band_name = data['band_name'],
            genre = data['genre'],
            leader_name = data['leader_name'],
            leader_mail = data['leader_mail'],
            passwd = data['passwd'],
            member_num = int(data['member_num']),
            member = data['member'],
            part = data['part'],
            music_name = data['music_name'],
            comment = data['comment'],
            upd_dt = datetime.now()
        )
        return True
    
    def change_passwd(self, id, ver, newPasswd):
        old_data = self.get_band_by_id(id)

        if old_data.__version__ != int(ver):
            return False
        self.db.update(
            old_data,
            passwd = newPasswd,
            upd_dt = datetime.now()
        )
        return True

    def delete_band(self, id):
        before_cnt = len(self.db)
        del self.db[int(id)]
        after_cnt = len(self.db)
        if before_cnt > after_cnt:
            return True
        return False

    """
    backup jbims band data.
    @return processResult, execCommand, backupFile
    """
    def backup(self, cfg):
        now = datetime.now()
        backupfile = '%s-%s.tgz' % (cfg.DB_BAND, now.strftime('%Y%m%d'))
        cmd = '%s %s -C%s %s' % (cfg.CMD_TARGZ, backupfile, cfg.DIR_DB, cfg.DB_BAND.replace(cfg.DIR_DB,''))
        res = os.system(cmd)
        if res != 0:
            return False, cmd, backupfile
        return True, cmd, backupfile

    def clear(self):
        pass

    def close(self):
        self.db.close()

    def __del__(self):
        self.db.close()
