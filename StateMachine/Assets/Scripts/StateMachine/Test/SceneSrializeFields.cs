using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class SceneSrializeFields : MonoBehaviour
{
	[SerializeField]
    private GameObject RootObject = null;
    public GameObject SFRootObject => RootObject;
}
