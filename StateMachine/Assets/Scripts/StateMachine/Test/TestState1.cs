using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TestState1 : StateBase {

    /// <summary>
    /// 初期化前処理.
    /// </summary>
    override public void OnBeforeInit()
    {
        Debug.Log("TestState1 OnBeforeInit");
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
    override public void OnAfterInit()
    {
        Debug.Log("TestState1 OnAfterInit");
    }

    /// <summary>
    /// メイン前処理.
    /// </summary>
    override public void OnBeforeMain()
    {
        Debug.Log("TestState1 OnBeforeMain");
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
    override public void OnAfterMain()
    {
        Debug.Log("TestState1 OnAfterMain");
    }

    /// <summary>
    /// 終了前処理.
    /// </summary>
    override public void OnBeforeEnd()
    {
        Debug.Log("TestState1 OnBeforeEnd");
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
    override public void OnAfterEnd()
    {
        Debug.Log("TestState1 OnAfterEnd");
    }

    /// <summary>
    /// ステート解放時処理.
    /// </summary>
    override public void OnRelease()
    {
        Debug.Log("TestState1 OnRelease");
    }
}
