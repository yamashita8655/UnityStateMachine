python masterdata_generator_for_flatbuffers.py

for /f %%a in ('dir /b fbs_files\*.fbs') do (
flatc.exe -n fbs_files\%%a
)

for /f %%a in ('dir /b MasterData\*.cs') do (
copy MasterData\%%a ..\..\Assets\Scripts\MasterData\
)

rmdir /s /q MasterData

pause
