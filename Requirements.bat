@echo off
chcp 65001
echo 本地需求:
pip install chardet
pip install numpy
pip install pillow
pip install requests
echo 服务器需求(如果需要的话):
pip install flask
echo 添加.nda文件格式说明
reg add "HKCR\.nda" /f
reg add "HKCR\.nda" /ve /d NahidaDataAssets /f
reg add "HKCR\NahidaDataAssets" /f
reg add "HKCR\NahidaDataAssets" /ve /d "Nahida Data Assets - 纳西妲资源库" /f
reg add "HKCR\NahidaDataAssets" /v FriendlyTypeName /d "Nahida Data Assets - 纳西妲资源库" /f
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.nda" /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.nda" /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.nda\OpenWithList" /f
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\FileExts\.nda\OpenWithProgids" /f
echo 请按任意键继续
pause