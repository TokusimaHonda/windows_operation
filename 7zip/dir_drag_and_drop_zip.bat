echo off
pushd %~dp0
rem 7zipのパス
set Path_7zip=.\7za.exe

if exist %Path_7zip% (
echo ドラッグアンドドロップされたフォルダを圧縮します。
for %%f in (%*) do (
rem フォルダ圧縮 
%Path_7zip% a -ssw -tzip %%f.zip %%f\*
)
pause
)

