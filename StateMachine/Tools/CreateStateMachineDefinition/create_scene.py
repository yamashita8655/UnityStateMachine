# coding: utf-8
#設計
#

import os
import sys

def CreateSceneFile(sceneName):
    s = "using System;\n"
    s += "using System.Collections;\n"
    s += "using System.Collections.Generic;\n"
    s += "using UnityEngine;\n"
    s += "using UnityEngine.UI;\n"
    s += "\n"
    s += "public class %sScene : SceneBase\n" % (sceneName)
    s += "{\n"
    s += "	// Start is called before the first frame update\n"
    s += "	IEnumerator Start() {\n"
    s += "		while (EntryPoint.IsInitialized == false) {\n"
    s += "			yield return null;\n"
    s += "		}\n"
    s += "\n"
    s += "		// データキャリア\n"
    s += "		%sDataCarrier.Instance.Initialize();\n" % (sceneName)
    s += "		%sDataCarrier.Instance.Scene = this;\n" % (sceneName)
    s += "		\n"
    s += "		// ステートマシン\n"
    s += "		StateMachineManager.Instance.Init();\n"
    s += "		var stm = StateMachineManager.Instance;\n"
    s += "		stm.CreateStateMachineMap(StateMachineName.%s);\n" % (sceneName)
    s += "		stm.AddState(StateMachineName.%s, (int)%sState.Initialize, new %sInitializeState());\n" % (sceneName, sceneName, sceneName)
    s += "		stm.AddState(StateMachineName.%s, (int)%sState.UserWait, new %sUserWaitState());\n" % (sceneName, sceneName, sceneName)
    s += "		stm.AddState(StateMachineName.%s, (int)%sState.End, new %sEndState());\n" % (sceneName, sceneName, sceneName)
    s += "		\n"
    s += "		stm.ChangeState(StateMachineName.%s, (int)%sState.Initialize);\n" % (sceneName, sceneName)
    s += "			\n"
    s += "		FadeManager.Instance.FadeIn(0.5f, null);\n"
    s += "	}\n"
    s += "\n"
    s += "	// Update is called once per frame\n"
    s += "	void Update()\n"
    s += "	{\n"
    s += "		StateMachineManager.Instance.Update(StateMachineName.%s, Time.deltaTime);\n" % (sceneName)
    s += "	}\n"
    s += "	\n"
    s += "	void OnDestroy()\n"
    s += "	{\n"
    s += "		StateMachineManager.Instance.Release(StateMachineName.%s);\n" % (sceneName)
    s += "		if (%sDataCarrier.IsNull() == false) {\n" % (sceneName)
    s += "			%sDataCarrier.Instance.Release();\n" % (sceneName)
    s += "			%sDataCarrier.DestroyInstance();\n" % (sceneName)
    s += "		}\n"
    s += "	}\n"
    s += "}\n"

    savePathAndName = '../../Assets/Scripts/%s/%sScene.cs' % (sceneName, sceneName)
    isExist = os.path.isfile(savePathAndName)
    if isExist == False:
        of = open(savePathAndName, 'xb') # 書き込みモードで開く
        of.write(s.encode('utf-8')) # 引数の文字列をファイルに書き込む
        of.close() # ファイルを閉じる
    else:
        print("ERROR:" + savePathAndName + " Already Exist")

def CreateInitializeFile(sceneName):
    s = "using System;\n"
    s += "using System.Collections;\n"
    s += "using System.Collections.Generic;\n"
    s += "using UnityEngine;\n"
    s += "\n"
    s += "public class %sInitializeState : StateBase {\n" % (sceneName)
    s += "\n"
    s += "	/// <summary>\n"
    s += "	/// 初期化前処理.\n"
    s += "	/// </summary>\n"
    s += "	override public bool OnBeforeInit()\n"
    s += "	{\n"
    s += "		var scene = %sDataCarrier.Instance.Scene as %sScene;\n" % (sceneName, sceneName)
    s += "\n"
    s += "		return true;\n"
    s += "	}\n"
    s += "\n"
    s += "	/// <summary>\n"
    s += "	/// メイン更新処理.\n"
    s += "	/// </summary>\n"
    s += "	/// <param name=\"delta\">経過時間</param>\n"
    s += "	override public void OnUpdateMain(float delta)\n"
    s += "	{\n"
    s += "		StateMachineManager.Instance.ChangeState(StateMachineName.%s, (int)%sState.UserWait);\n" % (sceneName, sceneName)
    s += "	}\n"
    s += "\n"
    s += "	/// <summary>\n"
    s += "	/// ステート解放時処理.\n"
    s += "	/// </summary>\n"
    s += "	override public void OnRelease()\n"
    s += "	{\n"
    s += "	}\n"
    s += "}\n"
    
    savePathAndName = '../../Assets/Scripts/%s/%sInitializeState.cs' % (sceneName, sceneName)
    isExist = os.path.isfile(savePathAndName)
    if isExist == False:
        of = open(savePathAndName, 'xb') # 書き込みモードで開く
        of.write(s.encode('utf-8')) # 引数の文字列をファイルに書き込む
        of.close() # ファイルを閉じる
    else:
        print("ERROR:" + savePathAndName + " Already Exist")

def CreateUserWaitFile(sceneName):
    s = "using System.Collections;\n"
    s += "using System.Collections.Generic;\n"
    s += "using UnityEngine;\n"
    s += "\n"
    s += "public class %sUserWaitState : StateBase {\n" % (sceneName)
    s += "\n"
    s += "	/// <summary>\n"
    s += "	/// 初期化前処理.\n"
    s += "	/// </summary>\n"
    s += "	override public bool OnBeforeInit()\n"
    s += "	{\n"
    s += "		var scene = %sDataCarrier.Instance.Scene as %sScene;\n" % (sceneName, sceneName)
    s += "		return true;\n"
    s += "	}\n"
    s += "	\n"
    s += "	/// <summary>\n"
    s += "	/// メイン更新処理.\n"
    s += "	/// </summary>\n"
    s += "	/// <param name=\"delta\">経過時間</param>\n"
    s += "	override public void OnUpdateMain(float delta)\n"
    s += "	{\n"
    s += "	}\n"
    s += "\n"
    s += "	/// <summary>\n"
    s += "	/// ステート解放時処理.\n"
    s += "	/// </summary>\n"
    s += "	override public void OnRelease()\n"
    s += "	{\n"
    s += "	}\n"
    s += "}\n"

    savePathAndName = '../../Assets/Scripts/%s/%sUserWaitState.cs' % (sceneName, sceneName)
    isExist = os.path.isfile(savePathAndName)
    if isExist == False:
        of = open(savePathAndName, 'xb') # 書き込みモードで開く
        of.write(s.encode('utf-8')) # 引数の文字列をファイルに書き込む
        of.close() # ファイルを閉じる
    else:
        print("ERROR:" + savePathAndName + " Already Exist")

def CreateEndFile(sceneName):
    s = "using System.Collections;\n"
    s += "using System.Collections.Generic;\n"
    s += "using UnityEngine;\n"
    s += "\n"
    s += "public class %sEndState : StateBase {\n" % (sceneName)
    s += "\n"
    s += "    /// <summary>\n"
    s += "    /// メイン前処理.\n"
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
    s += "		FadeManager.Instance.FadeOut(FadeManager.Type.Mask, 0.5f, () => {\n"
    s += "			LocalSceneManager.Instance.LoadScene(%sDataCarrier.Instance.NextSceneName, %sDataCarrier.Instance.Data);\n" % (sceneName, sceneName)
    s += "		});\n"
    s += "    }\n"
    s += "\n"
    s += "    /// <summary>\n"
    s += "    /// ステート解放時処理.\n"
    s += "    /// </summary>\n"
    s += "    override public void OnRelease()\n"
    s += "    {\n"
    s += "    }\n"
    s += "}\n"
    
    savePathAndName = '../../Assets/Scripts/%s/%sEndState.cs' % (sceneName, sceneName)
    isExist = os.path.isfile(savePathAndName)
    if isExist == False:
        of = open(savePathAndName, 'xb') # 書き込みモードで開く
        of.write(s.encode('utf-8')) # 引数の文字列をファイルに書き込む
        of.close() # ファイルを閉じる
    else:
        print("ERROR:" + savePathAndName + " Already Exist")

def CreateDataCarrierFile(sceneName):
    s = "using System;\n"
    s += "using System.Collections;\n"
    s += "using System.Collections.Generic;\n"
    s += "using UnityEngine;\n"
    s += "\n"
    s += "public class %sDataCarrier : SimpleMonoBehaviourSingleton<%sDataCarrier> {\n" % (sceneName, sceneName)
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
    savePathAndName = '../../Assets/Scripts/%s/%sDataCarrier.cs' % (sceneName, sceneName)
    isExist = os.path.isfile(savePathAndName)
    if isExist == False:
        of = open(savePathAndName, 'xb') # 書き込みモードで開く
        of.write(s.encode('utf-8')) # 引数の文字列をファイルに書き込む
        of.close() # ファイルを閉じる
    else:
        print("ERROR:" + savePathAndName + " Already Exist")

def CreateEndFile(sceneName):
    s = "using System.Collections;\n"
    s += "using System.Collections.Generic;\n"
    s += "using UnityEngine;\n"
    s += "\n"
    s += "public class %sEndState : StateBase {\n" % (sceneName)
    s += "\n"
    s += "    /// <summary>\n"
    s += "    /// メイン前処理.\n"
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
    s += "		FadeManager.Instance.FadeOut(FadeManager.Type.Mask, 0.5f, () => {\n"
    s += "			LocalSceneManager.Instance.LoadScene(%sDataCarrier.Instance.NextSceneName, %sDataCarrier.Instance.Data);\n" % (sceneName, sceneName)
    s += "		});\n"
    s += "    }\n"
    s += "\n"
    s += "    /// <summary>\n"
    s += "    /// ステート解放時処理.\n"
    s += "    /// </summary>\n"
    s += "    override public void OnRelease()\n"
    s += "    {\n"
    s += "    }\n"
    s += "}\n"
    
    savePathAndName = '../../Assets/Scripts/%s/%sEndState.cs' % (sceneName, sceneName)
    isExist = os.path.isfile(savePathAndName)
    if isExist == False:
        of = open(savePathAndName, 'xb') # 書き込みモードで開く
        of.write(s.encode('utf-8')) # 引数の文字列をファイルに書き込む
        of.close() # ファイルを閉じる
    else:
        print("ERROR:" + savePathAndName + " Already Exist")


# まずは、ディレクトリ走査
#new_dir_path_recursive = '../../Assets/Scripts/' + sys.argv[1]
new_dir_path_recursive = sys.argv[1]
os.makedirs(new_dir_path_recursive, exist_ok=True)
#CreateSceneFile(sys.argv[1])
#CreateInitializeFile(sys.argv[1])
#CreateUserWaitFile(sys.argv[1])
#CreateEndFile(sys.argv[1])
#CreateDataCarrierFile(sys.argv[1])
