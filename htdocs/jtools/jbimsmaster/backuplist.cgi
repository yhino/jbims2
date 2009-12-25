#!/usr/bin/env python
# coding: utf-8

def main():
    # module import.
    import os, sys
    import glob
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

        # create display values.
        fullfiles = glob.glob(cfg.DIR_DB+'/*.tgz');
        files = []
        for f in fullfiles:
            files.append(os.path.basename(f))
        files.reverse()
        file_cnt = len(files)

        tmpl_name = cfg.TMPL_JBIMSMASTER_BACKUPLIST
        # set template.
        tmpl_lookup = TemplateLookup(cfg.DIR_TMPL, output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'])
        tmpl_cls = tmpl_lookup.get_template(tmpl_name)

        print tmpl_cls.render(**locals())

    except:
        log.error(exceptions.text_error_template().render())
        return ut.redirect(cfg.URL_ERR_500)


if __name__ == '__main__':
    main()
