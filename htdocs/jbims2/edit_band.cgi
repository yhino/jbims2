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
    from jcore.logger import Logger

    log = Logger()

    try:
        ut  = Util()
        req = cgi.FieldStorage()
        ps  = ut.getParam(req, 'ps')    # entry process no.
        id  = ut.getParam(req, 'id')    # band reg id.
        ver  = ut.getParam(req, 'ver')  # band reg version.
        params = {}                     # for request params.
        errors = {}                     # for error.

        if id == '':
            # redirect error page.
            log.error('validate error. errors = [id]')
            return ut.redirect(cfg.URL_ERR_500)
        if ver == '':
            # redirect error page.
            log.error('validate error. errors = [ver]')
            return ut.redirect(cfg.URL_ERR_500)

        if req.has_key('cancel'):
            return ut.redirect(cfg.URL_TOP)

        dao = Dao(cfg.DB_BAND)
        band = dao.get_band_by_id(id)
        
        if ps == '1':
            tmpl_name_edit_band = cfg.TMPL_EDIT_BAND_PS1
            # get request.
            for key in cfg.REQ_GET_KEY_EDIT_BAND_PS1:
                tmp = ut.getParam(req, key)
                if tmp != '':
                    params[key] = tmp
        elif ps == '2':
            tmpl_name_edit_band = cfg.TMPL_EDIT_BAND_PS2
            # get request.
            for key in cfg.REQ_GET_KEY_EDIT_BAND_PS2:
                params[key] = ut.getParam(req, key)
                if key == 'passwd' or key == 're_passwd':
                    if params['chg_passwd'] != '':
                        continue
                # validate param.
                if cfg.REQUIRE_KEY_REG.has_key(key) and params[key] == '':
                    errors[key] = cfg.REQUIRE_KEY_REG[key]

            log.debug('get request. params[%s]' % (params))

            # check mailaddress.
            if not ut.chkMailAddr(params.get('leader_mail', '')):
                errors['leader_mail'] = '代表者メールアドレスを正しく入力して下さい'

            # check passwd
            if params['chg_passwd'] == '':
                if params.get('passwd') != params.get('re_passwd'):
                    errors['passwd'] = 'パスワード(再入力)と一致しません'
                    errors['re_passwd'] = 'パスワードと一致しません'

            if len(errors) > 0:
                tmpl_name_edit_band = cfg.TMPL_EDIT_BAND_PS1
            else:    
                # crypt passwd.
                if params['chg_passwd'] == '':
                    params['passwd'] = ut.cryptPasswd(params.get('passwd'))
                else:
                    params['passwd'] = band.passwd

        elif ps == '3':
            tmpl_name_edit_band = cfg.TMPL_EDIT_BAND_PS3
            # get request (without member).
            for key in cfg.REQ_GET_KEY_EDIT_BAND_PS3:
                if key == 'member':
                    continue
                params[key] = ut.getParam(req, key)
                # validate param.
                if cfg.REQUIRE_KEY_REG.has_key(key) and params[key] == '':
                    errors[key] = cfg.REQUIRE_KEY_REG[key]
            # get member and part.
            members = []
            parts   = []
            for i in range(int(params.get('member_num'))):
                members.append(ut.getParam(req, 'member'+ str(i)))
                parts.append(ut.getParam(req, 'part'+ str(i)))
                if cfg.REQUIRE_KEY_REG.has_key('member') and members[i] == '':
                    errors['member'+ str(i)] = cfg.REQUIRE_KEY_REG['member'] % (i+1)
            params['member'] = cfg.DATA_DELIMITER.join(members)
            params['part'] = cfg.DATA_DELIMITER.join(parts)

            log.debug('get request. params[%s]' % (params))

            # convert comment
            params['music_name'] = cfg.DATA_DELIMITER.join(params['music_name'].split("\r\n"))
            params['comment'] = cfg.DATA_DELIMITER.join(params['comment'].split("\r\n"))

            if len(errors) > 0:
                tmpl_reg_name = cfg.TMPL_REG_PS2
            else:
                # edit band.
                edit_res = dao.edit_band(id, ver, params)
                if edit_res == True:
                    band = dao.get_band_by_id(id)
                    log.info('edit band. rec_id[%s], rec_version[%s], band_name[%s]' % (id, ver, band.band_name))
                else:
                    log.error('edit band failed. rec_id[%s], rec_version[%s], band_name[%s]' % (id, ver, band.band_name))
                    return ut.redirect(cfg.URL_ERR_500)
        else:
            # redirect error page.
            log.warn('unknown process code. ps[%s], remote_addr[%s]' % (ps, os.environ.get('REMOTE_ADDR','')))
            return ut.redirect(cfg.URL_ERR_500)

        # set template.
        tmpl_lookup = TemplateLookup(cfg.DIR_TMPL, output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'])
        tmpl_entry  = tmpl_lookup.get_template(tmpl_name_edit_band)

        print tmpl_entry.render(**locals())

        dao.close()

    except: 
        #TODO エラー画面リダイレクトできない
        log.error(exceptions.text_error_template().render())
        return ut.redirect(cfg.URL_ERR_500)

if __name__ == '__main__':
    main()
