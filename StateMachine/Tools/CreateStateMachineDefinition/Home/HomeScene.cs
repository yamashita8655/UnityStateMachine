using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public partial class HomeScene : SceneBase
{
	// Start is called before the first frame update
	IEnumerator Start() {
		while (EntryPoint.IsInitialized == false) {
			yield return null;
		}

		// データキャリア
		HomeDataCarrier.Instance.Initialize();
		HomeDataCarrier.Instance.Scene = this;
		
		// ステートマシン
		InitializeStateMachine();

		StateMachineManager.Instance.ChangeState(StateMachineName.Home, (int)HomeState.Initialize);
		FadeManager.Instance.FadeIn(0.5f, null);
	}

	// Update is called once per frame
	void Update()
	{
		StateMachineManager.Instance.Update(StateMachineName.Home, Time.deltaTime);
	}
	
	void OnDestroy()
	{
		StateMachineManager.Instance.Release(StateMachineName.Home);
		if (HomeDataCarrier.IsNull() == false) {
			HomeDataCarrier.Instance.Release();
			HomeDataCarrier.DestroyInstance();
		}
	}
}
