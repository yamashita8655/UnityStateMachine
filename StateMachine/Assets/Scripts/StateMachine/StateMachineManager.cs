/*
 * @file StateMachineManager.cs
 * ステートマシンを管理するマネージャ.
 * @author 山下
 */

using UnityEngine;
using System.Collections;
using System.Collections.Generic;

/// <summary>
///	ステートマシンを管理するマネージャ.
/// </summary>
public class StateMachineManager
{
	private static StateMachineManager mInstance;
	
	private StateMachineManager()
	{ // Private Constructor
		Debug.Log("Create SampleSingleton instance.");
	}
	
	public static StateMachineManager Instance
	{
		get
		{
			if( mInstance == null ) mInstance = new StateMachineManager();
			
			return mInstance;
		}
	}

    Dictionary<StateMachineName, StateMachine> StateMachineMap = new Dictionary<StateMachineName, StateMachine>(); //< ステートマシンのマップ

	/// <summary>
	/// 初期化.
	/// </summary>
	public void Init()
	{
	}
	
	/// <summary>
	/// ステートマシンマップの作成.
	/// </summary>
	public void CreateStateMachineMap(StateMachineName name)
	{
		StateMachineMap.Add(name, new StateMachine());
	}
		
	/// <summary>
	/// ステートマシンの解放.
	/// </summary>
	/// <param name="machineName">ステートマシン名</param>
	public void Release(StateMachineName machineName)
	{
		StateMachine val = null;
		StateMachineMap.TryGetValue(machineName, out val);

		if (val != null) {
			val.Release();
			StateMachineMap.Remove(machineName);
		}
	}
		
	/// <summary>
	/// ステートの追加.
	/// </summary>
	/// <param name="machineName">ステートマシン名</param>
	/// <param name="stateType">ステートタイプ</param>
	/// <param name="state">ステート本体</param>
	public void AddState(StateMachineName machineName, int stateType, StateBase state)
	{
		StateMachine val = null;
		StateMachineMap.TryGetValue(machineName, out val);
		
		val.AddState(stateType, state);
	}

	/// <summary>
	/// ステートの変更.
	/// </summary>
	/// <param name="machineName">ステートマシン名</param>
	/// <param name="stateType">ステートタイプ</param>
	public void ChangeState(StateMachineName machineName, int stateType)
	{
		StateMachine val = null;
		StateMachineMap.TryGetValue(machineName, out val);
		
		val.ChangeState(stateType);
	}
	
	/// <summary>
	/// 保存していたステートに変更.
	/// </summary>
	/// <param name="machineName">ステートマシン名</param>
	public void ChangeSaveState(StateMachineName machineName)
	{
		StateMachine val = null;
		StateMachineMap.TryGetValue(machineName, out val);
		
		val.ChangeSaveState();
	}

	/// <summary>
	/// 現在のステート状態を保存して、ステートの変更.
	/// </summary>
	/// <param name="machineName">ステートマシン名</param>
	/// <param name="stateType">ステートタイプ</param>
	public void ChangeStateNowStatePause(StateMachineName machineName, int stateType)
	{
		StateMachine val = null;
		StateMachineMap.TryGetValue(machineName, out val);

		val.ChangeStateNowStatePause(stateType);
	}

	/// <summary>
	/// 更新.
	/// </summary>
	/// <param name="machineName">ステートマシン名</param>
	/// <param name="delta">経過時間</param>
    public void Update(StateMachineName machineName, float delta)
	{
		StateMachine val = null;
		StateMachineMap.TryGetValue(machineName, out val);

		// ステートマシンが存在しなければ、ここで終了
		if (val == null) return;

		val.Update(delta);
	}

	/// <summary>
	/// 一つ前のステートタイプの取得.
	/// </summary>
	/// <param name="machineName">ステートマシン名</param>
	/// <returns>ステートタイプ</returns>
	public int GetPrevState(StateMachineName machineName)
	{
		StateMachine val = null;
		StateMachineMap.TryGetValue(machineName, out val);

		return val.GetPrevState();
	}

	/// <summary>
	/// ステートタイプの取得.
	/// </summary>
	/// <param name="machineName">ステートマシン名</param>
	/// <returns>ステートタイプ</returns>
	public int GetState(StateMachineName machineName)
	{
		StateMachine val = null;
		if (StateMachineMap.TryGetValue(machineName, out val) == false) {
			return -1;
		}

		return val.GetState();
	}
	
	/// <summary>
	/// ステートのセーブ.
	/// </summary>
	/// <param name="machineName">ステートマシン名</param>
	public void SaveState(StateMachineName machineName)
	{
		StateMachine val = null;
		StateMachineMap.TryGetValue(machineName, out val);
		val.SaveState();
	}
	
	/// <summary>
	/// セーブしたステートの取得.
	/// </summary>
	/// <param name="machineName">ステートマシン名</param>
	/// <returns>ステートタイプ</returns>
	public int GetSaveState(StateMachineName machineName)
	{
		StateMachine val = null;
		StateMachineMap.TryGetValue(machineName, out val);

		return val.GetSaveState();
	}

	/// <summary>
	/// ステート本体の取得.
	/// </summary>
	/// <param name="machineName">ステートマシン名</param>
	/// <returns>ステート</returns>
	public StateBase GetStateBase(StateMachineName machineName)
	{
		StateMachine val = null;
		StateMachineMap.TryGetValue(machineName, out val);

		return val.GetStateBase();
	}
}

