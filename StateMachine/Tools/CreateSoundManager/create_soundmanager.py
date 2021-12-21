# coding: utf-8
#設計
#

import os
import sys
def CreateSoundEnum():
    s = "// このファイルは、Tools/CreateSoundManager/create_soundmanager.pyによって自動生成されるため、\n"
    s += "// 直接の編集は禁止です。\n"
    s += "using System.Collections;\n"
    s += "using System.Collections.Generic;\n"
    s += "using UnityEngine;\n"
    s += "\n"
    s += "// partialにしている理由は、このクラスは自動生成されるため、直接編集されるクラスとファイルを分割したかった\n"
    s += "public partial class EnumSelf : MonoBehaviour {\n"
    
    # BGM
    s += "	public enum eBgm {\n"
    path='..\..\Assets\Resources\Sound\BGM'
    rootList = os.listdir(path)
    soundDir = [f for f in rootList if os.path.isdir(os.path.join(path, f))]
    isFirst = True
    for i in range(len(soundDir)):
        print(soundDir[i])
        soundPath = path + "\\" + soundDir[i]
        dataList = os.listdir(soundPath)
        soundFiles = [f for f in dataList if os.path.isfile(os.path.join(soundPath, f))]
        soundFiles = [f for f in soundFiles if f.endswith('.meta') == False]
        for i2 in range(len(soundFiles)):
            print(soundFiles[i2])
            if isFirst == True:
                s += "		" +  soundDir[i] + "_" + os.path.splitext(soundFiles[i2])[0] + " = 0,\n"
                isFirst = False
            else:
                s += "		" +  soundDir[i] + "_" + os.path.splitext(soundFiles[i2])[0] + ",\n"
    s += "		Max,\n"
    s += "		None\n"
    s += "	};\n"
    s += "	\n"

    # SE
    s += "	public enum eSe {\n"
    path='..\..\Assets\Resources\Sound\SE'
    rootList = os.listdir(path)
    soundDir = [f for f in rootList if os.path.isdir(os.path.join(path, f))]
    isFirst = True
    for i in range(len(soundDir)):
        print(soundDir[i])
        soundPath = path + "\\" + soundDir[i]
        dataList = os.listdir(soundPath)
        soundFiles = [f for f in dataList if os.path.isfile(os.path.join(soundPath, f))]
        soundFiles = [f for f in soundFiles if f.endswith('.meta') == False]
        for i2 in range(len(soundFiles)):
            print(soundFiles[i2])
            if isFirst == True:
                s += "		" +  soundDir[i] + "_" + os.path.splitext(soundFiles[i2])[0] + " = 0,\n"
                isFirst = False
            else:
                s += "		" +  soundDir[i] + "_" + os.path.splitext(soundFiles[i2])[0] + ",\n"
    s += "		Max,\n"
    s += "	};\n"
    s += "}\n"

    print(s)

    savePathAndName = '../../Assets/Scripts/Utility/SoundEnum.cs'
    of = open(savePathAndName, 'wb') # 書き込みモードで開く
    of.write(s.encode('utf-8')) # 引数の文字列をファイルに書き込む
    of.close() # ファイルを閉じる

def CreateSoundManager():
    s = "// このファイルは、Tools/CreateSoundManager/create_soundmanager.pyによって自動生成されるため、\n"
    s += "// 直接の編集は禁止です。\n"
    s += "using System;\n"
    s += "using System.Collections;\n"
    s += "using System.Collections.Generic;\n"
    s += "using UnityEngine;\n"
    s += "using UnityEngine.Audio;\n"
    s += "\n"
    s += "public class SoundManager : SimpleMonoBehaviourSingleton<SoundManager> {\n"
    s += "	\n"
    s += "	private List<AudioSource> BgmAudioSources = null;\n"
    s += "	private List<AudioSource> SeAudioSources = null;\n"
    s += "	private List<AudioClip> BgmAudioClipList = null;\n"
    s += "	private List<AudioClip> SeAudioClipList = null;\n"
    s += "\n"
    s += "	private List<AudioMixerSnapshot> AudioMixerSnapshot_BgmCrossFade = null;\n"
    s += "	\n"
    s += "	// とりあえず、一個しか使わないのであれば、これ使っておけば良いと思われ\n"
    s += "	private AudioMixer SoundAudioMixer = null;\n"
    s += "\n"
    s += "	private EnumSelf.eBgm CurrentBgm = EnumSelf.eBgm.None;\n"
    s += "	private int BgmAudioUseIndex = 0;\n"
    s += "\n"
    s += "	private int SeAudioUseIndex = 0;\n"
    s += "\n"
    s += "	private int LoadCount = 0; \n"
    s += "	private int LoadedCount = 0; \n"
    s += "\n"
    s += "	// TODO 現状は、最初に全てのBGM/SEをキャッシュしているが、\n"
    s += "	// 処理が重くなったら、都度読み込みなど、読み込む量を調整する\n"
    s += "	public IEnumerator CoInitialize() {\n"
    s += "		BgmAudioSources = new List<AudioSource>();\n"
    s += "		for (int i = 0; i < 2; i++) {\n"
    s += "			BgmAudioSources.Add(null);\n"
    s += "		}\n"
    s += "\n"
    s += "		LoadCount = 0;\n"
    s += "		LoadedCount = 0;\n"
    s += "\n"
    s += "		LoadCount++;\n"
    s += "		ResourceManager.Instance.RequestExecuteOrder(\n"
    s += "			\"Prefab/Sound/BgmAudioSource1\",\n"
    s += "			ExecuteOrder.Type.GameObject,\n"
    s += "			this.gameObject,\n"
    s += "			(audioSource) => {\n"
    s += "				GameObject obj = GameObject.Instantiate(audioSource) as GameObject;\n"
    s += "				obj.transform.SetParent(this.gameObject.transform);\n"
    s += "			\n"
    s += "				BgmAudioSources[0] = obj.GetComponent<AudioSource>();\n"
    s += "				LoadedCount++;\n"
    s += "			}\n"
    s += "		);\n"
    s += "		\n"
    s += "		LoadCount++;\n"
    s += "		ResourceManager.Instance.RequestExecuteOrder(\n"
    s += "			\"Prefab/Sound/BgmAudioSource2\",\n"
    s += "			ExecuteOrder.Type.GameObject,\n"
    s += "			this.gameObject,\n"
    s += "			(audioSource) => {\n"
    s += "				GameObject obj = GameObject.Instantiate(audioSource) as GameObject;\n"
    s += "				obj.transform.SetParent(this.gameObject.transform);\n"
    s += "			\n"
    s += "				BgmAudioSources[1] = obj.GetComponent<AudioSource>();\n"
    s += "				LoadedCount++;\n"
    s += "			}\n"
    s += "		);\n"
    s += "		\n"
    s += "		SeAudioSources = new List<AudioSource>();\n"
    s += "		for (int i = 0; i < 4; i++) {\n"
    s += "			SeAudioSources.Add(null);\n"
    s += "		}\n"
    s += "		\n"
    s += "		LoadCount++;\n"
    s += "		ResourceManager.Instance.RequestExecuteOrder(\n"
    s += "			\"Prefab/Sound/SeAudioSource1\",\n"
    s += "			ExecuteOrder.Type.GameObject,\n"
    s += "			this.gameObject,\n"
    s += "			(audioSource) => {\n"
    s += "				GameObject obj = GameObject.Instantiate(audioSource) as GameObject;\n"
    s += "				obj.transform.SetParent(this.gameObject.transform);\n"
    s += "			\n"
    s += "				SeAudioSources[0] = obj.GetComponent<AudioSource>();\n"
    s += "				LoadedCount++;\n"
    s += "			}\n"
    s += "		);\n"
    s += "		\n"
    s += "		LoadCount++;\n"
    s += "		ResourceManager.Instance.RequestExecuteOrder(\n"
    s += "			\"Prefab/Sound/SeAudioSource2\",\n"
    s += "			ExecuteOrder.Type.GameObject,\n"
    s += "			this.gameObject,\n"
    s += "			(audioSource) => {\n"
    s += "				GameObject obj = GameObject.Instantiate(audioSource) as GameObject;\n"
    s += "				obj.transform.SetParent(this.gameObject.transform);\n"
    s += "			\n"
    s += "				SeAudioSources[1] = obj.GetComponent<AudioSource>();\n"
    s += "				LoadedCount++;\n"
    s += "			}\n"
    s += "		);\n"
    s += "		\n"
    s += "		LoadCount++;\n"
    s += "		ResourceManager.Instance.RequestExecuteOrder(\n"
    s += "			\"Prefab/Sound/SeAudioSource3\",\n"
    s += "			ExecuteOrder.Type.GameObject,\n"
    s += "			this.gameObject,\n"
    s += "			(audioSource) => {\n"
    s += "				GameObject obj = GameObject.Instantiate(audioSource) as GameObject;\n"
    s += "				obj.transform.SetParent(this.gameObject.transform);\n"
    s += "			\n"
    s += "				SeAudioSources[2] = obj.GetComponent<AudioSource>();\n"
    s += "				LoadedCount++;\n"
    s += "			}\n"
    s += "		);\n"
    s += "		\n"
    s += "		LoadCount++;\n"
    s += "		ResourceManager.Instance.RequestExecuteOrder(\n"
    s += "			\"Prefab/Sound/SeAudioSource4\",\n"
    s += "			ExecuteOrder.Type.GameObject,\n"
    s += "			this.gameObject,\n"
    s += "			(audioSource) => {\n"
    s += "				GameObject obj = GameObject.Instantiate(audioSource) as GameObject;\n"
    s += "				obj.transform.SetParent(this.gameObject.transform);\n"
    s += "			\n"
    s += "				SeAudioSources[3] = obj.GetComponent<AudioSource>();\n"
    s += "				LoadedCount++;\n"
    s += "			}\n"
    s += "		);\n"
    s += "\n"
    s += "        BgmAudioClipList = new List<AudioClip>();\n"
    s += "        for (int i = 0; i < (int)EnumSelf.eBgm.Max; i++) {\n"
    s += "			BgmAudioClipList.Add(null);\n"
    s += "		}\n"
    s += "\n"
    s += "		// これは、EnumSelf.Bgmの並びと揃える\n"
    s += "		List<string> bgmList = new List<string>() {\n"

    path='..\..\Assets\Resources\Sound\BGM'
    rootList = os.listdir(path)
    soundDir = [f for f in rootList if os.path.isdir(os.path.join(path, f))]
    isFirst = True
    for i in range(len(soundDir)):
        print(soundDir[i])
        soundPath = path + "\\" + soundDir[i]
        dataList = os.listdir(soundPath)
        soundFiles = [f for f in dataList if os.path.isfile(os.path.join(soundPath, f))]
        soundFiles = [f for f in soundFiles if f.endswith('.meta') == False]
        for i2 in range(len(soundFiles)):
            if isFirst == True:
                s += "			\"Sound/BGM/" + soundDir[i] + "/" + os.path.splitext(soundFiles[i2])[0] + "\""
                isFirst = False
            else:
                s += ",\n"
                s += "			\"Sound/BGM/" + soundDir[i] + "/" + os.path.splitext(soundFiles[i2])[0] + "\""
    
    
    s += "\n"
    s += "		};\n"
    s += "		\n"
    s += "		for (int i = 0; i < bgmList.Count; i++) {\n"
    s += "			LoadCount++;\n"
    s += "			int index = i;\n"
    s += "			ResourceManager.Instance.RequestExecuteOrder(\n"
    s += "				bgmList[index],\n"
    s += "				ExecuteOrder.Type.AudioClip,\n"
    s += "				this.gameObject,\n"
    s += "				(audioClip) => {\n"
    s += "					BgmAudioClipList[index] = audioClip as AudioClip;\n"
    s += "					LoadedCount++;\n"
    s += "				}\n"
    s += "			);\n"
    s += "		}\n"
    s += "\n"
    s += "        SeAudioClipList = new List<AudioClip>();\n"
    s += "        for (int i = 0; i < (int)EnumSelf.eSe.Max; i++) {\n"
    s += "			SeAudioClipList.Add(null);\n"
    s += "		}\n"
    s += "		\n"
    s += "		// これは、EnumSelf.Seの並びと揃える\n"
    s += "		List<string> seList = new List<string>() {\n"
    
    path='..\..\Assets\Resources\Sound\SE'
    rootList = os.listdir(path)
    soundDir = [f for f in rootList if os.path.isdir(os.path.join(path, f))]
    isFirst = True
    for i in range(len(soundDir)):
        print(soundDir[i])
        soundPath = path + "\\" + soundDir[i]
        dataList = os.listdir(soundPath)
        soundFiles = [f for f in dataList if os.path.isfile(os.path.join(soundPath, f))]
        soundFiles = [f for f in soundFiles if f.endswith('.meta') == False]
        for i2 in range(len(soundFiles)):
            print(soundFiles[i2])
            if isFirst == True:
                s += "			\"Sound/SE/" + soundDir[i] + "/" + os.path.splitext(soundFiles[i2])[0] + "\""
                isFirst = False
            else:
                s += ",\n"
                s += "			\"Sound/SE/" + soundDir[i] + "/" + os.path.splitext(soundFiles[i2])[0] + "\""
    
    s += "\n"
    s += "		};\n"
    s += "		\n"
    s += "		for (int i = 0; i < seList.Count; i++) {\n"
    s += "			LoadCount++;\n"
    s += "			int index = i;\n"
    s += "			ResourceManager.Instance.RequestExecuteOrder(\n"
    s += "				seList[index],\n"
    s += "				ExecuteOrder.Type.AudioClip,\n"
    s += "				this.gameObject,\n"
    s += "				(audioClip) => {\n"
    s += "					SeAudioClipList[index] = audioClip as AudioClip;\n"
    s += "					LoadedCount++;\n"
    s += "				}\n"
    s += "			);\n"
    s += "		}\n"
    s += "\n"
    s += "        AudioMixerSnapshot_BgmCrossFade = new List<AudioMixerSnapshot>();\n"
    s += "        for (int i = 0; i < 2; i++) {\n"
    s += "            AudioMixerSnapshot_BgmCrossFade.Add(null);\n"
    s += "        }\n"
    s += "\n"
    s += "		LoadCount++;\n"
    s += "        ResourceManager.Instance.RequestExecuteOrder(\n"
    s += "			\"Sound/AudioMixer\",\n"
    s += "			ExecuteOrder.Type.AudioMixer,\n"
    s += "			this.gameObject,\n"
    s += "			(audioMixer) => {\n"
    s += "				SoundAudioMixer = audioMixer as AudioMixer;\n"
    s += "                AudioMixerSnapshot_BgmCrossFade[0] = SoundAudioMixer.FindSnapshot(\"SnapshotBgm1\");\n"
    s += "                AudioMixerSnapshot_BgmCrossFade[1] = SoundAudioMixer.FindSnapshot(\"SnapshotBgm2\");\n"
    s += "				LoadedCount++;\n"
    s += "            }\n"
    s += "        );\n"
    s += "\n"
    s += "		CurrentBgm = EnumSelf.eBgm.None;\n"
    s += "		BgmAudioUseIndex = 0;\n"
    s += "		SeAudioUseIndex = 0;\n"
    s += "\n"
    s += "		while (LoadedCount < LoadCount) {\n"
    s += "			yield return null;\n"
    s += "		}\n"
    s += "	}\n"
    s += "\n"
    s += "	public void PlayBgm(EnumSelf.eBgm bgm, float fadeTime = 0f) {\n"
    s += "		if (bgm == CurrentBgm) {\n"
    s += "			return;\n"
    s += "		}\n"
    s += "\n"
    s += "		int currentIndex = BgmAudioUseIndex;\n"
    s += "		BgmAudioUseIndex++;\n"
    s += "		if (BgmAudioUseIndex >= BgmAudioSources.Count) {\n"
    s += "			BgmAudioUseIndex = 0;\n"
    s += "		}\n"
    s += "		int nextIndex = BgmAudioUseIndex;\n"
    s += "\n"
    s += "		AudioSource source = GetBgmAudioSource(nextIndex);\n"
    s += "		source.clip = BgmAudioClipList[(int)bgm];\n"
    s += "		source.Play();\n"
    s += "		source.loop = true;\n"
    s += "		CurrentBgm = bgm;\n"
    s += "		\n"
    s += "		float[] weights;\n"
    s += "		if (BgmAudioUseIndex == 0) {\n"
    s += "			weights = new float[2] { 1.0f, 0.0f };\n"
    s += "		} else {\n"
    s += "			weights = new float[2] { 0.0f, 1.0f };\n"
    s += "		}\n"
    s += "		SoundAudioMixer.TransitionToSnapshots(AudioMixerSnapshot_BgmCrossFade.ToArray(), weights, fadeTime);\n"
    s += "	}\n"
    s += "	\n"
    s += "	public void StopBgm(float fadeTime = 0f) {\n"
    s += "		BgmAudioUseIndex++;\n"
    s += "		if (BgmAudioUseIndex >= BgmAudioSources.Count) {\n"
    s += "			BgmAudioUseIndex = 0;\n"
    s += "		}\n"
    s += "		int nextIndex = BgmAudioUseIndex;\n"
    s += "\n"
    s += "		AudioSource source = GetBgmAudioSource(nextIndex);\n"
    s += "		source.Stop();\n"
    s += "		CurrentBgm = EnumSelf.eBgm.None;\n"
    s += "		\n"
    s += "		float[] weights;\n"
    s += "		if (BgmAudioUseIndex == 0) {\n"
    s += "			weights = new float[2] { 1.0f, 0.0f };\n"
    s += "		} else {\n"
    s += "			weights = new float[2] { 0.0f, 1.0f };\n"
    s += "		}\n"
    s += "		SoundAudioMixer.TransitionToSnapshots(AudioMixerSnapshot_BgmCrossFade.ToArray(), weights, fadeTime);\n"
    s += "	}\n"
    s += "\n"
    s += "    public AudioSource GetBgmAudioSourceForCheck()\n"
    s += "    {\n"
    s += "        AudioSource source = BgmAudioSources[BgmAudioUseIndex];\n"
    s += "        return source;\n"
    s += "    }\n"
    s += "\n"
    s += "    private AudioSource GetBgmAudioSource(int sourceIndex) {\n"
    s += "		AudioSource source = BgmAudioSources[sourceIndex];\n"
    s += "		return source;\n"
    s += "	}\n"
    s += "	\n"
    s += "	private AudioSource GetSeAudioSource(int sourceIndex) {\n"
    s += "		AudioSource source = SeAudioSources[sourceIndex];\n"
    s += "		return source;\n"
    s += "	}\n"
    s += "\n"
    s += "	public void PlaySe(EnumSelf.eSe se) {\n"
    s += "		int currentIndex = SeAudioUseIndex;\n"
    s += "		SeAudioUseIndex++;\n"
    s += "		if (SeAudioUseIndex >= SeAudioSources.Count) {\n"
    s += "			SeAudioUseIndex = 0;\n"
    s += "		}\n"
    s += "		int nextIndex = SeAudioUseIndex;\n"
    s += "\n"
    s += "		AudioSource source = GetSeAudioSource(nextIndex);\n"
    s += "		source.clip = SeAudioClipList[(int)se];\n"
    s += "		source.Play();\n"
    s += "	}\n"
    s += "	public void SetSeMuteFlag(bool isMute) {\n"
    s += "		for (int i = 0; i < SeAudioSources.Count; i++) {\n"
    s += "			SeAudioSources[i].mute = isMute;\n"
    s += "		}\n"
    s += "	}\n"
    s += "	\n"
    s += "	public void SetBgmMuteFlag(bool isMute) {\n"
    s += "		for (int i = 0; i < BgmAudioSources.Count; i++) {\n"
    s += "			BgmAudioSources[i].mute = isMute;\n"
    s += "		}\n"
    s += "	}\n"
    s += "	\n"
    s += "	public void SetSeVolume(float volume) {\n"
    s += "		for (int i = 0; i < SeAudioSources.Count; i++) {\n"
    s += "			SeAudioSources[i].volume = volume;\n"
    s += "		}\n"
    s += "	}\n"
    s += "	\n"
    s += "	public void SetBgmVolume(float volume) {\n"
    s += "		for (int i = 0; i < BgmAudioSources.Count; i++) {\n"
    s += "			BgmAudioSources[i].volume = volume;\n"
    s += "		}\n"
    s += "	}\n"
    s += "}\n"

    savePathAndName = '../../Assets/Scripts/Manager/SoundManager.cs'

    isExist = os.path.isfile(savePathAndName)
    of = open(savePathAndName, 'wb') # 書き込みモードで開く
    of.write(s.encode('utf-8')) # 引数の文字列をファイルに書き込む
    of.close() # ファイルを閉じる


# まずは、ディレクトリ走査
CreateSoundEnum()
CreateSoundManager()
