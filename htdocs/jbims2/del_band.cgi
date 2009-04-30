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
        
        if ps == '1':
            tmpl_name_del_band = cfg.TMPL_DEL_BAND_PS1
            band = dao.get_band_by_id(id)
        elif ps == '2':
            tmpl_name_del_band = cfg.TMPL_DEL_BAND_PS2
            del_res = dao.delete_band(id)
            if del_res == True:
                log.info('del band. rec_id[%s], rec_version[%s]' % (id, ver))
            else:
                log.error('del band failed. rec_id[%s], rec_version[%s]' % (id, ver))
                return ut.redirect(cfg.URL_ERR_500)
        else:
            # redirect error page.
            log.warn('unknown process code. ps[%s], remote_addr[%s]' % (ps, os.environ.get('REMOTE_ADDR','')))
            return ut.redirect(cfg.URL_ERR_500)

        # set template.
        tmpl_lookup = TemplateLookup(cfg.DIR_TMPL, output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'])
        tmpl_entry  = tmpl_lookup.get_template(tmpl_name_del_band)

        print tmpl_entry.render(**locals())

        dao.close()

    except: 
        #TODO エラー画面リダイレクトできない
        log.error(exceptions.text_error_template().render())
        return ut.redirect(cfg.URL_ERR_500)

if __name__ == '__main__':
    main()
