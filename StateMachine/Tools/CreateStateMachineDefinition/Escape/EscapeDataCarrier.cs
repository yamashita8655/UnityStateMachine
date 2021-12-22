using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class EscapeDataCarrier : SimpleMonoBehaviourSingleton<EscapeDataCarrier> {
	// シーン制御用
	public SceneBase Scene { get; set; }
	
	public LocalSceneManager.SceneName NextSceneName { get; set; }

	public SceneDataBase Data { get; set; }
	
	public void Initialize() {
		NextSceneName = LocalSceneManager.SceneName.None;
	}

	public void Release() {
		Scene = null;
	}
}
