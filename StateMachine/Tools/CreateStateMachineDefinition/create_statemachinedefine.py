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

#savePathAndName = '../../Assets/Scripts/Utility/StateMachine/StateMachineManager_define.cs'
savePathAndName = 'StateMachineManager_define.cs'
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

#savePathAndName = '../../Assets/Scripts/Manager/LocalSceneManager.cs'
savePathAndName = 'LocalSceneManager.cs'
of = open(savePathAndName, 'wb') # 書き込みモードで開く
of.write(s.encode('utf-8')) # 引数の文字列をファイルに書き込む
of.close() # ファイルを閉じる


def CreateStateFile():
    stateMachineNameList = json_load["StateMachineName"]
    stateString = ""
    for v in stateMachineNameList:
        stateList = json_load[v]
        for v2 in stateList:
            s = "using System.Collections;\n"
            s += "using System.Collections.Generic;\n"
            s += "using UnityEngine;\n"
            s += "\n"
            s += "public class %s%sState : StateBase {\n" % (v, v2)
            s += "\n"
            s += "    /// <summary>\n"
            s += "    /// メイン前処理.\n"
            s += "    /// 戻り値は、同一フレーム内で次の処理に移行してよければfalse、1フレーム飛ばして欲しい場合はfalse.\n"
            s += "    /// </summary>\n"
            s += "    override public bool OnBeforeMain()\n"
            s += "    {\n"
            s += "		return false;\n"
            s += "    }\n"
            s += "\n"
            s += "    /// <summary>\n"
            s += "    /// メイン更新処理.\n"
            s += "    /// </summary>\n"
            s += "    /// <param name=\"delta\">経過時間</param>\n"
            s += "    override public void OnUpdateMain(float delta)\n"
            s += "    {\n"
            s += "    }\n"
            s += "\n"
            s += "    /// <summary>\n"
            s += "    /// ステート解放時処理.\n"
            s += "    /// </summary>\n"
            s += "    override public void OnRelease()\n"
            s += "    {\n"
            s += "    }\n"
            s += "}\n"
            #savePath = '../../Assets/Scripts/%s' % (v)
            savePath = '%s' % (v)
            os.makedirs(savePath, exist_ok=True)
            #savePathAndName = '../../Assets/Scripts/%s/%s%sState.cs' % (v, v, v2)
            savePathAndName = '%s/%s%sState.cs' % (v, v, v2)
            isExist = os.path.isfile(savePathAndName)
            if isExist == False:
                of = open(savePathAndName, 'wb') # 書き込みモードで開く
                of.write(s.encode('utf-8')) # 引数の文字列をファイルに書き込む
                of.close() # ファイルを閉じる
                print("New:" + savePathAndName)
            else:
                print("WARNING:" + savePathAndName + " Already Exist")

def CreateDataCarrierFile():
    stateMachineNameList = json_load["StateMachineName"]
    for v in stateMachineNameList:
        s = "using System;\n"
        s += "using System.Collections;\n"
        s += "using System.Collections.Generic;\n"
        s += "using UnityEngine;\n"
        s += "\n"
        s += "public class %sDataCarrier : SimpleMonoBehaviourSingleton<%sDataCarrier> {\n" % (v, v)
        s += "	// シーン制御用\n"
        s += "	public SceneBase Scene { get; set; }\n"
        s += "	\n"
        s += "	public LocalSceneManager.SceneName NextSceneName { get; set; }\n"
        s += "\n"
        s += "	public SceneDataBase Data { get; set; }\n"
        s += "	\n"
        s += "	public void Initialize() {\n"
        s += "		NextSceneName = LocalSceneManager.SceneName.None;\n"
        s += "	}\n"
        s += "\n"
        s += "	public void Release() {\n"
        s += "		Scene = null;\n"
        s += "	}\n"
        s += "}\n"
        #savePathAndName = '../../Assets/Scripts/%s/%sDataCarrier.cs' % (v)
        savePathAndName = '%s/%sDataCarrier.cs' % (v, v)
        isExist = os.path.isfile(savePathAndName)
        if isExist == False:
            of = open(savePathAndName, 'wb') # 書き込みモードで開く
            of.write(s.encode('utf-8')) # 引数の文字列をファイルに書き込む
            of.close() # ファイルを閉じる
            print("New:" + savePathAndName)
        else:
            print("WARNING:" + savePathAndName + " Already Exist")

def CreateSceneFile():
    stateMachineNameList = json_load["StateMachineName"]
    for v in stateMachineNameList:
        # こっちは、一度だけ作って、上書きしないファイル
        s = "using System;\n"
        s += "using System.Collections;\n"
        s += "using System.Collections.Generic;\n"
        s += "using UnityEngine;\n"
        s += "using UnityEngine.UI;\n"
        s += "\n"
        s += "public partial class %sScene : SceneBase\n" % (v)
        s += "{\n"
        s += "	// Start is called before the first frame update\n"
        s += "	IEnumerator Start() {\n"
        s += "		while (EntryPoint.IsInitialized == false) {\n"
        s += "			yield return null;\n"
        s += "		}\n"
        s += "\n"
        s += "		// データキャリア\n"
        s += "		%sDataCarrier.Instance.Initialize();\n" % (v)
        s += "		%sDataCarrier.Instance.Scene = this;\n" % (v)
        s += "		\n"
        s += "		// ステートマシン\n"
        s += "		InitializeStateMachine();\n"
        s += "\n"
        s += "		StateMachineManager.Instance.ChangeState(StateMachineName.%s, (int)%sState.Initialize);\n" % (v, v)
        s += "		FadeManager.Instance.FadeIn(0.5f, null);\n"
        s += "	}\n"
        s += "\n"
        s += "	// Update is called once per frame\n"
        s += "	void Update()\n"
        s += "	{\n"
        s += "		StateMachineManager.Instance.Update(StateMachineName.%s, Time.deltaTime);\n" % (v)
        s += "	}\n"
        s += "	\n"
        s += "	void OnDestroy()\n"
        s += "	{\n"
        s += "		StateMachineManager.Instance.Release(StateMachineName.%s);\n" % (v)
        s += "		if (%sDataCarrier.IsNull() == false) {\n" % (v)
        s += "			%sDataCarrier.Instance.Release();\n" % (v)
        s += "			%sDataCarrier.DestroyInstance();\n" % (v)
        s += "		}\n"
        s += "	}\n"
        s += "}\n"

        #savePathAndName = '../../Assets/Scripts/%s/%sScene.cs' % (v, v)
        savePathAndName = '%s/%sScene.cs' % (v, v)
        isExist = os.path.isfile(savePathAndName)
        if isExist == False:
            of = open(savePathAndName, 'wb') # 書き込みモードで開く
            of.write(s.encode('utf-8')) # 引数の文字列をファイルに書き込む
            of.close() # ファイルを閉じる
            print("New:" + savePathAndName)
        else:
            print("WARNING:" + savePathAndName + " Already Exist")
        
        # こっちは常に上書きするファイル
        s = "// このファイルは/Tools/CreateStateMachineDefinition/create_statemachinedefine.pyで自動生成されるので、編集禁止です。\n"
        s += "using System;\n"
        s += "using System.Collections;\n"
        s += "using System.Collections.Generic;\n"
        s += "using UnityEngine;\n"
        s += "using UnityEngine.UI;\n"
        s += "\n"
        s += "public partial class %sScene : SceneBase\n" % (v)
        s += "{\n"
        s += "	private void InitializeStateMachine() {\n"
        s += "		// ステートマシン\n"
        s += "		StateMachineManager.Instance.Init();\n"
        s += "		var stm = StateMachineManager.Instance;\n"
        s += "		stm.CreateStateMachineMap(StateMachineName.%s);\n" % (v)

        stateList = json_load[v]
        for v2 in stateList:
            s += "		stm.AddState(StateMachineName.%s, (int)%sState.%s, new %s%sState());\n" % (v, v, v2, v, v2)

        s += "\n"
        s += "	}\n"
        s += "\n"
        s += "}\n"

        #savePathAndName = '../../Assets/Scripts/%s/%sScenePartial.cs' % (v, v)
        savePathAndName = '%s/%sScenePartial.cs' % (v, v)
        isExist = os.path.isfile(savePathAndName)
        of = open(savePathAndName, 'wb') # 書き込みモードで開く
        of.write(s.encode('utf-8')) # 引数の文字列をファイルに書き込む
        of.close() # ファイルを閉じる

CreateStateFile()
CreateDataCarrierFile()
CreateSceneFile()
