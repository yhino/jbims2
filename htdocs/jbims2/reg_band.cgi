#!/usr/bin/env python
# coding: utf-8

def main():
    import os, sys
    import cgi
    import traceback
    import logging.config
    import config as cfg

    sys.path.append(cfg.DIR_LIB)
    logging.config.fileConfig(cfg.LOG_CONF)

    from mako.lookup import TemplateLookup
    from mako import exceptions
    from jcore.util import Util
    from jcore.jband import Dao
    from jcore.logger import Logger

    log = Logger()

    try:
        ut  = Util()
        req = cgi.FieldStorage()
        ps  = ut.getParam(req, 'ps')    # reg process no.
        b_data = {}                     # for band data.
        errors = {}                     # for error data.

        # check goback.
        if req.has_key('goback'):
            ps = '1'

        if ps == '1':
            tmpl_reg_name = cfg.TMPL_REG_PS1
            # get request.
            for key in cfg.REQ_GET_KEY_PS1:
                b_data[key] = ut.getParam(req, key)
        elif ps == '2':
            tmpl_reg_name = cfg.TMPL_REG_PS2

            # get request.
            for key in cfg.REQ_GET_KEY_PS2:
                b_data[key] = ut.getParam(req, key)
                # validate param.
                if cfg.REQUIRE_KEY_REG.has_key(key) and b_data[key] == '':
                    errors[key] = cfg.REQUIRE_KEY_REG[key]
            
            log.debug('get request. params[%s]' % (b_data))

            # check mailaddress.
            if not ut.chkMailAddr(b_data.get('leader_mail', '')):
                errors['leader_mail'] = '代表者メールアドレスを正しく入力して下さい'
            
            if len(errors) > 0:
                tmpl_reg_name = cfg.TMPL_REG_PS1
            else:    
                # crypt passwd.
                b_data['passwd'] = ut.cryptPasswd(b_data.get('passwd'))

        elif ps == '3':
            tmpl_reg_name = cfg.TMPL_REG_PS3

            # get request (without member).
            for key in cfg.REQ_GET_KEY_PS3:
                if key == 'member':
                    continue
                b_data[key] = ut.getParam(req, key)
                # validate param.
                if cfg.REQUIRE_KEY_REG.has_key(key) and b_data[key] == '':
                    errors[key] = cfg.REQUIRE_KEY_REG[key]
            # get member and part.
            members = []
            parts = []
            for i in range(int(b_data['member_num'])):
                m_key   = 'member'  + str(i)
                p_key   = 'part'    + str(i)
                members.append(ut.getParam(req, m_key))
                parts.append(ut.getParam(req, p_key))
                if cfg.REQUIRE_KEY_REG.has_key('member') and members[i] == '':
                    errors[m_key] = cfg.REQUIRE_KEY_REG['member'] % (i+1)
            b_data['member'] = members
            b_data['part'] = parts

            log.debug('get request. params[%s]' % (b_data))

            if len(errors) > 0:
                tmpl_reg_name = cfg.TMPL_REG_PS2
            else:
                # regist band.
                dao = Dao(cfg.DB_BAND)
                _rec_id = dao.regist_band(b_data)
                dao.close()
                log.info('regist band. rec_id[%s], band_name[%s]' % (_rec_id, b_data['band_name']))
        else:
            # エラー画面リダイレクト
            log.warn('unknown process code. ps[%s], remote_addr[%s]' % (ps, os.environ.get('REMOTE_ADDR','')))
            return ut.redirect(cfg.URL_ERR_500)

        # set template.
        tmpl_lookup = TemplateLookup(cfg.DIR_TMPL, output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'])
        tmpl_reg    = tmpl_lookup.get_template(tmpl_reg_name)

        print tmpl_reg.render(**locals())
    except:
        #TODO エラー画面リダイレクトしたい
        log.error(exceptions.text_error_template().render())
        return ut.redirect(cfg.URL_ERR_500)

if __name__ == '__main__':
    main()
