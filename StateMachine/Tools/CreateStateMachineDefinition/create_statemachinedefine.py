# coding: utf-8
#設計
#

import os
import sys
import json

# まずは、ディレクトリ走査
json_open = open("meta.json", 'r')
json_load = json.load(json_open)

s = "/*\n"
s += " * @file StateMachineManager_define.cs\n"
s += " * ステートマシンの種類を記載する定義クラス.\n"
s += " * このスクリプトは、Tools/CreateStateMachineDefinition.pyで自動生成されます。\n"
s += " * @author 山下\n"
s += " */\n"
s += "\n"
s += "using UnityEngine;\n"
s += "using System.Collections;\n"
s += "\n"
s += "/// <summary>\n"
s += "///	ステートマシンの種類を記載する定義クラス.\n"
s += "/// </summary>\n"
s += "public enum StateMachineName : int\n"
s += "{\n"

stateMachineNameList = json_load["StateMachineName"]
isFirst = True
stateString = ""
for v in stateMachineNameList:
	if isFirst == True:
		s += "\t" + v + " = 0,\n"
		isFirst = False
	else:
		s += "\t" + v + ",\n"

	stateList = json_load[v]
	stateString += "public enum %sState : int\n" % (v)
	stateString += "{\n"
	isFirst2 = True
	for v2 in stateList:
		if isFirst2 == True:
			stateString += "\t" + v2 + " = 0,\n"
			isFirst2 = False
		else:
			stateString += "\t" + v2 + ",\n"
	
	stateString += "}\n"
	stateString += "\n"


s += "};\n"
s += "\n"

s += stateString
	
savePathAndName = '../../Assets/Scripts/Utility/StateMachine/StateMachineManager_define.cs'
#savePathAndName = 'StateMachineManager_define.cs'
of = open(savePathAndName, 'wb') # 書き込みモードで開く
of.write(s.encode('utf-8')) # 引数の文字列をファイルに書き込む
of.close() # ファイルを閉じる

s = "// このスクリプトは、Tools/CreateStateMachineDefinition.pyで自動生成されます。\n"
s += "using System;\n"
s += "using System.Collections;\n"
s += "using System.Collections.Generic;\n"
s += "using UnityEngine;\n"
s += "using UnityEngine.SceneManagement;\n"
s += "\n"
s += "public class LocalSceneManager : SimpleMonoBehaviourSingleton<LocalSceneManager> {\n"
s += "	private List<string> SceneNameList = new List<string>() {\n"

for v in stateMachineNameList:
	s += "\t\t\"" + v + "\",\n"

s += "		\"Fade\",\n"
s += "		\"SystemDialog\",\n"
s += "		\"Debug\",\n"
s += "		\"ImageProccess\",\n"
s += "	};\n"
s += "\n"
s += "	public enum SceneName : int {\n"

isFirst = True
stateString = ""
for v in stateMachineNameList:
	if isFirst == True:
		s += "\t\t" + v + " = 0,\n"
		isFirst = False
	else:
		s += "\t\t" + v + ",\n"

s += "		Fade,\n"
s += "		SystemDialog,\n"
s += "		Debug,\n"
s += "		ImageProccess,\n"
s += "		None\n"
s += "	};\n"
s += "\n"
s += "	// 初回起動のシーン指定なので、実装中は、ここを作業中のシーンに変えてください\n"
s += "	private SceneName FirstSceneName = SceneName.Home;\n"
s += "\n"
s += "	private SceneName CurrentSceneName = SceneName.None;\n"
s += "	\n"
s += "	public SceneDataBase SceneData { get; private set;}\n"
s += "\n"
s += "	public void Initialize() {\n"
s += "		SceneData = null;\n"
s += "		SceneManager.LoadScene(SceneNameList[(int)SceneName.Fade], LoadSceneMode.Additive);\n"
s += "		SceneManager.LoadScene(SceneNameList[(int)SceneName.SystemDialog], LoadSceneMode.Additive);\n"
s += "		SceneManager.LoadScene(SceneNameList[(int)SceneName.Debug], LoadSceneMode.Additive);\n"
s += "#if UNITY_EDITOR\n"
s += "		SceneManager.LoadScene(SceneNameList[(int)SceneName.ImageProccess], LoadSceneMode.Additive);\n"
s += "#endif\n"
s += "	}\n"
s += "\n"
s += "	public SceneName GetFirstSceneName() {\n"
s += "		return FirstSceneName;\n"
s += "	}\n"
s += "	\n"
s += "	public void LoadScene(SceneName name, SceneDataBase sceneData) {\n"
s += "		SceneData = sceneData;\n"
s += "\n"
s += "		// 本来は、この辺りでフェードなどの切り替え処理が入るので、\n"
s += "		// LoadとUnloadは一辺に行うべきではない\n"
s += "		SceneManager.LoadScene(SceneNameList[(int)name], LoadSceneMode.Additive);\n"
s += "		if (CurrentSceneName != SceneName.None) {\n"
s += "			SceneManager.UnloadSceneAsync(SceneNameList[(int)CurrentSceneName]);\n"
s += "		}\n"
s += "\n"
s += "		CurrentSceneName = name;\n"
s += "	}\n"
s += "}\n"


																							 
savePathAndName = '../../Assets/Scripts/Manager/LocalSceneManager.cs'
#savePathAndName = 'LocalSceneManager.cs'
of = open(savePathAndName, 'wb') # 書き込みモードで開く
of.write(s.encode('utf-8')) # 引数の文字列をファイルに書き込む
of.close() # ファイルを閉じる

# LocalSceneManagerも変更する必要があるので、対応してしまう

#for v in json_load.values():
#	print(v)
