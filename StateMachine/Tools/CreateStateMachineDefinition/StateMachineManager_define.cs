/*
 * @file StateMachineManager_define.cs
 * ステートマシンの種類を記載する定義クラス.
 * このスクリプトは、Tools/CreateStateMachineDefinition.pyで自動生成されます。
 * @author 山下
 */

using UnityEngine;
using System.Collections;

/// <summary>
///	ステートマシンの種類を記載する定義クラス.
/// </summary>
public enum StateMachineName : int
{
	Home = 0,
	Escape,
};

public enum HomeState : int
{
	Initialize = 0,
	UserWait,
	End,
}

public enum EscapeState : int
{
	Initialize = 0,
	BetInputWait,
	QuestionDisplay,
	CreateMap,
	CountDown,
	UserWait,
	ClearEffect,
	TimeUp,
	Result,
	End,
}

