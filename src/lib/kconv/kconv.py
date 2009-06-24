#Kconv UserInterface
# encoding: utf-8

from defaults import *
from kconvtools import *
kconvauto = AUTO

import imp
import os.path

prefix = imp.find_module("kconv")[1]
u2etablefile = os.path.join(prefix,"kconvu2etable.dat")
e2utablefile = os.path.join(prefix,"kconve2utable.dat")
tc2tableefile = os.path.join(prefix,"kconveuctable2.dat")
tc2tablesfile = os.path.join(prefix,"kconvsjistable2.dat")

__version__ = "Kconv-1.1.8p-2"

import cStringIO
import inputer
import outputer
import checker
import re
import crl

class Kconv:
	inputer = 0      #Inputer
	outputer = 0     #Outputer
	checker = 0      #Coding Checker
	linemode = 0     #Convert mode flag
	
	def convert(self,input_string):                  #Convert string
#		try:
			out = cStringIO.StringIO()
			if self.linemode == LINE:                         #Line by line mode = Auto mode
				pos = 0
				artemis = crl.crl()
				UnicodeMode = -1 # -1 -> not Unicode , 0 -> Big Endian , 1 -> Little Endian

				while(pos != -1):
					(line,pos) = artemis.ReadLine(input_string,pos)
					try:
						if(line[0:2] == crl.BIG):
							UnicodeMode = 0
						if(line[0:2] == crl.LIT):
							UnicodeMode = 1
					except IndexError:
						pass
					
					if(UnicodeMode >= 0): #Unicode らしい。
						self.inputer = inputer.UnicInputer(self.gaijiconvert,UnicodeMode)
						out.write(self.outputer.output(self.inputer.input(line)))
						if(pos != -1):
							out.write(self.outputer.output(crl.LF))
						continue
					
					else:
						self.inputer = eval("inputer."+
											self.checker.ChkCoding(line)+
											"Inputer(self.gaijiconvert)")
						out.write(self.outputer.output(self.inputer.input(line)))
						if(pos != -1):
							out.write(self.outputer.output(crl.LF))
						continue
				   
			else:                                        #Whole mode
				if type(self.inputer) == type(AUTO):
					self.inputer = eval("inputer."+
										self.checker.ChkCoding(input_string)+
										"Inputer(self.gaijiconvert)")
					out.write(self.outputer.output(
						self.inputer.input(input_string)))
					self.inputer = AUTO
				else:
					out.write(self.outputer.output(
						self.inputer.input(input_string)))

			return(out.getvalue())
#		except:
#			raise(KconvError)

	def __init__(self,outcode = DEFAULT_OUTPUT_CODING,   #出力コード
				 incode = AUTO,                          #入力コード
				 hankanaconvert = ZENKAKU,               #半角->全角コンバートフラグ
				 checkmode = DEFAULT_CHECK_MODE,         #入力コード判別ルーチン判別
				 mode = WHOLE,                           #変換モード
				 blcode = DEFAULT_BREAKLINE_CODE,        #改行コード
				 gaijiconvert = CONVERT,                 #外字の扱いについて
				 ):
		
		self.outputer = eval("outputer."+outcode+hankanaconvert+"Outputer(blcode)")
		self.gaijiconvert = gaijiconvert
		if incode == AUTO:
			self.inputer = AUTO
		else:
			self.inputer  = eval("inputer."+incode+"Inputer(self.gaijiconvert)")

		self.checker = eval("checker."+checkmode+"Checker()")
		self.linemode = mode

def convert(str,outcode = DEFAULT_OUTPUT_CODING,
			incode = AUTO,
			hankanaconvert = ZENKAKU,
			checkmode = TABLE,
			mode = WHOLE,
			blcode = DEFAULT_BREAKLINE_CODE,
			gaijiconvert = CONVERT,
			):
	#print str
	kc = Kconv(outcode=outcode,
			   incode=incode,
			   hankanaconvert=hankanaconvert,
			   checkmode=checkmode,
			   blcode=blcode,
			   gaijiconvert=gaijiconvert,
			   )
	return(kc.convert(str))

def ChkCoding(str,checkmode = DEFAULT_CHECK_MODE):
	return(eval("checker."+checkmode+"Checker()").ChkCoding(str))

class KconvError:
	message = "Kconv Error."

class KconvIncorrectInput(KconvError):
	message = "InputString has incorrect character."
