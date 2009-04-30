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
        db = Base(basedir+'/db/jbims.db')
        db.create(
            ('id'           , str),
            ('band_name'    , str),
            ('genre'        , str),
            ('leader_name'  , str),
            ('leader_mail'  , str),
            ('passwd'       , str),
            ('member_num'   , int),
            ('member'       , str),
            ('part'         , str),
            ('music_name'   , str),
            ('music_time'   , str),
            ('music_genre'  , str),
            ('music_comp'   , str),
            ('comment'      , str),
            ('live_entry'   , bool),
            ('stage_setting', str),
            ('stage_info'   , str),
            ('add_dt'       , datetime),
            ('upd_dt'       , datetime)
            , mode="override")
    except:
        print "buzhug error."
        traceback.print_exc()

if __name__ == '__main__':
    main()
