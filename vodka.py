import sys,os,random
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
if not file.endswith(".vod"):
    print("vodka.filetype.error : File is not a .vod file")
    sys.exit()
if not os.path.exists(file):
    print("vodka.filenotfound.error : File doesn't exist")
    sys.exit()
fileline=open(file,"r",encoding="utf-8").readlines()
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
for i in range(len(code)):
    if code[i].startswith("vodka"):
        line=code[i].split()
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
                ende(code[i],"vodka.notdefined.error : One of the variable is not defined.")
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
#Duplication
#
        elif len(line)==5 and line[3]=="vodka":
            data[line[1]]=data[line[4]]
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
            else:
                print()
                ende(code[i],"vodka.notdefined.error : \""+line[1]+"\" is not defined.")
        else:
            print()
            ende(code[i],"vodka.syntax.error : Syntax not correct.")
    elif code[i]=="vodabout":
        print("Vodka v0.3")
    elif code[i]=="vodata":
        print(data)
    else:
        if not code[i]=="":
            print()
            ende(code[i],"vodka.syntax.error : '"+code[i]+"' is not a function.")