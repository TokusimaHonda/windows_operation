echo off
pushd %~dp0
rem 7zip�̃p�X
set Path_7zip=.\7za.exe

if exist %Path_7zip% (
echo �h���b�O�A���h�h���b�v���ꂽ�t�H���_�����k���܂��B
for %%f in (%*) do (
rem �t�H���_���k 
%Path_7zip% a -ssw -tzip %%f.zip %%f\*
)
pause
)

