#!/usr/bin/env python
# coding: utf-8

def main():
    # module import.
    import os, sys
    import cgi
    import cgitb
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
    
    try:
        log = Logger()
        ut  = Util()
        req = cgi.FieldStorage()
        dao = Dao(cfg.DB_BAND)

        user = ''

        # get admin name.
        if os.environ.has_key('REMOTE_USER'):
            user = os.environ['REMOTE_USER']
        else:
            log.error('get admin name failed.')
            return ut.redirect(cfg.URL_ERR_500)

        # get params.
        id  = ut.getParam(req, 'id')
        ver = ut.getParam(req, 'ver')
        newPasswd = ut.getRandStr()
        cryptNewPasswd = ut.cryptPasswd(newPasswd)

        # validate params.
        if id == '':
            log.error('validate error. id is empty.')
            return ut.redirect(cfg.URL_ERR_500)

        # main process.
        band = dao.get_band_by_id(id)
        if str(band.__version__) != ver:
            log.error('band ver is not equal. param_ver[%s] = band_ver[%s]' % (ver, band.__version__))
            return ut.redirect(cfg.URL_ERR_500)

        change_res = dao.change_passwd(id, ver, cryptNewPasswd)
        if change_res == True:
            log.info('success to reset passwd. user[%s], remote_addr[%s], rec_id[%s]' % (user, os.environ.get('REMOTE_ADDR',''), band.__id__))
        else:
            log.error('failed to reset passwd. user[%s], remote_addr[%s], rec_id[%s]' % (user, os.environ.get('REMOTE_ADDR',''), band.__id__))
            return ut.redirect(cfg.URL_ERR_500)

        tmpl_name = cfg.TMPL_JBIMSMASTER_RESET_PASSWD
        # set template.
        tmpl_lookup = TemplateLookup(cfg.DIR_TMPL, output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'])
        tmpl_cls = tmpl_lookup.get_template(tmpl_name)

        print tmpl_cls.render(**locals())

    except:
        log.error(exceptions.text_error_template().render())
        return ut.redirect(cfg.URL_ERR_500)


if __name__ == '__main__':
    main()
