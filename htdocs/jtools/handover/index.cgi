#!/usr/bin/env python
# coding: utf-8

def main():
    # module import.
    import os, sys
    import cgi
    import datetime
    import traceback
    import logging.config
    import config as cfg

    sys.path.append(cfg.DIR_LIB)
    logging.config.fileConfig(cfg.LOG_CONF)

    from mako.lookup import TemplateLookup
    from mako import exceptions
    from jcore.util import Util
    from jcore.jadmin import Dao
    from jcore.logger import Logger
    
    try:
        log = Logger()
        ut  = Util()
        req = cgi.FieldStorage()
        dao = Dao(cfg.DB_ADMINS)
        dt  = datetime.datetime.today()

        # init variables.
        user = ''
        ps  = ut.getParam(req, 'ps', '1')
        params = {}
        errors = {}

        # get admin name.
        if os.environ.has_key('REMOTE_USER'):
            user = os.environ['REMOTE_USER']
        else:
            log.error('get admin name failed.')
            return ut.redirect(cfg.URL_ERR_500)

        if ps == '1':
            tmpl_name = cfg.TMPL_HANDOVER_PS1
            pass
        elif ps == '2':
            tmpl_name = cfg.TMPL_HANDOVER_PS2
            #-- get request
            params = ut.getParams(req, cfg.REQ_KEY_HANDOVER, cfg.REQUIRE_KEY_HANDOVER, errors)
            log.debug('get request. params[%s]' % (params))
            #-- check mailaddress
            if not ut.chkMailAddr(params.get('mail')):
                errors['mail'] = 'メールアドレスを正しく入力して下さい'
            #-- check error
            if len(errors) > 0:
                ps = int(ps) - 1
                tmpl_name = cfg.TMPL_HANDOVER_PS1
        elif ps == '3':
            #-- get request
            params = ut.getParams(req, cfg.REQ_KEY_HANDOVER, cfg.REQUIRE_KEY_HANDOVER, errors)
            log.debug('get request. params[%s]' % (params))
            #-- check mailaddress
            if not ut.chkMailAddr(params.get('mail')):
                errors['mail'] = 'メールアドレスを正しく入力して下さい'
            #-- check error
            if len(errors) > 0:
                #-- redirect error page.
                log.warn('params is invalid. ps[%s], user[%s], remote_addr[%s]' % (ps, user, os.environ.get('REMOTE_ADDR','')))
                return ut.redirect(cfg.URL_ERR_500)
            else:
                #-- regist db
                try:
                    params['crypt_passwd'] = ut.cryptPasswd(params.get('passwd'))
                    id = dao.regist_admin(params)
                    log.info("success to regist admin. account[%s], user[%s], remote_addr[%s]" % (params.get('account'), user, os.environ.get('REMOTE_ADDR','')))
                except:
                    log.error("failed to regist admin. account[%s], user[%s], remote_addr[%s]" % (params.get('account'), user, os.environ.get('REMOTE_ADDR','')))
                    return ut.redirect(cfg.URL_ERR_500)
                #-- regist htpasswd
                try:
                    cmd = '%s %s %s %s' % (cfg.CMD_HTPASSWD, cfg.HTPASSWD, params.get('account'), params.get('passwd'))
                    res = os.system(cmd)
                    if res != 0:
                        raise
                    log.info("htpasswd exec success. account[%s], user[%s], remote_addr[%s]" % (params.get('account'), user, os.environ.get('REMOTE_ADDR','')))
                except:
                    log.error("htpasswd exec failed. account[%s], cmd[%s], user[%s], remote_addr[%s]" % (params.get('account'), cmd, user, os.environ.get('REMOTE_ADDR','')))
                    return ut.redirect(cfg.URL_ERR_500)
                return ut.redirect(cfg.URL_HANDOVER_DONE)
        else:
            # redirect error page.
            log.warn('unknown process code. ps[%s], user[%s], remote_addr[%s]' % (ps, user, os.environ.get('REMOTE_ADDR','')))
            return ut.redirect(cfg.URL_ERR_500)

        # set template.
        tmpl_lookup = TemplateLookup(cfg.DIR_TMPL, output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'])
        tmpl_cls = tmpl_lookup.get_template(tmpl_name)

        print tmpl_cls.render(**locals())

    except:
        log.error(exceptions.text_error_template().render())
        return ut.redirect(cfg.URL_ERR_500)

if __name__ == '__main__':
    main()
