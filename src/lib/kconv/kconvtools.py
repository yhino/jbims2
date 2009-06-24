# encoding: utf-8
#kconvtools 日本語処理ルーチン集

import cStringIO

TCR = chr(0x0D)
TLF = chr(0x0A)

def ChkHiragana(input_string,icode = ''):#ひらがなのみの文字列かどうかちぇっくする。
	import kconv
	if(icode == ''):
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = kconv.AUTO).convert(input_string))
	else:
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = icode).convert(input_string))
	i = ins.read(1)
	while(i != ""):
		if((i == "\t") | (i == " ") | (i == "\n") | (i == TCR) | (i == TLF)):#タブ、スペース、改行はO.K.
			i = ins.read(1)
			continue
		if(ord(i) == 0xA4):#平仮名のleader
			i = ins.read(1)
			if(i == ""):
				return(0)
			if(0xA1 <= ord(i) <= 0xF3):#平仮名のtrailer
				i = ins.read(1)
				continue
			return(0)
		if(ord(i) == 0xA1):#−〜ーも通す
			i = ins.read(1)
			if(i == ""):
				return(0)
			if((ord(i) == 0xBC) | (ord(i) == 0xC1) | (ord(i) == 0xDD)):
				i = ins.read(1)
				continue
		return(0)
	return(1)

def ChkKatakana(input_string,icode = ''):#カタカナのみの文字列かどうかチェックする
	import kconv
	if(icode == ''):
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = kconv.AUTO).convert(input_string))
	else:
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = icode).convert(input_string))
	i = ins.read(1)
	while(i != ""):
		if((i == "\t") | (i == " ") | (i == "\n") | (i == TCR) | (i == TLF)):#タブ、スペース、改行はO.K.
			i = ins.read(1)
			continue
		if(ord(i) == 0xA5):#カタカナのleader
			i = ins.read(1)
			if(i == ""):
				return(0)
			if(0xA1 <= ord(i) <= 0xF3):#カタカナのtrailer
				i = ins.read(1)
				continue
			return(0)
		if(ord(i) == 0xA1):#−〜ーも通す
			i = ins.read(1)
			if(i == ""):
				return(0)
			if((ord(i) == 0xBC) | (ord(i) == 0xC1) | (ord(i) == 0xDD)):
				i = ins.read(1)
				continue
		return(0)
	return(1)

def NumberConvert(input_string,icode = ''):#全角の数字を半角に変換
	import kconv
	if(icode == ''):
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = kconv.AUTO).convert(input_string))
	else:
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = icode).convert(input_string))
	out = cStringIO.StringIO()
	i = ins.read(1)
	while(i != ""):
		if((i == "\t") | (i == " ") | (i == "\n") | (i == TCR) | (i == TLF)):
			i = ins.read(1)
			continue
		if(("0" <= i) & (i <= "9")):
			out.write(i)
			i = ins.read(1)
			continue
		if(ord(i) == 0xA3):
			i = ins.read(1)
			if(i == ""):
				raise(ValueError)
			if(0xB0 <= ord(i) <= 0xB9):
				out.write(chr(ord(i)-0xB0+ord("0")))
				i = ins.read(1)
				continue
			raise(ValueError)
		raise(ValueError)
	return(out.getvalue())

def Han2Zen(input_string,icode = ''):#半角の英数字を全角に変換
	h2z = [ 0xA1A1 , 
		0xA1AA, 0xA1C9, 0xA1F4, 0xA1F0, 0xA1F3, 0xA1F5, 0xA1C7, 0xA1CA, 
		0xA1CB, 0xA1F6, 0xA1DC, 0xA1A4, 0xA1DD, 0xA1A5, 0xA1BF, 0xA3B0, 
		0xA3B1, 0xA3B2, 0xA3B3, 0xA3B4, 0xA3B5, 0xA3B6, 0xA3B7, 0xA3B8, 
		0xA3B9, 0xA1A7, 0xA1A8, 0xA1E3, 0xA1E1, 0xA1E4, 0xA1A9, 0xA1F7, 
		0xA3C1, 0xA3C2, 0xA3C3, 0xA3C4, 0xA3C5, 0xA3C6, 0xA3C7, 0xA3C8, 
		0xA3C9, 0xA3CA, 0xA3CB, 0xA3CC, 0xA3CD, 0xA3CE, 0xA3CF, 0xA3D0, 
		0xA3D1, 0xA3D2, 0xA3D3, 0xA3D4, 0xA3D5, 0xA3D6, 0xA3D7, 0xA3D8, 
		0xA3D9, 0xA3DA, 0xA1CE, 0xA1C0, 0xA1CF, 0xA1B0, 0xA1B2, 0xA1C6, 
		0xA3E1, 0xA3E2, 0xA3E3, 0xA3E4, 0xA3E5, 0xA3E6, 0xA3E7, 0xA3E8, 
		0xA3E9, 0xA3EA, 0xA3EB, 0xA3EC, 0xA3ED, 0xA3EE, 0xA3EF, 0xA3F0, 
		0xA3F1, 0xA3F2, 0xA3F3, 0xA3F4, 0xA3F5, 0xA3F6, 0xA3F7, 0xA3F8, 
		0xA3F9, 0xA3FA, 0xA1D0, 0xA1C3, 0xA1D1, 0xA1C1]
	
	import kconv
	if(icode == ''):
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = kconv.AUTO).convert(input_string))
	else:
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = icode).convert(input_string))
	out = cStringIO.StringIO()
	i = ins.read(1)
	while(i != ""):
		if( 0x20 <= ord(i) <= 0x7E ):
			code = h2z[ord(i)-0x20]
			out.write(chr(code>>8))
			out.write(chr(code & 0x00FF))
		else:
			out.write(i)
		i = ins.read(1)
	return(out.getvalue())

def Zen2Han(input_string,icode = ''):#半角の英数字を全角に変換
	#変換テーブル追加したい文字があればここへ追加 at EUC
	z2h = {
		'a1aa' : 0x21 , 'a1c9' : 0x22 , 'a1f4' : 0x23 , 'a1f0' : 0x24 , 
		'a1f3' : 0x25 , 'a1f5' : 0x26 , 'a1c7' : 0x27 , 'a1ca' : 0x28 , 
		'a1cb' : 0x29 , 'a1f6' : 0x2A , 'a1dc' : 0x2B , 'a1a4' : 0x2C , 
		'a1dd' : 0x2D , 'a1a5' : 0x2E , 'a1bf' : 0x2F , 'a3b0' : 0x30 , 
		'a3b1' : 0x31 , 'a3b2' : 0x32 , 'a3b3' : 0x33 , 'a3b4' : 0x34 , 
		'a3b5' : 0x35 , 'a3b6' : 0x36 , 'a3b7' : 0x37 , 'a3b8' : 0x38 , 
		'a3b9' : 0x39 , 'a1a7' : 0x3A , 'a1a8' : 0x3B , 'a1e3' : 0x3C , 
		'a1e1' : 0x3D , 'a1e4' : 0x3E , 'a1a9' : 0x3F , 'a1f7' : 0x40 , 
		'a3c1' : 0x41 , 'a3c2' : 0x42 , 'a3c3' : 0x43 , 'a3c4' : 0x44 , 
		'a3c5' : 0x45 , 'a3c6' : 0x46 , 'a3c7' : 0x47 , 'a3c8' : 0x48 , 
		'a3c9' : 0x49 , 'a3ca' : 0x4A , 'a3cb' : 0x4B , 'a3cc' : 0x4C , 
		'a3cd' : 0x4D , 'a3ce' : 0x4E , 'a3cf' : 0x4F , 'a3d0' : 0x50 , 
		'a3d1' : 0x51 , 'a3d2' : 0x52 , 'a3d3' : 0x53 , 'a3d4' : 0x54 , 
		'a3d5' : 0x55 , 'a3d6' : 0x56 , 'a3d7' : 0x57 , 'a3d8' : 0x58 , 
		'a3d9' : 0x59 , 'a3da' : 0x5A , 'a1ce' : 0x5B , 'a1c0' : 0x5C , 
		'a1cf' : 0x5D , 'a1b0' : 0x5E , 'a1b2' : 0x5F , 'a1c6' : 0x60 , 
		'a3e1' : 0x61 , 'a3e2' : 0x62 , 'a3e3' : 0x63 , 'a3e4' : 0x64 , 
		'a3e5' : 0x65 , 'a3e6' : 0x66 , 'a3e7' : 0x67 , 'a3e8' : 0x68 , 
		'a3e9' : 0x69 , 'a3ea' : 0x6A , 'a3eb' : 0x6B , 'a3ec' : 0x6C , 
		'a3ed' : 0x6D , 'a3ee' : 0x6E , 'a3ef' : 0x6F , 'a3f0' : 0x70 , 
		'a3f1' : 0x71 , 'a3f2' : 0x72 , 'a3f3' : 0x73 , 'a3f4' : 0x74 , 
		'a3f5' : 0x75 , 'a3f6' : 0x76 , 'a3f7' : 0x77 , 'a3f8' : 0x78 , 
		'a3f9' : 0x79 , 'a3fa' : 0x7A , 'a1d0' : 0x7B , 'a1c3' : 0x7C , 
		'a1d1' : 0x7D , 'a1c1' : 0x7E , 'a1a2' : 0x2C , 'a1a3' : 0x2E ,
		'a1d6' : 0x5B , 'a1d7' : 0x5D , 'a1ef' : 0x5C , 'a1c1' : 0x2D ,
		'a1bc' : 0x2D , 'a1a1' : 0x20 ,}

	def isEuc(inc):
		if( 0xA1 <= ord(inc) <= 0xFE ):
			return(1)
		return(0)

	def isAscii(inc):
		if( 0x00 <= ord(inc) <= 0x7F ):
			return(1)
		return(0)

	import kconv
	if(icode == ''):
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = kconv.AUTO).convert(input_string))
	else:
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = icode).convert(input_string))
	out = cStringIO.StringIO()
	i = ins.read(1)
	while(i != ""):
		if(isEuc(i)):
			try:
				code = i
				i = ins.read(1)
				char = chr(z2h["%x%x"%(ord(code),ord(i))])
				out.write(char)
			except(KeyError):
				out.write(code+i)
				pass
		elif(isAscii(i)):
			out.write(i)
		else:
			raise(KconvIncorrectInput)
		i = ins.read(1)
	return(out.getvalue())

def Hira2Kata(input_string,icode = ''): #平仮名をカタカナにする。漢字、記号は通す。
	def isEuc(inc):
		if( 0xA1 <= ord(inc) <= 0xFE ):
			return(1)
		return(0)

	def isAscii(inc):
		if( 0x00 <= ord(inc) <= 0x7F ):
			return(1)
		return(0)

	import kconv
	if(icode == ''):
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = kconv.AUTO).convert(input_string))
	else:
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = icode).convert(input_string))
	out = cStringIO.StringIO()
	i = ins.read(1)
	while(i != ""):
		if(isAscii(i)):
			out.write(i)
			i = ins.read(1)
			continue
		if(isEuc(i)):
			i2 = ins.read(1)
			if(ord(i) == 0xA4):#平仮名のleader
				if(i2 == ""): #入力文字列が途中で終っている
					break
				if(0xA1 <= ord(i2) <= 0xF3):#平仮名のtrailer
					out.write(chr(0xA5))
					out.write(i2)
					i = ins.read(1)
					continue
			out.write(i)
			out.write(i2)
			i = ins.read(1)
			continue
	return(out.getvalue())

def Kata2Hira(input_string,icode = ''): #カタカナを平仮名にする。漢字、記号は通す。
	def isEuc(inc):
		if( 0xA1 <= ord(inc) <= 0xFE ):
			return(1)
		return(0)

	def isAscii(inc):
		if( 0x00 <= ord(inc) <= 0x7F ):
			return(1)
		return(0)

	import kconv
	if(icode == ''):
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = kconv.AUTO).convert(input_string))
	else:
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = icode).convert(input_string))
	out = cStringIO.StringIO()
	i = ins.read(1)
	while(i != ""):
		if(isAscii(i)):
			out.write(i)
			i = ins.read(1)
			continue
		if(isEuc(i)):
			i2 = ins.read(1)
			if(ord(i) == 0xA5):#カタカナのleader
				if(i2 == ""): #入力文字列が途中で終っている
					break
				if(0xA1 <= ord(i2) <= 0xF3):#カタカナのtrailer
					out.write(chr(0xA4))
					out.write(i2)
					i = ins.read(1)
					continue
			out.write(i)
			out.write(i2)
			i = ins.read(1)
			continue
	return(out.getvalue())

def Upper(input_string,icode = ''): #全角半角を問わず小文字のアルファベットを大文字にする
	def isEuc(inc):
		if( 0xA1 <= ord(inc) <= 0xFE ):
			return(1)
		return(0)

	def isAscii(inc):
		if( 0x00 <= ord(inc) <= 0x7F ):
			return(1)
		return(0)

	import kconv
	if(icode == ''):
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = kconv.AUTO).convert(input_string))
	else:
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = icode).convert(input_string))
	out = cStringIO.StringIO()
	i = ins.read(1)
	while(i != ""):
		if isAscii(i):
			code = ord(i)
			if( 0x61<= code <= 0x7A ):
				out.write(chr(code - 0x20))
			else:
				out.write(i)
		elif isEuc(i):
			if( i == chr(0xA3)):
				out.write(chr(0xA3))
				i = ins.read(1)
				code = ord(i)
				if( 0xE1 <= code <= 0xFA):
					out.write(chr(code - 0x20))
				else:
					out.write(i)
			else:
				out.write(i)
				out.write(ins.read(1))
		else:
			out.write(i)
		i = ins.read(1)

	return(out.getvalue())

def Lower(input_string,icode = ''): #全角半角を問わず大文字のアルファベットを小文字にする
	def isEuc(inc):
		if( 0xA1 <= ord(inc) <= 0xFE ):
			return(1)
		return(0)

	def isAscii(inc):
		if( 0x00 <= ord(inc) <= 0x7F ):
			return(1)
		return(0)

	import kconv
	if(icode == ''):
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = kconv.AUTO).convert(input_string))
	else:
		ins = cStringIO.StringIO(kconv.Kconv(outcode=kconv.EUC,incode = icode).convert(input_string))
	out = cStringIO.StringIO()
	i = ins.read(1)
	while(i != ""):
		if isAscii(i):
			code = ord(i)
			if( 0x41<= code <= 0x5A ):
				out.write(chr(code + 0x20))
			else:
				out.write(i)
		elif isEuc(i):
			if( i == chr(0xA3)):
				out.write(chr(0xA3))
				i = ins.read(1)
				code = ord(i)
				if( 0xC1 <= code <= 0xDA):
					out.write(chr(code + 0x20))
				else:
					out.write(i)
			else:
				out.write(i)
				out.write(ins.read(1))
		else:
			out.write(i)
		i = ins.read(1)

	return(out.getvalue())
