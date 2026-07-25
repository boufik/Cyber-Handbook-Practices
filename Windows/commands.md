# 1. PC Score
```powershell
WMIobject Win32_WinSAT
```
Output:
```powershell
__GENUS               : 2
__CLASS               : Win32_WinSAT
__SUPERCLASS          :
__DYNASTY             : Win32_WinSAT
__RELPATH             : Win32_WinSAT.TimeTaken="MostRecentAssessment"
__PROPERTY_COUNT      : 8
__DERIVATION          : {}
__SERVER              : <PC_NAME>
__NAMESPACE           : root\cimv2
__PATH                : \\<PC_NAME>\root\cimv2:Win32_WinSAT.TimeTaken="MostRecentAssessment"
CPUScore              : 9,1
D3DScore              : 9,9
DiskScore             : 9,05
GraphicsScore         : 8,1
MemoryScore           : 9,1
TimeTaken             : MostRecentAssessment
WinSATAssessmentState : 1
WinSPRLevel           : 8,1
PSComputerName        : <PC_NAME>
```