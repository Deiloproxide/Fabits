########################################################################################
#......................................................................................#
#..DDDD...EEEEE..IIIII..L.......OOO...PPPP...RRRR....OOO...X...X..IIIII..DDDD...EEEEE..#
#..D...D..E........I....L......O...O..P...P..R...R..O...O...X.X.....I....D...D..E......#
#..D...D..EEEEE....I....L......O...O..PPPP...RRRR...O...O....X......I....D...D..EEEEE..#
#..D...D..E........I....L......O...O..P......R...R..O...O...X.X.....I....D...D..E......#
#..DDDD...EEEEE..IIIII..LLLLL...OOO...P......R...R...OOO...X...X..IIIII..DDDD...EEEEE..#
#......................................................................................#
########################################################################################
import chardet,ctypes,hashlib,math,multiprocessing,numpy,json,os,random
import requests,subprocess,sys,threading,time,tkinter,turtle,webbrowser
from PIL import Image; from tkinter import filedialog,messagebox,ttk
def avgs(nm:str)->numpy.floating: return numpy.mean(numpy.array(Image.open(nm).convert('L')))
multiprocessing.freeze_support(); protmp=numpy.zeros(shape=(52,91,5,2))
pullst=numpy.zeros(shape=(38000,4),dtype=int); prolst=numpy.zeros(38000)
class Fabits:
    '''Fabits app class'''
    def __init__(self)->None:
        '''initialize app'''
        self.iniset(); self.wmset(); self.funset(); self.adconf()
        self.icc(self.cfg.get('ani',1),new=1); self.wm.mainloop()
    def adconf(self)->None:
        '''add main window widget and style'''
        self.cvs=tkinter.Canvas(self.wm); scrn=turtle.TurtleScreen(self.cvs)
        self.tul=turtle.RawTurtle(scrn); self.wmemp=[ttk.Frame(self.wm) for i in range(2)]
        self.csl=self.cretre(self.wmemp[0]); self.clear(self.csl)
        txslb=tkinter.Scrollbar(self.wmemp[1])
        self.edtr=tkinter.Text(self.wmemp[1],undo=1,yscrollcommand=txslb.set)
        txslb.config(command=self.edtr.yview)
        self.edtr.bind('<Key>',lambda s: self.chgcfg())
        txslb.pack(side='right',fill='y'); self.edtr.pack(fill='both',expand=1)
        sty=ttk.Style(self.wm); fnt=(self.fnt,round(0.4*self.scfac),self.fntknd)
        self.wm.config(bg=self.bg); scrn.bgcolor(self.bg)
        self.edtr.config(insertbackground=self.fg,font=fnt)
        self.edtr.config(background=self.bg,foreground=self.fg)
        if self.bgidx:
            sty.theme_use('clam')
        sty.configure('.',background=self.bgin,fieldbackground=self.bg)
        sty.configure('.',foreground=self.fg,font=self.fnt)
        sty.configure('Treeview',font=fnt,rowheight=self.scfac,background=self.bgin)
    def adend(self)->None:
        '''add end to file without end'''
        self.wm.after(0,self.show,self.csl,'cyan','(1/2)打开')
        try:
            pth=self.dlg(0,'打开',('Text files','*.txt'))
            flnms=[i for i in os.listdir(pth) if os.path.isfile(self.fulnm(pth,i))]
        except: return
        names=[i for i in flnms if not os.path.splitext(i)[1]]; hdnms=self.data['hdnms']
        self.wm.after(0,self.show,self.csl,'cyan','(2/2)转换'); lnm=len(names)
        if lnm:
            self.wm.after(0,self.pgini,'查找添加缺失后缀',lnm)
            for i in range(lnm):
                nm=self.fulnm(pth,names[i]); fl=open(nm,'rb')
                cnt,tol,byte,chs=0,0,bytearray(fl.read()),[9,10,13]
                for k in byte:
                    tol+=1
                    if k<32 and k not in chs: cnt+=1
                if tol==0:
                    self.wm.after(0,self.pgupd,i+1,f'{names[i]}为空文件 -> {names[i]}.txt','cyan')
                    fl.close(); os.rename(nm,nm+'.txt'); continue
                elif cnt/tol<0.001:
                    self.wm.after(0,self.pgupd,i+1,f'{names[i]}可能为文本文件 -> {names[i]}.txt','cyan')
                    fl.close(); os.rename(nm,nm+'.txt'); continue
                fl.seek(0); head=fl.read(32)
                for j in hdnms:
                    if j.encode() in head:
                        self.wm.after(0,self.pgupd,i+1,f'{names[i]} -> {names[i]+hdnms[j]}','cyan')
                        fl.close(); os.rename(nm,nm+hdnms[j]); break
                else: self.wm.after(0,self.pgupd,i+1,f'未知文件类型: {names[i]}','red')
            self.wm.after(1000,self.wmqut,self.pg,'pgini')
        self.wm.after(0,self.show,self.csl,'red','进程已结束')
        self.wm.after(0,self.show,self.csl,'purple','>>>')
    def admenu(self)->None:
        '''add menu to main window'''
        self.mnus={
        '文件(F)':{'新建':self.fopen,'打开':lambda: self.fopen(1),'保存':self.fsave,
            '另存为':lambda: self.fsave(1),'导入':lambda: self.fopen(nda=1),
            '导出':lambda: self.fsave(nda=1),'查找与替换':self.schgd,'撤销':self.undo,
            '重做':self.redo,'关闭':self.fclose,'退出':self.savcfg},
        '算法(A)':{'同分异构体数量':self.iso,'链表冒泡排序':self.lnksrt,
            '最大环长度':self.ring,'求解罗马数字':self.rome},
        '批处理(B)':{'缺失后缀修复':self.thr(self.adend),
            '图片颜色替换':self.clrplc,'图片排序':self.thr(self.imgsrt),
            '图片加解密':self.thr(self.picpt)},
        '网络(I)':{'项目仓库':lambda: self.web('proj'),'官网':lambda: self.web('web'),
            '检查更新':self.thr(self.upd)},
        '工具(T)':{'科学计算器':self.calc,'代码混合':self.cdo,'命令管理器':self.cmdmng,
            '编译链接库':self.cmpil,'圣遗物强化':self.itmsth,'迷宫可视化':self.mzgd,
            '抽卡概率计算':self.progd,'抽卡模拟器':self.pulgd,'批量重命名':self.renmgd,
            '文本处理':self.txmng},
        '设置(S)':{'清屏':lambda: self.clear(self.csl),'帮助':self.hlp,
            '图标':lambda: self.icc(1),'选项':self.preset}}
        for i in self.mnus:
            mnutmp=tkinter.Menu(self.mnu,tearoff=0,bg=self.bgin,fg=self.fg)
            self.mnu.add_cascade(label=i,menu=mnutmp)
            for j in self.mnus[i]: mnutmp.add_command(label=j,command=self.mnus[i][j])
    def adups(self,up:str,idx:int)->None:
        '''add up pull for'''
        if up in self.ups: self.mb('w','o','选择角色重复','请重新选择')
        else: self.ups[idx]=up; self.show(self.pultre,'red',f'角色{up}添加成功!')
        for i in self.ups:
            if not i: return
        upstx=f'当前角色:{self.ups[0]},{self.ups[1]},{self.ups[2]},{self.ups[3]}'
        self.pullb.config(text=upstx+' 祈愿结果')
        self.pulbtn[0].config(state='normal'); self.pulbtn[1].config(state='normal')
    def cal(self,expsyn:list[str])->None:
        '''deal calculate case for scientific calculator'''
        if not expsyn: return
        try:
            res=round(self.calstk(expsyn,self.lexp),self.acc)
            self.calshw[0].config(text=str(res)); self.res=res
        except OverflowError: self.calshw[0].config(text='堆栈错误')
        except ArithmeticError: self.calshw[0].config(text='数学错误')
        except ValueError: self.calshw[0].config(text='数学错误')
        except: self.calshw[0].config(text='语法错误')
    def calc(self)->None:
        '''scientific calculator'''
        cal,calemp=self.cretpl('科学计算器',32,12,'calc',1,8)
        mnutx,mnucmd=['精度','退出'],[self.calset,lambda: self.wmqut(cal,'calc')]
        self.calshw,caltx=[ttk.Label]*2,[' ','I']; self.res=self.m=0.0
        self.expsyn,self.lexp,self.expidx,self.acc=['']*100,0,0,12
        self.funs={'sin':math.sin,'cos':math.cos,'tan':math.tan,'arcsin':math.asin,
              'arccos':math.acos,'arctan':math.atan,'mod':lambda a,b: a%b,
              'log':lambda a,b=math.e: math.log(a,b),'√':lambda a,b=2: a**(1/b)}
        self.base=[{'C':lambda a,b: math.gamma(a+1)/math.gamma(b+1)/math.gamma(a-b+1),
                 'P':lambda a,b: math.gamma(a+1)/math.gamma(a-b+1)},
                {'^':lambda a,b: a**b},{'×':lambda a,b: a*b,'÷': lambda a,b: a/b},
                {'+': lambda a,b=0: a+b,'-': lambda a,b=None: -a if b is None else a-b}]
        calmnu=tkinter.Menu(cal); cal.config(menu=calmnu)
        calsmu=tkinter.Menu(calmnu,tearoff=0,bg=self.bgin,fg=self.fg)
        calmnu.add_cascade(label='选项(O)',menu=calsmu)
        for i in range(2):
            calsmu.add_command(label=mnutx[i],command=mnucmd[i])
            self.calshw[i]=ttk.Label(calemp[i],text=caltx[i],anchor='e')
            self.calshw[i].pack(fill='both',expand=1)
        for i in range(6):
            for j in range(7):
                btntx=self.data['calbtx'][i][j]; calbtn=ttk.Button(calemp[i+2],text=btntx)
                calbtn.config(command=lambda tx=btntx: self.calinp(tx))
                calbtn.pack(side='left',fill='both',expand=1)
        self.empck(calemp)
    def calinp(self,tx:str)->None:
        '''input for scientific calculator'''
        if tx=='M': self.m=self.res; return
        elif tx=='=':
            self.thr(self.cal,self.expsyn)(); return
        if tx=='AC': self.expidx,self.lexp=0,0
        elif tx=='←':
            if self.expidx!=0:
                self.expidx-=1; self.lexp-=1
                for i in range(self.expidx,self.lexp): self.expsyn[i]=self.expsyn[i+1]
        elif tx=='<':
            if self.expidx>0: self.expidx-=1
        elif tx=='>':
            if self.expidx<self.lexp: self.expidx+=1
        elif tx=='|x|':
            for i in range(self.lexp-1,self.expidx-1,-1): self.expsyn[i+2]=self.expsyn[i]
            self.expsyn[self.expidx]=self.expsyn[self.expidx+1]='|'
            self.expidx+=2; self.lexp+=2
        else:
            for i in range(self.lexp-1,self.expidx-1,-1): self.expsyn[i+1]=self.expsyn[i]
            self.expsyn[self.expidx]=tx; self.expidx+=1; self.lexp+=1
        newexp=''.join(self.expsyn[:self.expidx]+['I']+self.expsyn[self.expidx:self.lexp])
        self.calshw[0].config(text=' '); self.calshw[1].config(text=newexp)
    def calset(self)->None:
        '''set remain digest decimal for scientific calculator'''
        acc=self.wminp(f'保留小数位数(当前为{self.acc}位)',int)
        if acc is None: return
        self.acc=acc
        if self.acc<0: self.acc=0
        if self.acc>15: self.acc=15
    def calstk(self,syn:list[str],lsyn:int)->float:
        '''deal float, () and || in expresion for scientific calculator'''
        expsyn,lexp,dig,digs=['']*100,0,'',1
        nums,consts='0123456789.',{'m':self.m,'ANS':self.res,'π':math.pi,'e':math.e}
        for i in range(lsyn):
            if syn[i] in nums: dig+=syn[i]
            elif syn[i] in consts: digs*=consts[syn[i]]
            else:
                if dig or isinstance(digs,float):
                    digs*=float(dig) if dig else 1.0; expsyn[lexp]=digs; lexp+=1
                expsyn[lexp]=syn[i]; lexp+=1; dig,digs='',1
        if dig or isinstance(digs,float):
            digs*=float(dig) if dig else 1.0; expsyn[lexp]=digs; lexp+=1
        stk,top,res=[[0,[None]*100,0] for i in range(20)],0,0
        for i in range(lexp):
            if expsyn[i]=='(': top+=1; stk[top][0]=i
            elif expsyn[i]==')':
                if top>0 and expsyn[stk[top][0]]=='(':
                    res=self.calsyn(stk[top][1],stk[top][2]); stk[top][2]=0
                    top-=1; stk[top][1][stk[top][2]]=res; stk[top][2]+=1
                else: raise SyntaxError
            elif expsyn[i]=='|':
                if top>0 and expsyn[stk[top][0]]=='|':
                    res=abs(self.calsyn(stk[top][1],stk[top][2])); stk[top][2]=0
                    top-=1; stk[top][1][stk[top][2]]=res; stk[top][2]+=1
                else: top+=1; stk[top][0]=i
            else: stk[top][1][stk[top][2]]=expsyn[i]; stk[top][2]+=1
            if top>=20: raise OverflowError
        if top!=0: raise SyntaxError
        return self.calsyn(stk[top][1],stk[top][2])
    def calsyn(self,expsyn:list[float|str|tuple],lexp:int)->float|tuple:
        '''calculate value of expresion for scientific calculator'''
        tl,rl,tsyn,rsyn,chg=lexp,0,[any]*100,[any]*100,1
        for i in range(lexp):
            tsyn[i]=expsyn[i]
            if expsyn[i]==',':
                return self.calsyn(expsyn,i),self.calsyn(expsyn[i+1:],lexp-i-1)
        while chg:
            rl,mul=0,1
            for i in range(tl):
                if isinstance(tsyn[i],float): mul*=tsyn[i]
                else:
                    if isinstance(mul,float): rsyn[rl]=mul; rl+=1; mul=1
                    rsyn[rl]=tsyn[i]; rl+=1
            if isinstance(mul,float): rsyn[rl]=mul; rl+=1
            tl,flg,chg=0,0,0
            for i in range(rl):
                if flg: flg=0; continue
                if i<rl-1 and rsyn[i+1]=='!':
                    if isinstance(rsyn[i],float):
                        tsyn[tl]=math.gamma(rsyn[i]+1); tl+=1; chg=flg=1
                    else: tsyn[tl]=rsyn[i]; tl+=1
                elif rsyn[i] in self.funs:
                    if isinstance(rsyn[i+1],float):
                        tsyn[tl]=self.funs[rsyn[i]](rsyn[i+1]); tl+=1; chg=flg=1
                    elif isinstance(rsyn[i+1],tuple):
                        tsyn[tl]=self.funs[rsyn[i]](rsyn[i+1][0],rsyn[i+1][1]); tl+=1; chg=flg=1
                    else: tsyn[tl]=rsyn[i]; tl+=1
                else: tsyn[tl]=rsyn[i]; tl+=1
        for i in self.base:
            j,flg,rl=0,0,0
            while j<tl:
                if tsyn[j] in i:
                    if j==0: rsyn[rl]=i[tsyn[j]](tsyn[j+1]); rl+=1
                    else: rsyn[rl-1]=i[tsyn[j]](rsyn[rl-1],tsyn[j+1])
                    j+=1
                else: rsyn[rl]=tsyn[j]; rl+=1
                j+=1
            for j in range(rl): tsyn[j]=rsyn[j]
            tl=rl
        if rl==1: return rsyn[0]
        else: raise SyntaxError
    def calsz(self,w:int,h:int,key:str)->str:
        '''read last window info or make window center'''
        size=self.cfg.get(key,'')
        if size and self.check: return size
        a,b=w*self.scfac,h*self.scfac; c,d=(self.scwth-a)//2,(self.schgt-b)//2
        return f'{a}x{b}+{c}+{d}'
    def cdo(self)->None:
        '''code mixer'''
        cdo,cdoemp=self.cretpl('代码混合',24,7,'cdobf',0,4)
        self.cdovars=[tkinter.StringVar() for i in range(3)]
        cdotx=['Python源代码','C/C++源代码','生成到']
        cdobtx,cdocmd=['生成','退出'],[self.cdochk,lambda: self.wmqut(cdo,'cdobf')]
        for i in range(3):
            cdolb=ttk.Label(cdoemp[i],text=cdotx[i],width=12)
            cdoet=ttk.Entry(cdoemp[i],width=30,textvariable=self.cdovars[i])
            cdobtn=ttk.Button(cdoemp[i],text='浏览',command=lambda p=i: self.cdocmd(p))
            self.pck(cdolb); self.pck(cdoet); self.pck(cdobtn)
        for i in range(2):
            cdobtn=ttk.Button(cdoemp[3],text=cdobtx[i],command=cdocmd[i]); self.pck(cdobtn)
        self.empck(cdoemp)
    def cdochk(self)->None:
        '''check input for code mix'''
        fls=['']*3
        for i in range(3):
            fl=self.cdovars[i].get()
            if fl: fls[i]=fl
            else: self.mb('w','o','提示','请检查输入的内容'); return
        if not os.path.splitext(fls[2])[1]: fls[2]+='.cpy'
        self.thr(self.cdomix,fls)()
    def cdocmd(self,knd:int)->None:
        '''open or save path for code mix'''
        idx=1 if knd==2 else 0; tles=['打开','保存']
        knds=[('Python source files','*.py'),('C/C++ source files','*.c *.cpp'),
             ('All text files','*.*')]
        pth=self.dlg(idx+1,tles[idx],knds[knd])
        if not pth: return
        self.cdovars[knd].set(pth)
    def cdomix(self,fls:list[str])->None:
        '''generate mixed code'''
        try: fpy=open(fls[0],'rb'); fcpp=open(fls[1],'rb'); fcpy=open(fls[2],'w',encoding='utf-8')
        except: return
        pyb,cppb=fpy.read(),fcpp.read(); fpy.close(); fcpp.close()
        encpy,encpp=chardet.detect(pyb)['encoding'],chardet.detect(cppb)['encoding']
        py,cpp=pyb.decode(encpy).splitlines(),cppb.decode(encpp).splitlines()
        fcpy.write('#if 0\n')
        for i in py: fcpy.write(i+'\n')
        fcpy.write('\n\'\'\'\n#else\n')
        for i in cpp: fcpy.write(i+'\n')
        fcpy.write('\n#endif\n////\'\'\''); fcpy.close()
        self.wm.after(0,self.show,self.csl,'red','进程已结束')
        self.wm.after(0,self.show,self.csl,'purple','>>>')
    def chgcfg(self)->None:
        '''listen change for text editor'''
        if not self.modify: self.modify=1; self.wm.title(f"{self.data['tle']} - {self.flnm}*")
    def cinarg(self,tx:str)->str|None:
        '''input argument for command manager'''
        cin,cinemp=self.cretpl('命令参数',18,6,'cinarg',0,4)
        cinbtx=['文件夹打开','文件打开','文件保存','确认','跳过','取消']
        cinlb=ttk.Label(cinemp[0],text=tx); self.cmdvar=tkinter.StringVar()
        cinet=ttk.Entry(cinemp[1],width=40,textvariable=self.cmdvar)
        cincmd=[lambda: self.cinpth(0),lambda: self.cinpth(1),lambda: self.cinpth(2),
                lambda: self.getvar(self.cmdvar,cin,'cmdinp',str),
                lambda: self.inperr(cin,'cmdinp',''),lambda: self.inperr(cin,'cinarg')]
        for i in range(6):
            cinbtn=ttk.Button(cinemp[2+i//3],text=cinbtx[i],command=cincmd[i])
            self.pck(cinbtn)
        cinlb.pack(expand=1); cinet.pack(expand=1); self.empck(cinemp)
        cin.protocol('WM_DELETE_WINDOW',lambda: self.inperr(cin,'cmdinp'))
        cin.wait_window(); return self.val
    def cinpth(self,knd:int)->None:
        '''open or save path for command manager'''
        tles=['打开','打开','保存']; pth=self.dlg(knd,tles[knd],('All image files','*.*'))
        if pth: self.cmdvar.set(f'\"{pth}\"')
    def clear(self,tag:ttk.Treeview,sgn=1)->None:
        tag.delete(*tag.get_children())
        if sgn: self.show(tag,'purple','>>>')
    def clrplc(self)->None:
        '''color replace'''
        self.show(self.csl,'cyan','(1/4)打开')
        try: flnm=self.dlg(1,'打开',('All image files','*.*')); 
        except: return
        convrt=lambda cl: [int(cl[:2],16),int(cl[2:4],16),int(cl[4:],16)]
        sclrs=self.wminp('输入被替换颜色(16进制表示)')
        if sclrs is None: return
        sclr=self.wminp('输入替换颜色(16进制表示)')
        if sclr is None: return
        try: clrs=list(map(convrt,sclrs.split('/'))); clr=convrt(sclr)
        except: self.mb('w','o','提示','请检查输入的内容'); return
        self.thr(self.clrpld,flnm,clrs,clr)()
    def clrpld(self,flnm:str,clrs:list[list[int]],clr:list[int])->None:
        '''image replace color'''
        self.wm.after(0,self.show,self.csl,'cyan','(2/4)转换'); pic=Image.open(flnm)
        self.wm.after(0,self.show,self.csl,'cyan','(3/4)替换'); piarr=numpy.array(pic)
        for i in clrs: alc=(piarr[:,:,:3]==i).all(axis=-1); piarr[alc,:3]=clr
        self.wm.after(0,self.show,self.csl,'cyan','(4/4)保存'); pic=Image.fromarray(piarr)
        flnew=self.dlg(2,'保存',('Image files','*.png'))
        if not flnew: return
        if not flnew.endswith('.png'): flnew+='.png'
        pic.save(flnew); self.wm.after(0,self.show,self.csl,'red','进程已结束')
        self.wm.after(0,self.show,'purple',self.csl,'>>>')
    def cmdadd(self)->None:
        '''add new command for command manager'''
        nm=self.wminp('新名称')
        if nm is None: return
        if nm in self.cfg['commands']:
            if self.mb('q','yn','命令重复','是否替换')=='no': return
            cmd=self.wminp('输入命令,占位参数用{变量名}表示')
            if cmd is None: return
            for i in self.cmdtre.get_children():
                print(self.cmdtre.item(i,'values'))
                if self.cmdtre.item(i,'values')[0]==nm:
                    self.cmdtre.set(i,column='cmd',value=cmd)
                    self.cmdtre.see(i); break
        else:
            cmd=self.wminp('输入命令,占位参数用{变量名}表示')
            if cmd is None: return
            self.show(self.cmdtre,'green',nm,cmd)
        self.cfg['commands'][nm]=cmd
    def cmddel(self)->None:
        '''delete command for command manager'''
        scl=self.cmdtre.selection()
        if not scl: return
        if self.mb('q','yn','','确认删除?')=='yes':
            lnm,lcmd=self.cmdtre.item(scl,'values')
            self.cmdtre.delete(scl); self.cfg['commands'].pop(lnm)
    def cmdmdf(self)->None:
        '''modify command for command manager'''
        scl=self.cmdtre.selection()
        if not scl: return
        lnm,lcmd=self.cmdtre.item(scl,'values')
        nm=self.wminp('新名称',show=lnm)
        if nm is None: return
        cmd=self.wminp('输入命令,占位参数用{变量名}表示',show=lcmd)
        if cmd is None: return
        self.cmdtre.set(scl,column='nm',value=nm); self.cmdtre.set(scl,column='cmd',value=cmd)
        self.cfg['commands'].pop(lnm); self.cfg['commands'][nm]=cmd
    def cmdmng(self)->None:
        '''command manager'''
        cmd,cmdemp=self.cretpl('命令管理器',32,24,'cmdmng',1,3)
        cmdbtx=['添加','修改','删除','预览','运行','退出']
        cmdcmd=[self.cmdadd,self.cmdmdf,self.cmddel,lambda: self.cmdrun(pre=1),
              self.cmdrun,lambda: self.wmqut(cmd,'cmdmng')]
        self.cmdtre=ttk.Treeview(cmdemp[0],columns=('nm','cmd'),show='headings')
        self.cmdtre.heading('nm',text='名称'); self.cmdtre.heading('cmd',text='命令')
        self.cmdtre.column('nm',width=3*self.scfac,anchor='w')
        self.cmdtre.column('cmd',width=15*self.scfac,anchor='w')
        cmdslb=tkinter.Scrollbar(cmdemp[0]); self.cmdtre.config(yscrollcommand=cmdslb.set)
        cmdslb.config(command=self.cmdtre.yview)
        for i in self.data['clr']: self.cmdtre.tag_configure(i,foreground=i,background=self.bg)
        cmdslb.pack(side='right',fill='y'); self.cmdtre.pack(fill='both',expand=1)
        for i in range(6):
            cmdbtn=ttk.Button(cmdemp[1],text=cmdbtx[i],command=cmdcmd[i]); self.pck(cmdbtn)
        self.cmdres=self.cretre(cmdemp[2]); self.clear(self.cmdres)
        if 'commands' not in self.cfg: self.cfg['commands']={}
        for i in self.cfg['commands']: self.show(self.cmdtre,'green',i,self.cfg['commands'][i])
        self.empck(cmdemp)
    def cmdout(self,cmd:str,tag:ttk.Treeview)->None:
        '''print command line message'''
        pipe=subprocess.Popen(cmd,shell=1,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=1)
        for i in iter(pipe.stdout.readline,''): self.wm.after(0,self.cmpout,i,tag,'purple')
        out,err=pipe.communicate()
        if out: self.wm.after(0,self.cmpout,out,tag,'yellow')
        if err: self.wm.after(0,self.cmpout,err,tag,'red')
        self.wm.after(0,self.show,tag,'purple','>>>')
    def cmdrun(self,pre=0)->None:
        '''fill argument and run command for command manager'''
        scl=self.cmdtre.selection()
        if not scl: return
        nm,cmd=self.cmdtre.item(scl,'values'); form,arg,args,flg='','',[],0
        for i in cmd:
            if flg:
                if i=='}': flg=0; form+=i; args+=[arg]; arg=''
                else: arg+=i
            else:
                form+=i
                if i=='{': flg=1
        for i in range(len(args)):
            args[i]=self.cinarg(f'参数{args[i]}的值')
            if args[i] is None: return
        exe=form.format(*args)
        self.clear(self.cmdres); self.cmpout(exe,self.cmdres,'green')
        if pre and self.mb('q','yn','预览','是否运行?')=='no': return
        self.thr(self.cmdout,exe,self.cmdres)()
    def cmpadd(self)->None:
        '''open or save path for command compile'''
        pth=self.dlg(1,'打开',('C/C++ source files','*.c *.cpp'))
        if not pth: return
        self.cmpvars[0].set(pth)
    def cmpchk(self,pre=0)->None:
        '''check input and run compile for command compile'''
        pth=self.cmpvars[0].get()
        if not pth: self.mb('w','o','提示','请检查输入的内容'); return
        flnm,ext=os.path.splitext(pth); args=self.cmpvars[1].get()
        if ext=='.c': gcc='gcc'
        elif ext=='.cpp': gcc='g++'
        else: self.mb('w','o','提示','请检查输入的内容'); return
        try: fl=open(pth,'rb')
        except: return
        data=fl.read(); fl.close(); enc=chardet.detect(data)['encoding']
        enc=f'-finput-charset={enc} -fexec-charset={enc}'
        if self.cmpknd.get(): cmd=f'{gcc} {enc} -o \"{flnm}.exe\" \"{pth}\" {args}'
        else: cmd=f'{gcc} {enc} -shared -o \"{flnm}.dll\" \"{pth}\" {args}'
        self.wm.after(0,self.clear,self.cmptre)
        self.wm.after(0,self.cmpout,cmd,self.cmptre,'green')
        if pre: return
        self.cmdout(cmd,self.cmptre)
    def cmpil(self)->None:
        '''command compile'''
        cmp,cmpemp=self.cretpl('编译链接库',21,18,'cmpil',1,5)
        cmptx,cmpbtx=['编译类型','选择文件','其它参数'],['浏览','预览','开始','退出']
        self.cmpknd=tkinter.IntVar(value=0); cmppre=lambda: self.cmpchk(pre=1)
        self.cmpvars=[tkinter.StringVar() for i in range(2)]; cmpknd=['.dll','.exe']
        cmpcmd=[self.cmpadd,self.thr(cmppre),self.thr(self.cmpchk),
                lambda: self.wmqut(cmp,'cmpil')]
        for i in range(3): cmplb=ttk.Label(cmpemp[i],text=cmptx[i]); self.pck(cmplb)
        for i in range(2):
            cmprdb=ttk.Radiobutton(cmpemp[0],text=cmpknd[i],width=18)
            cmprdb.config(variable=self.cmpknd,value=i); self.pck(cmprdb)
            cmpet=ttk.Entry(cmpemp[i+1],textvariable=self.cmpvars[i],width=30); self.pck(cmpet)
            cmpbtn=ttk.Button(cmpemp[i+1],text=cmpbtx[i],command=cmpcmd[i]); self.pck(cmpbtn)
            cmpbtn=ttk.Button(cmpemp[4],text=cmpbtx[i+2],command=cmpcmd[i+2]); self.pck(cmpbtn)
        self.cmptre=self.cretre(cmpemp[3])
        self.show(self.cmptre,'purple','>>>'); self.empck(cmpemp)
    def cmpout(self,tx:str,tag:ttk.Treeview,cl:str)->None:
        '''multiline print'''
        idx=0; tmptx=tx[idx:idx+45]
        while tmptx: self.show(tag,cl,tmptx); idx+=45; tmptx=tx[idx:idx+45]
    def cretpl(self,tle:str,w:int,h:int,wid:str,re:int,num:int)->tuple[tkinter.Toplevel,list[ttk.Frame]]:
        '''create toplevel and frame'''
        tpl=tkinter.Toplevel(self.wm); tpl.withdraw(); tpl.geometry(self.calsz(w,h,wid))
        tpl.resizable(re,re); tpl.transient(self.wm); tpl.title(tle)
        tpl.protocol('WM_DELETE_WINDOW',lambda: self.wmqut(tpl,wid))
        if self.bgidx:
            tpl.update(); val=ctypes.c_int(2); prt=ctypes.windll.user32.GetParent(tpl.winfo_id())
            ctypes.windll.dwmapi.DwmSetWindowAttribute(prt,20,ctypes.byref(val),ctypes.sizeof(val))
        tpl.deiconify(); emps=[ttk.Frame(tpl) for i in range(num)]; return tpl,emps
    def cretre(self,tag:ttk.Frame)->ttk.Treeview:
        '''create treeview with a xview side scrollbar'''
        slb=tkinter.Scrollbar(tag)
        tre=ttk.Treeview(tag,columns=('opt',),show='tree',yscrollcommand=slb.set)
        slb.config(command=tre.yview); tre.column('#0',width=0,stretch=0)
        tre.column('opt',width=30*self.scfac,anchor='w')
        for i in self.data['clr']: tre.tag_configure(i,foreground=i,background=self.bg)
        tre.bind('<Control-c>',lambda *args: self.cpy(tre))
        slb.pack(side='right',fill='y'); tre.pack(fill='both',expand=1)
        return tre
    def cpy(self,tag:ttk.Treeview)->str:
        scl=tag.selection()
        if scl:
            val=tag.item(scl[0],'values')
            self.wm.clipboard_clear()
            self.wm.clipboard_append(val)
        return 'break'
    @staticmethod
    def dlg(knd:int,tl:str,tp:tuple[str,str])->str:
        '''open and save file or directory path'''
        if knd==0: pth=filedialog.askdirectory(title=tl)
        elif knd==1: pth=filedialog.askopenfilename(title=tl,filetypes=(tp,))
        else: pth=filedialog.asksaveasfilename(title=tl,filetypes=(tp,))
        return pth
    @staticmethod
    def encucd(tx:str)->str:
        '''unicode encoder for text manager'''
        ltx=len(tx); res=['']*ltx
        for i in range(ltx): res[i]=f'\\u{ord(tx[i]):04x}'
        return ''.join(res)
    def fclose(self)->None:
        '''close file for text editor'''
        if not self.onfile: return
        if self.modify:
            state=self.mb('q','ync','关闭文件时保存','未保存的内容将会丢失,是否保存?')
            if state=='yes':
                if self.newfl:
                    flnmtmp=self.dlg(2,'保存',('All text files','*.*'))
                    if not flnmtmp: return
                    if not os.path.splitext(flnmtmp)[1]: flnmtmp+='.txt'
                    self.flnm=flnmtmp
                fl=open(self.flnm,'w',encoding='utf-8',newline='\n')
                tx=self.edtr.get('1.0','end'); fl.write(tx); fl.close()
            elif state=='cancel': return
        self.edtr.delete('1.0','end'); self.modify=0
        self.wmemp[1].pack_forget(); self.onfile=0; self.wm.title(self.data['tle'])
    def fopen(self,ext=0,nda=0,opn=None)->None:
        '''open file for text editor'''
        self.onfile=1; self.wmemp[1].pack(fill='both',expand=1)
        if self.modify:
            state=self.mb('q','ync','关闭文件时保存','上一个未保存的内容将会丢失,是否保存?')
            if state=='yes':
                try: self.fsave()
                except: self.wm.title(f"{self.data['tle']} - {self.flnm}*"); return
            elif state=='cancel': self.wm.title(f"{self.data['tle']} - {self.flnm}*"); return
        self.modify=0; self.flnm='未命名文件'; self.edtr.delete('1.0','end')
        if ext:
            if opn is None: flnmtmp=self.dlg(1,'打开',('All text files','*.*'))
            else: flnmtmp=opn
            try: fl=open(flnmtmp,'rb'); self.flnm=flnmtmp
            except: self.wm.title(f"{self.data['tle']} - {self.flnm}"); return
            data=fl.read(); fl.close(); enc=chardet.detect(data)['encoding']; self.newfl=0
            dataln=data.decode(enc,errors='backslashreplace').splitlines()
            for i in dataln: self.edtr.insert('end',i+'\n')
        else:
            if nda:
                try: data=self.txcpt('',1,opn)
                except: return
                self.edtr.insert('insert',data)
            else: self.newfl=1
        self.wm.title(f"{self.data['tle']} - {self.flnm}")
    def fsave(self,copy=0,nda=0)->None:
        '''file save for text editor'''
        if not self.onfile: return
        if nda:
            try: self.txcpt(self.edtr.get('1.0','end'),clos=1); return
            except: return
        if self.newfl or copy:
            flnmtmp=self.dlg(2,'保存',('All text files','*.*'))
            if not flnmtmp: return
            if not os.path.splitext(flnmtmp)[1]: flnmtmp+='.txt'
            self.flnm=flnmtmp; self.wm.title(f"{self.data['tle']} - {self.flnm}")
        fl=open(self.flnm,'w',encoding='utf-8',newline='\n'); self.newfl=self.modify=0
        tx=self.edtr.get('1.0','end'); fl.write(tx); fl.close()
    def funset(self)->None:
        '''initialize useful function'''
        self.clrtul=lambda: (self.tul.reset(),self.tul.ht(),self.tul.speed(0),self.tul.penup())
        self.delmark=lambda tag: self.edtr.tag_remove('match',tag[0],tag[1]) if tag[0] else None
        self.empck=lambda tags: [i.pack(fill='both',expand=1) for i in tags]
        self.fulnm=lambda pth,flnm: os.path.join(pth,flnm)
        self.pck=lambda tag: tag.pack(side='left',expand=1)
        self.scl=lambda tag: (tag.focus_set(),tag.selection_range(0,'end'))
        self.show=lambda tag,clr,*args: tag.see(tag.insert('','end',values=args,tags=(clr,)))
        self.thr=lambda fun,*args: lambda: threading.Thread(target=fun,args=args).start()
        self.web=lambda tag: webbrowser.open(self.data[tag])
    def getvar(self,var:tkinter.StringVar,tag:tkinter.Toplevel,arg:str,knd:type)->None:
        '''get value of entry string variable'''
        res=var.get()
        try:
            if not res: self.mb('w','o','提示','请检查输入的内容'); return
            self.val=knd(res); self.wmqut(tag,arg)
        except: self.mb('w','o','提示','请检查输入的内容')
    def hlp(self)->None:
        '''help page'''
        hlp,hlpemp=self.cretpl('帮助',36,36,'hlp',1,1); hlptx=self.data['hlp']
        hlpmnu=tkinter.Menu(hlp); hlp.config(menu=hlpmnu)
        hlpmnus={'帮助内容':{i:lambda knd=hlptx[i]: self.hlpshw(knd) for i in hlptx},
                 '选项':{'退出':lambda: self.wmqut(hlp,'hlp')}}
        for i in hlpmnus:
            mnutmp=tkinter.Menu(hlpmnu,tearoff=0,bg=self.bgin,fg=self.fg)
            hlpmnu.add_cascade(label=i,menu=mnutmp)
            for j in hlpmnus[i]: mnutmp.add_command(label=j,command=hlpmnus[i][j])
        self.hlptre=self.cretre(hlpemp[0]); self.hlpshw('F'); self.empck(hlpemp)
    def hlpshw(self,knd:str)->None:
        '''print help message'''
        self.clear(self.hlptre,sgn=0); mdfls={'D':'README.md','N':'NEW.md'}
        if knd in mdfls:
            try: fl=open(mdfls[knd],'r',encoding='utf-8')
            except: self.mb('e','o','错误',f'{mdfls[knd]}不存在'); return
            self.hlptre.column('opt',anchor='w'); ln=fl.readline(); flg=0
            while ln:
                if ln=='\n' or ln.startswith('!'): ln=fl.readline(); continue 
                elif ln.startswith('```'): flg=1-flg
                elif flg: self.show(self.hlptre,'green',ln)
                else:
                    tx=''
                    for i in ln:
                        if i in '#*`- ': continue
                        tx+=i
                    self.show(self.hlptre,'green',tx)
                ln=fl.readline()
            fl.close()
        else:
            self.hlptre.column('opt',anchor='c')
            for i in self.data['hlps'][knd]: self.show(self.hlptre,'green',i)
    def hshgen(self):
        '''generate crypted hash code'''
        licc,ltmp,lhdg,hsh=len(self.data['icc']),0,64,hashlib.sha256()
        while 1:
            if lhdg==64:
                lhdg=0; hsh.update(self.data['icc'][ltmp%licc].encode())
                ltmp+=1; hdg=hsh.hexdigest()
            yield int(hdg[lhdg:lhdg+2],16)
            lhdg+=2
    def icc(self,show:int,new=0)->None:
        '''display icon icc'''
        if not show: self.ice(new); return
        self.wmemp[0].pack_forget(); szfun=lambda x: round(x*self.scfac)
        self.clrtul(); self.cvs.pack(fill='both',expand=1)
        self.icon(self.data['icc'],60,szfun(0.5),iter('d'))
        self.wm.after(500,self.icd,szfun,new)
    def icd(self,szfun,new:int)->None:
        '''display icon icd'''
        self.clrtul(); self.icon('l041r24l30',45,szfun(0.6),iter('d'))
        self.icon(self.data['icd'],90,self.scfac,iter('dwdwd'))
        self.tul.rt(45); self.tul.fd(12*self.scfac)
        chrc,chre='圣·西门科技股份有限公司 出品','Sig·WestGate Tech. L.C.D. present.'
        self.tul.write(chrc,align='center',font=('华文行楷',szfun(0.8)))
        self.tul.fd(szfun(2.2))
        self.tul.write(chre,align='center',font=('Consolas',szfun(0.7),'bold'))
        self.wm.after(1200,self.ice,new)
    def ice(self,new:int)->None:
        '''deal system argument'''
        self.cvs.pack_forget(); self.clrtul(); self.admenu()
        self.wmemp[0].pack(side='bottom',fill='both',expand=1)
        if new and len(sys.argv)>1:
            fl=sys.argv[1].strip('\"')
            if fl.endswith('.nda'): self.fopen(nda=1,opn=fl)
            else:
                fl=open(sys.argv[1],'rb')
                cnt,tol,byte,chs=0,0,bytearray(fl.read()),[9,10,13]; fl.close()
                for i in byte:
                    tol+=1
                    if i<32 and i not in chs: cnt+=1
                if tol==0 or cnt/tol<0.001: self.fopen(ext=1,opn=fl)
                else: self.mb('w','o','文件类型不正确','可能是非文本文件')
    def icon(self,iccd:str,ang:int,sz:int,clr)->None:
        '''use python turtle to draw icon'''
        cmds={'b':lambda a: (self.tul.begin_fill(),self.tul.pendown()),
              'e':lambda a: (self.tul.end_fill(),self.tul.penup()),
              'l':lambda a: (self.tul.lt(int(a[0])*ang),self.tul.fd(int(a[1:])*sz)),
              'r':lambda a: (self.tul.rt(int(a[0])*ang),self.tul.fd(int(a[1:])*sz)),
              'c':lambda a: self.tul.color(clrs[next(clr)])}
        clrs={'d':'#22cefc','w':self.bg}; cmd,dig=cmds['c'],''
        for i in range(len(iccd)):
            if iccd[i].isdigit(): dig+=iccd[i]
            else: cmd(dig); dig,cmd='',cmds[iccd[i]]
        cmd(dig)
    def imgsrt(self)->None:
        '''image sort use multiprocessing library'''
        self.wm.after(0,self.show,self.csl,'cyan','(1/3)打开')
        try:
            pth=self.dlg(0,'打开',('Text files','*.txt'))
            names=[i for i in os.listdir(pth) if i.lower().endswith('.png')]
        except: return
        self.wm.after(0,self.show,self.csl,'cyan','(2/3)排序'); lnm=len(names)
        lnmr,cnt=range(lnm),multiprocessing.cpu_count()
        res,pol=[[None,0,''] for i in lnmr],multiprocessing.Pool(processes=cnt)
        self.wm.after(0,self.pgini,'图片排序',lnm); self.cnt=0
        calbk=lambda *args: self.mulpgu(lnm)
        for i in lnmr:
            nm=self.fulnm(pth,names[i])
            tsk=pol.apply_async(avgs,args=(nm,),callback=calbk)
            res[i][0]=tsk; res[i][2]=nm
        pol.close(); pol.join(); self.wm.after(1000,self.wmqut,self.pg,'pgini')
        for i in lnmr: res[i][1]=res[i][0].get()
        res=sorted(res,key=lambda i:i[1])
        self.wm.after(0,self.show,self.csl,'cyan','(3/3)整理')
        for i in lnmr: os.rename(self.fulnm(pth,res[i][2]),self.fulnm(pth,f'pix{i:04d}.png'))
        names=[i for i in os.listdir(pth) if i.lower().endswith('.png')]
        for i in lnmr: os.rename(self.fulnm(pth,names[i]),self.fulnm(pth,f'pic{i:04d}.png'))
        self.wm.after(0,self.show,self.csl,'red','进程已结束')
        self.wm.after(0,self.show,self.csl,'purple','>>>')
    def iniset(self)->None:
        '''initialize program necessarity'''
        try:
            self.scfac=ctypes.windll.shcore.GetScaleFactorForDevice(0)//5
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
        except: self.scfac=20
        self.wm=tkinter.Tk()
        try: self.wm.iconphoto(1,tkinter.PhotoImage(file='Na.png')); self.wm.withdraw()
        except:
            self.wm.withdraw()
            messagebox.showerror('错误','找不到Na.png'); exit(0)
        try: fld=open('Data.json','r',encoding='utf-8'); self.data=json.load(fld); fld.close()
        except FileNotFoundError:
            messagebox.showerror('错误','找不到Data.json'); exit(0)
        except:
            messagebox.showerror('错误','非法的Data.json\n请检查是否存在语法错误')
            fld.close(); exit(0)
        try: flc=open('Config.json','r',encoding='utf-8'); self.cfg=json.load(flc); flc.close()
        except FileNotFoundError:
            messagebox.showwarning('提示','找不到Config.json')
            if messagebox.askyesno('','是否继续运行?'): self.cfg={}
            else: exit(0)
        except:
            messagebox.showwarning('提示','非法的Config.json\n请检查是否存在语法错误'); flc.close()
            if messagebox.askyesno('','是否继续运行?(会覆盖原有文件)'): self.cfg={}
            else: exit(0)
    def inperr(self,tag:tkinter.Toplevel,arg:str,val=None)->None:
        '''deal windows close without return value'''
        self.val=val; self.wmqut(tag,arg)
    def iso(self)->None:
        '''input for iso calculate'''
        num=self.wminp('基团-CnH2n+1,输入n值',int)
        if num is None: return
        self.thr(self.isocal,num)()
    def isocal(self,num:int)->None:
        '''calculate iso'''
        isonum,liso=numpy.zeros(num+1,dtype=int),1; isonum[0]=1
        for i in range(num):
            isob,isoc,isotmp=0,0,0; isoa=i-2*isoc
            while isoc<=isoa:
                isotmp+=isonum[isoa]*isonum[isob]*isonum[isoc]; isoa,isob=isoa-1,isob+1
                if isoa<isob: isoc+=1; isoa,isob=i-2*isoc,isoc
            isonum[liso],liso=isotmp,liso+1
        self.wm.after(0,self.show,self.csl,'green',f'{isonum[num]}')
        self.wm.after(0,self.show,self.csl,'purple','>>>')
    def itmgen(self)->None:
        '''generate item for Genshin Impact'''
        self.ppts,self.pptlvls,self.itknd=[0]*4,[0]*5,random.randint(0,4)
        mns=self.data['mns'][self.itknd]; self.mn=random.choices(mns[0],weights=mns[1])[0]
        if self.mn==-1: self.mn=random.randint(0,2)
        if self.mn==-2:
            self.mn=random.choice(self.data['elmnkd'])
            if self.mn==' ': self.mn='物理'
            else: self.mn+='元素'
            self.mn+='伤害加成'
        else: self.mn=self.data['name'][self.mn]
        self.lppts,self.nm=0,random.choices((3,4),weights=(4,1))[0]
        while self.lppts<self.nm:
            ppt=random.choices(range(len(self.data['pptpro'])),weights=self.data['pptpro'])[0]
            if ppt not in self.ppts and self.data['name'][ppt]!=self.mn:
                self.pptlvls[self.lppts]=self.data['pptmax'][ppt]*random.choice(self.data['pptupd'])
                self.ppts[self.lppts]=ppt; self.lppts+=1
        self.itmbtn[1].config(state='normal'); self.clear(self.itmtre,sgn=0); self.itmprt()
    def itmprt(self,pptidx=-1)->None:
        '''print item for item strength tool'''
        self.show(self.itmtre,'cyan',f"{self.data['itmknd'][self.itknd]}(+{self.pptlvls[4]})")
        self.show(self.itmtre,'blue',self.mn)
        for i in range(self.lppts):
            ppt=self.data['name'][self.ppts[i]]
            if pptidx!=-1 and i==pptidx: clr='green'
            else: clr='red'
            if ppt[-1]==' ':
                self.show(self.itmtre,clr,f'{ppt[:-1]}+{round(self.pptlvls[i]+0.05,1)}')
            else: self.show(self.itmtre,clr,f'{ppt}+{round(self.pptlvls[i]+0.05,1)}%')
        self.show(self.itmtre,'purple','>>>')
    def itmsth(self)->None:
        '''item strength tool for Genshin Impact'''
        itm,itmemp=self.cretpl('圣遗物强化',16,14,'itmsth',1,3)
        itmbtx=['获取','强化','退出']; self.itmbtn=[ttk.Button]*3
        itmcmd=[self.itmgen,self.itmupd,lambda: self.wmqut(itm,'itmsth')]
        itmlb=ttk.Label(itmemp[0],text='强化结果:'); itmlb.pack(expand=1)
        self.itmtre=self.cretre(itmemp[1])
        for i in range(3):
            self.itmbtn[i]=ttk.Button(itmemp[2],text=itmbtx[i],command=itmcmd[i],width=8)
            self.pck(self.itmbtn[i])
        self.itmbtn[1].config(state='disabled'); self.empck(itmemp)
    def itmupd(self)->None:
        '''upgrage item for item strength tool'''
        self.pptlvls[4]+=4
        if self.pptlvls[4]==20: self.itmbtn[1].config(state='disabled')
        if self.lppts==3:
            while self.lppts!=4:
                ppt=random.choices(range(len(self.data['pptpro'])),weights=self.data['pptpro'])[0]
                if ppt not in self.ppts and self.data['name'][ppt]!=self.mn:
                    sth=random.choice(self.data['pptupd'])
                    self.pptlvls[self.lppts]=self.data['pptmax'][ppt]*sth
                    self.ppts[self.lppts]=ppt; self.lppts+=1
            self.itmprt(pptidx=3)
        else:
            pptup=random.randint(0,3); sth=random.choice(self.data['pptupd'])
            self.pptlvls[pptup]+=self.data['pptmax'][self.ppts[pptup]]*sth
            self.itmprt(pptidx=pptup)
    def lnkcal(self,lnks:str,head:int)->None:
        '''link bubble sort'''
        lnk=json.loads(lnks); llnk,cur=0,head
        while cur!=-1: llnk+=1; cur=lnk[cur][1]
        for i in range(llnk-1,-1,-1):
            p,q=head,-1; r=lnk[p][1]
            for j in range(i):
                if lnk[p][0]>lnk[r][0]:
                    if q==-1: head=r
                    else: lnk[q][1]=r
                    lnk[p][1],lnk[r][1]=lnk[r][1],p; p,r=r,p
                p,q,r=r,p,lnk[r][1]
        self.wm.after(0,self.show,self.csl,'green',f'{lnk},head={head}')
        self.wm.after(0,self.show,self.csl,'purple','>>>')
    def lnksrt(self)->None:
        '''input for link bubble sort'''
        lnks=self.wminp('输入链表')
        if lnks is None: return
        head=self.wminp('输入头地址',int)
        if head is None: return
        self.thr(self.lnkcal,lnks,head)()
    def mb(self,icn:str,tp:str,tle:str,msg:str)->str:
        '''create message box'''
        mbdata=self.data['mb']
        mbtmp=messagebox.Message(icon=mbdata[icn],type=mbdata[tp],title=tle,message=msg)
        res=mbtmp.show(); return res
    def mulpgu(self,cnt:int)->None:
        '''update progressbar for image sort multiprocessing callback'''
        self.cnt+=1
        if not self.cnt%2:
            self.wm.after(0,self.pgupd,self.cnt,f'已完成({self.cnt}/{cnt})','cyan')
    def mzchk(self)->None:
        '''check input for visual maze'''
        args=[0]*6
        try:
            for i in range(6): args[i]=int(self.mzvars[i].get())
            self.wmemp[0].pack_forget(); self.cvs.pack(fill='both',expand=1)
            self.clrtul(); self.mzbtn[0].config(state='disabled')
            self.thr(self.mzgen,args)()
        except: self.mb('w','o','提示','请检查输入的内容'); return
    def mzclr(self,tag:tkinter.Toplevel)->None:
        '''clear and quit for visual maze'''
        self.wmqut(tag,'mzgd'); self.cvs.pack_forget(); self.clrtul()
        self.wmemp[0].pack(side='bottom',fill='both',expand=1)
    def mzgd(self)->None:
        '''visual maze'''
        mz,mzemp=self.cretpl('迷宫可视化',20,8,'mzgd',0,5)
        mzlb=ttk.Label(mzemp[0],text='迷宫设置'); mzlb.pack(expand=1)
        mztx,mzbtx=['迷宫长','迷宫宽','起点x','起点y','终点x','终点y'],['生成','解','退出']
        self.mzbtn=[ttk.Button]*3; self.mzvars=[tkinter.StringVar() for i in range(6)]
        mzcmd=[self.mzchk,self.thr(self.mzslv),lambda: self.mzclr(mz)]
        for i in range(6):
            mzlb=ttk.Label(mzemp[i//2+1],text=mztx[i],width=8); self.pck(mzlb)
            mzet=ttk.Entry(mzemp[i//2+1],width=12,textvariable=self.mzvars[i]); self.pck(mzet)
        for i in range(3):
            self.mzbtn[i]=ttk.Button(mzemp[4],text=mzbtx[i],command=mzcmd[i])
            self.pck(self.mzbtn[i])
        self.mzbtn[1].config(state='disabled'); self.empck(mzemp)
    def mzgen(self,args:list[int])->None:
        '''gen maze for visual maze'''
        self.hgt,self.wth,self.bgx,self.bgy,self.edx,self.edy=args
        self.sz=min(12*self.scfac/self.hgt,12*self.scfac/self.wth)
        self.maze=numpy.ones(shape=(self.hgt*2+1,self.wth*2+1),dtype=int)
        for i in range(self.hgt*2+1):
            for j in range(self.wth*2+1):
                if i in [0,self.hgt*2] or j in [0,self.wth*2]: self.maze[i,j]=0
        self.mzshw(0,0,self.hgt*2+1,self.wth*2+1,self.fg)
        self.mzshw(1,1,self.hgt*2,self.wth*2,self.bg)
        stk,top=numpy.zeros(shape=(self.hgt*self.wth,4),dtype=int),0
        stk[top]=[1,1,self.hgt*2-1,self.wth*2-1]; top+=1
        while top>0:
            top-=1; ltx,lty,rtx,rty=stk[top]
            if rtx-ltx<2 or rty-lty<2: continue
            wllx=random.randint(ltx+1,rtx-1)//2*2; wlly=random.randint(lty+1,rty-1)//2*2
            stk[top]=[wllx+1,wlly+1,rtx,rty]; top+=1; stk[top]=[wllx+1,lty,rtx,wlly-1]; top+=1
            stk[top]=[ltx,lty,wllx-1,wlly-1]; top+=1; stk[top]=[ltx,wlly+1,wllx-1,rty]; top+=1
            for i in range(ltx,rtx+1): self.maze[i,wlly]=0
            for i in range(lty,rty+1): self.maze[wllx,i]=0
            self.mzshw(ltx,wlly,rtx+1,wlly+1,self.fg); self.mzshw(wllx,lty,wllx+1,rty+1,self.fg)
            holes=[(random.randint(ltx,wllx-1)//2*2+1,wlly),
                  (random.randint(wllx+1,rtx)//2*2+1,wlly),
                  (wllx,random.randint(lty,wlly-1)//2*2+1),
                  (wllx,random.randint(wlly+1,rty)//2*2+1)]
            hole=random.randint(0,3)
            for i in range(4):
                if hole-i:
                    emp=holes[i]; self.maze[emp[0],emp[1]]=1
                    self.mzshw(emp[0],emp[1],emp[0]+1,emp[1]+1,self.bg)
        self.maze[self.bgx*2-1,self.bgy*2-1]=1; self.maze[self.edx*2-1,self.edy*2-1]=2
        self.mzshw(self.bgx*2-1,self.bgy*2-1,self.bgx*2,self.bgy*2,'#22cefc')
        self.mzshw(self.edx*2-1,self.edy*2-1,self.edx*2,self.edy*2,'#00ff00')
        self.mzbtn[0].config(state='normal')
        self.mzbtn[1].config(state='normal')
    def mzshw(self,ltx:int,lty:int,rtx:int,rty:int,clr:str)->None:
        '''draw rec for generate maze and solve maze'''
        tpx,tpy=(ltx-self.hgt)*self.sz+22*self.scfac,(lty-self.wth)*self.sz-12*self.scfac
        self.tul.teleport(tpx,tpy); self.tul.fillcolor(clr); self.tul.begin_fill()
        for i in range(2):
            self.tul.fd((rtx-ltx)*self.sz); self.tul.lt(90)
            self.tul.fd((rty-lty)*self.sz); self.tul.lt(90)
        self.tul.end_fill()
    def mzslv(self)->None:
        '''solve maze for visual maze'''
        self.mzbtn[0].config(state='disabled')
        self.mzbtn[1].config(state='disabled')
        dires=[[1,0],[-1,0],[0,1],[0,-1]]
        stk,top=numpy.zeros(shape=(self.hgt*self.wth,3),dtype=int),0
        f=lambda j: dires[dire][j]+(dires[dire][j]<0)
        g=lambda j: dires[dire][j]*2+1-(dires[dire][j]<0)
        stk[top]=[self.bgx*2-1,self.bgy*2-1,0]; flg=0
        while top>=0:
            tmpx,tmpy,dire=stk[top]; self.maze[tmpx][tmpy]=0
            if flg:
                self.mzshw(tmpx+f(0),tmpy+f(1),tmpx+g(0),tmpy+g(1),'#22cefc')
                top-=1; continue
            if dire==4: top-=1; continue
            if not self.maze[tmpx+dires[dire][0]][tmpy+dires[dire][1]]:
                stk[top][2]=dire+1; continue
            if self.maze[tmpx+dires[dire][0]*2][tmpy+dires[dire][1]*2]==2: flg=1; continue
            self.maze[tmpx+dires[dire][0]][tmpy+dires[dire][1]]=0
            self.mzshw(tmpx+f(0),tmpy+f(1),tmpx+g(0),tmpy+g(1),'#ff00ff')
            if not self.maze[tmpx+dires[dire][0]*2][tmpy+dires[dire][1]*2]:
                stk[top][2]=dire+1; continue
            top+=1; stk[top]=[tmpx+dires[dire][0]*2,tmpy+dires[dire][1]*2,0]
        self.mzbtn[0].config(state='normal')
    def pgini(self,tle:str,tol:int)->None:
        '''progress bar initialize'''
        self.pg,pgemp=self.cretpl(tle,16,13,'pgini',0,3)
        self.pglb=ttk.Label(pgemp[0],text='0.00%'); self.tol=tol/100
        self.pgpgb=ttk.Progressbar(pgemp[1],length=15*self.scfac)
        self.pgtre=self.cretre(pgemp[2]); self.pgpgb['maximum']=tol
        self.pglb.pack(expand=1); self.pgpgb.pack(fill='y',expand=1)
        self.empck(pgemp)
    def pgupd(self,num:int,tx:str,clr:str)->None:
        '''update progress bar'''
        self.pglb.config(text=f'{num/self.tol:.2f}%')
        self.show(self.pgtre,clr,tx); self.pgpgb['value']=num
    def picpt(self)->None:
        '''picture encrypt'''
        self.wm.after(0,self.show,self.csl,'cyan','(1/3)打开')
        try: flnm=self.dlg(1,'打开',('All image files','*.*')); pic=Image.open(flnm)
        except: return
        piarr,hgt,wth=numpy.array(pic),pic.height,pic.width
        self.wm.after(0,self.show,self.csl,'cyan','(2/3)加密')
        lclr=len(piarr[0,0]); hsh=self.hshgen()
        imgmsk=numpy.zeros_like(piarr); self.wm.after(0,self.pgini,'图片加密',hgt)
        for i in range(hgt):
            for j in range(wth):
                for k in range(lclr): imgmsk[i,j,k]=next(hsh)
            if i%2: self.wm.after(0,self.pgupd,i+1,f'已加密{i+1}/{hgt}','cyan')
        pic=Image.fromarray(numpy.bitwise_xor(piarr,imgmsk))
        self.wm.after(1000,self.wmqut,self.pg,'pgini')
        self.wm.after(0,self.show,self.csl,'cyan','(3/3)保存')
        new=self.dlg(2,'保存',('Image files','*.png'))
        if not new: return
        if new.endswith('.png'): pic.save(new)
        else: pic.save(f'{new}.png')
        self.wm.after(0,self.show,self.csl,'red','进程已结束')
        self.wm.after(0,self.show,self.csl,'purple','>>>')
    def precfg(self)->None:
        '''confirm and reboot for preference setting'''
        state={'白天模式':0,'夜间模式':1,'流转模式':2}
        self.preaply.config(state='disabled')
        self.cfg['bgidx']=state[self.datavar[0].get()]
        self.cfg['font']=self.datavar[1].get()
        for i in range(4): self.cfg[self.fntknds[i]]=self.prevars[i].get()
        self.cfg['ani']=self.anivar.get()
        if self.mb('q','yn','需要重启','是否立即重启以应用设置?')=='yes':
            if self.onfile:
                if self.flnm=='未命名文件': self.flnm+='.txt'
                fl=open(self.flnm,'w',encoding='utf-8')
                fl.write(self.edtr.get('1.0','end')); fl.close()
                self.newfl,self.modify,self.appargs=0,0,self.flnm
            self.reboot=1; self.savcfg()
    def preset(self)->None:
        '''preference setting'''
        pre,preemp=self.cretpl('选项',18,9,'preset',1,6)
        pretx=['UI显示模式','字体']; preoptx=[self.data['modes'],self.data['fonts']]
        optshw=[preoptx[0][self.cfg['bgidx']],self.cfg['font']]
        prebtx=['是否粗体','斜体','下划线','删除线']
        self.datavar=[tkinter.StringVar(value=optshw[i]) for i in range(2)]
        self.prevars=[tkinter.IntVar(value=self.cfg[self.fntknds[i]]) for i in range(4)]
        self.anivar=tkinter.IntVar(value=self.cfg.get('ani',1))
        enable=lambda *args: self.preaply.config(state='normal')
        for i in range(2):
            prelb=ttk.Label(preemp[i],text=pretx[i],width=15)
            preopt=ttk.OptionMenu(preemp[i],self.datavar[i],optshw[i],*preoptx[i])
            preopt['menu'].configure(bg=self.bgin,fg=self.fg)
            preopt.config(width=22); self.pck(prelb); self.pck(preopt)
            self.datavar[i].trace('w',enable)
        for i in range(4):
            prebtn=ttk.Checkbutton(preemp[2],variable=self.prevars[i],command=enable)
            prebtn.config(text=prebtx[i]); self.pck(prebtn)
        anibtn=ttk.Checkbutton(preemp[3],variable=self.anivar,command=enable,width=41)
        anibtn.config(text='是否启用动画'); prelb=ttk.Label(preemp[4],text='部分选项需重启后生效')
        self.preaply=ttk.Button(preemp[5],text='应用',command=self.precfg,state='disabled')
        clrbtn=ttk.Button(preemp[5],text='取消',command=lambda: self.wmqut(pre,'preset'))
        self.pck(anibtn); self.pck(prelb); self.pck(self.preaply); self.pck(clrbtn)
        self.empck(preemp)
    def pro(self,args:list[int])->None:
        '''calculate pull for probility'''
        global protmp,pullst; respro=numpy.zeros(52,dtype=float)
        stn,pbl,puts,fu,tu=args; self.procfm.config(state='disabled')
        lpro,st,ed=0,0,50; pbl+=stn//160; pullst[lpro]=[0,puts,fu,tu]
        prolst[lpro]=1; lpro+=1; self.wm.after(0,self.pgini,'抽卡模拟',pbl)
        for i in range(pbl):
            for j in range(lpro):
                upnum,put,false_up,true_up=pullst[j]; lstpro=prolst[j]
                upnum=min(upnum,50); putpro=self.data['pro_lst5'][put]
                tu_pro=self.data['tu_lst'][false_up]
                protmp[upnum,put+1,false_up,true_up]+=lstpro*(1-putpro)
                if true_up: protmp[upnum+1,0,false_up,0]+=lstpro*putpro
                else:
                    protmp[upnum,0,false_up+1,1]+=lstpro*putpro*(1 - tu_pro)
                    protmp[upnum+1,0,0,0]+=lstpro*putpro*tu_pro
            lpro=0
            for j in range(52):
                for t in range(90):
                    for p in range(4):
                        for k in range(2):
                            if protmp[j,t,p,k]!=0:
                                pullst[lpro]=[j,t,p,k]; prolst[lpro]=protmp[j,t,p,k]
                                lpro+=1; protmp[j,t,p,k]=0
            if i%2: self.wm.after(0,self.pgupd,i+1,f'已完成{i+1}抽','cyan')
        for i in range(lpro): respro[pullst[i,0]]+= prolst[i] * 100
        for i in range(ed+1):
            if respro[i]>0.1: st=i; break
        for i in range(ed,0,-1):
            if respro[i]<0.1: respro[i-1]+=respro[i]
            else: ed=i; break
        self.wm.after(1000,self.wmqut,self.pg,'pgini')
        self.wm.after(0,self.show,self.csl,'purple','UP数 概率')
        for i in range(st,ed+1):
            self.wm.after(0,self.show,self.csl,'purple',f'{i:>2d}{respro[i]:7.2f}%')
        self.wm.after(0,self.show,self.csl,'purple','>>>')
        self.procfm.config(state='normal')
    def prochk(self)->None:
        '''check input for pull for probility'''
        limit=[89,3,1]; args=[0]*5
        for i in range(5):
            val=self.provars[i].get()
            if (not val.isdigit()) or int(val)<0: self.mb('w','o','提示','请检查输入的内容'); return
            if i>1 and int(val)>limit[i-2]: self.mb('w','o','提示','请检查输入的内容'); return
            args[i]=int(val)
        self.thr(self.pro,args)()
    def progd(self)->None:
        '''pull for probility tool for Genshin Impact'''
        pro,proemp=self.cretpl('抽卡概率计算',20,9,'progd',0,6)
        self.provars=[tkinter.StringVar() for i in range(5)]
        probtx=['原石数','粉球数','垫池数(0-89)','已经连歪数(0-3)','是否大保底(0/1)']
        for i in range(5):
            prolb=ttk.Label(proemp[i],text=probtx[i],width=15); self.pck(prolb)
            proet=ttk.Entry(proemp[i],width=30,textvariable=self.provars[i]); self.pck(proet)
        self.procfm=ttk.Button(proemp[5],text='确认',command=self.prochk)
        probtn=ttk.Button(proemp[5],text='退出',command=lambda: self.wmqut(pro,'progd'))
        self.pck(self.procfm); self.pck(probtn); self.empck(proemp)
    def pul(self,num:int)->None:
        '''generate pull'''
        for i in range(num):
            kndpro,trupro=random.random(),random.random()
            if kndpro<=self.data['pro_lst5'][self.put5]:
                if self.true_up5: self.show(self.pultre,'yellow',self.ups[0]); self.true_up5=0
                elif trupro<=self.data['tu_lst'][self.fu]:
                    self.show(self.pultre,'yellow',self.ups[0]); self.true_up5=self.fu=0
                else:
                    fal_up=random.choice(self.data['fups5']+self.data['wpns5'])
                    self.show(self.pultre,'yellow',fal_up); self.show(self.pultre,'red','歪')
                    self.true_up5,self.fu=1,self.fu+1
                self.put5,self.put4=0,self.put4+1
            elif kndpro<=self.data['pro_lst5'][self.put5]+self.data['pro_lst4'][self.put4]:
                if trupro<=0.5 or self.true_up4:
                    self.show(self.pultre,'purple',random.choice(self.ups[1:])); self.true_up4=0
                else:
                    fal_up=random.choice(self.data['ups4']+self.data['wpns4'])
                    self.show(self.pultre,'purple',fal_up); self.true_up4=1
                self.put5,self.put4=self.put5+1,0
            else:
                self.show(self.pultre,'blue',random.choice(self.data['wpns3']))
                self.put5,self.put4=self.put5+1,self.put4+1
        self.show(self.pultre,'cyan',f'垫{self.put5}发'); self.show(self.pultre,'purple','>>>')
    def pulgd(self)->None:
        '''pull for tools for Genshin Impact'''
        pul,pulemp=self.cretpl('抽卡模拟器',16,14,'pulgd',1,3)
        pultx,pulbtx=['五星UP','四星UP1','四星UP2','四星UP3'],['祈愿一次','祈愿十次','退出']
        puldtx=['ups5','ups4','fups5','wpns5','wpns4','wpns3']
        self.ups,self.put5,self.put4,self.true_up5,self.true_up4,self.fu=['']*4,0,0,0,0,0
        pulcmd=[lambda: self.pul(1),lambda: self.pul(10),lambda: self.wmqut(pul,'pulgd')]
        self.pulbtn=[ttk.Button]*3; pulmnu=tkinter.Menu(pul); pul.config(menu=pulmnu)
        pulmnus=[tkinter.Menu(pul,tearoff=0,bg=self.bgin,fg=self.fg) for i in range(4)]
        for i in range(4): pulmnu.add_cascade(label=pultx[i],menu=pulmnus[i])
        for i in puldtx:
            for j in self.data[i]:
                if i=='ups5': pulmnus[0].add_command(label=j,command=lambda k=j: self.adups(k,0))
                elif i=='ups4':
                    for p in range(1,4):
                        pulmnus[p].add_command(label=j,command=lambda k=j,h=p: self.adups(k,h))
        self.pullb=ttk.Label(pulemp[0],text='祈愿结果')
        self.pullb.pack(expand=1); self.pultre=self.cretre(pulemp[1])
        for i in range(3):
            self.pulbtn[i]=ttk.Button(pulemp[2],text=pulbtx[i],width=8,command=pulcmd[i])
            self.pulbtn[i].config(state='disabled'); self.pck(self.pulbtn[i])
        self.pulbtn[2].config(state='normal'); self.empck(pulemp)
    def recmd(self,knd:int)->None:
        '''command for file rename tool'''
        if knd==0:
            exts=self.revars[0].get().split('/')
            flnm=self.dlg(1,'打开',('All files','*.*'))
            if not flnm: return
            ext=os.path.splitext(flnm)[1]
            if ext in exts: return
            exts+=[ext]; self.revars[0].set('/'.join(exts))
        elif knd==1:
            pth=self.dlg(0,'打开',('Text files','*.txt'))
            if not pth: return
            self.revars[1].set(pth)
        else: self.thr(self.renm,1)()
    def redo(self)->None:
        '''redo operation for text editor'''
        if self.onfile:
            try: self.edtr.edit_redo()
            except: self.wm.bell()
    def renm(self,show=0)->None:
        '''generate template and file rename'''
        exts,pth=self.revars[0].get().split('/'),self.revars[1].get()
        tmplt=self.revars[2].get(); ltpl=len(tmplt); newext=[]
        if not (pth and tmplt): self.mb('w','o','提示','请检查输入的内容'); return
        for i in exts:
            if i: newext+=[i]
        try:
            if not newext: names=[i for i in os.listdir(pth)]
            else: names=[i for i in os.listdir(pth) if os.path.splitext(i)[1] in newext]
        except: return
        names=[[i,''] for i in names if os.path.isfile(self.fulnm(pth,i))]
        keys=['name','index','ext','Y_a','m_a','D_a','H_a','M_a','S_a','Y_m',
              'm_m','D_m','H_m','M_m','S_m','Y_c','m_c','D_c','H_c','M_c','S_c']
        i,form,args,lnms=0,'','',len(names)
        while i<ltpl:
            form+=tmplt[i]
            if tmplt[i]=='{':
                for j in keys:
                    if tmplt[i+1:].startswith(j): args+=j+'/'; i+=len(j)
            i+=1
        args=args[:-1].split('/'); argfun=lambda arg: consts[arg]
        for i in range(lnms):
            nm=names[i][0]
            consts,times,knds={},'YmDHMS','amc'
            fltime={'a':time.localtime(os.path.getatime(self.fulnm(pth,nm))),
                    'm':time.localtime(os.path.getmtime(self.fulnm(pth,nm))),
                    'c':time.localtime(os.path.getctime(self.fulnm(pth,nm)))}
            gett={'Y':lambda tme:tme.tm_year,'m':lambda tme:tme.tm_mon,'D':lambda tme:tme.tm_mday,
                  'H':lambda tme:tme.tm_hour,'M':lambda tme:tme.tm_min,'S':lambda tme:tme.tm_sec}
            for j in knds:
                for k in times: consts[f'{k}_{j}']=gett[k](fltime[j])
            consts['ext']=os.path.splitext(nm)[1][1:]; consts['name']=os.path.splitext(nm)[0]
            consts['index']=i; names[i][1]=form.format(*list(map(argfun,args)))+'.'+consts['ext']
        if show:
            tx='预览效果:'
            for i in range(min(lnms,5)): tx+=f'\n{names[i][0]} -> {names[i][1]}'
            tx+=('' if lnms else '\n没有预览')+'\n是否使用?'
            if self.mb('q','yn','模板预览',tx)=='no': return
        if lnms:
            self.wm.after(0,self.pgini,'视频重命名',lnms); cnt=0
            for i in range(lnms):
                try:
                    os.rename(self.fulnm(pth,names[i][0]),self.fulnm(pth,names[i][1]))
                    self.wm.after(0,self.pgupd,i+1,f'{names[i][0]} -> {names[i][1]}','cyan')
                except: cnt+=1
            self.wm.after(1000,self.wmqut,self.pg,'pgini')
            if cnt: self.mb('w','o','重命名',self.data['failmsg'].format(lnms-cnt,cnt))
        self.wm.after(0,self.show,self.csl,'red','进程已结束')
        self.wm.after(0,self.show,self.csl,'purple','>>>')
    def renmgd(self)->None:
        '''file rename tool'''
        re,reemp=self.cretpl('批量重命名',24,7,'renmgd',0,4)
        revar=tkinter.StringVar(); self.revars=[tkinter.StringVar() for i in range(3)]
        retx,rebtx=['文件后缀(用/分隔)','目录','命名模板'],['重命名','取消']
        revarcmd=[self.thr(self.renm),lambda: self.wmqut(re,'renmgd')]
        refun=lambda *args: self.revars[2].set(self.data['tmplts'][int(revar.get()[0])-1])
        for i in range(3):
            recmd=lambda k=i: self.recmd(k); tx='浏览' if i-2 else '预览'
            relb=ttk.Label(reemp[i],text=retx[i],width=16); self.pck(relb)
            reet=ttk.Entry(reemp[i],width=30,textvariable=self.revars[i]); self.pck(reet)
            rebtn=ttk.Button(reemp[i],text=tx,command=recmd); self.pck(rebtn)
        tmplt=self.data['tmplt']; reopt=ttk.OptionMenu(reemp[3],revar,tmplt[0],*tmplt)
        reopt['menu'].configure(bg=self.bgin,fg=self.fg)
        reopt.config(width=15); revar.trace('w',refun); self.pck(reopt)
        for i in range(2):
            rebtn=ttk.Button(reemp[3],text=rebtx[i],command=revarcmd[i]); self.pck(rebtn)
        self.empck(reemp)
    def ring(self)->None:
        '''input for calculate ring number'''
        num=self.wminp('输入n值(对)',int)
        if num is None: return
        self.thr(self.ringcal,num)()
    def ringcal(self,num:int)->None:
        '''calculate ring number'''
        rmax,flg=0,[1]*(2*num)
        for i in range(2*num):
            tmp,lring=i,0
            while flg[tmp]:
                flg[tmp],lring=0,lring+1
                if tmp<num: tmp*=2
                else: tmp=2*(tmp-num)+1
            rmax=max(rmax,lring)
        self.wm.after(0,self.show,self.csl,'green',f'{rmax}')
        self.wm.after(0,self.show,self.csl,'purple','>>>')
    @staticmethod
    def rndchr(tx:str,num:int)->str:
        '''generate random combinate character for text manager'''
        slst=list(range(768,880))+list(range(1155,1162))
        lres,res=0,['']*len(tx)*(num+1)
        for i in tx:
            res[lres]=i; lres+=1; chs=map(chr,random.choices(slst,k=num))
            for j in chs: res[lres]=j; lres+=1
        return ''.join(res)
    def rome(self)->None:
        '''input for calculate rome number'''
        chs=self.wminp('输入罗马数字')
        if chs is None: return
        self.thr(self.romecal,chs)()
    def romecal(self,chs:str)->None:
        '''calculate rome number'''
        num,stk,top=0,[0]*len(chs),0
        rdic={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000,
             'i':1,'v':5,'x':10,'l':50,'c':100,'d':500,'m':1000}
        for i in chs:
            if i not in rdic: self.mb('w','o','提示','请检查输入的内容'); return
            while top>0 and rdic[i]>stk[top-1]: top-=1; num-=stk[top]
            stk[top]=rdic[i]; top+=1
        while top>0: top-=1; num+=stk[top]
        self.wm.after(0,self.show,self.csl,'green',f'{num}')
        self.wm.after(0,self.show,self.csl,'purple','>>>')
    def rplc(self,al=0)->None:
        '''text replace for text editor'''
        schtx,rplctx=self.schvars[0].get(),self.schvars[1].get()
        ncas,cnt=not self.case.get(),0
        if not (schtx and rplctx): self.mb('w','o','提示','请检查输入的内容'); return
        cur=self.edtr.index('insert'); pos=self.edtr.search(schtx,cur,'end',nocase=ncas)
        if not pos: pos=self.edtr.search(schtx,'1.0',cur,nocase=ncas)
        while pos:
            self.edtr.delete(pos,f'{pos}+{len(schtx)}c'); self.edtr.insert(pos,rplctx)
            aled=f'{pos}+{len(rplctx)}c'; self.edtr.mark_set('insert',aled); cnt+=1
            cur=self.edtr.index('insert'); pos=self.edtr.search(schtx,cur,'end',nocase=ncas)
            if not pos: pos=self.edtr.search(schtx,'1.0',cur,nocase=ncas)
            if not al: break
        if cnt:
            self.chgcfg()
            if al: self.mb('i','o','替换',f'已成功替换{cnt}处文本')
        else: self.mb('i','o','提示','找不到相应的文本')
    def savcfg(self)->None:
        '''save configure after app closed'''
        if self.onfile and self.modify:
            state=self.mb('q','ync','关闭文件时保存','未保存的内容将会丢失,是否保存?')
            if state=='yes':
                if self.newfl:
                    flnmtmp=self.dlg(2,'保存',('All text files','*.*'))
                    if not flnmtmp: return
                    if not os.path.splitext(flnmtmp)[1]: flnmtmp+='.txt'
                    self.flnm=flnmtmp
                fl=open(self.flnm,'w',encoding='utf-8',newline='\n')
                tx=self.edtr.get('1.0','end'); fl.write(tx); fl.close()
            elif state=='cancel': return
        self.wmqut(self.wm,'Fabits')
        fl=open('Config.json','w',encoding='utf-8')
        json.dump(self.cfg,fl,ensure_ascii=0,indent=4); fl.close()
        if self.reboot:
            now=sys.executable
            if sys.argv[0].endswith('.py'):
                if self.appargs: subprocess.Popen([now,sys.argv[0],self.appargs])
                else: subprocess.Popen([now,sys.argv[0]])
            else:
                if self.appargs: subprocess.Popen([now,self.appargs])
                else: subprocess.Popen([now])
            exit(0)
    def sch(self,dire=1,al=0)->None:
        '''search text for text editor'''
        schtx=self.schvars[0].get()
        if not schtx: self.mb('w','o','提示','请检查输入的内容'); return
        st,ed,cur,ncas='1.0','end',self.edtr.index('insert'),not self.case.get()
        if al: pos=self.edtr.search(schtx,st,ed,nocase=ncas)
        elif dire:
            pos=self.edtr.search(schtx,cur+'+1c',ed,nocase=ncas)
            if not pos: pos=self.edtr.search(schtx,st,cur+'+1c',nocase=ncas)
        else:
            pos=self.edtr.search(schtx,cur,st,backwards=1,nocase=ncas)
            if not pos: pos=self.edtr.search(schtx,ed,cur,backwards=1,nocase=ncas)
        if pos:
            self.delmark(self.lastpos); self.edtr.see(pos); self.edtr.mark_set('insert',pos)
            aled=f'{pos}+{len(schtx)}c'; self.edtr.tag_add('match',pos,aled)
            self.edtr.tag_config('match',background='yellow'); self.lastpos=pos,aled
        else: self.mb('i','o','提示','找不到相应的文本')
    def schgd(self)->None:
        '''search and replace text for text editor'''
        if not self.onfile: return
        sch,schemp=self.cretpl('查找与替换',18,7,'schgd',0,5); self.lastpos=('','')
        self.schvars=[tkinter.StringVar() for i in range(2)]
        self.case=tkinter.BooleanVar(value=0)
        schtx,schbtx=['查找','替换为'],['向上查找','向下查找','从头查找','替换','全部替换','退出']
        schqut=lambda: (self.delmark(self.lastpos),self.wmqut(sch,'schgd'))
        schcmd=[lambda: self.sch(dire=0),self.sch,lambda: self.sch(al=1),
                self.rplc,lambda: self.rplc(al=1),schqut]
        for i in range(2):
            schlb=ttk.Label(schemp[i],text=schtx[i],width=8); self.pck(schlb)
            schet=ttk.Entry(schemp[i],width=30,textvariable=self.schvars[i]); self.pck(schet)
        schbtn=ttk.Checkbutton(schemp[2],variable=self.case,text='是否区分大小写',width=40)
        self.pck(schbtn)
        for i in range(6):
            schbtn=ttk.Button(schemp[3+i//3],text=schbtx[i],command=schcmd[i]); self.pck(schbtn)
        sch.protocol('WM_DELETE_WINDOW',schqut); self.empck(schemp)
    def txcmd(self,knd:int,idx:int)->None:
        '''open or save file for text manager'''
        args=['打开','保存']; pth=self.dlg(knd+1,args[knd],('All text files','*.*'))
        if not pth: return
        self.txet[knd][idx].delete(0,'end'); self.txet[knd][idx].insert(0,pth)
    def txcpt(self,byte:str,opn=0,clos=0,opnfl='')->str|None:
        '''text encrypt for text manager and import and export nda'''
        if opn:
            if opnfl=='': flnm=self.dlg(1,'打开',('Nahida Data Assets','*.nda'))
            else: flnm=opnfl
            fl=open(flnm,'rb'); byte=fl.read(); fl.close()
        else: byte=byte.encode('utf-8')
        bytarr=bytearray(byte); gn=self.hshgen()
        bytarr=[i^next(gn) for i in bytarr]; byte=bytes(bytarr)
        if clos:
            if opn:
                flnm=self.dlg(2,'保存',('All text files','*.*'))
                if not os.path.splitext(flnm)[1]: flnm+='.txt'
            else:
                flnm=self.dlg(2,'保存',('Nahida Data Assets','*.nda'))
                if not flnm.endswith('.nda'): flnm+='.nda'
            fl=open(flnm,'wb'); fl.write(byte); fl.close()
        else: return byte.decode('utf-8',errors='backslashreplace')
    def txinp(self)->None:
        '''input for text manager'''
        tx,new,num=self.txet[0][1].get(),'',0
        if not self.txvars[0].get():
            tx=self.txet[0][0].get()
            if not tx: self.mb('w','o','提示','请检查输入的内容'); return
        if self.txvars[1].get():
            new=self.txet[1][1].get()
            if not new: return
        funknd=int(self.txfun.get()[0])-1
        if funknd==1:
            num=self.wminp('输入字符密度',int)
            if num is None: return
        self.thr(self.txpre,tx,new,num,funknd)()
    def txmng(self)->None:
        '''text manager'''
        tx,txemp=self.cretpl('文本处理',24,11,'txmng',0,7)
        self.txet=[[ttk.Entry]*2,[ttk.Entry]*2]
        self.txvars=[tkinter.IntVar(value=0) for i in range(2)]
        self.txfun=tkinter.StringVar(); txbtx=['生成','退出']
        txtx=['打开方式','文本输入','文件打开','保存方式','文本输出','文件保存']
        txfun=['1.编unicode','2.生成组合字符','3.解unicode','4.文本加解密']
        txcmd=[self.txinp,lambda: self.wmqut(tx,'txmng')]
        for i in range(2):
            txlb=ttk.Label(txemp[3*i],text=txtx[i]); self.pck(txlb)
            for j in range(2):
                mngrd=lambda knd=i,idx=j: self.txrdcmd(knd,idx)
                txbtn=ttk.Radiobutton(txemp[3*i+j+1],text=txtx[i])
                txbtn.config(variable=self.txvars[i],value=j,command=mngrd)
                self.pck(txbtn); self.txet[i][j]=ttk.Entry(txemp[3*i+j+1],width=30)
                if j: btx='浏览'; cmd=lambda knd=i,idx=j: self.txcmd(knd,idx)
                else: btx='全选'; cmd=lambda knd=i,idx=j: self.scl(tag=self.txet[knd][idx])
                txbtn=ttk.Button(txemp[3*i+j+1],text=btx,command=cmd)
                self.pck(self.txet[i][j]); self.pck(txbtn)
            self.txet[i][1].config(state='disabled')
        txopt=ttk.OptionMenu(txemp[6],self.txfun,txfun[0],*txfun)
        txopt['menu'].configure(bg=self.bgin,fg=self.fg); self.pck(txopt)
        for i in range(2):
            txbtn=ttk.Button(txemp[6],text=txbtx[i],command=txcmd[i]); self.pck(txbtn)
        self.empck(txemp)
    def txpre(self,tx:str,new:str,num:int,funknd:int)->None:
        '''set open and close format for text manager'''
        funs=[self.encucd,lambda tx: self.rndchr(tx,num),self.ucd,self.txcpt]
        if self.txvars[0].get():
            try: fl=open(tx,'rb')
            except: return
            data=fl.read(); fl.close(); enc=chardet.detect(data)['encoding']
            tx=data.decode(enc)
        else: enc='utf-8'
        res=funs[funknd](tx)
        if self.txvars[1].get():
            if not os.path.splitext(new)[1]: new+='.txt'
            fl=open(new,'w',encoding=enc); fl.write(res); fl.close()
        else:
            self.txet[1][0].delete(0,'end'); self.txet[1][0].insert('end',res)
        self.wm.after(0,self.show,self.csl,'red','进程已结束')
        self.wm.after(0,self.show,self.csl,'purple','>>>')
    def txrdcmd(self,idx:int,knd:int)->None:
        '''command for text manager radiobutton'''
        self.txet[idx][knd].config(state='normal')
        self.txet[idx][1-knd].config(state='disabled')
    @staticmethod
    def ucd(tx:str)->str:
        '''decode unicode for text manager'''
        ltx=len(tx); lres,res,i=0,['']*ltx,0
        while i<ltx:
            if ltx-i>5 and tx[i:i+2]=='\\u': res[lres]=chr(int(tx[i+2:i+6],16)); i+=6
            else: res[lres]=tx[i]; i+=1
            lres+=1
        return ''.join(res)
    def undo(self)->None:
        '''undo operation for text editor'''
        if self.onfile:
            try: self.edtr.edit_undo()
            except: self.wm.bell()
    def upd(self)->None:
        '''check update for app'''
        try:
            resp=requests.get(self.data['latest']); data=resp.json(); latvsn=data['tag_name']
            if latvsn==self.data['curvsn']: self.mb('i','o','提示','当前已经是最新版本')
            elif self.mb('i','yn','提示','有新版本!是否前往项目仓库下载?')=='yes':
                webbrowser.open(self.data['proj']+'/releases/latest')
        except:
            if self.mb('w','yn','无法连接服务器','是否重试?')=='yes': self.upd()
    def wminp(self,st:str,knd=str,show='')->any:
        '''a simple variable input widget'''
        inp,inpemp=self.cretpl('',18,5,'wminp',0,3); inpbtx=['全选','确认','取消']
        inplb=ttk.Label(inpemp[0],text=st); self.inpvar=tkinter.StringVar(value=show)
        inpet=ttk.Entry(inpemp[1],width=40,textvariable=self.inpvar)
        inpcmd=[lambda: self.scl(inpet),lambda: self.getvar(self.inpvar,inp,'wminp',knd),
                lambda: self.inperr(inp,'wminp')]
        for i in range(3):
            inpbtn=ttk.Button(inpemp[2],text=inpbtx[i],command=inpcmd[i]); self.pck(inpbtn)
        inplb.pack(expand=1); inpet.pack(expand=1); self.empck(inpemp)
        inp.protocol('WM_DELETE_WINDOW',lambda: self.inperr(inp,'wminp'))
        inp.wait_window(); return self.val
    def wmqut(self,arg,key:str):
        wth,hgt,spacex,spacey=arg.winfo_width(),arg.winfo_height(),arg.winfo_x(),arg.winfo_y()
        self.cfg[key]=f'{wth}x{hgt+self.scfac}+{spacex}+{spacey}'; arg.destroy()
    def wmset(self)->None:
        '''set const and setting for app start'''
        self.scwth,self.schgt=self.wm.winfo_screenwidth(),self.wm.winfo_screenheight()
        scmsg,self.reboot,self.appargs=self.cfg.get('sc',[0,0,0]),0,''
        self.cfg['sc']=[self.scfac,self.scwth,self.schgt]; self.check=scmsg==self.cfg['sc']
        self.fntknds=['bold','italic','underline','overstrike']
        self.bgidx,self.fnt,self.fntknd=self.cfg.get('bgidx',-1),self.cfg.get('font',''),''
        if self.bgidx==-1: self.cfg['bgidx']=self.bgidx=2
        if self.fnt=='': self.cfg['font']=self.fnt='TkDefaultFont'
        for i in self.fntknds:
            if i not in self.cfg: self.cfg[i]=0
            self.fntknd+=f'{i} ' if self.cfg[i] else ''
        if not self.fntknd: self.fntknd='normal'
        if self.bgidx==2: lctime=time.localtime(); self.bgidx=0 if 6<=lctime.tm_hour<18 else 1
        if self.bgidx:
            self.wm.update(); val=ctypes.c_int(2)
            prt=ctypes.windll.user32.GetParent(self.wm.winfo_id())
            ctypes.windll.dwmapi.DwmSetWindowAttribute(prt,20,ctypes.byref(val),ctypes.sizeof(val))
        self.bg=self.data['bg'][self.bgidx]; self.fg=self.data['fg'][self.bgidx]
        self.bgin=self.data['bgin'][self.bgidx]; self.wm.geometry(self.calsz(64,36,'Fabits'))
        self.wm.protocol('WM_DELETE_WINDOW',self.savcfg); self.wm.title(self.data['tle'])
        self.mnu=tkinter.Menu(self.wm); self.wm.config(menu=self.mnu)
        self.wm.deiconify(); self.onfile=self.newfl=self.modify=0; self.flnm='未命名文件'
if __name__=='__main__': Fabits()