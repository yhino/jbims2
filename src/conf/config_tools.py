# -*- coding: utf-8 -*-
"""
JTOOLS 設定ファイル
"""

#-- URL設定
URL_TOP             = '/~club/jtools/'
URL_IMG             = URL_TOP + 'img/'
URL_CSS             = URL_TOP + 'style.css'
URL_ERR_500         = URL_TOP + 'err.html'
URL_HANDOVER        = URL_TOP + 'handover/'
URL_HANDOVER_DONE   = URL_HANDOVER + 'done.cgi'
URL_CTRL            = URL_TOP + 'control/'
URL_CTRL_ENTRY_LIVE = URL_CTRL + 'entry_live.cgi'
URL_JBIMSMASTER     = URL_TOP + 'jbimsmaster/'
URL_JBIMSMASTER_RESET_PASSWD = URL_TOP + 'jbimsmaster/reset_passwd.cgi'
URL_JBIMSMASTER_BACKUP = URL_TOP + 'jbimsmaster/backup.cgi'

#-- ディレクトリ
DIR_SYS     = '/Users/yhino/UHD/dev/jacla/src/'
DIR_LIB     = DIR_SYS + 'lib/'
DIR_DB      = DIR_SYS + 'db/'
DIR_TMPL    = DIR_SYS + 'tmpl/tools/'
DIR_CONF    = DIR_SYS + 'conf/'

#-- ファイルパス
LOG_CONF        = DIR_CONF  + 'log_tools.conf'
DB_ADMINS       = DIR_DB    + 'admins.db'
DB_BAND         = DIR_DB    + 'jbims.db'
HTPASSWD        = DIR_DB    + '.htpasswd'
LIVE_STATUS     = DIR_DB    + '.on_live'

#-- テンプレート名
TMPL_HEADER             = 'header.tmpl'
TMPL_FOOTER             = 'footer.tmpl'
TMPL_INDEX              = 'index.tmpl'
TMPL_HANDOVER_PS1       = 'handover_ps1.tmpl'
TMPL_HANDOVER_PS2       = 'handover_ps2.tmpl'
TMPL_HANDOVER_DONE      = 'handover_done.tmpl'
TMPL_CTRL_ENTRY_LIVE    = 'ctrl_entry_live.tmpl'
TMPL_JBIMSMASTER_LIST   = 'jbimsmaster_list.tmpl'
TMPL_JBIMSMASTER_RESET_PASSWD = 'jbimsmaster_reset_passwd.tmpl'
TMPL_JBIMSMASTER_BACKUP = 'jbimsmaster_backup.tmpl'

#-- 各種設定
DATA_DELIMITER = ''
CMD_HTPASSWD = '/usr/sbin/htpasswd -b'
CMD_TARGZ = '/usr/bin/tar cfz'
CMD_UNTARGZ = '/usr/bin/tar xfz'

#-- ツール設定
TOOL_LISTS = [
    {'url': URL_HANDOVER, 'name': 'Web管理者引継ぎ', 'desc': 'Web管理者の引継ぎ時に使用します'},
    {'url': URL_CTRL_ENTRY_LIVE, 'name': 'ライブエントリー管理', 'desc': 'JBIMSライブエントリー機能を管理します'},
    {'url': URL_JBIMSMASTER, 'name': 'バンド情報管理', 'desc': 'JBIMSバンド情報を管理します'},
]

#-- 取得リクエストキー
REQ_KEY_HANDOVER    = ('generation', 'dept', 'name_sei', 'name_mei', 'mail', 'account', 'passwd')

#-- 必須リクエストキー
REQUIRE_KEY_HANDOVER = {
    'generation': '入学年度を選択して下さい',
    'dept'      : '学部を入力して下さい',
    'name_sei'  : '名前（姓）を入力して下さい',
    'name_mei'  : '名前（名）を入力して下さい',
    'mail'      : 'メールアドレスを入力して下さい',
    'account'   : 'アカウントを入力して下さい',
    'passwd'    : 'パスワードを入力して下さい'
}
