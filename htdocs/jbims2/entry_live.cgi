#!/usr/bin/env python
# coding: utf-8

def main():
    import os, sys
    import cgi
    import traceback
    import cgitb;
    import logging.config
    import config as cfg

    sys.path.append(cfg.DIR_LIB)
    logging.config.fileConfig(cfg.LOG_CONF)
    cgitb.enable()

    from mako.lookup import TemplateLookup
    from mako import exceptions
    from jcore.util import Util
    from jcore.jband import Dao
    from jcore.controller import Controller
    from jcore.logger import Logger

    log = Logger()

    try:
        ut  = Util()
        req = cgi.FieldStorage()
        ctrller = Controller(cfg.LIVE_STATUS)

        ps  = ut.getParam(req, 'ps')    # entry process no.
        id  = ut.getParam(req, 'id')    # band reg id.
        ver  = ut.getParam(req, 'ver')  # band reg version.
        params = {}                     # for request params.
        errors = {}                     # for error.

        if ctrller.is_start() == False:
            # redirect error page.
            log.error('live entry is not start. errors = [id]')
            return ut.redirect(cfg.URL_ERR_500)
            
        if id == '':
            # redirect error page.
            log.error('validate error. errors = [id]')
            return ut.redirect(cfg.URL_ERR_500)
        if ver == '':
            # redirect error page.
            log.error('validate error. errors = [ver]')
            return ut.redirect(cfg.URL_ERR_500)

        if req.has_key('goback'):
            ps = '1'

        dao = Dao(cfg.DB_BAND)
        band = dao.get_band_by_id(id)

        if ps == '1':
            tmpl_name_entry_live = cfg.TMPL_ENTRY_LIVE_PS1

            # get request.
            for key in cfg.REQ_GET_KEY_ENTRY_LIVE_PS1:
                tmp = ut.getParam(req, key)
                if tmp != '':
                    params[key] = tmp

        elif ps == '2':
            tmpl_name_entry_live = cfg.TMPL_ENTRY_LIVE_PS2

            # get request.
            for key in cfg.REQ_GET_KEY_ENTRY_LIVE_PS1:
                tmp = ut.getParam(req, key)
                if tmp != '':
                    params[key] = tmp

            #todo うまくないから関数化
            # get member.
            members = []
            parts   = []
            for i in range(int(band.member_num)):
                members.append(ut.getParam(req, 'member'+ str(i)))
                parts.append(ut.getParam(req, 'part'+ str(i)))
                if cfg.REQUIRE_KEY_REG.has_key('member') and members[i] == '':
                    errors['member'+ str(i)] = cfg.REQUIRE_KEY_REG['member'] % (i+1)
            params['member'] = cfg.DATA_DELIMITER.join(members)
            params['part'] = cfg.DATA_DELIMITER.join(parts)

            # convert comment
            params['comment'] = cfg.DATA_DELIMITER.join(params['comment'].split("\r\n"))

            if len(errors) > 0:
                tmpl_name_entry_live = cfg.TMPL_ENTRY_LIVE_PS1

        elif ps == '3':
            tmpl_name_entry_live = cfg.TMPL_ENTRY_LIVE_PS3

            # get request.
            for key in cfg.REQ_GET_KEY_ENTRY_LIVE_PS3:
                params[key] = ut.getParam(req, key)

            #todo うまくないから関数化
            # list to scalar
            m_name = []
            m_time = []
            m_genre = []
            m_comp = []
            for i in range(len(band.music_name.split(cfg.DATA_DELIMITER))):
                m_name.append(ut.getParam(req, 'music_name'+ str(i)))
                m_time.append(ut.getParam(req, 'music_time'+ str(i)))
                m_genre.append(ut.getParam(req, 'music_genre'+ str(i)))
                m_comp.append(ut.getParam(req, 'music_comp'+ str(i)))
            params['music_name'] = cfg.DATA_DELIMITER.join(m_name)
            params['music_time'] = cfg.DATA_DELIMITER.join(m_time)
            params['music_genre'] = cfg.DATA_DELIMITER.join(m_genre)
            params['music_comp'] = cfg.DATA_DELIMITER.join(m_comp)

        elif ps == '4':
            tmpl_name_entry_live = cfg.TMPL_ENTRY_LIVE_PS4
            # get request.
            for key in cfg.REQ_GET_KEY_ENTRY_LIVE_PS4:
                params[key] = ut.getParam(req, key)
            reg_res = dao.regist_liveinfo(id, ver, params)
            if reg_res == True:
                band = dao.get_band_by_id(id)
                log.info('entry live. rec_id[%s], rec_version[%s], band_name[%s]' % (id, ver, band.band_name))
            else:
                log.error('entry live failed. rec_id[%s], rec_version[%s], band_name[%s]' % (id, ver, band.band_name))
                return ut.redirect(cfg.URL_ERR_500)

        else:
            # redirect error page.
            log.warn('unknown process code. ps[%s], remote_addr[%s]' % (ps, os.environ.get('REMOTE_ADDR','')))
            return ut.redirect(cfg.URL_ERR_500)

        # set template.
        tmpl_lookup = TemplateLookup(cfg.DIR_TMPL, output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'])
        tmpl_entry  = tmpl_lookup.get_template(tmpl_name_entry_live)

        print tmpl_entry.render(**locals())

        dao.close()

    except: 
        #TODO エラー画面リダイレクトできない
        log.error(exceptions.text_error_template().render())
        return ut.redirect(cfg.URL_ERR_500)

if __name__ == '__main__':
    main()
