// このファイルは/Tools/CreateStateMachineDefinition/create_statemachinedefine.pyで自動生成されるので、編集禁止です。
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public partial class HomeScene : SceneBase
{
	private void InitializeStateMachine() {
		// ステートマシン
		StateMachineManager.Instance.Init();
		var stm = StateMachineManager.Instance;
		stm.CreateStateMachineMap(StateMachineName.Home);
		stm.AddState(StateMachineName.Home, (int)HomeState.Initialize, new HomeInitializeState());
		stm.AddState(StateMachineName.Home, (int)HomeState.UserWait, new HomeUserWaitState());
		stm.AddState(StateMachineName.Home, (int)HomeState.End, new HomeEndState());

	}

}
