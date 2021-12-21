/*
 * @file StateMachine.cs
 * ステートを管理するステートマシン
 * @author 山下
 */

using UnityEngine;
using System.Collections;
using System.Collections.Generic;

enum MachineState : int
{
	None,
	BeforeInit,
	UpdateInit,
	AfterInit,
	BeforeMain,
	UpdateMain,
	AfterMain,
	BeforeEnd,
	UpdateEnd,
	AfterEnd,
	Release	
};

/// <summary>
///	ステートを管理するステートマシン
/// </summary>
public class StateMachine
{
	
	private StateBase NowState;
	private MachineState ManageState;
	private int State;
	private int NextState;
	private int PrevState;
	private int CurrentSaveState;

	private Dictionary<int, StateBase> StateMap;

	/// <summary>
	/// コンストラクタ.
	/// </summary>
	public StateMachine()
	{
		Init();
	}

	/// <summary>
	/// 初期化.
	/// </summary>
	public void Init()
	{
		NowState       = null;
		ManageState	= MachineState.None;
		State			= 0;
		NextState 		= 0;
		PrevState 		= 0;
	
		StateMap		= new Dictionary<int, StateBase>();
	}
	
	/// <summary>
	/// 更新処理.
	/// </summary>
	/// <param name="delta">経過時間</param>
	public void Update(float delta)
	{
		if(NowState == null)
		{
			return;
		}

		bool canSkip = false;

		switch(ManageState)
		{
		case MachineState.BeforeInit:
			if (NowState.IsPause() == true)
			{
				// ポーズ状態だったら、即メインのアップデート処理状態にする
				ManageState = MachineState.UpdateMain;
				NowState.PauseDisable();
			}
			else
			{
				ManageState = MachineState.UpdateInit;
				canSkip = NowState._OnBeforeInit();
			}
			break;
		
		case MachineState.UpdateInit:
			{
				bool isEnd = NowState.OnUpdateInit(delta);
				if(isEnd == true)
				{
					ManageState = MachineState.AfterInit;
				}
			}
			break;
		
		case MachineState.AfterInit:
			ManageState = MachineState.BeforeMain;
			canSkip = NowState.OnAfterInit();
			break;
		
		case MachineState.BeforeMain:
			ManageState = MachineState.UpdateMain;
			canSkip = NowState.OnBeforeMain();
			break;
		
		case MachineState.UpdateMain:
			NowState.OnUpdateMain(delta);
			break;
		
		case MachineState.AfterMain:
			ManageState = MachineState.BeforeEnd;
			canSkip = NowState.OnAfterMain();
			break;
		
		case MachineState.BeforeEnd:
			ManageState = MachineState.UpdateEnd;
			canSkip = NowState.OnBeforeEnd();
			break;
		
		case MachineState.UpdateEnd:
			{
				bool isEnd = NowState.OnUpdateEnd(delta);
				if(isEnd == true)
				{
					ManageState = MachineState.AfterEnd;
				}
			}
			break;
		
		case MachineState.AfterEnd:
			ManageState = MachineState.Release;
			canSkip = NowState.OnAfterEnd();
			break;
		
		case MachineState.Release:
			{
				ManageState = MachineState.BeforeInit;
				if (NowState.IsPause() != true)
				{
					NowState._OnRelease();
				}
				PrevState = State;
				State = NextState;
				
				StateBase val = null;
				StateMap.TryGetValue(State, out val);
				NowState = val;
				break;
			}
		}
		
		// 同一フレーム内で、先のステートに進んで良ければ、
		// もう一度Updateを呼び出す
		if (canSkip == true) {
			Update(delta);
		}
	}
	
	/// <summary>
	/// 解放処理.
	/// </summary>
	public void Release()
	{
		foreach(var it in StateMap)
		{
			if(it.Value.IsInitCalled() == true)
			{
				it.Value._OnRelease();
			}
			//it.Value = null;
		}

		StateMap.Clear();
		NowState = null;
	}
	
	/// <summary>
	/// ステートの変更.
	/// </summary>
	/// <param name="stateType">変更後のステート</param>
	public void ChangeState(int stateType)
	{
		// 仮 ここ、直す必要がある。途中で呼び出された場合に、流れがおかしくなる可能性がある
		if (ManageState != MachineState.AfterInit &&
			ManageState != MachineState.UpdateMain		)
		{
			Debug.Log("StateMachine::changeState");
			Debug.Log((int)ManageState + " state isnt use changeState");
		}

		if(NowState != null)
		{
			NextState = stateType;
			ManageState = MachineState.AfterMain;
		}
		else
		{
			StateBase val = null;
			StateMap.TryGetValue(stateType, out val);
			NowState = val;
			ManageState = MachineState.BeforeInit;
		}
	}
	
	/// <summary>
	/// 今居るステートを保存して、戻れるようにしておく.
	/// </summary>
	public void ChangeSaveState()
	{
		ChangeState(CurrentSaveState);
	}
	
	/// <summary>
	/// 今のステートを保存して、次回戻ってきた際に初期化処理を呼ばないようにしたステートの変更.
	/// </summary>
	/// <param name="stateType">変更後のステート</param>
	public void ChangeStateNowStatePause(int stateType)
	{
		if (ManageState != MachineState.AfterInit &&
			ManageState != MachineState.UpdateMain)
		{
			Debug.Log("StateMachine::changeState");
			Debug.Log(ManageState + " state isnt use changeState");
		}

		if(NowState != null)
		{
			NowState.PauseEnable();
			NextState = stateType;
			ManageState = MachineState.Release;// 即リリース状態にしているが、PAUSEをかけているので、リリースの処理は呼び出されない
		}
		else
		{
			StateBase val = null;
			StateMap.TryGetValue(stateType, out val);
			NowState = val;
			ManageState = MachineState.BeforeInit;
		}
	}

	/// <summary>
	/// ステートの追加.
	/// </summary>
	/// <param name="stateType">ステートタイプ</param>
	/// <param name="state">ステート本体</param>
	public void AddState(int stateType, StateBase state)
	{
		StateBase val = null;
		if(StateMap.TryGetValue(stateType, out val) == true)
		{
			return;
		}

		//StateMap.insert(std::make_pair(stateType, state));
		StateMap.Add(stateType, state);
	}
	
	/// <summary>
	/// ステートの取得.
	/// </summary>
	/// <returns>ステートタイプ</returns>
	public int GetState()
	{
		return State;
	}
	
	/// <summary>
	/// 予約した次のステートの取得.
	/// 今のステートだと、毎フレームチェックする場合に、Releaseが呼ばれるまで次ステートに切り替わらないので、判定に使えない
	/// </summary>
	/// <returns>ステートタイプ</returns>
	public int GetNextState()
	{
		return NextState;
	}
	
	/// <summary>
	/// 一個前のステートの取得.
	/// </summary>
	/// <returns>ステートタイプ</returns>
	public int GetPrevState()
	{
		return PrevState;
	}
	
	/// <summary>
	/// ステートのセーブ
	/// </summary>
	public void SaveState()
	{
		CurrentSaveState = State;
	}
	
	/// <summary>
	/// セーブしたステートの取得.
	/// </summary>
	/// <returns>ステートタイプ</returns>
	public int GetSaveState()
	{
		return CurrentSaveState;
	}

	/// <summary>
	/// ステート本体の取得.
	/// </summary>
	/// <returns>ステート</returns>
	public StateBase GetStateBase()
	{
		return NowState;
	}
}
