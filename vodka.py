import sys,os
try:
    file=sys.argv
    file=file[1] 
except:
    print("vodka.arg.error : File not found")
    sys.exit()
if not file.endswith(".vod"):
    print("vodka.filetype.error : File is not a .vod file")
    sys.exit()
if not os.path.exists(file):
    print("vodka.filenotfound.error : File don't exist")
    sys.exit()
fileline=open(file,"r").readlines()
try:
    start=None
    for i in range(len(fileline)):
        if fileline[i].startswith("VODSTART"):
            start=i
        if start==None and i==len(fileline)-1:
            print("""vodka.filestart.error : File must start by "VODSTART\"""")
            sys.exit()
except IndexError:
    print("vodka.fileempty.error : File must have at least two lines")
    sys.exit()
try:
    end=None
    for i in range(len(fileline)):
        if fileline[i].startswith("VODEND"):
            end=i
        if end==None and i==len(fileline)-1:
            print("""vodka.fileend.error : File must end by "VODEND\"""")
            sys.exit()
except IndexError:
    print("vodka.fileempty.error : File must have at least two lines")
    sys.exit()
for i in range(len(fileline)):
    fileline[i]=fileline[i].rstrip("\n")
code=[]
for i in range(start+1,end):
    code.append(fileline[i])
data={}
for i in range(len(code)):
    if code[i].startswith("vodka"):
        line=code[i].split()
        if len(line)==5 and line[3]=="vodkint":
            if not line[1] in data:
                try:
                    if len(line[4])>4300:
                        print("vodka.maxintlimit.error : Value has too many digits")
                        sys.exit()
                    int(line[4])
                    data[line[1]]=["vodkint",line[4]]
                except:
                    if len(line[4])>4300:
                        print("vodka.maxintlimit.error : Value has too many digits")
                        sys.exit()
                    print("vodka.notint.error : Value is not a int")
                    sys.exit()
            else:
                try:
                    if len(line[4])>4300:
                        print("vodka.maxintlimit.error : Value has too many digits")
                        sys.exit()
                    int(line[4])
                    data[line[1]]=["vodkint",line[4]]
                except:
                    if len(line[4])>4300:
                        print("vodka.maxintlimit.error : Value has too many digits")
                        sys.exit()
                    print("vodka.notint.error : Value is not a int")
                    sys.exit()
        else:
            print("vodka.syntax.error : Syntax not correct")
            sys.exit()
    elif code[i].startswith("vodimp"):
        line=code[i].split()
        if line[1]=="vodkint":
            startt=len(line[2])+16
            importt=code[i][startt::]
            if not os.path.exists(importt):
                print("vodka.filenotfound.error : File doesn't exist")
                sys.exit()
            if not importt.endswith(".txt"):
                print("vodka.filetype.error : File isn't a .txt file")
                sys.exit()
            text=open(importt,"r").readlines()
            try:
                text=text[0]
            except IndexError:
                print("vodka.firstlineempty.error : First line of the file is empty.")
                sys.exit()
            try:
                text=text.rstrip("\n")
            except:
                pass
            try:
                if len(text)>4300:
                    print("vodka.maxintlimit.error : Value has too many digits.")
                    sys.exit()
                int(text)
                data[line[2]]=["vodkint",text]
            except ValueError:
                if len(text)>4300:
                    print("vodka.maxintlimit.error : Value has too many digits")
                    sys.exit()
                print("vodka.notint.error : Value is not a int.")
                sys.exit()
        else:
            print("vodka.syntax.error : Syntax not correct.")
            sys.exit()
    elif code[i].startswith("vodprint"):
        line=code[i].split()
        if len(line)==2:
            try:
                if data[line[1]][0]=="vodkint":
                    print(data[line[1]][1])
            except KeyError:
                print("vodka.notdefined.error : \""+line[1]+"\" is not defined.")
                sys.exit()
        elif len(line)==1:
            print("vodka.syntax.error : Can't find any variable to print.")
            sys.exit()
        else:
            print("vodka.syntax.error : Can't print several variables at once.")
            sys.exit()
    elif code[i].startswith("vodexp"):
        line=code[i].split()
        if len(line)>2:
            if line[1] in data:
                startt=len(line[1])+8
                exportt=code[i][startt::]
                if not os.path.exists(exportt):
                    print("vodka.filenotvalid.error : File doesn't exists.")
                    sys.exit()
                if not exportt.endswith(".txt"):
                    print("vodka.filetype.error : File isn't a .txt file")
                    sys.exit()
                if data[line[1]][0]=="vodkint":
                    try:
                        open(exportt,"w").write(str(data[line[1]][1]))
                    except:
                        print("vodka.unknow.error : An unknow error happen. Please verify the file exists before retry.")
                        sys.exit()
            else:
                print("vodka.notdefined.error : \""+line[1]+"\" is not defined.")
                sys.exit()
        else:
            print("vodka.syntax.error : Syntax not correct.")
            sys.exit()
    elif code[i]=="vodabout":
        print("Vodka v0.1.3")
    else:
        if not code[i]=="":
            print("vodka.syntax.error : '"+code[i]+"' is not a function.")
            sys.exit()