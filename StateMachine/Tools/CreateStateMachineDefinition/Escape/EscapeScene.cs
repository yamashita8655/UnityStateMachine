using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public partial class EscapeScene : SceneBase
{
	// Start is called before the first frame update
	IEnumerator Start() {
		while (EntryPoint.IsInitialized == false) {
			yield return null;
		}

		// データキャリア
		EscapeDataCarrier.Instance.Initialize();
		EscapeDataCarrier.Instance.Scene = this;
		
		// ステートマシン
		InitializeStateMachine();

		StateMachineManager.Instance.ChangeState(StateMachineName.Escape, (int)EscapeState.Initialize);
		FadeManager.Instance.FadeIn(0.5f, null);
	}

	// Update is called once per frame
	void Update()
	{
		StateMachineManager.Instance.Update(StateMachineName.Escape, Time.deltaTime);
	}
	
	void OnDestroy()
	{
		StateMachineManager.Instance.Release(StateMachineName.Escape);
		if (EscapeDataCarrier.IsNull() == false) {
			EscapeDataCarrier.Instance.Release();
			EscapeDataCarrier.DestroyInstance();
		}
	}
}
