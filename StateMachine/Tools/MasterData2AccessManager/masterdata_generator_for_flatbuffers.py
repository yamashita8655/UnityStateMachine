# coding: utf-8
#設計
#

import os

# _の次の文字を大文字にして、_を削除する
def FileNameCustom(intext, offset):
	pos = intext.find("_", offset) 
	if pos == -1:
		ret = intext.replace("_", "")
		return ret
	else:
		li = list(intext)
		upper = intext[pos+1].upper()
		li[pos+1] = upper
		intext = "".join(li)
		return FileNameCustom(intext, pos+1)

# 頭文字を大文字に
def FirstStringUpper(intext):
	li = list(intext)
	upper = li[0].upper()
	li[0] = upper

	output = "".join(li)
	#intext = "".join(li)
	return output

def GetStringParseString(className, parameter):
	output = "			%s.replace" % (className)
	first = FirstStringUpper(FileNameCustom(parameter, 0))
	second = FileNameCustom(parameter, 0)
	return output.replace("replace", ("Add%s(fbb, %s)" % (first, second)))

def GetIntParseString(className, parameter):
	output = "			%s.replace" % (className)
	first = FirstStringUpper(FileNameCustom(parameter, 0))
	return output.replace("replace", ("Add%s(fbb, int.Parse(lineList[(int)DataKey.%s]))" % (first, first)))

def GetFloatParseString(className, parameter):
	output = "			%s.replace" % (className)
	first = FirstStringUpper(FileNameCustom(parameter, 0))
	return output.replace("replace", ("Add%s(fbb, float.Parse(lineList[(int)DataKey.%s]))" % (first, first)))

def GetBoolParseString(className, parameter):
	output = "			%s.replace" % (className)
	first = FirstStringUpper(FileNameCustom(parameter, 0))
	return output.replace("replace", ("Add%s(fbb, bool.Parse(lineList[(int)DataKey.%s]))" % (first, first)))

def GetEnumParseString(parameter, typeString, enumParameter):
	output = "			%s.replace" % (className)
	enumName, enumParameterList = GetEnumNameAndParameter(typeString)
	enumName = FirstStringUpper(FileNameCustom(enumName, 0))
	enumString = "%s.%s" % (enumName, FirstStringUpper(FileNameCustom(parameter, 0)))
	"Add%s(fbb, %s.%s)" % (eunmname, enumname, enumparam)
	return output.replace("replace", "Add%s(fbb, %s.%s)" % (enumString, enumString, enumParameter))

def GetEnumNameAndParameter(parameter):
	enumTag, enumName, enumParameter = parameter.split(":")

	className, enumName = enumName.split(".")
	className = FileNameCustom(className, 0)
	enumName = FileNameCustom(enumName, 0)
	enumParameterList = []
	for val in enumParameter.split("/"):
		enumParameterList.append(FileNameCustom(val, 0))
	
	return enumName, enumParameterList, className


# まずは、ディレクトリ走査
srcPath = '../../Assets/Resources/MasterData/'
#srcPath = './src_csv/'
fileList = os.listdir(srcPath);
for file in fileList:
        if (".meta" in file) == True:
            continue

	f = open(srcPath + file)

	# マスターファイル作成
	lines = f.readlines() # 1行毎にファイル終端まで全て読む(改行文字も含まれる)
	# 0~3は、Googleスプレッドシート上でマスターデータの説明文などが入る予定
	className = lines[4].replace('\n', '').replace(',', '')
	print(className)
	# emptyという文字列と、余計な,を削除する
	parameterList = lines[5].replace(',empty', '').replace('empty,', '').replace(',,', '').replace(',\n', '').replace('\n', '').split(',')
	typeList = lines[6].replace(',empty', '').replace('empty,', '').replace(',,', '').replace(',\n', '').replace('\n', '').split(',')
	
	count = len(parameterList)
	fbs_string = ""
	fbs_string += "// this file is auto create\n"
	fbs_string += "namespace MasterData;\n"
	# enumの定義があれば、それを記述する
	enumCheckList = []
	for index in range(0, count):
		typeString = typeList[index]
		enumOutput = ""
		if ("enum:" in typeList[index]) == True:
			parameterName = FileNameCustom(parameterList[index], 0)
			enumString, enumParameterList, enumClassName = GetEnumNameAndParameter(typeList[index])
			if (enumString in enumCheckList) == False:
				enumCheckList.append(enumString)
				enumOutput = "enum %s:int { " % (FirstStringUpper(enumString))
				enumParameterString = ""
				for val in enumParameterList:
					enumParameterString += FirstStringUpper(val) + ", "
				enumOutput += enumParameterString
				enumOutput += "}\n"
				enumOutput = enumOutput.replace(", }", " }")

			fbs_string += enumOutput
	
	fbs_string += "table %s {\n" % (FirstStringUpper(className))
	for index in range(0, count):
		typeString = typeList[index]
		if ("enum:" in typeList[index]) == True:
			enumString, enumParameterList, enumClassName = GetEnumNameAndParameter(typeList[index])
			fbs_string += "	%s:%s;\n" % (parameterList[index], FirstStringUpper(enumString))
		elif ("list:" in typeList[index]) == True:
			listTag, listType = typeList[index].split(":")
			fbs_string += "	%s:[%s];\n" % (parameterList[index], listType)
		else:
			fbs_string += "	%s:%s;\n" % (parameterList[index], typeString)
	fbs_string += "}\n"

	fbs_string += "root_type %s;" % (FirstStringUpper(className))

	# マスターファイル保存
	savePath = 'fbs_files/'
#	savePath = 'output_cs/'
	of = open(savePath + className + 'Master' + ".fbs", 'wb') # 書き込みモードで開く
	of.write(fbs_string) # 引数の文字列をファイルに書き込む
	of.close() # ファイルを閉じる


	# マネージャファイル作成
	manager_cs = ""
	manager_cs += "// このファイルは自動生成されます\n"
	manager_cs += "using UnityEngine;\n"
	manager_cs += "using FlatBuffers;\n"
	manager_cs += "using MasterData;\n"
	manager_cs += "using System.Collections;\n"
	manager_cs += "using System.Collections.Generic;\n"
	manager_cs += "\n"
	manager_cs += "public class %sManager\n" % (className)
	manager_cs += "{\n"
	manager_cs += "	public enum DataKey {\n"
	for index in range(0, count):
		if index == 0:
			manager_cs += "		%s = 0,\n" % (FirstStringUpper(FileNameCustom(parameterList[index], 0)))
		elif index < (count-1):
			manager_cs += "		%s,\n" % (FirstStringUpper(FileNameCustom(parameterList[index], 0)))
		else:
			manager_cs += "		%s\n" % (FirstStringUpper(FileNameCustom(parameterList[index], 0)))

	manager_cs += "	}\n"
	manager_cs += "\n"
	manager_cs += "	private static %sManager mInstance;\n" % (className)
	manager_cs += "	\n"
	manager_cs += "	private %sManager () { // Private Constructor\n" % (className)
	manager_cs += '		Debug.Log("Create SampleSingleton instance.");\n'
	manager_cs += "	}\n"
	manager_cs += "	\n"
	manager_cs += "	public static %sManager Instance {\n" % (className)
	manager_cs += "		get {\n"
	manager_cs += "			if( mInstance == null ) mInstance = new %sManager();\n" % (className)
	manager_cs += "			\n"
	manager_cs += "			return mInstance;\n"
	manager_cs += "		}\n"
	manager_cs += "	}\n"
	manager_cs += "\n"
	manager_cs += "	Dictionary<int, ByteBuffer> %sList = new Dictionary<int, ByteBuffer>();\n" % (className)
	manager_cs += "\n"
	manager_cs += "	public void Initialize(string src, bool useLocal = false) {\n"
	manager_cs += "		char[] splitReturn = {'\\n'};\n"
	manager_cs += "		List<string> dataList = CsvParser.Instance.SplitString(src, splitReturn);\n"

	manager_cs += "		// 型指定の部分を分割して、カラム数を計算する\n"
	manager_cs += "		char[] split = {','};\n"
	manager_cs += "		int column = 0;\n"
	manager_cs += "		int i = 0;\n"
	manager_cs += "		if (useLocal == true) {\n"
	manager_cs += "			column = CsvParser.Instance.SplitString(dataList[6], split).Count;\n"
	manager_cs += "			i = 8;\n"
	manager_cs += "		} else {\n"
	manager_cs += "			column = CsvParser.Instance.SplitString(dataList[0], split).Count;\n"
	manager_cs += "			i = 0;\n"
	manager_cs += "		}\n"

	manager_cs += "		// 最初の数行はメタデータなので飛ばす\n"
	manager_cs += "		for (; i < dataList.Count; i++) {\n"
	manager_cs += "			string line = dataList[i];\n"
	manager_cs += '			if (line.StartsWith("#")) {\n'
	manager_cs += "				continue;\n"
	manager_cs += "			}\n"
	manager_cs += "\n"
	manager_cs += "			if (string.IsNullOrEmpty(line)) {\n"
	manager_cs += "				continue;\n"
	manager_cs += "			}\n"
	manager_cs += "\n"
	manager_cs += ""
	manager_cs += "			List<string> lineList = new List<string>();\n"
	manager_cs += "			string param = line;\n"
	manager_cs += "			for (int j = 0; j < column; j++) {\n"
	manager_cs += '				if (param.StartsWith("{")) {\n'
	manager_cs += "					// ひとくくりの文字列\n"
	manager_cs += '					int startIndex = param.IndexOf("{");\n'
	manager_cs += '					int endIndex = param.IndexOf("}");\n'
	manager_cs += "					string substring = param.Substring(startIndex+1, endIndex-1);\n"
	manager_cs += "					lineList.Add(substring);\n"
	manager_cs += "					param = param.Remove(0, endIndex+1);\n"
	manager_cs += '					if (param.StartsWith(",")) {\n'
	manager_cs += "						param = param.Remove(0, 1);\n"
	manager_cs += "					}\n"
	manager_cs += '				} else if (line.StartsWith("[")) {\n'
	manager_cs += "				} else {\n"
	manager_cs += "					// 通常の分割\n"
	manager_cs += '					int endIndex = param.IndexOf(",")\n;'
	manager_cs += '					string substring = "";\n'
	manager_cs += "					if (endIndex == -1) {\n"
	manager_cs += "						substring = param;\n"
	manager_cs += "					} else {\n"
	manager_cs += "						substring = param.Substring(0, endIndex);\n"
	manager_cs += "						param = param.Remove(0, endIndex+1);\n"
	manager_cs += "					}\n"
	manager_cs += "					lineList.Add(substring);\n"
	manager_cs += "				}\n"
	manager_cs += "			}\n"

#===
	manager_cs += "			var fbb = new FlatBufferBuilder(1);\n"
	# 先に文字列があったら、生成しておく
	manager_cs += "			char[] splitSlash = {'/'};\n"
	for index in range(0, count):
		typeString = typeList[index]
		if ("list:" in typeList[index]) == True:
			manager_cs += "			List<string> %sList = CsvParser.Instance.SplitString(lineList[(int)DataKey.%s], splitSlash);\n" % (FileNameCustom(parameterList[index], 0), FirstStringUpper(FileNameCustom(parameterList[index], 0)))
			listTag, listType = typeList[index].split(':')
			if listType == "int":
				manager_cs += "			List<int> %sForArray = new List<int>();\n" % (FileNameCustom(parameterList[index], 0))
				manager_cs += "			for (int k = 0; k < %sList.Count; k++) {\n" % (FileNameCustom(parameterList[index], 0))
				manager_cs += "				%sForArray.Add(int.Parse(%sList[k]));\n" % (FileNameCustom(parameterList[index], 0), FileNameCustom(parameterList[index], 0))
				manager_cs += "			}\n"
				manager_cs += "			VectorOffset %s = %s.Create%sVector(fbb, %sForArray.ToArray());\n" % (FileNameCustom(parameterList[index], 0), className, (FirstStringUpper(FileNameCustom(parameterList[index], 0))), FileNameCustom(parameterList[index], 0))
			elif listType == "string":
				manager_cs += "			List<StringOffset> %sForArray = new List<StringOffset>();\n" % (FileNameCustom(parameterList[index], 0))
				manager_cs += "			for (int k = 0; k < %sList.Count; k++) {\n" % (FileNameCustom(parameterList[index], 0))
				manager_cs += "				%sForArray.Add(fbb.CreateString(%sList[k]));\n" % (FileNameCustom(parameterList[index], 0), FileNameCustom(parameterList[index], 0))
				manager_cs += "			}\n"
				manager_cs += "			VectorOffset %s = %s.Create%sVector(fbb, %sForArray.ToArray());\n" % (FileNameCustom(parameterList[index], 0), className, (FirstStringUpper(FileNameCustom(parameterList[index], 0))), FileNameCustom(parameterList[index], 0))
		elif ("string" in typeList[index]) == True:
			manager_cs += "			StringOffset %s = fbb.CreateString(lineList[(int)DataKey.%s]);\n" % (parameterList[index], (FirstStringUpper(parameterList[index])))
	
	manager_cs += "			%s.Start%s(fbb);\n" % (className, className)

	counter = 0
	for index in range(0, count):
		typeString = typeList[index]
		enumOutput = ""
		if ("enum:" in typeList[index]) == True:
			parameterName = FileNameCustom(parameterList[index], 0)
			enumString, enumParameterList, enumClassName = GetEnumNameAndParameter(typeList[index])
			typeName = FileNameCustom(enumString, 0)
			localEnumName = typeName + str(counter)
			
			enumOutput += "			%s %s = %s.%s;\n" % (FirstStringUpper(typeName), localEnumName, FirstStringUpper(typeName), FirstStringUpper(enumParameterList[0]))
			
			enumParameterCount = 0
			for val in enumParameterList:
				if enumParameterCount == 0:
					enumOutput += "			if (lineList[(int)DataKey.%s] == \"%s\") {\n" % (FirstStringUpper(parameterName), FirstStringUpper(val))
					enumOutput += "				%s = %s.%s;\n" % (localEnumName, FirstStringUpper(typeName), FirstStringUpper(val))
					enumOutput += "			}"
				else:
					enumOutput += " else if (lineList[(int)DataKey.%s] == \"%s\") {\n" % (FirstStringUpper(parameterName), FirstStringUpper(val))
					enumOutput += "				%s = %s.%s;\n" % (localEnumName, FirstStringUpper(typeName), FirstStringUpper(val))
					enumOutput += "			}"
				enumParameterCount = enumParameterCount + 1
			enumOutput += "\n"
			output = "			%s.replace" % (className)
			parseString = output.replace("replace", ("Add%s(fbb, %s)" % (FirstStringUpper(FileNameCustom(parameterList[index], 0)), localEnumName)))
			parseString += ";\n"
			enumOutput += parseString
			manager_cs += enumOutput
			manager_cs += "\n"
			manager_cs += "\n"
			counter += 1
		
	manager_cs += "\n"
#===#

	for index in range(0, count):
		typeString = typeList[index]
		parseString = ""
		if ("enum:" in typeList[index]) == False:
			if ("list:" in typeList[index]) == True:
				parseString = "			%s.Add%s(fbb, %s)" % (className, FirstStringUpper(FileNameCustom(parameterList[index], 0)), (FileNameCustom(parameterList[index], 0)))
			else:
				if typeString == "string":
					parseString = GetStringParseString(className, parameterList[index])
				elif typeString == "int":
					parseString = GetIntParseString(className, parameterList[index])
				elif typeString == "float":
					parseString = GetFloatParseString(className, parameterList[index])
				elif typeString == "bool":
					parseString = GetBoolParseString(className, parameterList[index])
			parseString += ";\n"
		
		manager_cs += parseString

	manager_cs += "			Offset<%s> offset = %s.End%s(fbb);\n" % (className, className, className)
	manager_cs += "			%s.Finish%sBuffer(fbb, offset);\n" % (className, className)
	manager_cs += "			%sList.Add(int.Parse(lineList[(int)DataKey.Id]), fbb.DataBuffer);\n" % (className)
	manager_cs += "		}\n"
	manager_cs += "	}\n"
	manager_cs += "	\n"
	
	manager_cs += "	public %s GetData(int id) {\n" % (className)
	manager_cs += "		ByteBuffer output = null;\n"
	manager_cs += "		%sList.TryGetValue(id, out output);\n" % (className)
	manager_cs += "		return %s.GetRootAs%s(output);\n" % (className, className)
	manager_cs += "	}\n"
	manager_cs += "}\n"

	savePath = '../../Assets/Scripts/MasterData/'
	of = open(savePath + className + 'Manager' + ".cs", 'wb') # 書き込みモードで開く
	of.write(manager_cs) # 引数の文字列をファイルに書き込む
	of.close() # ファイルを閉じる

