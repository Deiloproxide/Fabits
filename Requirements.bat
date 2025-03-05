@echo off
pip install chardet numpy pillow requests
reg add "HKCR\.nda" /f
reg add "HKCR\.nda" /ve /d NahidaDataAssets /f
reg add "HKCR\NahidaDataAssets" /f
reg add "HKCR\NahidaDataAssets" /ve /d "Nahida Data Assets - 纳西妲资源库" /f
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.nda" /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.nda" /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.nda\OpenWithList" /f
pause