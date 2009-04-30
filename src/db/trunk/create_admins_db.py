#!/usr/bin/python
# -*- coding: utf-8 -*-

def main():
    import sys
    from datetime import datetime
    import traceback
    sys.path.append('/Users/yoshiyuki/dev/jbims2/lib')
    from buzhug import Base

    try:
        db = Base('/Users/yoshiyuki/dev/jbims2/db/admins_db')
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
