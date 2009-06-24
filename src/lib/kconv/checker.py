# encoding: utf-8
#Kconv0.5 Checker
#漢字コードの判別を行なう

import kconv
import inputer

from kconv import tc2tableefile
from kconv import tc2tablesfile
from common import baseclass

class Checker(baseclass):             #checker interface & some methods
	def ChkCoding(self,input_string):
		return(kconv.EUC)

	def ChkAnycode5(self,input_string,cnt,codings):
		if ((input_string[cnt] == chr(0x00)) |
			(input_string[cnt] == chr(0xFF))): #Unicodeのみに現れるコード
			##TEST##
			return(kconv.UNICODE)
			codings["UNIC"] = codings["UNIC"] + 1

		try: #単独のUTF8 trailerバイトは減点対象
			if(( 0x00 <= ord(input_string[cnt]) <= 0x7F ) &
			   ( 0x80 <= ord(input_string[cnt+1]) <= 0xBF )):
				codings["UTF8"] = codings["UTF8"] - 100
		except IndexError:
			pass

		try: #UTF8の2バイトコード
			if ( 0xC0 <= ord(input_string[cnt]) <= 0xDF ):
				if ( 0x80 <= ord(input_string[cnt+1]) <= 0xBF ):
					code = ((ord(input_string[cnt]) & 0x1f) << 6) | (ord(input_string[cnt+1]) & 0x3f)
					if((inputer.u2etable[2*code] == chr(0))&
					   (inputer.u2etable[2*code+1] == chr(0))):
						codings["UTF8"] = codings["UTF8"] - 1
					else:
						codings["UTF8"] = codings["UTF8"] + 1

					try: #UTF8の2バイトコードの後2バイト以上trailerバイトが続いていたら減点
						if ( 0x80 <= ord(input_string[cnt+2]) <= 0xBF ):
							codings["UTF8"] = codings["UTF8"] - 100
					except IndexError:
						pass

				else:
					codings["UTF8"] = codings["UTF8"] - 100
		except IndexError:
			pass

		try: #UTF8の3バイトコード
			if ( 0xE0 <= ord(input_string[cnt]) <= 0xEF ):
				if (( 0x80 <= ord(input_string[cnt+1]) <= 0xBF) &
					( 0x80 <= ord(input_string[cnt+2]) <= 0xBF)):
					codings["UTF8"] = codings["UTF8"] + 1
				else:
					codings["UTF8"] = codings["UTF8"] - 100
		except IndexError:
			pass

		try:
			chars = input_string[cnt:cnt+6]
		except IndexError:
			chars = input_string[cnt:]
		
		if(self.isJisEscape(chars)): #JISとかだね。
			return(kconv.JIS)
		    #codings["JIS"] = codings["JIS"] + 1

		if( 0x80 <= ord(input_string[cnt]) <= 0xFF ): #JISに出てこない文字列は減点
			codings["JIS"] = codings["JIS"] - 1
		if not self.isAscii(input_string[cnt]):
			if not self.isHankana(input_string[cnt]): #Asciiでなく半角仮名でもなければJISではない。
				codings["JIS"] = codings["JIS"] - 1

		try: # SS2(Hankaku katakana)
			if ord(input_string[cnt]) == 0x8E:
				if self.isHankana(input_string[cnt+1]):
					codings["EUC"] = codings["EUC"] + 1
		except IndexError:
			pass
		
		try: # SS3(Hojyo kanji)
			if ord(input_string[cnt]) == 0x8F:
				if self.isHankana(input_string[cnt+1]):
					if self.isHankana(input_string[cnt+2]):
						codings["EUC"] = codings["EUC"] + 1
		except IndexError:
			pass

		return(kconv.UNKNOWN)
		
class FastChecker(Checker):#Fast check coding 最初の判別可能文字で決定
	def ChkCoding(self,input_string):
		coding = kconv.UNKNOWN
		cnt = 0
		while(cnt < len(input_string)):
			try:
				if(self.isJisEscape(input_string[cnt:])):
					coding = kconv.JIS
					break
				if not self.isAscii(input_string[cnt]):
					if not self.isHankana(input_string[cnt]):
						coding = self.ChkCoding2(input_string[cnt:])
						break
				cnt = cnt + 1
			except IndexError:
				cnt = cnt + 1
		if coding == kconv.UNKNOWN:
			coding = kconv.DEFAULT_INPUT_CODING
		return coding
		
	
	def ChkCoding2(self,input_string):
		coding = kconv.UNKNOWN
		cnt = 0
		try:
			while(cnt < len(input_string)):
				if self.isAscii(input_string[cnt]):
					cnt = cnt + 1
					continue
				if self.isSjis1(input_string[cnt]):
					coding = kconv.SJIS
					break
				if self.isHankana(input_string[cnt]):
					try:
						if(self.isAscii(input_string[cnt+1]) |\
						   (0x80 <= input_string[cnt+1] <= 0xA0)):
							coding = kconv.SJIS
							break
					except IndexError:
						break
				if self.isEuc1(input_string[cnt]):
					coding = kconv.EUC
					break
				cnt = cnt + 1
				if self.isSjis2(input_string[cnt]):
					coding = kconv.SJIS
					break
				if self.isEuc2(input_string[cnt]):
					coding = kconv.EUC
					break
				cnt = cnt + 1
		except IndexError:
			pass
		if coding == kconv.UNKNOWN:
			coding = kconv.DEFAULT_INPUT_CODING
		return(coding)
	
class FullChecker(Checker):#Full check coding 全部を見て最も判別できたコードにする
	def ChkCoding(self,input_string):
		cnt = 0
		codings = {"EUC":0 , "SJIS":0 , "JIS":0 , "UTF8":0 , "UNIC":0}
		#最初の1バイトがUTF8 trailer byte だったら減点
		try:
			if(0x80 <= ord(input_string[0]) <= 0xBF):
				codings["UTF8"] = codings["UTF8"] - 100
		except IndexError:
			return(kconv.DEFAULT_INPUT_CODING)
		try:
			while(cnt < len(input_string)):
				if ((input_string[cnt] == chr(0x00)) |
					(input_string[cnt] == chr(0xFF))): #Unicodeのみに現れるコード
					codings["UNIC"] = codings["UNIC"] + 1

				try: #単独のUTF8 trailerバイトは減点対象
					if(( 0x00 <= ord(input_string[cnt]) <= 0x7F ) &
					   ( 0x80 <= ord(input_string[cnt+1]) <= 0xBF )):
						codings["UTF8"] = codings["UTF8"] - 100
				except IndexError:
					pass

				try: #UTF8の2バイトコード
					if ( 0xC0 <= ord(input_string[cnt]) <= 0xDF ):
						if ( 0x80 <= ord(input_string[cnt+1]) <= 0xBF ):
							codings["UTF8"] = codings["UTF8"] + 1
						else:
							codings["UTF8"] = codings["UTF8"] - 1
				except IndexError:
					pass

				try: #UTF8の3バイトコード
					if ( 0xC0 <= ord(input_string[cnt]) <= 0xDF ):
						if (( 0x80 <= ord(input_string[cnt+1]) <= 0xBF) &
							( 0x80 <= ord(input_string[cnt+2]) <= 0xBF)):
							codings["UTF8"] = codings["UTF8"] + 1
						else:
							codings["UTF8"] = codings["UTF8"] - 1
				except IndexError:
					pass
				
				if self.isAscii(input_string[cnt]):
					if self.isJisEscape(input_string[cnt:]):
						codings["JIS"] = codings["JIS"] + 1
					cnt = cnt + 1
					continue
				else:
					if not self.isHankana(input_string[cnt]): #Asciiでなく半角仮名でもなければJISではない。
						codings["JIS"] = codings["JIS"] - 1

				if( 0x80 <= ord(input_string[cnt]) <= 0xFF ): #JISに出てこない文字列は減点
					codings["JIS"] = codings["JIS"] - 1

				if ord(input_string[cnt]) == 0x8E:
					if self.isHankana(input_string[cnt+1]):
						codings["EUC"] = codings["EUC"] + 1
						cnt = cnt + 1
						continue
				if (0x81 <= ord(input_string[cnt]) <= 0x9F):
					codings["SJIS"] = codings["SJIS"] + 1
					cnt = cnt + 1
					continue
				if self.isHankana(input_string[cnt]):
					cnt = cnt + 1
					if (0x80 <= ord(input_string[cnt]) <= 0x9F):
						codings["SJIS"] = codings["SJIS"] + 1
						cnt = cnt + 1
						continue
					if (0xF0 <= ord(input_string[cnt]) <= 0xFE):
						codings["EUC"] = codings["EUC"] + 1
						cnt = cnt + 1
						continue
				if(0xFD <= input_string[cnt] <= 0xFE):
					codings["EUC"] = codings["EUC"] + 1
					cnt = cnt + 1
					continue
				cnt = cnt + 1
		except IndexError:
			codings = codings

#		print codings
		max = 0
		if(codings["UNIC"] > 0):
			return(kconv.UNIC)
		if(codings["UTF8"] > 0):
			return(kconv.UTF8)
		for key in codings.keys():
			if(codings[key] >= max):
				max = codings[key];
				maxname = key
		if(maxname == "UNIC"):
			maxname = "UNICODE"
		return(eval("kconv."+maxname))


#Table Checker用の定数
#start : SJIS/EUC判別テーブルの最初の値
#end : SJIS/EUC判別テーブルの最後の値
#tables,tablee : SJIS/EUC判別テーブル（頻度表）
	
start = 0x80
end = 0xFE
hoehoe = 0

tables = [0.00223387561787, 0.0730618018026, 0.22234824392, 0.108494260574, 0.00132758734236, 0.00182077965556, 0.00249474981963, 0.00256757171932, 0.00779372318562, 0.0160764597444, 0.0163259579427, 0.0179701386874, 0.0170891562155, 0.0162740307432, 0.0222915496338, 0.0149333648663, 0.0167686160364, 0.0171465005595, 0.0116619513003, 0.0269934762876, 0.0118910965129, 0.0137699943902, 0.0140956421626, 0.0119119138253, 0.00312445417432, 0.000410155226728, 0.000510681951166, 0.000380360931956, 0.00105495019826, 0.00144583586811, 0.00206006266708, 0.00187526065171, 0.00273496148449, 0.00160889191767, 0.0113309637711, 0.000760102761683, 0.00549855644707, 0.000367514560704, 0.00237255451717, 0.00163079265903, 0.00160850497878, 0.00766069359416, 0.00973693030697, 0.00350110049291, 0.00191016253987, 0.00458313641368, 0.00157816896956, 0.00369487949059, 0.000635508438093, 0.00441907432299, 0.0014143390422, 0.00322250448985, 0.00111105633776, 0.00855289729396, 0.00218411527622, 0.00721083843699, 0.00115733422938, 0.00165625323819, 0.00117141880509, 0.00339964511512, 0.00176227449492, 0.00943387976586, 0.00467824599362, 0.00215114808252, 0.00119285521977, 0.00471771376072, 0.00254745089687, 0.000797016732089, 0.00825340659067, 0.00977090354178, 0.0104316403957, 0.00265796064475, 0.00831253085354, 0.0112574453814, 0.00281397440647, 0.00050704472557, 0.020764147047, 0.00993736465361, 0.00195187455255, 0.00157499607064, 0.00213164636231, 0.000614923288977, 0.00131241933775, 0.000752363983821, 0.00179725377085, 0.000255843996144, 0.0018061533654, 0.000706627806652, 0.000989634913094, 0.000887096106412, 0.00166437895495, 0.00101323818558, 0.00472963147862, 0.00185289558369, 0.000892900189809, 0.00276761912707, 0.00559536855813, 0.000789742280898, 0.00262638643107, 0.00341040201635, 0.000774574276287, 0.00294886130462, 0.00421972340524, 0.00430307004283, 0.00612980855734, 0.0107484659614, 0.00704522859073, 0.000801659998807, 0.00190257853757, 0.00265494252139, 0.00151896731891, 0.00242409477774, 0.0107198324833, 0.00407872287258, 0.000325338221352, 0.000959763230544, 0.000259403833961, 0.00123541849802, 0.000771246601806, 0.000287031270931, 0.000574294705198, 0.000166538499607, 0.00466741170461, 0.00130251370209, 0.00215300538921, 0.0, 0.0]
tablee = [0.0, 1.25547465416e-07, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3.76642396249e-07, 0.0, 0.0, 6.27737327082e-08, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.27737327082e-08, 0.0, 0.0, 0.0, 0.0, 0.0, 0.066129553685, 0.0160557003885, 0.0258200917375, 0.178688694388, 0.0882604331513, 0.00951725116335, 0.00147198125827, 0.00311728079256, 0.00219952882036, 0.0041537378933, 0.00855053567965, 0.00898430217266, 0.00451236422826, 0.00237228213278, 0.00860565101697, 0.00926960878782, 0.00739945374298, 0.00967537819605, 0.0112247594667, 0.00846202471653, 0.00991950524255, 0.00708464347345, 0.0155543265854, 0.0119600909717, 0.0180467576425, 0.00741163184712, 0.0111668193115, 0.020979232566, 0.0113930558441, 0.00799084507882, 0.0166875807819, 0.0129220356517, 0.00863898386903, 0.00894977661967, 0.0131318882402, 0.00912598248738, 0.0085189604921, 0.017455052438, 0.014174183298, 0.0172288786791, 0.00941091246015, 0.0177846773085, 0.0172332728404, 0.00913269927678, 0.0111223755087, 0.0217208414442, 0.0112842689654, 0.00642677475466, 0.00391293785463, 0.0028918603184, 0.00338582682108, 0.00361432320814, 0.0031998910248, 0.00521153806317, 0.00630606086667, 0.00309738151929, 0.00204899740933, 0.00229569817887, 0.0019481827946, 0.00420998315781, 0.00192953899598, 0.00540205634194, 0.00260699311937, 0.00254302668574, 0.00432542405226, 0.00565961696724, 0.00171064699003, 0.00316737423126, 0.0042339627237, 0.00265018144747, 0.00438907661722, 0.00504493657656, 0.00623795136668, 0.00805882903134, 0.0129636546365, 0.00760240122082, 0.00214190253374, 0.0031797406566, 0.00304509099994, 0.00155923674674, 0.00368519475237, 0.00887965836024, 0.0101748687872, 0.0017840922573, 0.00104392717494, 0.00174404261583, 0.00171924699141, 0.00143663964676, 0.000556489140458, 0.000858995758379, 0.000430376711447, 0.00459058029922, 0.00219551130147, 0.00339875821002]

class TableChecker(Checker):# Table check coding Sjis/Eucの特徴を使って判定する。
	def ChkCoding(self,input_string):
		cnt = 0
		codings = {"EUC":0 , "SJIS":0 , "JIS":0  , "UTF8":0 , "UNIC":0}
		#最初の1バイトがUTF8 traler byte だったら減点
		try:
			if(0x80 <= ord(input_string[0]) <= 0xBF):
				codings["UTF8"] = codings["UTF8"] - 100
		except IndexError:
			return(kconv.DEFAULT_INPUT_CODING)
		try:
			while(cnt < len(input_string)):
				try:
					retcode = self.ChkAnycode5(input_string,cnt,codings)
				except IndexError:
					pass
				if(retcode != kconv.UNKNOWN):
						return(retcode)
				if(start <= ord(input_string[cnt]) <= end):
					codings["SJIS"] = codings["SJIS"] + tables[ord(input_string[cnt]) - start]
					codings["EUC"] = codings["EUC"] + tablee[ord(input_string[cnt]) - start]
				cnt = cnt + 1
				continue
		except IndexError:
			pass
		
#		print codings
		
		if(codings["UNIC"] > 0):
			return(kconv.UNICODE)
		if(codings["UTF8"] >0):
			return(kconv.UTF8)
		if(codings["JIS"] > 0):
			return(kconv.JIS)
		if(codings["EUC"] > codings["SJIS"]):
			return(kconv.EUC)
		if(codings["SJIS"] > codings["EUC"]):
			return(kconv.SJIS)
		return(kconv.DEFAULT_INPUT_CODING)

	def __init__(self):
		A = 200  #判別文字増幅率(確実にSjis/Euc判定できる文字は倍率をかけておく)
		A2 = 2  #デフォルトのコードに対する倍率
		global hoehoe
		if(hoehoe == 0): #まだ倍率をかけていない
			for i in range(start,end+1):
				if(tablee[i - start] == 0):
					tables[i - start] = tables[i - start] * A
				if(tables[1 - start] == 0):
					tablee[i - start] = tablee[i - start] * A
				if(kconv.DEFAULT_INPUT_CODING == 'Euc'):
					tablee[i - start] = tablee[i - start] * A2
				if(kconv.DEFAULT_INPUT_CODING == 'Sjis'):
					tables[i - start] = tables[i - start] * A2
			hoehoe = 1

#Euc code Data.
elstart = 0xA1
elend = 0xFE
etstart = 0xA1
etend = 0xFE

#Sjis code Data.
slstart = 0x80
slend = 0xFC
ststart = 0x40
stend = 0xFC

#Table Size
lstart = min(slstart,elstart)
lend = max(slend,elend)
tstart = min(ststart,etstart)
tend = max(stend,etend)

llength = lend - lstart + 1
tlength = tend - tstart + 1

tables2 = 'UNLOADED'
tablee2 = 'UNLOADED'


class Table2Checker(Checker):# Table check coding Sjis/Eucの特徴を使って判定する。
	def ChkCoding(self,input_string):
		cnt = 0
		codings = {"EUC":0 , "SJIS":0 , "JIS":0 , "UNIC":0 , "UTF8":0}

		#最初の1バイトがUTF8 traler byte だったら減点
		try:
			if(0x80 <= ord(input_string[0]) <= 0xBF):
				codings["UTF8"] = codings["UTF8"] - 100
		except IndexError:
			return(kconv.DEFAULT_INPUT_CODING)

		while(cnt < len(input_string)):
			try:
				retcode = self.ChkAnycode5(input_string,cnt,codings)
			except IndexError:
				pass
			try:
				c1 = ord(input_string[cnt])
				c2 = ord(input_string[cnt+1])
				if(lstart <= c1 <= lend):
					if(tstart <= c2 <= tend):
						codings["SJIS"] = codings["SJIS"] + tables2[c1 - lstart][c2 - tstart]/65536.0
						codings["EUC"] = codings["EUC"] + tablee2[c1 - lstart][c2 - tstart]/65536.0
			except IndexError:
				pass
	
			cnt = cnt + 1
			continue
		
#		print codings

		if(codings["UNIC"] > 0):
			return(kconv.UNICODE)
		if(codings["UTF8"] >0):
			return(kconv.UTF8)
		if(codings["JIS"] > 0):
			return(kconv.JIS)
		if(codings["EUC"] > codings["SJIS"]):
			return(kconv.EUC)
		if(codings["SJIS"] > codings["EUC"]):
			return(kconv.SJIS)
		return(kconv.DEFAULT_INPUT_CODING)

	def __init__(self):
		global tables2,tablee2
		if(tables2 == 'UNLOADED'):
			tables2 = []
			tablee2 = []
			tfe = open(tc2tableefile,'rb')
			tfs = open(tc2tablesfile,'rb')
			for i in range(llength):
				ttablee = []
				ttables = []
				for ii in range(tlength):
					ta = tfe.read(3)
					ta = (ord(ta[0]),ord(ta[1]),ord(ta[2]))
					ttablee.append(ta[0] + (ta[1] << 8) + (ta[2] << 16))
					ta = tfs.read(3)
					ta = (ord(ta[0]),ord(ta[1]),ord(ta[2]))
					ttables.append(ta[0] + (ta[1] << 8) + (ta[2] << 16))
				tablee2.append(ttablee)
				tables2.append(ttables)
			
