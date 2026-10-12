' ============================================================================
'  CHAY TOOL TRICH XUAT LOI BAI HAT - CHE DO AN
'
'  Nhap dup vao file nay de bat tool ma KHONG hien cua so den.
'  Tool chay ngam o duoi, trinh duyet tu mo trang lam viec.
'
'  Muon tat tool: bam nut "Tat tool" o cuoi trang web.
'  (File nay co chu y viet khong dau de Windows doc chac chan dung.)
' ============================================================================

Option Explicit

Dim shell, fso, goc, pythonw, appPy, lenh

Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Thu muc goc = thu muc dang chua file .vbs nay
goc = fso.GetParentFolderName(WScript.ScriptFullName)
appPy = goc & "\yt_lyrics\app.py"

' Python ban khong cua so (pythonw) - khac python.exe o cho khong hien console
pythonw = "C:\Users\nguye\.workbuddy-ai\binaries\python\envs\default\Scripts\pythonw.exe"

If Not fso.FileExists(appPy) Then
    MsgBox "Khong tim thay thu muc yt_lyrics." & vbCrLf & vbCrLf & _
           "Duong dan dang mo:" & vbCrLf & goc, 16, "Tool trich xuat loi bai hat"
    WScript.Quit 1
End If

If Not fso.FileExists(pythonw) Then
    MsgBox            "Khong tim thay Python o duong dan:" & vbCrLf & pythonw & vbCrLf & vbCrLf & _
           "Nho Tro ly kiem tra lai.", 16, "Tool trich xuat loi bai hat"
    WScript.Quit 1
End If

' Dat thu muc lam viec dung cho tool (de tim thay templates, .env...)
shell.CurrentDirectory = goc & "\yt_lyrics"

' 0 = chay hoan toan an | False = khong cho doi, tra ve ngay
lenh = """" & pythonw & """ """ & appPy & """"
shell.Run lenh, 0, False
