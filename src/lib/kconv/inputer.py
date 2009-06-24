# encoding: utf-8
#Kconv0.5 Inputer
#入力文字列をEUCに変換
#半角仮名は0x8E+??で格納（2バイト半角仮名）
#改行はLFに変換して格納

import cStringIO
from kconv import u2etablefile
from crl import LF
from crl import CR
from crl import CL
from crl import REUC
from kconv import DROP
from kconv import CONVERT
from common import baseclass

class Inputer(baseclass):             #inputer interface & some methods
	def input(self,input_string):
		return input_string
	
	def __init__(self,gaijiconvert):
		if(gaijiconvert == DROP):
			self.OpGaiji = self.OpGaijiCut
		else:
			self.OpGaiji = self.OpGaijiConv
		return

class JisInputer(Inputer):         #JIS etc. -> EUC
	def input(self,input_string):
		out = cStringIO.StringIO()
		cnt = 0
		while(cnt < len(input_string)):
			if self.isCtrl(input_string[cnt]): #Ctrl文字
				chars = input_string[cnt:cnt+6]
				mode = self.isJisEscape(chars)
				if(mode):
					self.JisMode = mode
					cnt = cnt + self.Kc_EscLen[self.JisMode]
					continue
 
                #Jisなどのエスケープシーケンスでなければそのまま書く
				#改行はすべてLFにして格納
				if(input_string[cnt:cnt+2] == CL):
					out.write(LF)
					cnt = cnt + 1
				elif((input_string[cnt] == LF)|(input_string[cnt] == CR)):
					out.write(LF)
				else:
					out.write(input_string[cnt])
				cnt = cnt + 1
				continue

			if self.isPict(input_string[cnt]): #表示可能文字
				if(self.JisMode & 0x0F00): #漢字ですね
					out.write(self.OpGaiji(chr(ord(input_string[cnt])|0x80)+
										   chr(ord(input_string[cnt+1])|0x80)))
					cnt = cnt + 1
					
				if(self.JisMode & 0xC000): #補助漢字みたいです
					out.write(0x8F + chr(ord(input_string[cnt])|0x80) +
							  chr(ord(input_string[cnt+1])|0x80))
					cnt = cnt + 1
					
				if(self.JisMode & self.Kc_Jis7Hankana): #7bit半角カナ
					out.write(chr(0x8E) + chr(ord(input_string[cnt])|0x80))

				if(self.JisMode & 0x000F): #半角英数字
					out.write(input_string[cnt])
			
			if self.isHankana(input_string[cnt]):
				if(self.JisMode & self.Kc_Nec_Kanji): 
				    #NEC拡張漢字
				    #EUCに変換不能なのでカット
					cnt = cnt + 2
					continue
				out.write(chr(0x8E)+input_string[cnt])
			cnt = cnt + 1

		return(out.getvalue())

	def __init__(self,gaijiconvert):
		Inputer.__init__(self,gaijiconvert)
		self.JisMode = self.Kc_Ascii
		
		
class EucInputer(Inputer):   #EUC -> EUC 何もしない(^^;
	def input(self,input_string):
		out = cStringIO.StringIO()
		cnt = 0
		while(cnt < len(input_string)):
			#改行はすべてLFにして格納
			if(input_string[cnt:cnt+2] == CL):
				out.write(LF)
				cnt = cnt + 1
			elif((input_string[cnt] == LF)|(input_string[cnt] == CR)):
				out.write(LF)

			elif(input_string[cnt] == self.SS2): #半角かな
				out.write(input_string[cnt:cnt+2])
				cnt = cnt + 1
				
			elif(input_string[cnt] == self.SS3): #補助漢字
				out.write(input_string[cnt:cnt+3])
				cnt = cnt + 2
				
			elif(self.isEuc(input_string[cnt])): #新JIS
				out.write(self.OpGaiji(input_string[cnt] +
									   input_string[cnt+1]))
				cnt = cnt + 1
			
			elif(self.isAscii(input_string[cnt])): #Ascii
				out.write(input_string[cnt])
				
			cnt = cnt + 1
		return(out.getvalue())
	
	def __init__(self,gaijiconvert):
		Inputer.__init__(self,gaijiconvert)

class SjisInputer(Inputer):  #SJIS -> EUC
	def isSjisLead(self,char):
		if(0x81 <= ord(char) <= 0x9F):
			return 1
		if(0xE0 <= ord(char) <= 0xFC):
			return 1
		return 0
	
	def isSjisTrail(self,char):
		if(0x40 <= ord(char) <= 0xFC):
			return 1
		return 0
	
	def input(self,input_string):
		out = cStringIO.StringIO()
		cnt = 0
		while(cnt < len(input_string)):
			if (self.isSjisLead(input_string[cnt])):
				if(self.isSjisTrail(input_string[cnt+1])):
					leader = ord(input_string[cnt])
					trailer = ord(input_string[cnt+1])
					leaderlow = 0
					if(trailer < 0x9F):
						leaderlow = 0
						if(0x80 <= trailer <= 0x9E):
							trailer = trailer - 1
						trailer = trailer - 0x1F
					else:
						leaderlow = 1
						trailer = trailer - 0x7E
					if(0x81 <= leader <= 0x9F):
						leader = leader - 0x81
					else:
						leader = leader - 0xC1
					leader = (leader << 1) + 0x21 + leaderlow
					
					out.write(self.OpGaiji(chr(leader|0x80) +
							               chr(trailer|0x80)))
					cnt = cnt + 1
			elif (self.isHankana(input_string[cnt])):
				out.write(chr(0x8E)+input_string[cnt])
			elif (self.isAscii(input_string[cnt])):
				try: #改行はすべてLFにして格納
					if(input_string[cnt:cnt+2] == CL):
						out.write(LF)
						cnt = cnt + 1
					elif((input_string[cnt] == LF)|(input_string[cnt] == CR)):
						out.write(LF)
					else:
						out.write(input_string[cnt])
				except IndexError:
					out.write(input_string[cnt])
			cnt = cnt + 1
		return(out.getvalue())
	
	def __init__(self,gaijiconvert):
		Inputer.__init__(self,gaijiconvert)

u2etable = open(u2etablefile,'rb').read()

class UnicInputer(Inputer): # Unicode -> EUC
	def CutNull(self,input_char): #変換できない文字は無視（出力しない）
		if(ord(input_char) == 0):
			return("")
		return(input_char)
	
	def ChkBL(self,input_string):
		if((input_string[1-self.endian] == NC) & # CR + LF
		   (input_string[self.endian]   == CR) &
		   (input_string[3-self.endian] == NC) &
		   (input_string[2+self.endian] == LF)):
			return(4)
		if(input_string[1-self.endian] != NC): # 0x00
			return(0)
		if((input_string[self.endian] == CR) | # CR or LF
		   (input_string[self.endian] == LF)):
			return(2)
		return(0)

	def ChkEndian(self,input_string):
		if((ord(input_string[0]) == 0xFE) & (ord(input_string[1]) == 0xFF)):
			self.endian = 1
			return(2) # Little endian
		if((ord(input_string[0]) == 0xFF) & (ord(input_string[1]) == 0xFE)):
			self.endian = 0
			return(2) # big endian
		return(0)
	
	def MakeCode(self,input_string,cnt):
		return((ord(input_string[cnt]) << (8*self.endian)) + (ord(input_string[cnt+1]) << (8*(1-self.endian))),cnt+2)
		
	def input(self,input_string):
		global u2etable
		out = cStringIO.StringIO()
		cnt = 0
		while(cnt < len(input_string)):
			endiansize = 0
			try:
				endiansize = self.ChkEndian(input_string[cnt:cnt+3])
			except:
				pass

			if(endiansize > 0):
				cnt = cnt + endiansize
				continue
			
			bltmp = 0
			try:
				bltmp = self.ChkBL(input_stirng[cnt:cnt+4])
			except:
				pass
			
			if(bltmp > 0):
				out.write(LF)
				cnt = cnt + bltmp
				continue
			(code,cnt) = self.MakeCode(input_string,cnt)
			out.write(self.CutNull(u2etable[code*2]))
			out.write(self.CutNull(u2etable[code*2+1]))

		return(out.getvalue())

	def __init__(self,gaijiconvert,endian = 0):
		Inputer.__init__(self,gaijiconvert)
		global u2etable
		"""
		if(u2etable == 'UNLOADED'):
			u2etable = open(u2etablefile,'rb').read()
		"""
		self.endian = endian # big endian を仮定。どっちがいいのか誰か教えて(^^;
		
class Utf8Inputer(UnicInputer): #UTF-8 -> EUC
	def ChkBL(self,input_string):
		if(input_string[0:2] == CL): # CR + LF
			return(2)
		if((input_string[0] == CR) | # CR or LF
		   (input_string[0] == LF)):
			return(1)
		return(0)

	def ChkEndian(self,input_string):
		if((ord(input_string[0]) == 0xEF) &
		   (ord(input_string[1]) == 0xBB) &
		   (ord(input_string[2]) == 0xBF)):
			self.endian = 1
			return(3) # Little endian
		if((ord(input_string[0]) == 0xEF) &
		   (ord(input_string[1]) == 0xBF) &
		   (ord(input_string[2]) == 0xBE)):
			self.endian = 0
			return(3) # Big endian
		return(0)
	
	def MakeCode(self,input_string,cnt):
		c1 = ord(input_string[cnt])

		if((c1 & 0x80) == 0):
			code = c1
		elif((c1 & 0xE0) == 0xC0):
			cnt = cnt + 1
			c2 = ord(input_string[cnt])
			code = ((c1 & 0x1f) << 6) | (c2 & 0x3f)
		elif((c1 & 0xF0) == 0xE0):
			cnt = cnt + 1
			c2 = ord(input_string[cnt])
			cnt = cnt + 1
			c3 = ord(input_string[cnt])
			code = ((c1 & 0x0f) << 12) |((c2 & 0x3f) << 6) | (c3 & 0x3f)
		else:
			code = 0
		return(code,cnt+1)
