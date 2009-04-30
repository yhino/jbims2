#!/usr/bin/python
# -*- coding: utf-8 -*-

def main():
    basedir = '/Users/yhino/UHD/dev/jacla/src'
    import sys
    from datetime import datetime
    import traceback
    sys.path.append(basedir+'/lib')
    from buzhug import Base

    try:
        db = Base(basedir+'/db/admins.db')
        db.create(
            ('generation'   , str),
            ('dept'         , str),
            ('name_sei'     , str),
            ('name_mei'     , str),
            ('mail'         , str),
            ('account'      , str),
            ('passwd'       , str),
            ('add_dt'       , datetime),
            ('upd_dt'       , datetime)
            , mode="override")
    except:
        print "buzhug error."
        traceback.print_exc()

if __name__ == '__main__':
    main()
