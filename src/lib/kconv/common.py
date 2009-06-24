# encoding: utf-8
class baseclass:
	ESC = chr(0x1B)
	SS2 = chr(0x8E)
	SS3 = chr(0x8F)
	
	def isAscii(self,char):
		if(0x00 <= ord(char) <= 0x7F):
			return 1
		return 0
	
	def isPict(self,char):
		if(0x20 <= ord(char) <= 0x7E):
			return 1
		return 0
	
	def isCtrl(self,char):
		if(0x00 <= ord(char) <= 0x1F):
			return 1
		if(char == chr(0x7F)):
			return 1
		return 0
		
	def isHankana(self,char):
		if(0xA1 <= ord(char) <= 0xDF):
			return 1
		return 0

	def isSjis1(self,char):
		if(0x81 <= ord(char) <= 0x9F):
			return 1
		return 0
	
	def isSjis2(self,char):
		if(0x0 <= ord(char) <= 0x7E):
			return 1
		if(0x80 <= ord(char) <= 0xA0):
			return 1
		return 0
	
	def isEuc(self,char):
		if(0xA1 <= ord(char) <= 0xFE):
			return(1)
		return(0)
	
	def isEuc1(self,char):
		if(0xF0 <= ord(char) <= 0xFE):
			return 1
		return 0
	
	def isEuc2(self,char):
		if(0xFD <= ord(char) <= 0xFE):
			return 1
		return 0
	
	#Jisなどのエスケープじゃない
	Kc_NotJisEscape = Kc_None = 0

	#半角アルファベット
	Kc_Ascii = 0x1
	Kc_JisRoma = 0x2

	#7bit半角仮名
	Kc_Jis7Hankana = 0x10
	
	#全角漢字
	Kc_Jis_C_6226_1978 = Kc_J7   = 0x0100 #旧JIS
	Kc_Jis_X_0208_1983 = Kc_J8   = 0x0200 #新JIS
	Kc_Jis_X_0208_1990 = Kc_J908 = 0x0400 #なんなのでしょう？通称あるのかな？
	Kc_Jis_X_0212_1990 = Kc_J912 = 0x4000 #補助漢字
	Kc_Nec_Kanji                 = 0x0800 #NEC漢字

	#エスケープシーケンス辞書
	Kc_Escs = { Kc_Ascii : ESC+'(B' ,
				Kc_JisRoma : ESC+'(J' ,
				Kc_J7 : ESC+'$@' ,
				Kc_J8 : ESC+'$B' ,
				Kc_J908 : ESC+'$@'+ESC+'$B' ,
				Kc_J912 : ESC+'$(D' ,
				Kc_Nec_Kanji : ESC+'K' ,}
	
	#エスケープシーケンスの長さ辞書
	Kc_EscLen = {}
	for keyname in Kc_Escs.keys():
		Kc_EscLen[keyname] = len(Kc_Escs[keyname])
		
	#エスケープかどうか調べる
	def isJisEscape(self,chars):
		ESC = self.ESC
		if(chars[0] != ESC):
			return(self.Kc_None)
		
		chs = ""
		for i in range(1,6):
			try:
				chs = chs + chars[i]
			except IndexError:
				chs = chs + " "
		
		#Jis等かもしれない
		if(chs[0] == "("):
			if(chs[1] == "J"):
				return(self.Kc_JisRoma)
			if(chs[1] == "H"):
				return(self.Kc_JisRoma)
			if(chs[1] == "B"):
				return(self.Kc_Ascii)
			if(chs[1] == "I"):
				return(self.Kc_Jis7Hankana)
		if(chs[0] == "$"):
			if(chs[1] == "@"):
				return(self.Kc_J7) 
			if(chs[1] == "B"):
				return(self.Kc_J8) 
			if(chs[1:3] == "(D"):
				return(self.Kc_J912)
		if(chs[0:5] == "&@\x0A$B"):
			return(self.Kc_J908)
		if(chs[0] == "K"):
			return(self.Kc_Nec_Kanji)
		if(chs[0] == "H"):
			return(self.Kc_Jis_Roma)
		
		#ちがったみたい
		return(self.Kc_None)
	
	def OpGaijiCut(self,eucchar):
		c1 = eucchar[0]
		c2 = eucchar[1]
		
		if((0xA9 <= ord(c1) <= 0xAF) or
		   (0xF5 <= ord(c1) <= 0xFE)):
			return('')
		return(eucchar)
	
	def OpGaijiConv(self,eucchar):
		c1 = eucchar[0]
		c2 = eucchar[1]
		
		GaijiMapAD = { 0xA1 : '(1)' , 0xA2 : '(2)' , 0xA3 : '(3)' , 0xA4 : '(4)' ,
					   0xA5 : '(5)' , 0xA6 : '(6)' , 0xA7 : '(7)' , 0xA8 : '(8)' ,
					   0xA9 : '(9)' , 0xAA : '(10)' , 0xAB : '(11) ' , 0xAC : '(12)' ,
					   0xAD : '(13)' , 0xAE : '(14)' , 0xAF : '(15)' , 0xB0 : '(16)' ,
					   0xB1 : '(17)' , 0xB2 : '(18)' , 0xB3 : '(19)' , 0xB4 : '(20)' ,
					   0xB5 : 'I' , 0xB6 : 'II' , 0xB7 : 'III' , 0xB8 : 'IV' ,
					   0xB9 : 'V' , 0xBA : 'VI' , 0xBB : 'VII' , 0xBC : 'VIII' ,
					   0xBD : 'IX' , 0xBE : 'X' ,
					   0xD0 : 'mm' , 0xD1 : 'cm' , 0xD2 : 'km' , 0xD3 : 'mg' ,
					   0xD4 : 'kg' , 0xD5 : 'cc' , 
					   0xE2 : 'No.' , 0xE3 : 'K.K.' , 0xE4 : 'Tel' ,
					   0xBF : "\xA1\xA6" ,
					   0xC0 : "\xA5\xDF\xA5\xEA" ,
					   0xC1 : "\xA5\xAD\xA5\xED" ,
					   0xC2 : "\xA5\xBB\xA5\xF3\xA5\xC1" ,
					   0xC3 : "\xA5\xE1\xA1\xBC\xA5\xC8\xA5\xEB" ,
					   0xC4 : "\xA5\xB0\xA5\xE9\xA5\xE0" ,
					   0xC5 : "\xA5\xC8\xA5\xF3" ,
					   0xC6 : "\xA5\xA2\xA1\xBC\xA5\xEB" ,
					   0xC7 : "\xA5\xD8\xA5\xAF\xA5\xBF\xA1\xBC\xA5\xEB" ,
					   0xC8 : "\xA5\xEA\xA5\xC3\xA5\xC8\xA5\xEB" ,
					   0xC9 : "\xA5\xEF\xA5\xC3\xA5\xC8" ,
					   0xCA : "\xA5\xAB\xA5\xED\xA5\xEA\xA1\xBC" ,
					   0xCB : "\xA5\xC9\xA5\xEB" ,
					   0xCC : "\xA5\xBB\xA5\xF3\xA5\xC8" ,
					   0xCD : "\xA5\xD1\xA1\xBC\xA5\xBB\xA5\xF3\xA5\xC8" ,
					   0xCE : "\xA5\xDF\xA5\xEA\xA5\xD0\xA1\xBC\xA5\xEB" ,
					   0xCF : "\xA5\xDA\xA1\xBC\xA5\xB8" ,
					   0xDF : "\xCA\xBF\xC0\xAE" ,
					   0xE0 : "\xA1\xC9" ,
					   0xE1 : "\xA1\xC9" ,
					   0xE5 : "(\xBE\xE5)" ,
					   0xE6 : "(\xC3\xE6)" ,
					   0xE7 : "(\xB2\xBC)" ,
					   0xE8 : "(\xBA\xB8)" ,
					   0xE9 : "(\xB1\xA6)" ,
					   0xEA : "(\xB3\xF4)" ,
					   0xEB : "(\xCD\xAD)" ,
					   0xEC : "(\xC2\xE5)" ,
					   0xED : "\xCC\xC0\xBC\xA3" ,
					   0xEE : "\xC2\xE7\xC0\xB5" ,
					   0xEF : "\xBE\xBC\xCF\xC2" ,}
		if(ord(c1) == 0xAD):
			try:
#				print "Mapping to %s" % GaijiMapAD[ord(c2)]
				return(GaijiMapAD[ord(c2)])
			except KeyError:
#				print "Cut(%02X %02X)" % (ord(c1) , ord(c2))
				return('')

		if((0xA9 <= ord(c1) <= 0xAF) or
		   (0xF5 <= ord(c1) <= 0xFE)):
#			print "Cut(%02X %02X)" % (ord(c1) , ord(c2))
			return('')
		return(eucchar)
