#!/usr/bin/env python
# coding: utf-8

def main():
    import os, sys
    import cgi
    import traceback
    import cgitb
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
        params = {}     # for request params.
        errors = {}     # for error.
        
        # get request (but out passwd).
        for key in cfg.REQ_GET_KEY_LOGIN:
            params[key] = ut.getParam(req, key)
            # validate param.
            if cfg.REQUIRE_KEY_LOGIN.has_key(key) and params[key] == '':
                # redirect error page.
                log.error('validate error. errors = [%s]' % (cfg.REQUIRE_KEY_LOGIN[key]))
                return ut.redirect(cfg.URL_ERR_500)
        
        # authenticate band reader.
        params['passwd'] = ut.getParam(req, 'passwd')
        if params.get('passwd') != '':
            dao = Dao(cfg.DB_BAND)
            band = dao.get_band_by_id(params.get('id'))
            dao.close()
            if (ut.cryptPasswd(params.get('passwd')) == band.passwd):
                return ut.redirect(params.get('_done'))
            else:
                errors['passwd'] = 'パスワードが間違っています。ログイン出来ません。'

        # set template.
        tmpl_lookup = TemplateLookup(cfg.DIR_TMPL, output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'])
        tmpl_login  = tmpl_lookup.get_template(cfg.TMPL_LOGIN)

        print tmpl_login.render(**locals())

    except: 
        #TODO エラー画面リダイレクトできない
        log.error(exceptions.text_error_template().render())
        return ut.redirect(cfg.URL_ERR_500)

if __name__ == '__main__':
    main()
