# encoding: utf-8
#Kconv 0.5 Outputer
#EUC文字列をそれぞれのコードに変換

import cStringIO

from kconv import e2utablefile
from crl import LF
from crl import CL
from crl import CR
from common import baseclass

class Outputer(baseclass):                   #Outputer Interface & some methods
 	def output(self,input_string): #OutputerInterface
		return(input_string)
	
	def hankanapack(self,input_string,pos):
		c1 = ord(input_string[pos])
		pos = pos + 2
		try:
			c2 = ord(input_string[pos])
		except IndexError:
			return(c1 - 0xA1,pos - 2)
		if( c1 == 0xB3 and
			c2 == 0xDE ): #ヴ
			ret = 88
		elif( 0xB6 <= c1 <= 0xC4 and
			  c2 == 0xDE ): #ガ - ド
			ret = c1 - 0x77
		elif( 0xCA <= c1 <= 0xCE and
			  c2 == 0xDE ): #バ - ボ
			ret = c1 - 0xD5
		elif( 0xCA <= c1 <= 0xCE and
			  c2 == 0xDF ): #パ - ポ
			ret = c1 - 0xD0
		else: #他の半角カナ
			ret = c1 - 0xA1
			pos = pos - 2
		return(ret,pos)
	
	def __init__(self,Blcode):
		self.BLCODE = Blcode; #改行コードだよ

class JisOutputer(Outputer):   #EUC -> JIS
	def hankanaconv(self,input_string,cnt): #半角仮名に手を出さない
		return(input_string[cnt],cnt)

	def output(self,input_string):
		cnt = 0
		Jismode = self.Kc_None
		out = cStringIO.StringIO()
		ESC = self.ESC
		SS2 = self.SS2
		SS3 = self.SS3
		Escs = self.Kc_Escs
		while(cnt < len(input_string)):
			if self.isAscii(input_string[cnt]): #Ascii コード
				if(Jismode):
					out.write(Escs[self.Kc_Ascii])
					Jismode = self.Kc_None
				if(input_string[cnt] == LF):
					out.write(self.BLCODE)
				else:
					out.write(input_string[cnt])

			elif(self.isEuc(input_string[cnt])): #新JIS
				if(Jismode != self.Kc_J8):
					out.write(Escs[self.Kc_J8])
					Jismode = self.Kc_J8
				out.write(chr(ord(input_string[cnt]) & 0x7F))
				out.write(chr(ord(input_string[cnt+1]) & 0x7F))
				cnt = cnt + 1

			elif input_string[cnt] == SS2: #半角カナ
				cnt = cnt + 1
				chartowrite,cnt = self.hankanaconv(input_string,cnt)
				if self.isHankana(chartowrite[0]):
					if(Jismode):
						out.write(Escs[self.Kc_Ascii])
						Jismode = self.Kc_None
				else:
					if(Jismode != self.Kc_J8):
						out.write(Escs[self.Kc_J8])
						Jismode = self.Kc_J8
				out.write(chartowrite)

			elif input_string[cnt] == SS3: #補助漢字
				cnt = cnt + 1
				if(Jismode != self.Kc_J912):
					out.write(Escs[self.Kc_J912])
					JisMode = self.Kc_J912
				out.write(input_string[cnt:cnt+2])
				cnt = cnt + 1
					
			cnt = cnt + 1

		if Jismode:
			out.write(ESC+"(B")
		return(out.getvalue())

	def __init__(self,Blcode):
		Outputer.__init__(self,Blcode)

class JisZenkanaOutputer(JisOutputer): #EUC -> JIS 全角仮名に変換
#Table for kana -> JIS
	jisconvtable = (
		0x2123,0x2156,0x2157,0x2122,0x2126,0x2572,0x2521,0x2523,
		0x2525,0x2527,0x2529,0x2563,0x2565,0x2567,0x2543,0x213c,
		0x2522,0x2524,0x2526,0x2528,0x252a,0x252b,0x252d,0x252f,
		0x2531,0x2533,0x2535,0x2537,0x2539,0x253b,0x253d,0x253f,
		0x2541,0x2544,0x2546,0x2548,0x254a,0x254b,0x254c,0x254d,
		0x254e,0x254f,0x2552,0x2555,0x2558,0x255b,0x255e,0x255f,
		0x2560,0x2561,0x2562,0x2564,0x2566,0x2568,0x2569,0x256a,
		0x256b,0x256c,0x256d,0x256f,0x2573,0x212b,0x212c,
		#以下濁音文字
		0x252c,0x252e,0x2530,0x2532,0x2534,0x2536,0x2538,0x253a,
		0x253c,0x253e,0x2540,0x2542,0x2545,0x2547,0x2549,0x2550,
		0x2553,0x2556,0x2559,0x255c,0x2551,0x2554,0x2557,0x255a,
		0x255d,0x2574)
	
	def hankanaconv(self,input_string,cnt): #半角仮名を全角JISに変換（テーブル使用）
		index , cnt = self.hankanapack(input_string,cnt)
		leader = self.jisconvtable[index] >> 8
		trailer = self.jisconvtable[index] & 0xFF
		return(chr(leader)+chr(trailer),cnt)
		
class EucOutputer(Outputer):    #EUC -> EUC 何もしない(^^;
	def output(self,input_string):
		cnt = 0
		out = cStringIO.StringIO()
		while(cnt < len(input_string)):
			if(input_string[cnt] == LF):
				out.write(self.BLCODE)
			else:
				out.write(input_string[cnt])
			cnt = cnt + 1
		return(out.getvalue())

	def __init__(self,Blcode):
		Outputer.__init__(self,Blcode)

#Table for kana -> EUC
eucconvtable = (
	0xa1a3,0xa1d6,0xa1d7,0xa1a2,0xa1a6,0xa5f2,0xa5a1,0xa5a3,
	0xa5a5,0xa5a7,0xa5a9,0xa5e3,0xa5e5,0xa5e7,0xa5c3,0xa1bc,
	0xa5a2,0xa5a4,0xa5a6,0xa5a8,0xa5aa,0xa5ab,0xa5ad,0xa5af,
	0xa5b1,0xa5b3,0xa5b5,0xa5b7,0xa5b9,0xa5bb,0xa5bd,0xa5bf,
	0xa5c1,0xa5c4,0xa5c6,0xa5c8,0xa5ca,0xa5cb,0xa5cc,0xa5cd,
	0xa5ce,0xa5cf,0xa5d2,0xa5d5,0xa5d8,0xa5db,0xa5de,0xa5df,
	0xa5e0,0xa5e1,0xa5e2,0xa5e4,0xa5e6,0xa5e8,0xa5e9,0xa5ea,
	0xa5eb,0xa5ec,0xa5ed,0xa5ef,0xa5f3,0xa1ab,0xa1ac, # 63
	#以下濁音文字
	0xa5ac,0xa5ae,0xa5b0,0xa5b2,0xa5b4,0xa5b6,0xa5b8,0xa5ba,
	0xa5bc,0xa5be,0xa5c0,0xa5c2,0xa5c5,0xa5c7,0xa5c9,0xa5d0,
	0xa5d3,0xa5d6,0xa5d9,0xa5dc,0xa5d1,0xa5d4,0xa5d7,0xa5da,
	0xa5dd,0xa5f4) # 89

class EucZenkanaOutputer(EucOutputer): #EUC -> EUC 全角仮名に変換
	
	def output(self,input_string): #半角仮名を全EUCに変換（テーブル使用）
		cnt = 0
		out = cStringIO.StringIO()
		while(cnt < len(input_string)):
			if(input_string[cnt] == LF):
				out.write(self.BLCODE)
			elif(ord(input_string[cnt]) == 0x8E):
				cnt = cnt + 1
				index,cnt = self.hankanapack(input_string,cnt)
				out.write(chr(self.eucconvtable[index]>>8))
				out.write(chr(self.eucconvtable[index]&0xFF))
			else:
				out.write(input_string[cnt])
			cnt = cnt + 1
		return(out.getvalue())

	def __init__(self,Blcode):
		Outputer.__init__(self,Blcode)
		self.eucconvtable = eucconvtable
	
class SjisOutputer(Outputer):     #EUC -> SJIS
	def output(self,input_string):
		out = cStringIO.StringIO()
		SS2 = self.SS2
		SS3 = self.SS3
		cnt = 0
		while(cnt < len(input_string)):
			if self.isAscii(input_string[cnt]): #Ascii
				if(input_string[cnt] == LF):
					out.write(self.BLCODE)
				else:
					out.write(input_string[cnt])

			elif self.isEuc(input_string[cnt]): #新JIS
				leader = ord(input_string[cnt]) & 0x7F
				trailer = ord(input_string[cnt+1]) & 0x7F
				leader = leader - 0x21
				if leader & 0x1:
					trailer = trailer + 0x7E
				else:
					trailer = trailer + 0x1F
					if(0x7F <= trailer <= 0x9D):
						trailer = trailer + 1
				leader = (leader & 0x7E) >> 1
				if(0x00 <= leader <= 0x1E):
					leader = leader + 0x81
				else:
					leader = leader + 0xC1
				out.write(chr(leader)+chr(trailer))
				cnt = cnt + 1

			elif input_string[cnt] == SS2: #半角かな
				cnt = cnt + 1
				chartowrite, cnt = self.hankanaconv(input_string,cnt)
				out.write(chartowrite)

			elif input_string[cnt] == SS3: #補助漢字
				#補助漢字はSJISで表現不能なので無視
				cnt = cnt + 2
				
			cnt = cnt + 1
		return(out.getvalue())
	
	def hankanaconv(self,input_string,cnt): #半角仮名には触ない
		return(input_string[cnt],cnt)

	def __init__(self,Blcode):
		Outputer.__init__(self,Blcode)

class SjisZenkanaOutputer(SjisOutputer):
#Table for kana -> SJIS
	sjisconvtable = (
		0x8142,0x8175,0x8176,0x8141,0x8145,0x8392,0x8340,0x8342,
		0x8344,0x8346,0x8348,0x8383,0x8385,0x8387,0x8362,0x815b,
		0x8341,0x8343,0x8345,0x8347,0x8349,0x834a,0x834c,0x834e,
		0x8350,0x8352,0x8354,0x8356,0x8358,0x835a,0x835c,0x835e,
		0x8360,0x8363,0x8365,0x8367,0x8369,0x836a,0x836b,0x836c,
		0x836d,0x836e,0x8371,0x8374,0x8377,0x837a,0x837d,0x837e,
		0x8380,0x8381,0x8382,0x8384,0x8386,0x8388,0x8389,0x838a,
		0x838b,0x838c,0x838d,0x838f,0x8393,0x814a,0x814b,
		#以下濁音文字
		0x834b,0x834d,0x834f,0x8351,0x8353,0x8355,0x8357,0x8359,
		0x835b,0x835d,0x835f,0x8361,0x8364,0x8366,0x8368,0x836f,
		0x8372,0x8375,0x8378,0x837b,0x8370,0x8373,0x8376,0x8379,
		0x837c,0x8394)

	def hankanaconv(self,input_string,cnt):  #半角仮名を全角SJISに変換（テーブル使用）
		index , cnt = self.hankanapack(input_string,cnt)
		leader = self.sjisconvtable[index] >> 8
		trailer = self.sjisconvtable[index] & 0xFF
		return(chr(leader)+chr(trailer),cnt)
		

e2utable = 'UNLOADED'

class UnicOutputer(Outputer):     #EUC -> Unicode
	def output(self,input_string): #Unicodeで出力(半角仮名は全角に変換)
		global e2utable
		out = cStringIO.StringIO()
		cnt = 0
		SS2 = self.SS2
		SS3 = self.SS3
		if( e2utable == 'UNLOADED'):
			e2utable = open(e2utablefile,'rb').read()
		endian = 0 # big endian で出力。どっちがいいのか誰か教えて(^^;
		self.writehead(endian,out)
		while(cnt < len(input_string)):
			ch = 0
			if(input_string[cnt] == SS2): #半角かな
				cnt = cnt + 1
				index,cnt = self.hankanapack(input_string,cnt)
				ch = self.eucconvtable[index]

			if(input_string[cnt] == SS3): #補助漢字
				cnt = cnt + 2

			elif self.isAscii(input_string[cnt]):
				if(input_string[cnt] == LF):
					if(len(self.BLCODE)==2):
						write(CR+chr(0x00),endian,out)
					ch = ord(self.BLCODE[-1]) #改行文字の最後の文字
				else:
					ch = ord(input_string[cnt])
			else:
				ch = (ord(input_string[cnt]) << 8) + ord(input_string[cnt+1])
				cnt = cnt +1
			pos =  ((ch & 0x7F00) >> 1) + (ch & 0x7F)
			code = e2utable[2*pos:2*pos+2]
			if(ch != 0):
				self.write(code,endian,out)
			cnt = cnt + 1
		return(out.getvalue())

	def write(self,unicode,endian,out):
		out.write(unicode[endian]+unicode[1-endian])
		return
	
	def writehead(self,endian,out):
		out.write(chr(0xFF-endian) + chr(0xFE+endian))
		return
	
	def __init__(self,Blcode):
		Outputer.__init__(self,Blcode)
		self.eucconvtable = eucconvtable
		return
	
class Utf8Outputer(UnicOutputer):
	def write(self,unicode,endian,out):
		code = ord(unicode[0]) + (ord(unicode[1]) << 8)
#		if(code == 0):
		if((code & 0xFF80) == 0): #1バイトコード
			out.write( chr(code) )
		elif((code & 0xF800) == 0): #2バイトコード
			out.write( chr((code >> 6) | 0xC0) +
					   chr((code & 0x3F) | 0x80) )
		else: #3バイトコード 4バイトコードは無視(^^;
			out.write( chr((code >> 12) | 0xE0) +
					   chr(((code >> 6) & 0x3F) | 0x80) +
					   chr((code & 0x3F) | 0x80) )
		return

	def writehead(self,endian,out):
		return
	
class UnicZenkanaOutputer(UnicOutputer): #元から半角仮名は全角仮名に変換するようになっている。
	def output(self,input_string):
		return(UnicOutputer.output(self,input_string))

class Utf8ZenkanaOutputer(Utf8Outputer): #元から半角仮名は全角仮名に変換するようになっている。
	def output(self,input_string):
		return(Utf8Outputer.output(self,input_string))
