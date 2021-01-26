#get_txt_from_sdf.py written by He
#2021.01.17
'''
note:this is a python script to get target txt file from a SDF file like 
S01Compounds_List_for_Cp_liq_298_calculations.sdf
S02Compounds_List_for_Cp_sol_298_calculations.sdf

Command line arguments include
 - filename of a SDF file
 - filename of output file
'''

import sys
import pandas as pd

def getString(inFile):
	ans = str()
	ll = "somestring"
	i = 0
	flag = 0
	while ll != "" and ll.find("$$$$") == -1:
		ll = inFile.readline()
		#print("ll:",ll)
		if i == 0 or flag ==1 :
			ans +=ll
			flag = 0
		#elif ll.find(">  <Cp(liq,298)>   J/mol/K") >=0:
		elif ll.find(">  <Cp(sol,298)>   J/mol/K") >=0:
			flag = 1
		else :
			flag = 0
		i +=1
	return ans

def extract(inf):
	targetlist = []
	#df = pd.DataFrame(columns=['CID', 'a']) 
	# note that there would be a bug about decoding if we do not use 'encoding='cp1252''in the open
	with open(inf,encoding='cp1252') as f:
		eachmol = getString(f)
		while eachmol:
			#print("eachmol:",eachmol)
			target = eachmol.split("\n")
			CID = target[0]
			a = target[1]
			#print("target:",target)
			a = float(a)
			#print("CID:",CID)
			#print(type(a))
			#print("a:",a)
			targetlist.append((CID,a))
			eachmol = getString(f)
			#sys.exit(1)
	return targetlist




def main(argv):
	inf = argv[1]
	outname = argv[2]
	targetlist = extract(inf)
	#print("targetlist:",targetlist)
	df = pd.DataFrame(targetlist)
	dfCID = df.iloc[:,0]
	dfCID.columns = ['CID']
	dfA = df.iloc[:,1]
	dfA.columns = ['a']
	print("dfCID:",dfCID)
	#print("dfA:",dfA)
	dfCID2 = dfCID.str.replace(',','_')
	dfCID2.columns = ['CID']
	print("dfCID2:",dfCID2)
	df2 = pd.concat([dfCID2,dfA],axis = 1)
	df2.columns = ['CID','a']
	print("df2:",df2)
	df2.to_csv(str(outname+'.txt'),sep=',',index=None)



'''
	with open(inf) as f:
		oldString = getString(f)
		#print(oldString)
		sdfString = str(str(i) + oldString[3:])
		#for j in range(len(sdfString)):
		#	print("sdfString[{}]:".format(j),sdfString[j])
		ans += sdfString
'''


'''
	file = pd.read_csv(inf)
	df = pd.DataFrame(file)
	print("df :")
	print(df)
	newdf = df.iloc[:,[1,4]] # Which rows of data do you need?
	print(newdf)
	newdf.columns = ['CID','a']
	print("newdf :")
	print(newdf)
	outname = str(inf)
	outname = outname[:-3]
	newdf.to_csv(str(outname+'txt'),sep=',',index=None)
'''


main(sys.argv)