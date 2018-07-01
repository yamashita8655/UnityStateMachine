using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TestState2 : StateBase {

    /// <summary>
    /// メイン更新処理.
    /// </summary>
    /// <param name="delta">経過時間</param>
    override public void OnUpdateMain(float delta)
    {
        Debug.Log("TestState2 OnUpdateMain");
    }

    /// <summary>
    /// ステート解放時処理.
    /// </summary>
    override public void OnRelease()
    {
        Debug.Log("TestState2 OnRelease");
    }
}
