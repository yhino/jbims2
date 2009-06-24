# encoding: utf-8
# version check
import sys
if sys.version[0] == "1":
	import regex
	remod = regex
elif sys.version[0] == "2":
	import re
	remod = re
else:
	import re
	remod = re

LF = chr(0x0A) # for Unix
CR = chr(0x0D) # for Mac
CL = CR + LF   # for Gates
NC = chr(0x00) # Null Character
UBLF = LF + NC # Unicode Big-Endian LF
UBCR = CR + NC # Unicode Big-Endian CR
UBCL = UBCR + UBLF # Unicode Big-Endian CR+LF
ULLF = NC + LF # Unicode Little-Endian LF
ULCR = NC + CR # Unicode Little-Endian CR
ULCL = ULLF + ULCR # Unicode Little-Endian CR+LF
BIG = chr(0xFF)+chr(0xFE) # Unicode Big-Endian
LIT = chr(0xFE)+chr(0xFF) # Unicode Little-Endian

def patadd(*hoe):
	ret = ""
	for ukyu in hoe:
		if(len(ret) == 0):
			ret = ret + ukyu
		else:
			ret = ret + "\|" + ukyu
	return(ret)

# 対象がUnicodeでない時に探す文字列
REC = remod.compile(patadd(LIT,BIG,CL,LF,CR))

# Temporary String
REUC = ['Honoka','Sawatari'] 

# Big-Endianの時に探す文字列
REUC[0] = remod.compile(patadd(LIT,BIG,UBCL,UBCR,UBLF))

# Little-Endianの時に探す文字列
REUC[1] = remod.compile(patadd(BIG,LIT,ULCL,ULCR,ULLF))


# 改行コードによらないReadLine()
#
# input_stringと改行文字を探し始める最初のpositionを与える
#
# Return Val ( one_line , next_start)
# one_lineにはstartposから始まった1行が返る。改行文字は含まない
# next_startには次に呼ぶ時のstartposが返る
# -1ならば文字列の終端
# input_stringがUnicodeの時にはエンディアン指示文字列 0xFEFF は返る
#
# 使い方
# pos = 0
# asd = crl()
# while(pos != -1):
# 	(One_Line,pos) = asd.ReadLine(input_string,pos)
#
class crl:
	# 対象がUnicodeでない時に探す文字列
	REC = remod.compile(patadd(LIT,BIG,CL,LF,CR))
	
	# Temporary String
	REUC = ['Honoka','Sawatari'] 
	
	# Big-Endianの時に探す文字列
	REUC[0] = remod.compile(patadd(LIT,BIG,UBCL,UBCR,UBLF))
	
	# Little-Endianの時に探す文字列
	REUC[1] = remod.compile(patadd(BIG,LIT,ULCL,ULCR,ULLF))

	ReadLine_UnicodeFlag = 0
	UnicodeChar_StartPos = 0
	ReadLine_UnicodeEndian = 0 # 0 is Big-Endian , 1 is Little-Endian

	def ReadLine(self,input_string,startpos):
		if(self.ReadLine_UnicodeFlag == 1):
			return(self.ReadLineUnicode(input_string,startpos))
		try:
			if((input_string[startpos:startpos+2] == BIG) | (input_string[startpos:startpos+2] == LIT)):
				self.ReadLine_UnicodeFlag = 1
				self.UnicodeChar_StartPos = startpos * 1
				return(self.ReadLineUnicode(input_string,startpos))
		except IndexError:
			pass
		hoe = REC.search(input_string,startpos)
		if(hoe < 0):
			return(input_string[startpos:],-1)
		try:
			if((input_string[hoe:hoe+2] == BIG) | (input_string[hoe:hoe+2] == LIT)):
				self.ReadLine_UnicodeFlag = 1
				self.UnicodeChar_StartPos = hoe * 1
				return(input_string[startpos:REC.regs[0][0]],REC.regs[0][0])
		except IndexError:
			pass
		return(input_string[startpos:REC.regs[0][0]],REC.regs[0][1])

	def ReadLineUnicode(self,input_string,startpos):
		hoe = self.REUC[self.ReadLine_UnicodeEndian].search(input_string,startpos)
		if(hoe < 0):
			return(input_string[startpos:],-1)
 		while((( hoe - self.UnicodeChar_StartPos) % 2) == 1):
			tstartpos = hoe + 1
			hoe = self.REUC[self.ReadLine_UnicodeEndian].search(input_string,tstartpos)
			if(hoe < 0):
				return(input_string[startpos:],-1)
		(reg0 , reg1) = self.REUC[self.ReadLine_UnicodeEndian].regs[0]
		if(input_string[reg0:reg1] == BIG):
			self.ReadLine_UnicodeEndian = 0
			if(startpos == reg0):
				return(input_string[startpos:reg1],reg1)
			else:
				return(input_string[startpos:reg0],reg0)
		if(input_string[reg0:reg1] == LIT):
			self.ReadLine_UnicodeEndian = 1
			if(startpos == reg0):
				return(input_string[startpos:reg1],reg1)
			else:
				return(input_string[startpos:reg0],reg0)
		return(input_string[startpos:reg0],reg1)
