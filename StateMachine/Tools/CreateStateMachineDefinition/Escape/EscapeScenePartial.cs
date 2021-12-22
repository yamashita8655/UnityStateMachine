// このファイルは/Tools/CreateStateMachineDefinition/create_statemachinedefine.pyで自動生成されるので、編集禁止です。
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public partial class EscapeScene : SceneBase
{
	private void InitializeStateMachine() {
		// ステートマシン
		StateMachineManager.Instance.Init();
		var stm = StateMachineManager.Instance;
		stm.CreateStateMachineMap(StateMachineName.Escape);
		stm.AddState(StateMachineName.Escape, (int)EscapeState.Initialize, new EscapeInitializeState());
		stm.AddState(StateMachineName.Escape, (int)EscapeState.BetInputWait, new EscapeBetInputWaitState());
		stm.AddState(StateMachineName.Escape, (int)EscapeState.QuestionDisplay, new EscapeQuestionDisplayState());
		stm.AddState(StateMachineName.Escape, (int)EscapeState.CreateMap, new EscapeCreateMapState());
		stm.AddState(StateMachineName.Escape, (int)EscapeState.CountDown, new EscapeCountDownState());
		stm.AddState(StateMachineName.Escape, (int)EscapeState.UserWait, new EscapeUserWaitState());
		stm.AddState(StateMachineName.Escape, (int)EscapeState.ClearEffect, new EscapeClearEffectState());
		stm.AddState(StateMachineName.Escape, (int)EscapeState.TimeUp, new EscapeTimeUpState());
		stm.AddState(StateMachineName.Escape, (int)EscapeState.Result, new EscapeResultState());
		stm.AddState(StateMachineName.Escape, (int)EscapeState.End, new EscapeEndState());

	}

}
