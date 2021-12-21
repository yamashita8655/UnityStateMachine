// このスクリプトは、Tools/CreateStateMachineDefinition.pyで自動生成されます。
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class LocalSceneManager : SimpleMonoBehaviourSingleton<LocalSceneManager> {
	private List<string> SceneNameList = new List<string>() {
		"Home",
		"Escape",
		"Fade",
		"SystemDialog",
		"Debug",
		"ImageProccess",
	};

	public enum SceneName : int {
		Home = 0,
		Escape,
		Fade,
		SystemDialog,
		Debug,
		ImageProccess,
		None
	};

	// 初回起動のシーン指定なので、実装中は、ここを作業中のシーンに変えてください
	private SceneName FirstSceneName = SceneName.Home;

	private SceneName CurrentSceneName = SceneName.None;
	
	public SceneDataBase SceneData { get; private set;}

	public void Initialize() {
		SceneData = null;
		SceneManager.LoadScene(SceneNameList[(int)SceneName.Fade], LoadSceneMode.Additive);
		SceneManager.LoadScene(SceneNameList[(int)SceneName.SystemDialog], LoadSceneMode.Additive);
		SceneManager.LoadScene(SceneNameList[(int)SceneName.Debug], LoadSceneMode.Additive);
#if UNITY_EDITOR
		SceneManager.LoadScene(SceneNameList[(int)SceneName.ImageProccess], LoadSceneMode.Additive);
#endif
	}

	public SceneName GetFirstSceneName() {
		return FirstSceneName;
	}
	
	public void LoadScene(SceneName name, SceneDataBase sceneData) {
		SceneData = sceneData;

		// 本来は、この辺りでフェードなどの切り替え処理が入るので、
		// LoadとUnloadは一辺に行うべきではない
		SceneManager.LoadScene(SceneNameList[(int)name], LoadSceneMode.Additive);
		if (CurrentSceneName != SceneName.None) {
			SceneManager.UnloadSceneAsync(SceneNameList[(int)CurrentSceneName]);
		}

		CurrentSceneName = name;
	}
}
