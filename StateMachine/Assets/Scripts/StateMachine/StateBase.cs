/*
 * @file StateBase.cs
 * ステートマシンが管理する、各ステートのベースクラス.
 * @author 山下
 */

using UnityEngine;
using System.Collections;

/// <summary>
///	ステートマシンが管理する、各ステートのベースクラス.
/// </summary>
public class StateBase
{
	private bool IsPauseFlag;// 今のステートが、次のChangeStateで有効になるまで動作させなくする。次の有効で、自動的にfalseにする
	private bool InitCalled;// 

	/// <summary>
	/// コンストラクタ.
	/// </summary>
	public StateBase()
	{
		IsPauseFlag = false;
	}

	/// <summary>
	/// 停止中かどうか.
	/// </summary>
	/// <returns>停止中かどうか</returns>
	public bool IsPause()
	{
		return IsPauseFlag;
	}

	/// <summary>
	/// ポーズする.
	/// </summary>
	public void PauseEnable()
	{
		IsPauseFlag = true;
	}

	/// <summary>
	/// ポーズ解除.
	/// </summary>
	public void PauseDisable()
	{
		IsPauseFlag = false;
	}

	/// <summary>
	/// 初期化前処理.
	/// </summary>
	public bool _OnBeforeInit()
	{
		InitCalled = true;
		return OnBeforeInit();
	}

	/// <summary>
	/// 解放処理.
	/// </summary>
	virtual public void _OnRelease()
	{
		InitCalled = false;
		OnRelease();
	}

	/// <summary>
	/// 初期化済みかどうか.
	/// </summary>
	/// <returns>初期化済みかどうか</returns>
	public bool IsInitCalled()
	{
		return InitCalled;
	}

	/// <summary>
	/// 初期化前処理.
	/// </summary>
	virtual public bool OnBeforeInit()
	{
		return true;
	}
	
	/// <summary>
	/// 初期化更新処理.
	/// </summary>
	/// <param name="delta">経過時間</param>
	/// <returns>次の状態に進んでいいかどうかのBool値。trueだと、onAfterInitへ。</returns>
	virtual public bool OnUpdateInit(float delta)
	{
		return true;
	}
	
	/// <summary>
	/// 初期化後処理.
	/// </summary>
	virtual public bool OnAfterInit()
	{
		return true;
	}

	/// <summary>
	/// メイン前処理.
	/// </summary>
	virtual public bool OnBeforeMain()
	{
		return true;
	}
	
	/// <summary>
	/// メイン更新処理.
	/// </summary>
	/// <param name="delta">経過時間</param>
	virtual public void OnUpdateMain(float delta)
	{
	}
	
	/// <summary>
	/// メイン後処理.
	/// </summary>
	virtual public bool OnAfterMain()
	{
		return true;
	}

	/// <summary>
	/// 終了前処理.
	/// </summary>
	virtual public bool OnBeforeEnd()
	{
		return true;
	}
	
	/// <summary>
	/// 終了更新処理.
	/// </summary>
	/// <param name="delta">経過時間</param>
	/// <returns>次の状態に進んでいいかどうかのBool値。trueだと、onAfterEndへ。</returns>
	virtual public bool OnUpdateEnd(float delta)
	{
		return true;
	}
	
	/// <summary>
	/// 終了後処理.
	/// </summary>
	virtual public bool OnAfterEnd()
	{
		return true;
	}

	/// <summary>
	/// ステート解放時処理.
	/// </summary>
	virtual public void OnRelease()
	{
	}
}

