#define MyAppName "Fabits"
#define MyAppVersion "2.1.1"
#define MyAppPublisher "Deiloproxide"
#define MyAppURL "https://nahida520.love"
#define MyAppExeName "Fabits.exe"
[Setup]
;注意:AppId 的值唯一标识此应用程序。请勿在安装程序中对其他应用程序使用相同的 AppId 值。
;（若要生成新的 GUID，请单击“工具”|”在 IDE 中生成 GUID）。
AppId={{7C3C62AB-FDAD-4C9F-89E6-68FE66803B20}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExeName}
DisableWelcomePage=no
DisableReadypage=yes
;下行注释，指定安装程序无法运行，除 Arm 上的 x64 和 Windows 11 之外的任何平台上.
ArchitecturesAllowed=x64compatible
WizardImageFile=Icon\Side.bmp
;WizardSmallImageFile=顶图165x54.bmp,
WizardSmallImageFile=Icon\Na.bmp
;下行注释，强制安装程序在 64 位系统上，但不强制以 64 位模式运行.
ArchitecturesInstallIn64BitMode=x64compatible
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
LicenseFile=..\LICENSE.txt
;取消下行前面 ; 符号，在非管理安装模式下运行（仅为当前用户安装）.
;PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
OutputDir=..\FabitsSetup
OutputBaseFilename=Fabits Setup
SetupIconFile=Icon\Na.ico
SolidCompression=yes
WizardStyle=modern
[Languages]
Name: "chs"; MessagesFile: "compiler:Default.isl"
[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkablealone
[Files]
Source: "Fabits\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "Fabits\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
[code]
procedure InitializeWizard();
begin
WizardForm.LICENSEACCEPTEDRADIO.checked:= true;
end;
[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent