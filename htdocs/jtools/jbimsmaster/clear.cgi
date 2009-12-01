#!/usr/bin/env python
# coding: utf-8

def main():
    # module import.
    import os, sys
    from datetime import datetime
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

        # main process.
        # backup
        result, cmd, backupfile = dao.backup(cfg)
        if result == False:
            log.error('failed to backup band data. user[%s], remote_addr[%s], cmd[%s]' % (user, os.environ.get('REMOTE_ADDR',''), cmd))
            return ut.redirect(cfg.URL_ERR_500)
        else:
            log.info('success to backup band data. user[%s], remote_addr[%s], cmd[%s]' % (user, os.environ.get('REMOTE_ADDR',''), cmd))
        
        # close
        dao.close()
        # clear
        result, cmd = dao.clear(cfg)
        if result == False:
            log.error('failed to cleanup band data. user[%s], remote_addr[%s], cmd[%s]' % (user, os.environ.get('REMOTE_ADDR',''), cmd))
            return ut.redirect(cfg.URL_ERR_500)
        else:
            log.info('success to cleanup band data. user[%s], remote_addr[%s], cmd[%s]' % (user, os.environ.get('REMOTE_ADDR',''), cmd))

        # create
        dao.create(cfg.DB_BAND)

        tmpl_name = cfg.TMPL_JBIMSMASTER_CLEAR
        # set template.
        tmpl_lookup = TemplateLookup(cfg.DIR_TMPL, output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'])
        tmpl_cls = tmpl_lookup.get_template(tmpl_name)

        print tmpl_cls.render(**locals())

    except:
        log.error(exceptions.text_error_template().render())
        return ut.redirect(cfg.URL_ERR_500)


if __name__ == '__main__':
    main()
