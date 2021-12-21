■MaterDataManager用ソースコードジェネレータの資料

▼更新履歴
○2016/08/05　Fizz株式会社　山下	初版
○2016/08/10　Fizz株式会社　山下	FlatBuffersを使用した方式に変更に伴い、FlatBuffers説明の項追加、MAC対応
○2016/08/17　Fizz株式会社　山下	文章をひとまとめのブロックとして扱う為の設定方法追加
○2016/09/20　Fizz株式会社　山下	配列設定追加。intとstringのみ対応

▼資料の概要
・この資料を読めば、MaterDataManagerの使い方、作り、思想が理解できるようになります

▼MaterDataManagerとは
・row/column形式(行ごとにカンマ区切りで設定されているデータ)の
　CSV形式で出力された「マスターデータ」を、プログラム上で扱う時に、扱いやすく
　する為の手助けをしてくれる物の総称です。

・マスターデータCSVにメタデータを記載して、そのメタデータを解析して、アクセス
マネージャクラスを自動生成する、という設計思想の基、実装されています

▼設計思想
CSVに設定した物を読み込んで、アクセスしてデータを取り出す機構は、以下の特徴を
持つことが多いです。
・大抵似たような構造になる
・変更/更新が頻繁に発生する

その為、これらにアクセスするマネージャクラスは、メタデータを作成して、そのメタ
データからソースコードを自動でコンバートさせるのが望ましいと思い現在の形になっ
ています。

▼FlatBuffersとは
・Googleが提供してくれている、高速なシリアライザー
・http://google.github.io/flatbuffers/index.html
・http://qiita.com/y_miyoshi/items/873ae853509f8cd59f0b

▼構成
・masterdata_generator_for_flatbuffers.py
	⇒マスターデータに記載されているメタデータから、以下の物を生成するPythonスクリプト
		・アクセスする為のマネージャクラス群
		・FlatBuffersを扱う定義ファイル

		これを実行すると
		・fbs_files\*.fbs
		・Assets\Scripts\MasterData\*Manager.cs
		が生成されます。

	※動作環境
		・Python2.n系
		・Windowsでのみ確認。ただ、Macでも動くと思います

・flatc.exe
	⇒FlatBuffersを使用する為のソースコードを作成してくれる実行ファイル

・create_masterdata_from_csvdata.bat
	⇒masterdata_generator_for_flatbuffers.pyの実行と、それにより生成されたfbsファイルに対して
	　flatc.exeを実行してソースコードを生成し、
	　それらを適切なディレクトリに移動させるまでの手順をひとまとめにしたバッチファイル。

・create_masterdata_from_csvdata
	⇒create_masterdata_from_csvdata.batのMACで動かすためのシェルスクリプト版

・fbs_filse
	⇒masterdata_generator_for_flatbuffers.pyによって生成された、FlatBuffersのスキーマファイル(*.fbs)を格納しておくディレクトリ

▼マスターデータの形式
※[n]は、説明する為のタグなので、実際のマスターデータに記載する必要はありません
[1]EnumTestdata
[2]id,name,pos_x,pos_y,flag,number_enum,hp,second_enum
[3]int,string,float,float,bool,enum:enum_test_access_class.enum_test:zero/one/two,int,enum:enum_test_access_class.secon
_enum:first/second/third/force,list:int
[4]10000,name1,100,200,TRUE,Zero,1000,Third,0/1/2
[5]10001,name2,150,300,FALSE,One,200,Second,11/12/13/14
[6]10002,name3,200,400,TRUE,Two,500,Second,15


○基本ルール
・[1][2][3]が、マスターデータ出力に関係する、「メタデータ」を記載する行です
・[4]以降は、マスターデータ設定の実際の内容です
・「メタデータ」の記述ルールは、基本的に以下になります
	・小文字で記載
	・文字の区切りは、"_"で区切る
	・コンバート例「enemy_max_hp　⇒　enemyMaxHp」
	・enumの記述に関してだけ、特別ルールがあります
		・enum:クラス名.enum名:enumパラメータ1/enumパラメータ2/enumパラメータ3
			⇒これを、ソースコードで表すと
				public enum enum名 {
					enumパラメータ1,
					enumパラメータ2,
					enumパラメータ3
				}

		・クラス名ですが、FlatBuffers使用に伴い不必要なパラメータになっているので、適当な文字列を入れてください

	・listの記述に関してだけ、特別ルールがあります
		・list:型名
			⇒型名の配列でデータを保持してくれるようになります

・一番最初の要素が、プログラム上でデータを取得する際のキーになります。いわゆ
る、Dictionary型のKeyに該当する物です。

○説明
・[1]　	⇒　クラス名です
・[2]	⇒	アクセスする際の、マスターデータ上の変数名です
・[3]	⇒	アクセスする際の、マスターデータ上の変数の型名です
・[4～]	⇒	マスターデータの設定内容です
	※stringのデータを設定する際に、{}で囲うと、文章中の「,」を文章の一部と認識するようになります

▼作業フロー
1．マスターデータCSVを生成し、Assets\Resources\MasterDataに格納する。
2．Tools\MasterData2AccessManagerの階層まで移動し、create_masterdata_from_csvdata.bat を
実行する
MACの場合は、sh create_masterdata_from_csvdata を実行する
3．Assets\Scripts\MasterDataに、～Manager.csとFlatBuffersの各種定義ファイルが生成される
4．UnityEditorを起動して、エラーが出ていないか確認

▼マネージャクラスの使い方
// csv読み込み。ここは、リソースマネージャが行う所。そこから、CSVのTextを取得する
TextAsset tAsset = Resources.Load("testdata") as TextAsset;
TestdataManager.Instance.Initialize(tAsset.text);
Testdata data = TestdataManager.Instance.GetData(10000);

▼今後手を入れると思われる箇所
・Pythonコードの整理
・コーディング規約に則した記述に修正
・マネージャクラスの破棄関数対応
・ソースコード関連は使っているうちに整備が必要にあると思われるので、その都度対応

