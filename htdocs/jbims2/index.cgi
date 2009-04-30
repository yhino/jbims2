#!/usr/bin/env python
# coding: utf-8

def main():
    import os, sys
    import traceback
    import urllib
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

    log = Logger()

    try:
        ut  = Util()

        # set template.
        tmpl_lookup = TemplateLookup(cfg.DIR_TMPL, output_encoding='utf-8', input_encoding='utf-8', default_filters=['decode.utf8'])
        tmpl_index  = tmpl_lookup.get_template(cfg.TMPL_INDEX)

        dao = Dao(cfg.DB_BAND)
        bands = dao.get_band_list()
        cnt_band = len(bands)
        ctrller = Controller(cfg.LIVE_STATUS)

        print tmpl_index.render(**locals())

        dao.close()
    except: 
        #TODO エラー画面リダイレクトできない
        log.error(exceptions.text_error_template().render())
        return ut.redirect(cfg.URL_ERR_500)

if __name__ == '__main__':
    main()
