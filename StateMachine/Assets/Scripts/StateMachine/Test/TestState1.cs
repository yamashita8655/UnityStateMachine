using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TestState1 : StateBase {

    /// <summary>
    /// 初期化前処理.
    /// </summary>
    override public bool OnBeforeInit()
    {
        Debug.Log("TestState1 OnBeforeInit");
		return true;
    }
    /// <summary>
    /// 初期化更新処理.
    /// </summary>
    /// <param name="delta">経過時間</param>
    /// <returns>次の状態に進んでいいかどうかのBool値。trueだと、onAfterInitへ。</returns>
    override public bool OnUpdateInit(float delta)
    {
        Debug.Log("TestState1 OnUpdateInit");
        return true;
    }
    /// <summary>
    /// 初期化後処理.
    /// </summary>
    override public bool OnAfterInit()
    {
        Debug.Log("TestState1 OnAfterInit");
		return true;
    }

    /// <summary>
    /// メイン前処理.
    /// </summary>
    override public bool OnBeforeMain()
    {
        Debug.Log("TestState1 OnBeforeMain");
		return true;
    }

    /// <summary>
    /// メイン更新処理.
    /// </summary>
    /// <param name="delta">経過時間</param>
    override public void OnUpdateMain(float delta)
    {
        StateMachineManager.Instance.ChangeState(StateMachineName.Test, 1);
        Debug.Log("TestState1 OnUpdateMain");
    }

    /// <summary>
    /// メイン後処理.
    /// </summary>
    override public bool OnAfterMain()
    {
        Debug.Log("TestState1 OnAfterMain");
		return true;
    }

    /// <summary>
    /// 終了前処理.
    /// </summary>
    override public bool OnBeforeEnd()
    {
        Debug.Log("TestState1 OnBeforeEnd");
		return true;
    }

    /// <summary>
    /// 終了更新処理.
    /// </summary>
    /// <param name="delta">経過時間</param>
    /// <returns>次の状態に進んでいいかどうかのBool値。trueだと、onAfterEndへ。</returns>
    override public bool OnUpdateEnd(float delta)
    {
        Debug.Log("TestState1 OnUpdateEnd");
        return true;
    }

    /// <summary>
    /// 終了後処理.
    /// </summary>
    override public bool OnAfterEnd()
    {
        Debug.Log("TestState1 OnAfterEnd");
		return true;
    }

    /// <summary>
    /// ステート解放時処理.
    /// </summary>
    override public void OnRelease()
    {
        Debug.Log("TestState1 OnRelease");
    }
}
