using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BaseStateMachineSampleScene : MonoBehaviour {

	[SerializeField]
    private SceneSrializeFields CuSF = null;
    public SceneSrializeFields SF => CuSF;

	// Use this for initialization
	void Start () {
        StateMachineManager.Instance.Init();
        StateMachineManager.Instance.CreateStateMachineMap(StateMachineName.Test);
        StateMachineManager.Instance.AddState(StateMachineName.Test, 0, new TestState1Base());
        StateMachineManager.Instance.AddState(StateMachineName.Test, 1, new TestState2());
        StateMachineManager.Instance.ChangeState(StateMachineName.Test, 0);
	}
	
	// Update is called once per frame
	void Update () {
        StateMachineManager.Instance.Update(StateMachineName.Test, Time.deltaTime);
	}
}
