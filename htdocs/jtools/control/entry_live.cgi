#!/usr/bin/env python
# coding: utf-8

def main():
    # module import.
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
    from jcore.controller import Controller
    from jcore.logger import Logger
    
    try:
        log = Logger()
        ut  = Util()
        ctrller = Controller(cfg.LIVE_STATUS)
        req = cgi.FieldStorage()
        dao = Dao(cfg.DB_BAND)
        bands = dao.get_band_list()

        # init variables.
        user = ''
        func  = ut.getParam(req, 'func')
        params = {}
        errors = {}

        # get admin name.
        if os.environ.has_key('REMOTE_USER'):
            user = os.environ['REMOTE_USER']
        else:
            log.error('get admin name failed.')
            return ut.redirect(cfg.URL_ERR_500)

        try:
            if func == 'on':
                if ctrller.is_start() == False:
                    ctrller.start()
                log.info('success to start live entry. user[%s], remote_addr[%s]' % (user, os.environ.get('REMOTE_ADDR','')))
                return ut.redirect(cfg.URL_CTRL_ENTRY_LIVE)
            elif func == 'off':
                if ctrller.is_start() == True:
                    #todo clear live data.
                    for band in bands:
                        reset_res = dao.reset_live_entry(band.__id__, band.__version__)
                        if reset_res == True:
                            log.info('success to reset live entry. user[%s], remote_addr[%s], band[%s]' % (user, os.environ.get('REMOTE_ADDR',''), band.__id__))
                        else:
                            log.error('failed to reset live entry. user[%s], remote_addr[%s], band[%s]' % (user, os.environ.get('REMOTE_ADDR',''), band.__id__))
                            return ut.redirect(cfg.URL_ERR_500)
                    ctrller.stop()
                log.info('success to stop live entry. user[%s], remote_addr[%s]' % (user, os.environ.get('REMOTE_ADDR','')))
                return ut.redirect(cfg.URL_CTRL_ENTRY_LIVE)
        except:
            log.error('failed to control live entry. func[%s], user[%s], remote_addr[%s]' % (func, user, os.environ.get('REMOTE_ADDR','')))
            return ut.redirect(cfg.URL_ERR_500)

        # create display values.
        band_cnt = 0
        for band in bands:
            if band.live_entry == True:
                band_cnt += 1

        tmpl_name = cfg.TMPL_CTRL_ENTRY_LIVE
        # set template.
        tmpl_lookup = TemplateLookup(cfg.DIR_TMPL, output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'])
        tmpl_cls = tmpl_lookup.get_template(tmpl_name)

        print tmpl_cls.render(**locals())

    except:
        log.error(exceptions.text_error_template().render())
        return ut.redirect(cfg.URL_ERR_500)

if __name__ == '__main__':
    main()
