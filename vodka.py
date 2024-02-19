import sys,os,subprocess,pickle
def fonction(path,linecall,line):
    funccontent=open(path,"r",encoding="utf-8").readlines()
    datafunc={}
    try:
        start=None
        for i in range(len(funccontent)):
            if funccontent[i].startswith("VODSTART"):
                start=i
                break
            if start==None and i==len(funccontent)-1:
                    print("""vodka.functionvodstart.error : Function must start by VODSTART""")
                    sys.exit()
    except IndexError:
        print("vodka.functionempty.error : Function must have at least two lines")
        sys.exit()
    try:
        end=None
        for i in range(len(funccontent)):
            if funccontent[i].startswith("VODEND"):
                end=i
            if end==None and i==len(funccontent)-1:
                print("""vodka.functionvodend.error : Function must end by VODEND""")
                sys.exit()
    except IndexError:
        print("vodka.functionempty.error : Function must have at least two lines")
        sys.exit()
    for i in range(len(funccontent)):
        funccontent[i]=funccontent[i].rstrip("\n")
    codefunc=[]
    for i in range(start+1,end):
        codefunc.append(funccontent[i])
    nbargument=len(funccontent[start].split())-1
    listargument=funccontent[start].split()
    listargument.remove("VODSTART")
    argstransmit=linecall
    for g in range(4):
        argstransmit.remove(argstransmit[0])
    if not len(argstransmit)==nbargument:
        print()
        ende(code[line-1],"vodka.argsnumber.error : The number of argument isn't the one expected ("+str(nbargument)+").")
    for g in range(nbargument):
        datafunc[listargument[g]]=data[argstransmit[g]]
    if not len(funccontent[end].split()) in [1,2]:
        print()
        ende(code[line-1],"vodka.returnnumber.error : You can only return 1 variable.")
    try:
        returnvar=funccontent[end].split()[1]
    except:
        returnvar=None
    funcwrite=open("temp.json","wb")
    pickle.dump(datafunc,funcwrite)
    funcwrite.close()
    out=subprocess.run('vodka '+path, shell = True, text = True, stdout = subprocess.PIPE, check = False).stdout
    out=out.rstrip("\n")
    toprint=out.split("\n")
    for i in range(len(toprint)):
        print(toprint[i])
    try:
        with open("temp.json","rb") as dicttrans:
            dataimp=pickle.load(dicttrans)
    except:
        print("vodka.errorinfunction.error : An error happened in the function")
        sys.exit()
    os.remove("temp.json")
    if not returnvar==None:
        return dataimp[returnvar]
    else:
        return None
try:
    files=sys.argv
    file=files[1]
    files.remove("vodka")
    files.remove(files[0])
    if "-noerror" in files:
        debug=0
    else:
        debug=1
except:
    print("vodka.arg.error : File not found")
    sys.exit()
if file.endswith(".vodf"):
    funcexe=1
else:
    funcexe=0
if not file.endswith(".vod") and not funcexe==1:
    print("vodka.filetype.error : File is not a .vod file")
    sys.exit()
if not os.path.exists(file):
    print("vodka.filenotfound.error : File doesn't exist")
    sys.exit()
fileline=open(file,"r",encoding="utf-8").readlines()
if not os.path.isabs(file) and os.path.exists(os.getcwd()+"/"+file):
    adressfile=os.getcwd()+"/"+file
else:
    adressfile=file
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
if debug==1:
    def ende(content,error):
        lineh=fileline.index(content)
        print("File \""+os.path.abspath(file)+"\", line "+str(lineh+1)+" :")
        print("   "+content)
        print(error)
        sys.exit()
else:
    def ende(content,error):
        sys.exit()
if funcexe==1:
    if os.path.exists("temp.json"):
        datafile=open("temp.json","rb")
        data=pickle.load(datafile)
        datafile.close()
        os.remove("temp.json")
    else:
        print("vodka.tempnotfound.error : temp.json file for the function not found.")
        sys.exit()
else:
    data={}
#
#Commentaires
#
for i in range(len(code)):
    try:
        if code[i].startswith("§"):
            code[i]=""
        else:
            linecomment=code[i].split("§")
            code[i]=linecomment[0]
    except:
        pass
#
#Fonctions
#
func=[]
funcy=[]
funcpathdict={}
for i in range(len(code)):
    if code[i].startswith("vodfunc"):
        funcfile=os.path.dirname(adressfile)+"/"+code[i][8::]+".vodf"
        if not os.path.exists(funcfile):
            print()
            ende(code[i],"vodka.functionnotfound.error : Can't find "+code[i][8::]+"'s function.")
        func.append(funcfile)
        truc=str(os.path.basename(funcfile)).rstrip(".vodf")
        funcy.append(truc)
for i in range(len(func)):
    funcpathdict[funcy[i]]=func[i]
for i in range(len(code)):
    if code[i].startswith("vodka"):
        line=code[i].split()
        if len(line)>=5 and line[1].startswith("$") and line[1] in data:
            print()
            ende(code[i],"vodka.trymodifyconstance.error : You can't reassign a constance.")
#
#Vodkint
#
        if len(line)==5 and line[3]=="vodkint":
            if not line[1] in data:
                try:
                    int(line[4])
                    data[line[1]]=["vodkint",line[4]]
                except:
                    if len(line[4])>4300:
                        print()
                        ende(code[i],"vodka.maxintlimit.error : Value has too many digits.")
                    print()
                    ende(code[i],"vodka.notint.error : Value is not a int.")
            else:
                try:
                    int(line[4])
                    data[line[1]]=["vodkint",line[4]]
                except:
                    if len(line[4])>4300:
                        print()
                        ende(code[i],"vodka.maxintlimit.error : Value has too many digits.")
                    print()
                    ende(code[i],"vodka.notint.error : Value is not a int.")
#
#Vodkint attributes
#
        elif len(line)==5 and line[3]=="vodkint.len":
            if line[4] in data and data[line[4]][0]=="vodkint":
                data[line[1]]=["vodkint",len(data[line[4]][1])]
            elif line[4] in data and not data[line[4]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[4]+" is not vodkint's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==6 and line[3]=="vodkint.add":
            if line[4] in data and line[5] in data and data[line[4]][0]=="vodkint" and data[line[5]][0]=="vodkint":
                try:
                    data[line[1]]=["vodkint",str(int(data[line[4]][1])+int(data[line[5]][1]))]
                except:
                    print()
                    ende(code[i],"vodka.notint.error : \""+line[5]+"\" is not a int.")
            elif line[4] in data and not data[line[4]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[4]+" is not vodkint's type.")
            elif line[5] in data and not data[line[5]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[5]+" is not vodkint's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==6 and line[3]=="vodkint.sub":
            if line[4] in data and line[5] in data and data[line[4]][0]=="vodkint" and data[line[5]][0]=="vodkint":
                try:
                    data[line[1]]=["vodkint",str(int(data[line[4]][1])-int(data[line[5]][1]))]
                except:
                    print()
                    ende(code[i],"vodka.notint.error : \""+line[5]+"\" is not a int.")
            elif line[4] in data and not data[line[4]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[4]+" is not vodkint's type.")
            elif line[5] in data and not data[line[5]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[5]+" is not vodkint's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==6 and line[3]=="vodkint.time":
            if line[4] in data and line[5] in data and data[line[4]][0]=="vodkint" and data[line[5]][0]=="vodkint":
                try:
                    data[line[1]]=["vodkint",str(int(data[line[4]][1])*int(data[line[5]][1]))]
                except:
                    print()
                    ende(code[i],"vodka.notint.error : \""+line[5]+"\" is not a int.")
            elif line[4] in data and not data[line[4]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[4]+" is not vodkint's type.")
            elif line[5] in data and not data[line[5]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[5]+" is not vodkint's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==6 and line[3]=="vodkint.div":
            if line[4] in data and line[5] in data and data[line[4]][0]=="vodkint" and data[line[5]][0]=="vodkint":
                try:
                    data[line[1]]=["vodkint",str(int(int(data[line[4]][1])/int(data[line[5]][1])))]
                except ZeroDivisionError:
                    print()
                    ende(code[i],"vodka.zerodivision.error : Can't divide by 0.")
                except:
                    print()
                    ende(code[i],"vodka.notint.error : \""+line[5]+"\" is not a int.")
            elif line[4] in data and not data[line[4]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[4]+" is not vodkint's type.")
            elif line[5] in data and not data[line[5]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[5]+" is not vodkint's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==6 and line[3]=="vodkint.dive":
            if line[4] in data and line[5] in data and data[line[4]][0]=="vodkint" and data[line[5]][0]=="vodkint":
                try:
                    data[line[1]]=["vodkint",str(int(int(data[line[4]][1])//int(data[line[5]][1])))]
                except ZeroDivisionError:
                    print()
                    ende(code[i],"vodka.zerodivision.error : Can't divide by 0.")
                except:
                    print()
                    ende(code[i],"vodka.notint.error : \""+line[5]+"\" is not a int.")
            elif line[4] in data and not data[line[4]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[4]+" is not vodkint's type.")
            elif line[5] in data and not data[line[5]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[5]+" is not vodkint's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==6 and line[3]=="vodkint.mod":
            if line[4] in data and line[5] in data and data[line[4]][0]=="vodkint" and data[line[5]][0]=="vodkint":
                try:
                    data[line[1]]=["vodkint",str(int(int(data[line[4]][1])%int(data[line[5]][1])))]
                except ZeroDivisionError:
                    print()
                    ende(code[i],"vodka.zerodivision.error : Can't divide by 0.")
                except:
                    print()
                    ende(code[i],"vodka.notint.error : \""+line[5]+"\" is not a int.")
            elif line[4] in data and not data[line[4]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[4]+" is not vodkint's type.")
            elif line[5] in data and not data[line[5]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[5]+" is not vodkint's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==5 and line[3]=="vodkint.abs":
            if line[4] in data and data[line[4]][0]=="vodkint":
                data[line[1]]=["vodkint",abs(int(data[line[4]][1]))]
            elif line[4] in data and not data[line[4]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[4]+" is not vodkint's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==6 and line[3]=="vodkint.exp":
            if line[4] in data and line[5] in data and data[line[4]][0]=="vodkint" and data[line[5]][0]=="vodkint":
                try:
                    data[line[1]]=["vodkint",str(int(data[line[4]][1])**int(data[line[5]][1]))]
                except:
                    print()
                    ende(code[i],"vodka.notint.error : \""+line[5]+"\" is not a int.")
            elif line[4] in data and not data[line[4]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[4]+" is not vodkint's type.")
            elif line[5] in data and not data[line[5]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[5]+" is not vodkint's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==5 and line[3]=="vodkint.convfloat":
            if line[4] in data and data[line[4]][0]=="vodfloat":
                data[line[1]]=["vodkint",str(int(float(data[line[4]][1])))]
            elif line[4] in data and not data[line[4]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.notfloat.error : "+line[4]+" is not vodfloat's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodkint.convtext":
            if line[4] in data and data[line[4]][0]=="vodtext":
                try:
                    data[line[1]]=["vodkint",str(int(data[line[4]][1]))]
                except:
                    print()
                    ende(code[i],"vodka.conversion.error : the value of this variable can't be convert to vodkint's type.")
            elif line[4] in data and not data[line[4]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[4]+" is not vodtext's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodkint.convstring":
            if line[4] in data and data[line[4]][0]=="vodstring":
                try:
                    data[line[1]]=["vodkint",str(int(data[line[4]][1]))]
                except:
                    print()
                    ende(code[i],"vodka.conversion.error : the value of this variable can't be convert to vodkint's type.")
            elif line[4] in data and not data[line[4]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[4]+" is not vodstring's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
#
#Vodfloat
#
        elif len(line)==5 and line[3]=="vodfloat":
            if not line[1] in data:
                try:
                    float(line[4])
                    data[line[1]]=["vodfloat",line[4]]
                except:
                    print()
                    ende(code[i],"vodka.notfloat.error : Value is not a float.")
            else:
                try:
                    float(line[4])
                    data[line[1]]=["vodfloat",line[4]]
                except:
                    print()
                    ende(code[i],"vodka.notfloat.error : Value is not a float.")
#
#Vodfloat attributes
#
        elif len(line)==5 and line[3]=="vodfloat.convstring":
            if line[4] in data and data[line[4]][0]=="vodstring":
                try:
                    data[line[1]]=["vodfloat",str(float(data[line[4]][1]))]
                except:
                    print()
                    ende(code[i],"vodka.conversion.error : the value of this variable can't be convert to vodfloat's type.")
            elif line[4] in data and not data[line[4]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[4]+" is not vodstring's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodfloat.convtext":
            if line[4] in data and data[line[4]][0]=="vodtext":
                try:
                    data[line[1]]=["vodfloat",str(float(data[line[4]][1]))]
                except:
                    print()
                    ende(code[i],"vodka.conversion.error : the value of this variable can't be convert to vodfloat's type.")
            elif line[4] in data and not data[line[4]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[4]+" is not vodtext's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodfloat.convint":
            if line[4] in data and data[line[4]][0]=="vodkint":
                data[line[1]]=["vodfloat",data[line[4]][1]]
            elif line[4] in data and not data[line[4]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notfloat.error : "+line[4]+" is not vodkint's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodfloat.len":
            if line[4] in data and data[line[4]][0]=="vodfloat":
                data[line[1]]=["vodkint",len(data[line[4]][1])]
            elif line[4] in data and not data[line[4]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.nofloat.error : "+line[4]+" is not vodfloat's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodfloat.lenu":
            if line[4] in data and data[line[4]][0]=="vodfloat":
                truc=str(int(float(data[line[4]][1])))
                data[line[1]]=["vodkint",len(truc)]
            elif line[4] in data and not data[line[4]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.nofloat.error : "+line[4]+" is not vodfloat's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodfloat.lend":
            if line[4] in data and data[line[4]][0]=="vodfloat":
                truc=int(float(data[line[4]][1]))
                trux=data[line[4]][1][len(str(truc))+1::]
                data[line[1]]=["vodkint",len(trux)]
            elif line[4] in data and not data[line[4]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.nofloat.error : "+line[4]+" is not vodfloat's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodfloat.unit":
            if line[4] in data and data[line[4]][0]=="vodfloat":
                truc=data[line[4]][1].split(".")[0]
                data[line[1]]=["vodkint",truc]
            elif line[4] in data and not data[line[4]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.nofloat.error : "+line[4]+" is not vodfloat's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodfloat.decimal":
            if line[4] in data and data[line[4]][0]=="vodfloat":
                truc=data[line[4]][1].split(".")[1]
                data[line[1]]=["vodkint",truc]
            elif line[4] in data and not data[line[4]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.nofloat.error : "+line[4]+" is not vodfloat's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==6 and line[3]=="vodfloat.add":
            if line[4] in data and line[5] in data and data[line[4]][0]=="vodfloat" and data[line[5]][0]=="vodfloat":
                try:
                    data[line[1]]=["vodfloat",str(float(data[line[4]][1])+float(data[line[5]][1]))]
                except:
                    print()
                    ende(code[i],"vodka.notfloat.error : \""+line[5]+"\" is not a float.")
            elif line[4] in data and not data[line[4]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.notfloat.error : "+line[4]+" is not vodfloat's type.")
            elif line[5] in data and not data[line[5]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.notfloat.error : "+line[5]+" is not vodfloat's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==6 and line[3]=="vodfloat.sub":
            if line[4] in data and line[5] in data and data[line[4]][0]=="vodfloat" and data[line[5]][0]=="vodfloat":
                try:
                    data[line[1]]=["vodfloat",str(float(data[line[4]][1])-float(data[line[5]][1]))]
                except:
                    print()
                    ende(code[i],"vodka.notfloat.error : \""+line[5]+"\" is not a float.")
            elif line[4] in data and not data[line[4]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.notfloat.error : "+line[4]+" is not vodfloat's type.")
            elif line[5] in data and not data[line[5]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.notfloat.error : "+line[5]+" is not vodfloat's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==6 and line[3]=="vodfloat.time":
            if line[4] in data and line[5] in data and data[line[4]][0]=="vodfloat" and data[line[5]][0]=="vodfloat":
                try:
                    data[line[1]]=["vodfloat",str(float(data[line[4]][1])*float(data[line[5]][1]))]
                except:
                    print()
                    ende(code[i],"vodka.notfloat.error : \""+line[5]+"\" is not a float.")
            elif line[4] in data and not data[line[4]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.notfloat.error : "+line[4]+" is not vodfloat's type.")
            elif line[5] in data and not data[line[5]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.notfloat.error : "+line[5]+" is not vodfloat's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==6 and line[3]=="vodfloat.div":
            if line[4] in data and line[5] in data and data[line[4]][0]=="vodfloat" and data[line[5]][0]=="vodfloat":
                try:
                    data[line[1]]=["vodfloat",str(float(float(data[line[4]][1])/float(data[line[5]][1])))]
                except ZeroDivisionError:
                    print()
                    ende(code[i],"vodka.zerodivision.error : Can't divide by 0.")
                except:
                    print()
                    ende(code[i],"vodka.notfloat.error : \""+line[5]+"\" is not a float.")
            elif line[4] in data and not data[line[4]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.notfloat.error : "+line[4]+" is not vodfloat's type.")
            elif line[5] in data and not data[line[5]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.notfloat.error : "+line[5]+" is not vodfloat's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==6 and line[3]=="vodfloat.mod":
            if line[4] in data and line[5] in data and data[line[4]][0]=="vodfloat" and data[line[5]][0]=="vodfloat":
                try:
                    data[line[1]]=["vodfloat",str(float(float(data[line[4]][1])%float(data[line[5]][1])))]
                except ZeroDivisionError:
                    print()
                    ende(code[i],"vodka.zerodivision.error : Can't divide by 0.")
                except:
                    print()
                    ende(code[i],"vodka.notfloat.error : \""+line[5]+"\" is not a float.")
            elif line[4] in data and not data[line[4]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.notfloat.error : "+line[4]+" is not vodfloat's type.")
            elif line[5] in data and not data[line[5]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.notfloat.error : "+line[5]+" is not vodfloat's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==5 and line[3]=="vodfloat.abs":
            if line[4] in data and data[line[4]][0]=="vodfloat":
                data[line[1]]=["vodfloat",abs(float(data[line[4]][1]))]
            elif line[4] in data and not data[line[4]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.notfloat.error : "+line[4]+" is not vodfloat's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==6 and line[3]=="vodfloat.exp":
            if line[4] in data and line[5] in data and data[line[4]][0]=="vodfloat" and data[line[5]][0]=="vodkint":
                try:
                    data[line[1]]=["vodfloat",str(float(data[line[4]][1])**int(data[line[5]][1]))]
                except:
                    print()
                    ende(code[i],"vodka.notint.error : \""+line[5]+"\" is not a int.")
            elif line[4] in data and not data[line[4]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.notfloat .error : "+line[4]+" is not vodfloat's type.")
            elif line[5] in data and not data[line[5]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[5]+" is not vodkint's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
#
#Vodtype
#
        elif len(line)==5 and line[3]=="vodtype":
            if line[4] in data:
                data[line[1]]=["vodtype",data[line[4]][0]]
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
#
#Vodtext
#
        elif len(line)>=5 and line[3]=="vodtext":
            try:
                text=code[i][len(line[1])+17::]
                data[line[1]]=["vodtext",text]
            except:
                print()
                ende(code[i],"vodka.nottext.error : Value is not text.")
#
#Vodtext attribute
#
        elif len(line)==5 and line[3]=="vodtext.convint":
            if line[4] in data and data[line[4]][0]=="vodkint":
                data[line[1]]=["vodtext",str(int(data[line[4]][1]))]
            elif line[4] in data and not data[line[4]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[4]+" is not vodkint's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodtext.convstring":
            if line[4] in data and data[line[4]][0]=="vodstring":
                data[line[1]]=["vodtext",repr(str(data[line[4]][1]))]
                data[line[1]][1]=list(data[line[1]][1])
                del(data[line[1]][1][0])
                del(data[line[1]][1][len(data[line[1]][1])-1])
                truc=""
                for o in range(len(data[line[1]][1])):
                    truc=truc+data[line[1]][1][o]
                data[line[1]][1]=truc
            elif line[4] in data and not data[line[4]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[4]+" is not vodstring's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodtext.convfloat":
            if line[4] in data and data[line[4]][0]=="vodfloat":
                data[line[1]]=["vodtext",str(float(data[line[4]][1]))]
            elif line[4] in data and not data[line[4]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.notfloat.error : "+line[4]+" is not vodfloat's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodtext.convtype":
            if line[4] in data and data[line[4]][0]=="vodtype":
                data[line[1]]=["vodtext",str(data[line[4]][1])]
            elif line[4] in data and not data[line[4]][0]=="vodtype":
                print()
                ende(code[i],"vodka.nottype.error : "+line[4]+" is not vodtype's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodtext.lower":
            if line[4] in data and data[line[4]][0]=="vodtext":
                data[line[1]]=["vodtext",str(data[line[4]][1]).lower()]
            elif line[4] in data and not data[line[4]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[4]+" is not vodtext's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodtext.upper":
            if line[4] in data and data[line[4]][0]=="vodtext":
                data[line[1]]=["vodtext",str(data[line[4]][1]).upper()]
            elif line[4] in data and not data[line[4]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[4]+" is not vodtext's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodtext.capitalize":
            if line[4] in data and data[line[4]][0]=="vodtext":
                data[line[1]]=["vodtext",str(data[line[4]][1]).capitalize()]
            elif line[4] in data and not data[line[4]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[4]+" is not vodtext's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==6 and line[3]=="vodtext.find":
            if line[4] in data and data[line[4]][0]=="vodtext" and line[5] in data and data[line[5]][0]=="vodtext":
                data[line[1]]=["vodkint",data[line[4]][1].find(data[line[5]][1])]
            elif line[4] in data and not data[line[4]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[4]+" is not vodtext's type.")
            elif line[5] in data and not data[line[5]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[5]+" is not vodtext's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==6 and line[3]=="vodtext.index":
            if line[4] in data and data[line[4]][0]=="vodtext" and line[5] in data and data[line[5]][0]=="vodtext":
                data[line[1]]=["vodkint",data[line[4]][1].find(data[line[5]][1])]
                if data[line[4]][1].find(data[line[5]][1])==-1:
                    print()
                    ende(code[i],"vodka.textnotfound.error : the wanted text can't be found in the main text")
            elif line[4] in data and not data[line[4]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[4]+" is not vodtext's type.")
            elif line[5] in data and not data[line[5]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[5]+" is not vodtext's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==7 and line[3]=="vodtext.replace":
            if line[4] in data and data[line[4]][0]=="vodtext" and line[5] in data and data[line[5]][0]=="vodtext" and line[6] in data and data[line[6]][0]=="vodtext":
                data[line[1]]=["vodtext",data[line[4]][1].replace(data[line[5]][1],data[line[6]][1])]
            elif line[4] in data and not data[line[4]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[4]+" is not vodtext's type.")
            elif line[5] in data and not data[line[5]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[5]+" is not vodtext's type.")
            elif line[6] in data and not data[line[6]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[6]+" is not vodtext's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==6 and line[3]=="vodtext.join":
            if line[4] in data and data[line[4]][0]=="vodtext" and line[5] in data and data[line[5]][0]=="vodtext":
                data[line[1]]=["vodtext",data[line[4]][1]+data[line[5]][1]]
            elif line[4] in data and not data[line[4]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[4]+" is not vodtext's type.")
            elif line[5] in data and not data[line[5]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[5]+" is not vodtext's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)>=6 and line[3]=="vodtext.get":
            if line[4] in data and data[line[4]][0]=="vodtext" and len(line)==7 and line[5] in data and data[line[5]][0]=="vodkint" and line[6] in data and data[line[6]][0]=="vodkint":
                try:
                    data[line[1]]=["vodtext",data[line[4]][1][int(data[line[5]][1])-1:int(data[line[6]][1])]]
                except IndexError:
                    print()
                    ende(code[i],"vodka.index.error : Index out of range")
            elif  line[4] in data and data[line[4]][0]=="vodtext" and len(line)==6 and line[5] in data and data[line[5]][0]=="vodkint":
                try:
                    data[line[1]]=["vodtext",data[line[4]][1][int(data[line[5]][1])-1]]
                except IndexError:
                    print()
                    ende(code[i],"vodka.index.error : Index out of range")
            elif line[4] in data and not data[line[4]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[4]+" is not vodtext's type.")
            elif line[5] in data and not data[line[5]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[5]+" is not vodkint's type.")
            elif line[6] in data and not data[line[6]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[6]+" is not vodkint's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==5 and line[3]=="vodtext.len":
            if line[4] in data and data[line[4]][0]=="vodtext":
                data[line[1]]=["vodkint",len(data[line[4]][1])]
            elif line[4] in data and not data[line[4]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[4]+" is not vodtext's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodtext.input":
            if line[4] in data and data[line[4]][0]=="vodtext":
                data[line[1]]=["vodtext",input(data[line[4]][1])]
            elif line[4] in data and not data[line[4]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[4]+" is not vodtext's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
#
#Vodstring
#
        elif len(line)>=5 and line[3]=="vodstring":
            try:
                text=code[i][len(line[1])+19::]
                data[line[1]]=["vodstring",text]
                data[line[1]][1]=data[line[1]][1].replace("\\n","\n")
                data[line[1]][1]=data[line[1]][1].replace("\\t","\t")
            except:
                print()
                ende(code[i],"vodka.notstring.error : Value is not text.")
#
#Vodstring attribute
#
        elif len(line)==5 and line[3]=="vodstring.convint":
            if line[4] in data and data[line[4]][0]=="vodkint":
                data[line[1]]=["vodstring",str(int(data[line[4]][1]))]
            elif line[4] in data and not data[line[4]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[4]+" is not vodkint's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodstring.convtext":
            if line[4] in data and data[line[4]][0]=="vodtext":
                data[line[1]]=["vodstring",str(data[line[4]][1])]
            elif line[4] in data and not data[line[4]][0]=="vodtext":
                print()
                ende(code[i],"vodka.nottext.error : "+line[4]+" is not vodtext's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodstring.convfloat":
            if line[4] in data and data[line[4]][0]=="vodfloat":
                data[line[1]]=["vodstring",str(float(data[line[4]][1]))]
            elif line[4] in data and not data[line[4]][0]=="vodfloat":
                print()
                ende(code[i],"vodka.notfloat.error : "+line[4]+" is not vodfloat's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodstring.convtype":
            if line[4] in data and data[line[4]][0]=="vodtype":
                data[line[1]]=["vodstring",str(data[line[4]][1])]
            elif line[4] in data and not data[line[4]][0]=="vodtype":
                print()
                ende(code[i],"vodka.nottype.error : "+line[4]+" is not vodtype's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodstring.lower":
            if line[4] in data and data[line[4]][0]=="vodstring":
                data[line[1]]=["vodstring",str(data[line[4]][1]).lower()]
            elif line[4] in data and not data[line[4]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[4]+" is not vodstring's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodstring.upper":
            if line[4] in data and data[line[4]][0]=="vodstring":
                data[line[1]]=["vodstring",str(data[line[4]][1]).upper()]
            elif line[4] in data and not data[line[4]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[4]+" is not vodstring's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodstring.capitalize":
            if line[4] in data and data[line[4]][0]=="vodstring":
                data[line[1]]=["vodstring",str(data[line[4]][1]).capitalize()]
            elif line[4] in data and not data[line[4]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[4]+" is not vodstring's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==6 and line[3]=="vodstring.find":
            if line[4] in data and data[line[4]][0]=="vodstring" and line[5] in data and data[line[5]][0]=="vodstring":
                data[line[1]]=["vodkint",data[line[4]][1].find(data[line[5]][1])]
            elif line[4] in data and not data[line[4]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[4]+" is not vodstring's type.")
            elif line[5] in data and not data[line[5]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[5]+" is not vodstring's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==6 and line[3]=="vodstring.index":
            if line[4] in data and data[line[4]][0]=="vodstring" and line[5] in data and data[line[5]][0]=="vodstring":
                data[line[1]]=["vodkint",data[line[4]][1].find(data[line[5]][1])]
                if data[line[4]][1].find(data[line[5]][1])==-1:
                    print()
                    ende(code[i],"vodka.stringnotfound.error : the wanted string can't be found in the main string")
            elif line[4] in data and not data[line[4]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[4]+" is not vodstring's type.")
            elif line[5] in data and not data[line[5]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[5]+" is not vodstring's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==7 and line[3]=="vodstring.replace":
            if line[4] in data and data[line[4]][0]=="vodstring" and line[5] in data and data[line[5]][0]=="vodstring" and line[6] in data and data[line[6]][0]=="vodstring":
                data[line[1]]=["vodstring",data[line[4]][1].replace(data[line[5]][1],data[line[6]][1])]
            elif line[4] in data and not data[line[4]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[4]+" is not vodstring's type.")
            elif line[5] in data and not data[line[5]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[5]+" is not vodstring's type.")
            elif line[6] in data and not data[line[6]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[6]+" is not vodstring's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==6 and line[3]=="vodstring.join":
            if line[4] in data and data[line[4]][0]=="vodstring" and line[5] in data and data[line[5]][0]=="vodstring":
                data[line[1]]=["vodstring",data[line[4]][1]+data[line[5]][1]]
            elif line[4] in data and not data[line[4]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[4]+" is not vodstring's type.")
            elif line[5] in data and not data[line[5]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[5]+" is not vodstring's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)>=6 and line[3]=="vodstring.get":
            if line[4] in data and data[line[4]][0]=="vodstring" and len(line)==7 and line[5] in data and data[line[5]][0]=="vodkint" and line[6] in data and data[line[6]][0]=="vodkint":
                try:
                    data[line[1]]=["vodstring",data[line[4]][1][int(data[line[5]][1])-1:int(data[line[6]][1])]]
                except IndexError:
                    print()
                    ende(code[i],"vodka.index.error : Index out of range")
            elif  line[4] in data and data[line[4]][0]=="vodstring" and len(line)==6 and line[5] in data and data[line[5]][0]=="vodkint":
                try:
                    data[line[1]]=["vodstring",data[line[4]][1][int(data[line[5]][1])-1]]
                except IndexError:
                    print()
                    ende(code[i],"vodka.index.error : Index out of range")
            elif line[4] in data and not data[line[4]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[4]+" is not vodstring's type.")
            elif line[5] in data and not data[line[5]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[5]+" is not vodkint's type.")
            elif line[6] in data and not data[line[6]][0]=="vodkint":
                print()
                ende(code[i],"vodka.notint.error : "+line[6]+" is not vodkint's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : One of the variable/constance is not defined.")
        elif len(line)==5 and line[3]=="vodstring.len":
            if line[4] in data and data[line[4]][0]=="vodstring":
                data[line[1]]=["vodkint",len(data[line[4]][1])]
            elif line[4] in data and not data[line[4]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[4]+" is not vodstring's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
        elif len(line)==5 and line[3]=="vodstring.input":
            if line[4] in data and data[line[4]][0]=="vodstring":
                data[line[1]]=["vodstring",input(data[line[4]][1])]
            elif line[4] in data and not data[line[4]][0]=="vodstring":
                print()
                ende(code[i],"vodka.notstring.error : "+line[4]+" is not vodstring's type.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[4]+"\" is not defined.")
#
#Duplication
#
        elif len(line)==5 and line[3]=="vodka":
            data[line[1]]=data[line[4]]
#
#Fonctions externes
#
        elif len(line)>=4 and line[3] in funcy:
            donne=fonction(funcpathdict[line[3]],code[i].split(),i+1)
            if not donne==None:
                data[line[1]]=donne
        else:
            print()
            ende(code[i],"vodka.syntax.error : Syntax not correct.")
#
#Vodimp
#
    elif code[i].startswith("vodimp"):
        line=code[i].split()
        if line[1]=="vodkint":
            startt=len(line[2])+16
            importt=code[i][startt::]
            if not os.path.exists(importt):
                print()
                ende(code[i],"vodka.filenotfound.error : File doesn't exist.")
            try:
                text=open(importt,"r",encoding="utf-8").readlines()
            except UnicodeDecodeError:
                print()
                ende(code[i],"vodka.notreadable.error : File isn't readable.")                
            try:
                text=text[0]
            except IndexError:
                print()
                ende(code[i],"vodka.firstlineempty.error : First line of the file is empty.")
            try:
                text=text.rstrip("\n")
            except:
                pass
            try:
                int(text)
                data[line[2]]=["vodkint",text]
            except ValueError:
                if len(text)>4300:
                    print()
                    ende(code[i],"vodka.maxintlimit.error : Value has too many digits.")
                print()
                ende(code[i],"vodka.notint.error : Value is not a int.")
        elif line[1]=="vodfloat":
            startt=len(line[2])+17
            importt=code[i][startt::]
            if not os.path.exists(importt):
                print()
                ende(code[i],"vodka.filenotfound.error : File doesn't exist.")
            try:
                text=open(importt,"r",encoding="utf-8").readlines()
            except UnicodeDecodeError:
                print()
                ende(code[i],"vodka.notreadable.error : File isn't readable.")     
            try:
                text=text[0]
            except IndexError:
                print()
                ende(code[i],"vodka.firstlineempty.error : First line of the file is empty.")
            try:
                text=text.rstrip("\n")
            except:
                pass
            try:
                float(text)
                data[line[2]]=["vodfloat",text]
            except ValueError:
                print()
                ende(code[i],"vodka.notfloat.error : Value is not a float.")
        elif line[1]=="vodtext":
            startt=len(line[2])+16
            importt=code[i][startt::]
            if not os.path.exists(importt):
                print()
                ende(code[i],"vodka.filenotfound.error : File doesn't exist.")
            try:
                text=open(importt,"r",encoding="utf-8").readlines()
            except UnicodeDecodeError:
                print()
                ende(code[i],"vodka.notreadable.error : File isn't readable.")                
            try:
                text=text[0]
            except IndexError:
                print()
                ende(code[i],"vodka.firstlineempty.error : First line of the file is empty.")
            try:
                text=text.rstrip("\n")
            except:
                pass
            try:
                repr(text)
                data[line[2]]=["vodtext",text]
            except ValueError:
                print()
                ende(code[i],"vodka.nottext.error : Value is not text.")
        elif line[1]=="vodstring":
            startt=len(line[2])+18
            importt=code[i][startt::]
            if not os.path.exists(importt):
                print()
                ende(code[i],"vodka.filenotfound.error : File doesn't exist.")
            try:
                text=open(importt,"r",encoding="utf-8").readlines()
            except UnicodeDecodeError:
                print()
                ende(code[i],"vodka.notreadable.error : File isn't readable.")                
            try:
                tuxt=""
                for i in range(len(text)):
                    tuxt=tuxt+text[i]
                text=tuxt
            except IndexError:
                print()
                ende(code[i],"vodka.firstlineempty.error : First line of the file is empty.")
            try:
                str(text)
                data[line[2]]=["vodstring",text]
            except ValueError:
                print()
                ende(code[i],"vodka.notstring.error : Value is not string.")
        else:
            print()
            ende(code[i],"vodka.syntax.error : Syntax not correct.")
#
#Vodprint
#
    elif code[i].startswith("vodprint"):
        line=code[i].split()
        if len(line)==2:
            try:
                if data[line[1]][0]=="vodkint":
                    print(data[line[1]][1])
                elif data[line[1]][0]=="vodfloat":
                    print(data[line[1]][1])
                elif data[line[1]][0]=="vodtype":
                    print(data[line[1]][1])
                elif data[line[1]][0]=="vodstring":
                    print(data[line[1]][1])
                elif data[line[1]][0]=="vodtext":
                    truc=list(str(data[line[1]][1]))
                    for p in range(len(truc)):
                        if p==len(truc)-1:
                            print(truc[p])
                        else:
                            print(truc[p],end="")    
                else:
                    print()
                    ende(code[i],"vodka.unknowtype.error : \""+data[line[1]][0]+"\" is not a type.")
            except KeyError:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[1]+"\" is not defined.")
        elif len(line)==1:
            print()
            ende(code[i],"vodka.syntax.error : Can't find any variable to print.")
        else:
            print()
            ende(code[i],"vodka.syntax.error : Can't print several variables at once.")
#
#Vodexp
#
    elif code[i].startswith("vodexp"):
        line=code[i].split()
        if len(line)>2:
            if line[1] in data:
                startt=len(line[1])+8
                exportt=code[i][startt::]
                if not os.path.exists(exportt):
                    print()
                    ende(code[i],"vodka.filenotvalid.error : File doesn't exists.")
                if not exportt.endswith(".txt"):
                    print()
                    ende(code[i],"vodka.filetype.error : File isn't a .txt file.")
                if data[line[1]][0]=="vodkint":
                    try:
                        open(exportt,"w").write(str(data[line[1]][1]))
                    except:
                        print()
                        ende(code[i],"vodka.unknow.error : An unknow error happen. Please verify the file exists before retry.")
                elif data[line[1]][0]=="vodfloat":
                    try:
                        open(exportt,"w").write(str(data[line[1]][1]))
                    except:
                        print()
                        ende(code[i],"vodka.unknow.error : An unknow error happen. Please verify the file exists before retry.")
                elif data[line[1]][0]=="vodtext":
                    try:
                        open(exportt,"w",encoding="utf-8").write(str(data[line[1]][1]))
                    except:
                        print()
                        ende(code[i],"vodka.unknow.error : An unknow error happen. Please verify the file exists before retry.")
                elif data[line[1]][0]=="vodstring":
                    try:
                        open(exportt,"w",encoding="utf-8").write(str(data[line[1]][1]))
                    except:
                        print()
                        ende(code[i],"vodka.unknow.error : An unknow error happen. Please verify the file exists before retry.")
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[1]+"\" is not defined.")
        else:
            print()
            ende(code[i],"vodka.syntax.error : Syntax not correct.")
#
#Autres
#
    elif code[i].startswith("vodfunc"):
        pass
    elif code[i]=="vodabout":
        print("Vodka v0.4")
    elif code[i]=="vodata":
        print(data)
    else:
        if not code[i]=="":
            print()
            ende(code[i],"vodka.syntax.error : '"+code[i]+"' is not a function.")
if funcexe==1:
    with open("temp.json","wb") as dicttrans:
        pickle.dump(data,dicttrans)