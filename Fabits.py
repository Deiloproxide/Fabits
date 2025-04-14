import chardet,ctypes,hashlib,math,multiprocessing,numpy,json,os,random
import requests,subprocess,sys,threading,time,tkinter,turtle,webbrowser
from tkinter import filedialog,ttk; from PIL import Image
lst=numpy.zeros(shape=(38000,4),dtype=int)
proes=numpy.zeros(38000); dic=numpy.zeros(shape=(52,91,5,2))
def avgs(nm): return numpy.mean(numpy.array(Image.open(nm).convert('L'))),nm
class Fabits:
    def __init__(self):
        self.preset(); self.check(); self.rt.geometry(self.calsz(64,36,'Fabits'))
        self.rt.deiconify(); self.prefn(); self.rt.title(self.data['til'])
        self.admnu(); self.adcon(); self.style(); self.ics1(fir=1)
        self.rt.mainloop(); self.savcfg()
    def adcon(self):
        self.cvs=tkinter.Canvas(self.rt); self.sc=turtle.TurtleScreen(self.cvs)
        self.tl=turtle.RawTurtle(self.sc); self.memp1=ttk.Frame(self.rt)
        self.ls=ttk.Treeview(self.memp1,columns=('opt',),show='tree')
        slb=tkinter.Scrollbar(self.memp1); self.ls.column('#0',width=0,stretch=False)
        self.ls.column('opt',width=30*self.scr,anchor='w')
        self.ls.config(yscrollcommand=slb.set); slb.config(command=self.ls.yview)
        self.memp2=ttk.Frame(self.rt); self.tetr=tkinter.Text(self.memp2,undo=True)
        slb2=tkinter.Scrollbar(self.memp2); self.tetr.config(yscrollcommand=slb2.set)
        slb2.config(command=self.tetr.yview); self.tetr.bind('<Key>',lambda s: self.cchg())
        self.ofl=self.nfl=self.chg=0; self.txflnm='未命名文件'; self.show(self.ls,'>>>','purple')
        slb.pack(side='right',fill='y'); self.ls.pack(fill='both',expand=True)
        slb2.pack(side='right',fill='y'); self.tetr.pack(fill='both',expand=True)
    def adfun(self,lbl,knd,mnu):
        mntmp=tkinter.Menu(mnu,tearoff=0,bg=self.bgin,fg=self.txchrc)
        mnu.add_cascade(label=lbl,menu=mntmp)
        for i in knd: mntmp.add_command(label=i,command=knd[i])
    def adlsnd(self):
        self.rt.after(0,self.show,self.ls,'(1/2)打开','cyan')
        try:
            self.pth=self.dlg(0,'打开',('Text files','*.txt'))
            fnames=[i for i in os.listdir(self.pth) if self.tp.isfile(self.pnm(i))]
        except: return
        names=[i for i in fnames if not self.tp.splitext(i)[1]]; hdnms=self.data['hds']
        self.rt.after(0,self.show,self.ls,'(2/2)转换','cyan'); lnm=len(names)
        if lnm:
            self.rt.after(0,self.pginit,'查找添加缺失后缀',lnm)
            for i in range(lnm):
                nm=self.pnm(names[i]); fl=open(nm,'rb'); hd=fl.read(32); fl.close()
                for j in hdnms:
                    if j.encode() in hd:
                        self.rt.after(0,self.pgu,i+1,f"{nm} -> {nm+hdnms[j]}",'cyan')
                        os.rename(nm,nm+hdnms[j]); break
                else: self.rt.after(0,self.pgu,i+1,f"未知文件类型: {names[i]}",'red')
            self.rt.after(250,self.winqut,self.pgm,'pginit')
        self.rt.after(0,self.show,self.ls,'进程已结束','red')
        self.rt.after(0,self.show,self.ls,'>>>','purple')
    def admnu(self):
        self.funknd={
        '文件(F)':{'新建':self.opnf,'打开':lambda: self.opnf(1),'保存':lambda: self.savf(rse=0),
            '另存为':lambda: self.savf(1,rse=0),'导入':lambda: self.opnf(nda=1),
            '导出':lambda: self.savf(nda=1,rse=0),'查找与替换':self.schgd,'撤销':self.undo,
            '重做':self.redo,'关闭':self.clsf,'退出':self.qutmn},
        '算法(A)':{'同分异构体数量':self.iso,'链表冒泡排序':self.lnksrt,
            '最大环长度':self.ring,'求解罗马数字':self.rome},
        '批处理(B)':{'缺失后缀修复':lambda: self.thr(self.adlsnd),
            '图片颜色替换':lambda: self.thr(self.clrplc),'图片排序':lambda: self.thr(self.imgsrt),
            '图片加解密':lambda: self.thr(self.picpt)},
        '网络(I)':{'官网':lambda: webbrowser.open(self.data['ofwb']),
            '项目仓库':lambda: webbrowser.open(self.data['hub']),'检查更新':lambda: self.thr(self.upd)},
        '工具(T)':{'科学计算器':self.calc,'代码混合':self.cdobf,'抽卡模拟器':self.conpuw,
            '圣遗物强化':self.itsth,'迷宫可视化':self.mazepl,'抽卡概率计算':self.pulprogd,
            '批量重命名':self.renmgd,'文本处理':self.txmng},
        '设置(S)':{'清屏':self.clear,'帮助':self.hlp,'图标':self.ics1,'选项':self.prefr}}
        mnu=tkinter.Menu(self.rt); self.rt.config(menu=mnu)
        for i in self.funknd: self.adfun(i,self.funknd[i],mnu)
    def adups(self,i,n):
        if i in self.ups: self.mb('w','o','选择角色重复','请重新选择')
        else: self.ups[n]=i; self.show(self.et,f'角色{i}添加成功!','red')
        for i in self.ups:
            if not i: return
        self.conbtn[0].config(state='normal'); self.conbtn[1].config(state='normal')
    def calc(self):
        cal=self.crttpl('科学计算器',32,12,'calc',1)
        calmnu=tkinter.Menu(cal); cal.config(menu=calmnu)
        calsmu=tkinter.Menu(calmnu,tearoff=0,bg=self.bgin,fg=self.txchrc)
        calmnu.add_cascade(label='选项(O)',menu=calsmu)
        calsmu.add_command(label='精度',command=self.calset)
        calsmu.add_command(label='退出',command=lambda: self.winqut(cal,'calc'))
        self.calshw,caltx=[None]*2,[' ','I']; self.res=self.m=0; self.acc=12
        calcmp=[ttk.Frame(cal) for i in range(8)]
        self.expsyn,self.lexp,self.expidx=[None]*100,0,0
        for i in range(2):
            self.calshw[i]=ttk.Label(calcmp[i],text=caltx[i],anchor='e')
            self.calshw[i].pack(fill='both',expand=True)
        calbtns=[[None]*7 for i in range(7)]
        sig=[['sin','log','!','<','>','←','AC'],['cos','P','C','√','(',')','÷'],
            ['tan','^','7','8','9','e','×'],['arcsin','mod','4','5','6','π','-'],
            ['arccos','|x|','1','2','3','m','+'],['arctan','M',',','0','.','ANS','=']]
        self.funs={'sin':math.sin,'cos':math.cos,'tan':math.tan,'arcsin':math.asin,
              'arccos':math.acos,'arctan':math.atan,'mod':lambda a,b: a%b,
              'log':lambda a,b=math.e: math.log(a,b),'√':lambda a,b=2: a**(1/b)}
        self.bas=[{'C':lambda a,b: math.gamma(a+1)/math.gamma(b+1)/math.gamma(a-b+1),
                 'P':lambda a,b: math.gamma(a+1)/math.gamma(a-b+1)},
                {'^':lambda a,b: a**b},{'×':lambda a,b: a*b,'÷': lambda a,b: a/b},
                {'+': lambda a,b=0: a+b,'-': lambda a,b=None: -a if b is None else a-b}]
        for i in range(6):
            for j in range(7):
                calbtns[i][j]=ttk.Button(calcmp[i+2],text=sig[i][j])
                calbtns[i][j].config(command=lambda k=sig[i][j]: self.syn(k))
                calbtns[i][j].pack(side='left',fill='both',expand=True)
        for i in range(8): calcmp[i].pack(fill='both',expand=True)
    def cald(self,syn,lsyn):
        expsyn,lexp,dig,digs=[None]*100,0,'',1
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
        stk,top,res=[[None,[None]*100,0] for i in range(20)],0,None
        for i in range(lexp):
            if expsyn[i]=='(': top+=1; stk[top][0]=i
            elif expsyn[i]==')':
                if top>0 and expsyn[stk[top][0]]=='(':
                    res=self.calsyn(stk[top][1][:stk[top][2]]); stk[top][2]=0
                    top-=1; stk[top][1][stk[top][2]]=res; stk[top][2]+=1
                else: raise SyntaxError
            elif expsyn[i]=='|':
                if top>0 and expsyn[stk[top][0]]=='|':
                    res=abs(self.calsyn(stk[top][1][:stk[top][2]])); stk[top][2]=0
                    top-=1; stk[top][1][stk[top][2]]=res; stk[top][2]+=1
                else: top+=1; stk[top][0]=i
            else: stk[top][1][stk[top][2]]=expsyn[i]; stk[top][2]+=1
            if top>=20: raise OverflowError
        if top!=0: raise SyntaxError
        return self.calsyn(stk[top][1][:stk[top][2]])
    def calset(self):
        try: self.acc=int(self.inp(f'保留小数位数(当前为{self.acc}位)'))
        except: return
        if self.acc<0: self.acc=0
        if self.acc>15: self.acc=15
    def calsyn(self,expsyn):
        lexp=len(expsyn); tl,rl,tsyn,rsyn,stc=lexp,0,[None]*100,[None]*100,True
        for i in range(lexp):
            tsyn[i]=expsyn[i]
            if expsyn[i]==',': return self.calsyn(expsyn[:i]),self.calsyn(expsyn[i+1:lexp])
        while stc:
            rl,mul=0,1
            for i in range(tl):
                if isinstance(tsyn[i],float): mul*=tsyn[i]
                else:
                    if isinstance(mul,float): rsyn[rl]=mul; rl+=1; mul=1
                    rsyn[rl]=tsyn[i]; rl+=1
            if isinstance(mul,float): rsyn[rl]=mul; rl+=1
            tl,fls,stc=0,False,False
            for i in range(rl):
                if fls: fls=False; continue
                if i<rl-1 and rsyn[i+1]=='!':
                    if isinstance(rsyn[i],float):
                        tsyn[tl]=math.gamma(rsyn[i]+1); tl+=1; stc=fls=True
                    else: tsyn[tl]=rsyn[i]; tl+=1
                elif rsyn[i] in self.funs:
                    if isinstance(rsyn[i+1],float):
                        tsyn[tl]=self.funs[rsyn[i]](rsyn[i+1]); tl+=1; stc=fls=True
                    elif isinstance(rsyn[i+1],tuple):
                        tsyn[tl]=self.funs[rsyn[i]](rsyn[i+1][0],rsyn[i+1][1]); tl+=1; stc=fls=True
                    else: tsyn[tl]=rsyn[i]; tl+=1
                else: tsyn[tl]=rsyn[i]; tl+=1
        for i in self.bas:
            fls,rl=0,0
            for j in range(tl):
                if fls: fls-=1; continue 
                if j==0 and tsyn[j] in i:
                    rsyn[rl]=i[tsyn[j]](tsyn[j+1]); rl+=1; fls=1
                elif tsyn[j+1] in i: rsyn[rl]=i[tsyn[j+1]](tsyn[j],tsyn[j+2]); rl+=1; fls=2
                else: rsyn[rl]=tsyn[j]; rl+=1
            for j in range(rl): tsyn[j]=rsyn[j]
            tl=rl
        if rl==1: return rsyn[0]
        else: raise SyntaxError
    def calsz(self,w,h,ky):
        size=self.cfg.get(ky,'')
        if size and self.chek: return size
        a,b=w*self.scr,h*self.scr; c,d=(self.scwth-a)//2,(self.schgt-b)//2
        return f'{a}x{b}+{c}+{d}'
    def cbbpgu(self,cb):
        self.cbbcnt+=1
        self.rt.after(0,self.pgu,self.cbbcnt,f'已完成({self.cbbcnt}/{cb})','cyan')
    def cchg(self):
        if not self.chg: self.chg=1; self.rt.title(f"{self.data['til']} - {self.txflnm}*")
    def cdchk(self):
        fls=['']*3
        for i in range(3):
            fl=self.cdobj[i][1].get()
            if fl: fls[i]=fl
            else: self.mb('w','o','提示','请检查输入的内容'); return
        if not self.tp.splitext(fls[2])[1]: fls[2]+='.cpy'
        self.thr(self.cdmix(fls))
    def cdcmd(self,p):
        idx=1 if p==2 else 0; tles=['打开','保存']
        knd=[('Python source files','*.py'),('C++ source files','*.cpp'),('All text files','*.*')]
        getpth=self.dlg(idx+1,tles[idx],knd[p])
        if not getpth: return
        self.cdobj[p][1].delete(0,'end'); self.cdobj[p][1].insert(0,getpth)
    def cdmix(self,fls):
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
        self.rt.after(0,self.show,self.ls,'进程已结束','red')
        self.rt.after(0,self.show,self.ls,'>>>','purple')
    def cdobf(self):
        cdo=self.crttpl('代码混合',22,7,'cdobf',0)
        cdemp=[ttk.Frame(cdo) for i in range(4)]
        cdtx=['py源代码','cpp源代码','生成到']; self.cdobj=[[None,None,None] for i in range(3)]
        for i in range(3):
            self.cdobj[i][0]=ttk.Label(cdemp[i],text=cdtx[i],width=10)
            self.cdobj[i][1]=ttk.Entry(cdemp[i],width=30)
            self.cdobj[i][2]=ttk.Button(cdemp[i],text='浏览',command=lambda p=i: self.cdcmd(p))
            self.cdobj[i][0].pack(side='left',expand=True)
            self.cdobj[i][1].pack(side='left',expand=True)
            self.cdobj[i][2].pack(side='left',expand=True)
        cdgen=ttk.Button(cdemp[3],text='生成',command=self.cdchk)
        cdqut=ttk.Button(cdemp[3],text='退出',command=lambda: self.winqut(cdo,'cdobf'))
        cdgen.pack(side='left',expand=True); cdqut.pack(side='left',expand=True)
        for i in range(4): cdemp[i].pack(fill='both',expand=True)
    def check(self):
        self.scwth,self.schgt=self.rt.winfo_screenwidth(),self.rt.winfo_screenheight()
        sc,self.reboot,self.rbtarg,self.tp=self.cfg.get('sc',[0,0,0]),0,'',os.path
        self.chek=sc[0]==self.scr and sc[1]==self.scwth and sc[2]==self.schgt
        self.cfg['sc']=[self.scr,self.scwth,self.schgt]
        self.fntkys=['bold','italic','underline','overstrike']
        self.bgidx,self.fnt,self.fwgt=self.cfg.get('bgidx',None),self.cfg.get('font',None),''
        if self.bgidx==None: self.cfg['bgidx']=self.bgidx=2
        if self.fnt==None: self.cfg['font']=self.fnt='TkDefaultFont'
        for i in self.fntkys:
            if i not in self.cfg: self.cfg[i]=0
            self.fwgt+=f'{i} ' if self.cfg[i] else ''
        if not self.fwgt: self.fwgt='normal'
        if self.bgidx==2: lctme=time.localtime(); self.bgidx=0 if 6<=lctme.tm_hour<18 else 1
        self.bg=self.data['bg'][self.bgidx]; self.txchrc=self.data['chr'][self.bgidx]
        self.bgin=self.data['bgin'][self.bgidx]
    def clrplc(self):
        self.rt.after(0,self.show,self.ls,'(1/4)打开','cyan')
        try: pnm=self.dlg(1,'打开',('All image files','*.*')); pic=Image.open(pnm)
        except: return
        fm=lambda cl: (int(cl[:2],16),int(cl[2:4],16),int(cl[4:],16))
        try:
            nclr=list(map(fm,self.inp('输入被替换颜色(16进制表示)').split('/')))
            clr=fm(self.inp('输入替换颜色(16进制表示)'))
        except: return
        self.rt.after(0,self.show,self.ls,'(2/4)转换','cyan'); pix=numpy.array(pic)
        self.rt.after(0,self.show,self.ls,'(3/4)替换','cyan')
        for i in nclr: alc=(pix[:,:,:3]==i).all(axis=-1); pix[alc,:3]=clr
        self.rt.after(0,self.show,self.ls,'(4/4)保存','cyan'); pic=Image.fromarray(pix)
        new=self.dlg(2,'保存',('Image files','*.png'))
        if not new: return
        if not new.endswith('.png'): new+='.png'
        pic.save(new); self.rt.after(0,self.show,self.ls,'进程已结束','red')
        self.rt.after(0,self.show,self.ls,'>>>','purple')
    def clsf(self,rse=0):
        if not self.ofl: return
        if self.chg:
            svst=self.mb('q','ync','关闭文件时保存','未保存的内容将会丢失,是否保存?')
            if svst=='yes':
                if rse: self.savf()
                else:
                    try: self.savf()
                    except: return
            elif svst=='cancel': return
        self.tetr.delete('1.0','end'); self.chg=0
        self.memp2.pack_forget(); self.ofl=0; self.rt.title(self.data['til'])
    def conpuw(self):
        puw=self.crttpl('抽卡模拟器',16,14,'conpuw',1); pum=tkinter.Menu(puw)
        puw.config(menu=pum); uptx=['五星UP','四星UP1','四星UP2','四星UP3']
        up=[tkinter.Menu(pum,tearoff=0,bg=self.bgin,fg=self.txchrc) for i in range(4)]
        for i in range(4): pum.add_cascade(label=uptx[i],menu=up[i])
        dtm=['ups5','ups4','fups5','wpns5','wpns4','wpns3']
        self.ups,self.put5,self.put4,self.true_up4,self.true_up5,self.fu=['']*4,0,0,0,0,0
        for i in dtm:
            for j in self.data[i]:
                if i=='ups5': up[0].add_command(label=j,command=lambda k=j: self.adups(k,0))
                elif i=='ups4':
                    for p in range(1,4):
                        up[p].add_command(label=j,command=lambda k=j,h=p: self.adups(k,h))
        pu=[ttk.Frame(puw) for i in range(3)]
        contx=['祈愿一次','祈愿十次','退出']; self.conbtn=[None]*3
        concmd=[lambda: self.pul(1),lambda: self.pul(10),lambda: self.winqut(puw,'conpuw')]
        puwlb=ttk.Label(pu[0],text='祈愿结果'); slet=tkinter.Scrollbar(pu[1])
        self.et=ttk.Treeview(pu[1],columns=('opt',),show='tree')
        self.et.column('#0',width=0,stretch=False); self.et.column('opt',width=15*self.scr,anchor='w')
        self.et.config(yscrollcommand=slet.set); slet.config(command=self.et.yview)
        for i in self.data['clr']: self.et.tag_configure(i,foreground=i,background=self.bg)
        for i in range(3):
            self.conbtn[i]=ttk.Button(pu[2],text=contx[i],width=8)
            self.conbtn[i].config(command=concmd[i],state='disabled')
            self.conbtn[i].pack(side='left',expand=True)
        self.conbtn[2].config(state='normal'); puwlb.pack(expand=True)
        slet.pack(side='right',fill='y'); self.et.pack(fill='both',expand=True)
        for i in range(3): pu[i].pack(fill='both',expand=True)
    def crttpl(self,tle,w,h,wid,re):
        tpl=tkinter.Toplevel(self.rt); tpl.geometry(self.calsz(w,h,wid))
        tpl.resizable(re,re); tpl.transient(self.rt); tpl.title(tle); return tpl
    @staticmethod
    def dlg(n,tle,flt):
        if n==0: dl=filedialog.askdirectory(title=tle)
        elif n==1: dl=filedialog.askopenfilename(title=tle,filetypes=(flt,))
        else: dl=filedialog.asksaveasfilename(title=tle,filetypes=(flt,))
        return dl
    @staticmethod
    def eucd(itx):
        litx=len(itx); otx=['']*litx
        for i in range(litx): otx[i]=f'\\u{ord(itx[i]):04x}'
        return ''.join(otx)
    def gen(self,arg):
        self.ln,self.wd,self.bx,self.by,self.ex,self.ey=arg
        self.sz=min(12*self.scr/self.ln,12*self.scr/self.wd)
        self.maze=numpy.ones(shape=(self.ln*2+1,self.wd*2+1),dtype=int)
        for i in range(self.ln*2+1):
            for j in range(self.wd*2+1):
                if i in [0,self.ln*2] or j in [0,self.wd*2]: self.maze[i,j]=0
        self.rt.after(0,self.mzshw,0,0,self.ln*2+1,self.wd*2+1,self.txchrc)
        self.rt.after(0,self.mzshw,1,1,self.ln*2,self.wd*2,self.bg)
        stk,top=numpy.zeros(shape=(self.ln*self.wd,4),dtype=int),0
        stk[top]=[1,1,self.ln*2-1,self.wd*2-1]; top+=1
        while top>0:
            top-=1; lx,ly,rx,ry=stk[top]
            if rx-lx<2 or ry-ly<2: continue
            x=random.randint(lx+1,rx-1)//2*2; y=random.randint(ly+1,ry-1)//2*2
            stk[top]=[lx,y+1,x-1,ry]; top+=1; stk[top]=[lx,ly,x-1,y-1]; top+=1
            stk[top]=[x+1,ly,rx,y-1]; top+=1; stk[top]=[x+1,y+1,rx,ry]; top+=1
            for i in range(lx,rx+1): self.maze[i,y]=0
            for i in range(ly,ry+1): self.maze[x,i]=0
            self.rt.after(0,self.mzshw,lx,y,rx+1,y+1,self.txchrc)
            self.rt.after(0,self.mzshw,x,ly,x+1,ry+1,self.txchrc)
            rtmp=[(random.randint(lx,x-1)//2*2+1,y),(random.randint(x+1,rx)//2*2+1,y),
                  (x,random.randint(ly,y-1)//2*2+1),(x,random.randint(y+1,ry)//2*2+1)]
            k=random.randrange(4)
            for i in range(4):
                if k-i:
                    p=rtmp[i]; self.maze[p[0],p[1]]=1
                    self.rt.after(0,self.mzshw,p[0],p[1],p[0]+1,p[1]+1,self.bg)
        self.maze[self.bx*2-1,self.by*2-1]=1; self.maze[self.ex*2-1,self.ey*2-1]=2
        self.rt.after(0,self.mzshw,self.bx*2-1,self.by*2-1,self.bx*2,self.by*2,'#22cefc')
        self.rt.after(0,self.mzshw,self.ex*2-1,self.ey*2-1,self.ex*2,self.ey*2,'#00ff00')
        self.mzbtns[0].config(state='normal')
        self.mzbtns[1].config(state='normal')
    def genchk(self):
        arg=[0]*6
        try:
            for i in range(6): arg[i]=int(self.mzwid[i+6].get())
            self.memp1.pack_forget(); self.cvs.pack(fill='both',expand=True)
            self.restul(); self.mzbtns[0].config(state='disabled')
            self.thr(lambda: self.gen(arg))
        except: self.mb('w','o','提示','请检查输入的内容'); return
    def getit(self):
        self.sis,self.lvl,self.kd=[0]*4,[0]*5,random.randrange(5)
        mns=self.data['mnpro'][self.kd]; self.mn=random.choices(mns[0],weights=mns[1])[0]
        if self.mn==-1: self.mn=random.randint(0,2)
        if self.mn==-2:
            self.mn=random.choice(self.data['elmnkd'])
            if self.mn==' ': self.mn='物理'
            else: self.mn+='元素'
            self.mn+='伤害加成'
        else: self.mn=self.data['name'][self.mn]
        self.sisl,self.nm=0,random.choices((3,4),weights=(4,1))[0]
        while self.sisl in range(self.nm):
            si=random.choices(range(len(self.data['sipro'])),weights=self.data['sipro'])[0]
            if si not in self.sis and self.data['name'][si]!=self.mn:
                self.lvl[self.sisl]=self.data['siup'][si]*random.choice(self.data['siupro'])
                self.sis[self.sisl]=si; self.sisl+=1
        self.itbtn[1].config(state='normal'); self.et.delete(*self.et.get_children()); self.prit()
    def getvar(self,tag,win):
        get=tag.get()
        if get: self.var=get; self.winqut(win,'inp')
        else: self.mb('w','o','提示','请检查输入的内容'); return
    def hlp(self):
        hlp=self.crttpl('帮助',36,36,'hlp',1)
        hlpmnu=tkinter.Menu(hlp); hlp.config(menu=hlpmnu)
        mnop=tkinter.Menu(hlpmnu,tearoff=0,bg=self.bgin,fg=self.txchrc)
        hlpmnu.add_cascade(label='选项',menu=mnop)
        mnop.add_command(label='退出',command=lambda: self.winqut(hlp,'hlp'))
        mntmp=tkinter.Menu(hlpmnu,tearoff=0,bg=self.bgin,fg=self.txchrc)
        hlpmnu.add_cascade(label='帮助内容',menu=mntmp)
        for i in self.data['hlps']:
            mnucmd=lambda k=self.data['hlps'][i]: self.hlpshw(k)
            mntmp.add_command(label=i,command=mnucmd)
        self.hlptrv=ttk.Treeview(hlp,columns=('opt',),show='tree')
        hlpslb=tkinter.Scrollbar(hlp); self.hlptrv.column('#0',width=0,stretch=False)
        self.hlptrv.column('opt',width=15*self.scr,anchor='w')
        self.hlptrv.config(yscrollcommand=hlpslb.set)
        hlpslb.config(command=self.hlptrv.yview)
        for i in self.data['clr']: self.hlptrv.tag_configure(i,foreground=i,background=self.bg)
        hlpslb.pack(side='right',fill='y'); self.hlptrv.pack(fill='both',expand=True)
        self.hlpshw('F')
    def hlpshw(self,k):
        self.hlptrv.delete(*self.hlptrv.get_children())
        mds={'D':'README.md','N':'NEW.md'}
        if k in mds:
            try: fl=open(mds[k],'r',encoding='utf-8')
            except: self.mb('e','o','错误',f'{mds[k]}不存在'); return
            self.hlptrv.column('opt',anchor='w')
            ln=fl.readline(); flg=0
            while ln:
                if ln=='\n' or ln.startswith('!'): ln=fl.readline(); continue 
                elif ln.startswith('```'): flg=1-flg
                elif flg: self.show(self.hlptrv,ln,'green')
                else:
                    tmp=''
                    for i in ln:
                        if i in '#*`- ': continue
                        tmp+=i
                    self.show(self.hlptrv,tmp,'green')
                ln=fl.readline()
            fl.close()
        else:
            self.hlptrv.column('opt',anchor='c')
            for i in self.data['details'][k]: self.show(self.hlptrv,i,'green')
    def hshgn(self):
        licc,lictmp,hdgl,hsh=len(self.data['icc']),0,64,hashlib.sha256()
        while True:
            if hdgl==64:
                hdgl=0; hsh.update(self.data['icc'][lictmp%licc].encode())
                lictmp+=1; hdg=hsh.hexdigest()
            yield int(hdg[hdgl:hdgl+2],16)
            hdgl+=2
    def ico(self,icx,ang,sz,clr):
        cmds={'b':lambda a: (self.tl.begin_fill(),self.tl.pendown()),
              'e':lambda a: (self.tl.end_fill(),self.tl.penup()),
              'l':lambda a: (self.tl.lt(int(a[0])*ang),self.tl.fd(int(a[1:])*sz)),
              'r':lambda a: (self.tl.rt(int(a[0])*ang),self.tl.fd(int(a[1:])*sz)),
              'c':lambda a: self.tl.color(cmds[next(clr)]),
              'd':'#22cefc','w':self.bg}
        cmd,dig=cmds['c'],''
        for i in range(len(icx)):
            if icx[i].isdigit(): dig+=icx[i]
            else: cmd(dig); dig,cmd='',cmds[icx[i]]
        cmd(dig)
    def ics1(self,fir=0):
        if fir and not self.cfg.get('ani',1):
            self.rt.after(0,self.icsclm); return
        self.memp1.pack_forget(); sztmp=lambda x: round(x*self.scr)
        self.restul(); self.cvs.pack(fill='both',expand=True)
        self.ico(self.data['icc'],60,sztmp(0.5),iter('d')); self.rt.after(500,self.ics2,sztmp)
    def ics2(self,sztmp):
        self.restul(); self.ico('l041r24l30',45,sztmp(0.6),iter('d'))
        self.ico(self.data['icd'],90,self.scr,iter('dwdwd'))
        self.tl.rt(45); self.tl.fd(12*self.scr)
        icm1,icm2='圣·西门科技股份有限公司 出品','Sig·WestGate Tech. L.C.D. present.'
        self.tl.write(icm1,align='center',font=('华文行楷',sztmp(0.8)))
        self.tl.fd(sztmp(2.2))
        self.tl.write(icm2,align='center',font=('Consolas',sztmp(0.7),'bold'))
        self.rt.after(1200,self.icsclm)
    def icsclm(self):
        self.cvs.pack_forget(); self.restul()
        self.memp1.pack(side='bottom',fill='both',expand=True)
        if len(sys.argv)>1:
            fl=sys.argv[1].strip('\"')
            if fl.endswith('.nda'): self.opnf(nda=1,opn=fl)
            else: self.opnf(ext=1,opn=fl)
    def imgsrt(self):
        self.rt.after(0,self.show,self.ls,'(1/3)打开','cyan')
        try:
            self.pth=self.dlg(0,'打开',('Text files','*.txt'))
            names=[i for i in os.listdir(self.pth) if i.lower().endswith('.png')]
        except: return
        self.rt.after(0,self.show,self.ls,'(2/3)排序','cyan'); cbbln=len(names)
        lnr=range(cbbln); sort=[[] for i in lnr]
        lsrt=0; cct=multiprocessing.cpu_count()
        polres=[None]*cbbln; lpr=0; pol=multiprocessing.Pool(processes=cct)
        self.rt.after(0,self.pginit,'图片排序',cbbln); self.cbbcnt=0
        calbk=lambda cb=cbbln: self.cbbpgu(cb)
        for i in names:
            res=pol.apply_async(avgs,args=[self.pnm(i)],callback=calbk)
            polres[lpr]=res; lpr+=1
        pol.close(); pol.join(); self.rt.after(250,self.winqut,self.pgm,'pginit')
        for res in polres: sort[lsrt]=res.get(); lsrt+=1
        sort=sorted(sort,key=lambda i:i[0])
        self.rt.after(0,self.show,self.ls,'(3/3)整理','cyan')
        for i in lnr: os.rename(self.pnm(sort[i][1]),self.pnm(f'pix{i:04d}.png'))
        names=[i for i in os.listdir(self.pth) if i.lower().endswith('.png')]
        for i in lnr: os.rename(self.pnm(names[i]),self.pnm(f'pic{i:04d}.png'))
        self.rt.after(0,self.show,self.ls,'进程已结束','red')
        self.rt.after(0,self.show,self.ls,'>>>','purple')
    def inp(self,st):
        tmp=self.crttpl('',18,5,'inp',0); inbtx=['全选','确认','取消']; btns=[None]*3
        inemp=[ttk.Frame(tmp) for i in range(3)]; self.var=None
        inlb=ttk.Label(inemp[0],text=st); etr=ttk.Entry(inemp[1],width=40)
        inbcmd=[lambda: self.scl(etr),lambda: self.getvar(etr,tmp),
                lambda: self.winqut(tmp,'inp')]
        for i in range(3):
            btns[i]=ttk.Button(inemp[2],text=inbtx[i],command=inbcmd[i])
            btns[i].pack(side='left',expand=True)
        inlb.pack(expand=True); etr.pack(expand=True)
        for i in range(3): inemp[i].pack(fill='both',expand=True)
        tmp.wait_window(); return self.var
    def iso(self):
        try: n=int(self.inp('基团-CnH2n+1,输入n值'))
        except: return
        self.thr(lambda: self.isocal(n))
    def isocal(self,n):
        hm,isol=numpy.zeros(n+1,dtype=int),1; hm[0]=1
        for i in range(n):
            b,c,res=0,0,0; a=i-2*c
            while c<=a:
                res+=hm[a]*hm[b]*hm[c]; a,b=a-1,b+1
                if a<b: c+=1; a,b=i-2*c,c
            hm[isol],isol=res,isol+1
        self.rt.after(0,self.show,self.ls,f'{hm[n]}','green')
        self.rt.after(0,self.show,self.ls,'>>>','purple')
    def itsth(self):
        itw=self.crttpl('圣遗物强化',16,14,'itsth',1)
        it=[ttk.Frame(itw) for i in range(3)]
        ittx=['获取','强化','退出']; self.itbtn=[None]*3
        itcmd=[self.getit,self.upgd,lambda: self.winqut(itw,'itsth')]
        itlb=ttk.Label(it[0],text='强化结果:'); slet=tkinter.Scrollbar(it[1])
        self.et=ttk.Treeview(it[1],columns=('opt',),show='tree')
        self.et.column('#0',width=0,stretch=False); self.et.column('opt',width=15*self.scr,anchor='w')
        self.et.config(yscrollcommand=slet.set); slet.config(command=self.et.yview)
        for i in self.data['clr']: self.et.tag_configure(i,foreground=i,background=self.bg)
        for i in range(3):
            self.itbtn[i]=ttk.Button(it[2],text=ittx[i],command=itcmd[i],width=8)
            self.itbtn[i].pack(side='left',expand=True)
        self.itbtn[1].config(state='disabled'); itlb.pack(expand=True)
        slet.pack(side='right',fill='y'); self.et.pack(fill='both',expand=True)
        for i in range(3): it[i].pack(fill='both',expand=True)
    def lnkcal(self,arr,hd):
        lnkl,cur=0,hd
        while cur!=-1: lnkl+=1; cur=arr[cur][1]
        for i in range(lnkl-1,-1,-1):
            p,q=hd,-1; r=arr[p][1]
            for j in range(i):
                if arr[p][0]>arr[r][0]:
                    if q==-1: hd=r
                    else: arr[q][1]=r
                    arr[p][1],arr[r][1]=arr[r][1],p; p,r=r,p
                p,q,r=r,p,arr[r][1]
        self.rt.after(0,self.show,self.ls,f'{arr},head={hd}','green')
        self.rt.after(0,self.show,self.ls,'>>>','purple')
    def lnksrt(self):
        try: arr,hd=eval(self.inp('输入链表')),int(self.inp('输入头地址'))
        except: return
        self.thr(lambda: self.lnkcal(arr,hd))
    def mazepl(self):
        mz=self.crttpl('迷宫可视化',18,8,'mazepl',0)
        mzemp=[ttk.Frame(mz) for i in range(5)]
        lb=ttk.Label(mzemp[0],text='迷宫设置')
        mztx=['迷宫长','迷宫宽','起点x','起点y','终点x','终点y']; self.mzwid=[None]*12
        self.mzbtns=[None]*3; mzbtx=['生成','解','退出']
        mzbtc=[self.genchk,lambda: self.thr(self.slv),lambda: self.mzrst(mz)]
        for i in range(6):
            self.mzwid[i]=ttk.Label(mzemp[i//2+1],text=mztx[i],width=8)
            self.mzwid[i+6]=ttk.Entry(mzemp[i//2+1],width=12)
            self.mzwid[i].pack(side='left',expand=True)
            self.mzwid[i+6].pack(side='left',expand=True)
        for i in range(3):
            self.mzbtns[i]=ttk.Button(mzemp[4],text=mzbtx[i],command=mzbtc[i])
            self.mzbtns[i].pack(side='left',expand=True)
        self.mzbtns[1].config(state='disabled'); lb.pack(expand=True)
        for i in range(5): mzemp[i].pack(fill='both',expand=True)
    def mb(self,icn,tp,tle,msg):
        mbs=self.data['mb']
        mbt=tkinter.messagebox.Message(icon=mbs[icn],type=mbs[tp],title=tle,message=msg)
        res=mbt.show(); return res
    def mngrd(self,i):
        j=i-1 if i%3-1 else i+1
        self.wids[i][1].config(state='normal'); self.wids[j][1].config(state='disabled')
    def mzrst(self,tag):
        self.winqut(tag,'mazepl'); self.cvs.pack_forget(); self.restul()
        self.memp1.pack(side='bottom',fill='both',expand=True)
    def mzshw(self,lx,ly,rx,ry,clr):
        self.tl.teleport((lx-self.ln)*self.sz+22*self.scr,(ly-self.wd)*self.sz-12*self.scr)
        self.tl.fillcolor(clr); self.tl.begin_fill()
        for i in range(2):
            self.tl.fd((rx-lx)*self.sz); self.tl.lt(90); self.tl.fd((ry-ly)*self.sz); self.tl.lt(90)
        self.tl.end_fill()
    def opnf(self,ext=0,nda=0,opn=None):
        self.ofl=1; self.memp2.pack(fill='both',expand=True)
        if self.chg:
            svst=self.mb('q','ync','关闭文件时保存','上一个未保存的内容将会丢失,是否保存?')
            if svst=='yes':
                try: self.savf()
                except: self.rt.title(f"{self.data['til']} - {self.txflnm}*"); return
            elif svst=='cancel': self.rt.title(f"{self.data['til']} - {self.txflnm}*"); return
        self.chg=0; self.txflnm='未命名文件'; self.tetr.delete('1.0','end')
        if ext:
            if opn is None: rsflnm=self.dlg(1,'打开',('All text files','*.*'))
            else: rsflnm=opn
            try: fl=open(rsflnm,'rb'); self.txflnm=rsflnm
            except: self.rt.title(f"{self.data['til']} - {self.txflnm}"); return
            data=fl.read(); fl.close(); enc=chardet.detect(data)['encoding']; self.nfl=0
            dataln=data.decode(enc,errors='backslashreplace').splitlines()
            for i in dataln: self.tetr.insert('end',i+'\n')
        else:
            if nda:
                try: byt=self.txcbtb(None,1,opn)
                except: return
                self.tetr.insert('insert',byt)
            self.nfl=1
        self.rt.title(f"{self.data['til']} - {self.txflnm}")
    def pginit(self,tx,tol):
        self.pgm=self.crttpl(tx,16,13,'pginit',0)
        pgf=[ttk.Frame(self.pgm) for i in range(3)]
        self.pgl=ttk.Label(pgf[0],text='0.00%')
        self.pgb=ttk.Progressbar(pgf[1],length=15*self.scr)
        pgsb=tkinter.Scrollbar(pgf[2])
        self.pgt=ttk.Treeview(pgf[2],columns=('opt',),show='tree')
        self.pgt.column('#0',width=0,stretch=False)
        self.pgt.column('opt',width=15*self.scr,anchor='w')
        self.pgt.config(yscrollcommand=pgsb.set)
        pgsb.config(command=self.pgt.yview)
        for i in self.data['clr']: self.pgt.tag_configure(i,foreground=i,background=self.bg)
        self.pgb['maximum']=tol; self.pgl.pack(expand=True)
        self.tol=tol/100; self.pgb.pack(fill='y',expand=True)
        pgsb.pack(side='right',fill='y'); self.pgt.pack(fill='both',expand=True)
        for i in range(3): pgf[i].pack(fill='both',expand=True)
    def pgu(self,num,tx,clr):
        self.pgl.config(text=f'{num/self.tol:.2f}%')
        self.show(self.pgt,tx,clr); self.pgb['value']=num
    def picpt(self):
        self.rt.after(0,self.show,self.ls,'(1/3)打开','cyan')
        try: fl=self.dlg(1,'打开',('All image files','*.*')); pic=Image.open(fl)
        except: return
        pix,h,w=numpy.array(pic),pic.height,pic.width
        self.rt.after(0,self.show,self.ls,'(2/3)加密','cyan')
        ln=len(pix[0,0]); gn=self.hshgn()
        immsk=numpy.zeros_like(pix); self.rt.after(0,self.pginit,'图片加密',h)
        for i in range(h):
            for j in range(w):
                for k in range(ln): immsk[i,j,k]=next(gn)
            self.rt.after(0,self.pgu,i+1,f'已加密{i+1}/{h}','cyan')
        pic=Image.fromarray(numpy.bitwise_xor(pix,immsk))
        self.rt.after(250,self.winqut,self.pgm,'pginit')
        self.rt.after(0,self.show,self.ls,'(3/3)保存','cyan')
        new=self.dlg(2,'保存',('Image files','*.png'))
        if not new: return
        if new.endswith('.png'): pic.save(new)
        else: pic.save(f'{new}.png')
        self.rt.after(0,self.show,self.ls,'进程已结束','red')
        self.rt.after(0,self.show,self.ls,'>>>','purple')
    def prconf(self):
        lim=[89,3,1]; res=[0]*5
        for i in range(5):
            val=self.proinp[i].get()
            if (not val.isdigit()) or int(val)<0: self.mb('w','o','提示','请检查输入的内容'); return
            if i>1 and int(val)>lim[i-2]: self.mb('w','o','提示','请检查输入的内容'); return
            res[i]=int(val)
        self.thr(lambda: self.pulpro(res))
    def prefn(self):
        self.clear=lambda: (self.ls.delete(*self.ls.get_children()))
        self.delmark=lambda tag: self.tetr.tag_remove('match',tag[0],tag[1]) if tag[0] else None
        self.pnm=lambda fn: self.tp.join(self.pth,fn)
        self.restul=lambda: (self.tl.reset(),self.tl.ht(),self.tl.speed(0),self.tl.penup())
        self.scl=lambda tag: (tag.focus_set(),tag.selection_range(0,'end'))
        self.show=lambda arg,st,cl: arg.see(arg.insert('','end',values=(st,),tags=(cl,)))
        self.thr=lambda fun: threading.Thread(target=fun).start()
    def prefr(self):
        prf=self.crttpl('选项',18,8,'prefr',1); prfemp=[ttk.Frame(prf) for i in range(5)]
        cbblb=['UI显示模式','字体']; cbblan=[self.data['modes'],self.data['fonts']]
        varini=[cbblan[0][self.cfg['bgidx']],self.cfg['font']]
        self.anivar=tkinter.IntVar(value=self.cfg.get('ani',1))
        self.datavar=[tkinter.StringVar(value=varini[i]) for i in range(2)]; cbb=[None]*4
        for i in range(2):
            cbb[i]=ttk.Label(prfemp[i],text=cbblb[i],width=15)
            cbb[i+2]=ttk.OptionMenu(prfemp[i],self.datavar[i],varini[i],*cbblan[i])
            cbb[i+2]['menu'].configure(bg=self.bgin,fg=self.txchrc)
            cbb[i+2].config(width=22); cbb[i].pack(side='left',expand=True)
            cbb[i+2].pack(side='left',expand=True)
        able=lambda *args: self.subtn.config(state='normal')
        txchk=['是否粗体','斜体','下划线','删除线']; prechk=[None]*4
        self.prevars=[tkinter.IntVar(value=self.cfg[self.fntkys[i]]) for i in range(4)]
        for i in range(4):
            prechk[i]=ttk.Checkbutton(prfemp[2],variable=self.prevars[i],command=able)
            prechk[i].config(text=txchk[i]); prechk[i].pack(side='left',expand=True)
        anibtn=ttk.Checkbutton(prfemp[3],variable=self.anivar,command=able)
        tips=ttk.Label(prfemp[3],text='部分选项需等待重启后生效'); anibtn.config(text='是否启用动画')
        anibtn.pack(side='left',expand=True); tips.pack(side='left',expand=True)
        self.subtn=ttk.Button(prfemp[4],text='应用',command=self.submt,state='disabled')
        canbtn=ttk.Button(prfemp[4],text='取消',command=lambda: self.winqut(prf,'prefr'))
        for i in range(2): self.datavar[i].trace('w',able)
        self.subtn.pack(side='left',expand=True); canbtn.pack(side='left',expand=True)
        for i in range(5): prfemp[i].pack(fill='both',expand=True)
    def preset(self):
        try:
            self.scr=ctypes.windll.shcore.GetScaleFactorForDevice(0)//5
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except: self.scr=20
        try: fld=open('Data.json','r',encoding='utf-8'); self.data=json.load(fld); fld.close()
        except FileNotFoundError:
            tkinter.messagebox.showerror('错误','找不到Data.json'); sys.exit(0)
        except:
            tkinter.messagebox.showerror('错误','非法的Data.json\n请检查是否存在语法错误')
            fld.close(); sys.exit(0)
        self.rt=tkinter.Tk()
        try: self.rt.iconphoto(True,tkinter.PhotoImage(file='Na.png')); self.rt.withdraw()
        except:
            self.rt.withdraw()
            tkinter.messagebox.showerror('错误','找不到Na.png'); sys.exit(0)
        try: flc=open('Config.json','r',encoding='utf-8'); self.cfg=json.load(flc); flc.close()
        except FileNotFoundError:
            tkinter.messagebox.showerror('错误','找不到Config.json')
            if tkinter.messagebox.askyesno('','是否继续运行?'): self.cfg={}
            else: sys.exit(0)
        except:
            tkinter.messagebox.showerror('错误','非法的Config.json\n请检查是否存在语法错误'); flc.close()
            if tkinter.messagebox.askyesno('','是否继续运行?(会覆盖原有文件)'): self.cfg={}
            else: sys.exit(0)
    def prit(self,st=None):
        self.show(self.et,f"{self.data['knd'][self.kd]}(+{self.lvl[4]})",'cyan')
        self.show(self.et,self.mn,'blue')
        for i in range(self.sisl):
            nm=self.data['name'][self.sis[i]]
            if st is not None and i==st: clr='green'
            else: clr='red'
            if nm[-1]==' ':
                self.show(self.et,f'{nm[:-1]}+{round(self.lvl[i]+0.05,1)}',clr)
            else: self.show(self.et,f'{nm}+{round(self.lvl[i]+0.05,1)}%',clr)
        self.show(self.et,'>>>','purple')
    def pul(self,n):
        for i in range(n):
            ran,tup=random.random(),random.random()
            if ran<=self.data['pro_lst5'][self.put5]:
                if self.true_up5: self.show(self.et,self.ups[0],'yellow'); self.true_up5=0
                elif tup<=self.data['tu_lst'][self.fu]:
                    self.show(self.et,self.ups[0],'yellow'); self.true_up5,self.fu=0,0
                else:
                    it=random.choice(self.data['fups5']+self.data['wpns5'])
                    self.show(self.et,it,'yellow'); self.show(self.et,'歪','red')
                    self.true_up5,self.fu=1,self.fu+1
                self.put5,self.put4=0,self.put4+1
            elif ran<=self.data['pro_lst5'][self.put5]+self.data['pro_lst4'][self.put4]:
                if tup<=0.5 or self.true_up4:
                    self.show(self.et,random.choice(self.ups[1:]),'purple'); self.true_up4=0
                else:
                    it=random.choice(self.data['ups4']+self.data['wpns4'])
                    self.show(self.et,it,'purple'); self.true_up4=1
                self.put5,self.put4=self.put5+1,0
            else:
                self.show(self.et,random.choice(self.data['wpns3']),'blue')
                self.put5,self.put4=self.put5+1,self.put4+1
        self.show(self.et,f'垫{self.put5}发','cyan'); self.show(self.et,'>>>','purple')
    def pulpro(self,vals):
        global dic,lst; res=numpy.zeros(52,dtype=float)
        self.rt.after(0,self.pginit,'抽卡模拟',res[1]+res[0]//160)
        s,pb,put,fu,tu=vals; self.proys.config(state='disabled')
        _len,st,ed=0,0,50; pb+=s//160; lst[_len]=[0,put,fu,tu]; proes[_len]=1; _len+=1
        for i in range(pb):
            for j in range(_len):
                ups,puts,false_up,true_up=lst[j]; pro=proes[j]
                ups=min(ups,50); pros=self.data['pro_lst5'][puts]; tu_pro=self.data['tu_lst'][false_up]
                dic[ups,puts+1,false_up,true_up]+=pro*(1-pros)
                if true_up: dic[ups+1,0,false_up,0]+=pro*pros
                else:
                    dic[ups,0,false_up+1,1]+=pro*pros*(1-tu_pro)
                    dic[ups+1,0,0,0]+=pro*pros*tu_pro
            _len=0
            for j in range(52):
                for t in range(90):
                    for p in range(4):
                        for k in range(2):
                            if dic[j,t,p,k]!=0:
                                lst[_len]=[j,t,p,k]; proes[_len]=dic[j,t,p,k]
                                _len+=1; dic[j,t,p,k]=0
            self.rt.after(0,self.pgu,i+1,f'已完成{i+1}抽','cyan')
        for i in range(_len): res[lst[i,0]]+=proes[i]*100
        for i in range(ed+1):
            if res[i]>0.1: st=i; break
        for i in range(ed,0,-1):
            if res[i]<0.1: res[i-1]+=res[i]
            else: ed=i; break
        self.rt.after(250,self.winqut,self.pgm,'pginit')
        self.rt.after(0,self.show,self.ls,'UP数 概率','purple')
        for i in range(st,ed+1):
            self.rt.after(0,self.show,self.ls,f'{i:>2d}{res[i]:7.2f}%','purple')
        self.rt.after(0,self.show,self.ls,'>>>','purple')
        self.proys.config(state='normal')
    def pulprogd(self):
        progd=self.crttpl('抽卡概率计算',18,9,'pulprogd',0)
        prem=[ttk.Frame(progd) for i in range(6)]
        prolb,self.proinp=[None]*5,[None]*5
        probtntx=['原石数','粉球数','垫池数(0-89)','已经连歪数(0-3)','是否大保底(0/1)']
        for i in range(5):
            prolb[i]=ttk.Label(prem[i],text=probtntx[i],width=12)
            self.proinp[i]=ttk.Entry(prem[i],width=30)
            prolb[i].pack(side='left',expand=True)
            self.proinp[i].pack(side='left',expand=True)
        self.proys,prono=ttk.Button(prem[5]),ttk.Button(prem[5])
        self.proys.config(text='确认',command=self.prconf)
        prono.config(text='退出',command=lambda: self.winqut(progd,'pulprogd'))
        self.proys.pack(side='left',expand=True); prono.pack(side='left',expand=True)
        for i in range(6): prem[i].pack(fill='both',expand=True)
    def qutmn(self):
        try: self.clsf(rse=1)
        except: return
        self.winqut(self.rt,'Fabits')
    def recmd(self,k):
        if k==0:
            exts=self.rewids[0][1].get().split('/')
            flnm=self.dlg(1,'打开',('All files','*.*'))
            if not flnm: return
            ext=self.tp.splitext(flnm)[1]
            if ext in exts: return
            exts+=[ext]; self.rewids[0][1].delete(0,'end')
            self.rewids[0][1].insert(0,'/'.join(exts))
        elif k==1:
            getpth=self.dlg(0,'打开',('Text files','*.txt'))
            if not getpth: return
            self.rewids[1][1].delete(0,'end'); self.rewids[1][1].insert(0,getpth)
        else: self.thr(lambda: self.renm(show=True))
    def redo(self):
        if self.ofl:
            try: self.tetr.edit_redo()
            except: self.rt.bell()
    def renm(self,show=False):
        exts,self.pth=self.rewids[0][1].get().split('/'),self.rewids[1][1].get()
        model=self.intepl.get(); lmdl=len(model); newext=[]
        if not (self.pth and model): self.mb('w','o','提示','请检查输入的内容'); return
        for i in exts:
            if i: newext+=[i]
        try:
            if not newext: names=[i for i in os.listdir(self.pth)]
            else: names=[i for i in os.listdir(self.pth) if self.tp.splitext(i)[1] in newext]
        except: return
        names=[[i,''] for i in names if self.tp.isfile(self.pnm(i))]
        keys=['name','index','ext','Y_a','m_a','D_a','H_a','M_a','S_a','Y_m',
              'm_m','D_m','H_m','M_m','S_m','Y_c','m_c','D_c','H_c','M_c','S_c']
        i,flg,form,args,lnms=0,False,'','',len(names)
        while i<lmdl:
            form+=model[i]; i+=1
            if model[i]=='{':
                for j in keys:
                    if model[i:].startswith(j): args+=j+'/'; i+=len(j)
        args=args[:-1].split('/'); argfun=lambda arg: consts[arg]
        for i in range(lnms):
            nm=names[i][0]
            consts,ts,ks={},'YmDHMS','amc'
            tmst={'a':time.localtime(self.tp.getatime(self.pnm(nm))),
                  'm':time.localtime(self.tp.getmtime(self.pnm(nm))),
                  'c':time.localtime(self.tp.getctime(self.pnm(nm)))}
            gett={'Y':lambda tme:tme.tm_year,'m':lambda tme:tme.tm_mon,'D':lambda tme:tme.tm_mday,
                  'H':lambda tme:tme.tm_hour,'M':lambda tme:tme.tm_min,'S':lambda tme:tme.tm_sec}
            for j in ks:
                for k in ts: consts[f'{k}_{j}']=gett[k](tmst[j])
            consts['ext']=self.tp.splitext(nm)[1][1:]; consts['name']=self.tp.splitext(nm)[0]
            consts['index']=i; names[i][1]=form.format(*list(map(argfun,args)))+'.'+consts['ext']
        if show:
            txs='预览效果:'
            for i in range(min(lnms,5)): txs+=f'\n{names[i][0]} -> {names[i][1]}'
            txs+=('' if lnms else '\n没有预览')+'\n是否使用?'
            if self.mb('q','yn','模板预览',txs)=='no': return
        if lnms:
            self.rt.after(0,self.pginit,'视频重命名',lnms); cnt=0
            for i in range(lnms):
                try:
                    os.rename(self.pnm(names[i][0]),self.pnm(names[i][1]))
                    self.rt.after(0,self.pgu,i+1,f'{names[i][0]} -> {names[i][1]}','cyan')
                except: cnt+=1
            self.rt.after(250,self.winqut,self.pgm,'pginit')
            if cnt: self.mb('w','o','重命名',self.data['fails'].format(lnms-cnt,cnt))
    def renmgd(self):
        rewin=self.crttpl('批量重命名',24,7,'rename',0)
        remp=[ttk.Frame(rewin) for i in range(4)]
        tepl,self.intepl=tkinter.StringVar(),tkinter.StringVar()
        self.rewids=[[None]*3 for i in range(3)]; rebtns=[None]*3
        retx,rebtx=['文件后缀(用/分隔)','目录','命名模板'],['重命名','预设','取消']
        recmds=[lambda: self.thr(self.renm),None,lambda: self.winqut(rewin,'rename')]
        chgtmp=lambda *args: self.intepl.set(self.data['temps'][int(tepl.get()[0])-1])
        for i in range(3):
            recmd=lambda k=i: self.recmd(k)
            self.rewids[i][0]=ttk.Label(remp[i],text=retx[i],width=15)
            self.rewids[i][1]=ttk.Entry(remp[i],width=30)
            self.rewids[i][2]=ttk.Button(remp[i],text='浏览' if i-2 else '预览',command=recmd)
            self.rewids[i][0].pack(side='left',expand='True')
            self.rewids[i][1].pack(side='left',expand='True')
            self.rewids[i][2].pack(side='left',expand='True')
        self.rewids[2][1].config(textvariable=self.intepl)
        for i in range(3):
            if i==1:
                temp=self.data['temp']; rebtns[i]=ttk.OptionMenu(remp[3],tepl,temp[0],*temp)
                rebtns[i]['menu'].configure(bg=self.bgin,fg=self.txchrc)
                rebtns[i].config(width=15); tepl.trace('w',chgtmp)
            else:
                rebtns[i]=ttk.Button(remp[3],text=rebtx[i],command=recmds[i])
            rebtns[i].pack(side='left',expand='True')
        for i in range(4): remp[i].pack(fill='both',expand=True)
    def ring(self):
        try: n=int(self.inp('输入n值(对)'))
        except: return
        self.thr(lambda: self.ringcal(n))
    def ringcal(self,n):
        m,flg=0,[1]*(2*n)
        for i in range(2*n):
            k,rngl=i,0
            while flg[k]: flg[k],rngl=0,rngl+1; k=k*2 if k<n else 2*(k-n)+1
            m=max(m,rngl)
        self.rt.after(0,self.show,self.ls,f'{m}','green')
        self.rt.after(0,self.show,self.ls,'>>>','purple')
    def rndchr(self,itx):
        try: n=int(self.inp('输入字符密度'))
        except: return ''
        lstr=list(range(768,880))+list(range(1155,1162)); io,otx=0,['']*len(itx)*(n+1)
        for i in itx:
            otx[io]=i; io+=1; chs=map(chr,random.choices(lstr,k=n))
            for j in chs: otx[io]=j; io+=1
        return ''.join(otx)
    def rome(self):
        try: ch=self.inp('输入罗马数字')
        except: return
        self.thr(lambda: self.romecal(ch))
    def romecal(self,ch):
        num,stk,top=0,[0]*len(ch),0
        dicr={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000,
             'i':1,'v':5,'x':10,'l':50,'c':100,'d':500,'m':1000}
        for i in ch:
            if i not in dicr: self.mb('w','o','提示','输入不合法'); return
            while top>0 and dicr[i]>stk[top-1]: top-=1; num-=stk[top]
            stk[top]=dicr[i]; top+=1
        while top>0: top-=1; num+=stk[top]
        self.rt.after(0,self.show,self.ls,f'{num}','green')
        self.rt.after(0,self.show,self.ls,'>>>','purple')
    def rplc(self):
        schtx=self.consf[2].get(); rplctx=self.consf[4].get(); ncs=not self.upchk.get()
        if not (schtx and rplctx): self.mb('w','o','提示','请检查输入的内容'); return
        cur=self.tetr.index('insert'); pos=self.tetr.search(schtx,cur,'end',nocase=ncs)
        if not pos: pos=self.tetr.search(schtx,'1.0',cur,nocase=ncs)
        if pos:
            self.tetr.delete(pos,f'{pos}+{len(schtx)}c'); self.delmark(self.lastsc)
            self.tetr.insert(pos,rplctx); aled=f'{pos}+{len(rplctx)}c'
            self.tetr.mark_set('insert',aled); self.tetr.tag_add('match',pos,aled)
            self.tetr.tag_config('match',background='yellow')
            self.lastsc=pos,aled; self.cchg()
        else: self.mb('i','o','提示','找不到相应的文本')
    def rplcal(self):
        schtx=self.consf[2].get(); rplctx=self.consf[4].get(); ncs=not self.upchk.get(); cnt=0
        if not (schtx and rplctx): self.mb('w','o','提示','请检查输入的内容'); return
        cur=self.tetr.index('insert'); pos=self.tetr.search(schtx,cur,'end',nocase=ncs)
        if not pos: pos=self.tetr.search(schtx,'1.0',cur,nocase=ncs)
        while pos:
            self.tetr.delete(pos,f'{pos}+{len(schtx)}c'); self.tetr.insert(pos,rplctx)
            aled=f'{pos}+{len(rplctx)}c'; self.tetr.mark_set('insert',aled); cnt+=1
            cur=self.tetr.index('insert'); pos=self.tetr.search(schtx,cur,'end',nocase=ncs)
            if not pos: pos=self.tetr.search(schtx,'1.0',cur,nocase=ncs)
        if cnt: self.cchg(); self.mb('i','o','替换',f'已成功替换{cnt}处文本')
        else: self.mb('i','o','提示','找不到相应的文本')
    def savcfg(self):
        fl=open('Config.json','w',encoding='utf-8')
        json.dump(self.cfg,fl,ensure_ascii=False,indent=4); fl.close()
        if self.reboot:
            now=sys.executable
            sarg=[now] if now==sys.argv[0] else [now,sys.argv[0]]
            if self.rbtarg: subprocess.Popen(sarg+[self.rbtarg])
            else: subprocess.Popen(sarg,start_new_session=True)
            sys.exit(0)
    def savf(self,at=0,nda=0,rse=1):
        if not self.ofl: return
        if nda:
            try: self.txcbtb(self.tetr.get('1.0','end'),clos=1); return
            except: return
        if self.nfl or at:
            rsflnm=self.dlg(2,'保存',('All text files','*.*'))
            if rse and not rsflnm: raise Exception
            elif not rsflnm: return
            if not self.tp.splitext(rsflnm)[1]: rsflnm+='.txt'
            self.txflnm=rsflnm; self.rt.title(f"{self.data['til']} - {self.txflnm}")
        fl=open(self.txflnm,'w',encoding='utf-8',newline='\n'); self.nfl=self.chg=0
        txres=self.tetr.get('1.0','end'); fl.write(txres); fl.close()
    def sch(self,dire,al=False):
        schtx=self.consf[2].get()
        if not schtx: self.mb('w','o','提示','请检查输入的内容'); return
        st,ed,cur,ncs='1.0','end',self.tetr.index('insert'),not self.upchk.get()
        if al: pos=self.tetr.search(schtx,st,ed,nocase=ncs)
        elif dire:
            pos=self.tetr.search(schtx,cur+'+1c',ed,nocase=ncs)
            if not pos: pos=self.tetr.search(schtx,st,cur+'+1c',nocase=ncs)
        else:
            pos=self.tetr.search(schtx,cur,st,backwards=True,nocase=ncs)
            if not pos: pos=self.tetr.search(schtx,ed,cur,backwards=True,nocase=ncs)
        if pos:
            self.delmark(self.lastsc); self.tetr.see(pos); self.tetr.mark_set('insert',pos)
            aled=f'{pos}+{len(schtx)}c'; self.tetr.tag_add('match',pos,aled)
            self.tetr.tag_config('match',background='yellow'); self.lastsc=pos,aled
        else: self.mb('i','o','提示','找不到相应的文本')
    def schgd(self):
        if not self.ofl: return
        schtl=self.crttpl('查找与替换',18,7,'schgd',0); self.lastsc=('','')
        scs=[ttk.Frame(schtl) for i in range(5)]
        concm={'l':lambda idx,arg: ttk.Label(scs[idx],text=arg,width=8),
               'e':lambda idx,arg: ttk.Entry(scs[idx],width=30),
               'b':lambda idx,arg: ttk.Button(scs[idx],text=arg)}
        wid=['l0查找','e0','l1替换为','e1','l2','b3向上查找',
             'b3向下查找','b3从头查找','b4替换','b4全部替换','b4退出']
        self.consf=[None]*12; lcon=1; self.upchk=tkinter.BooleanVar(value=False)
        self.consf[0]=ttk.Checkbutton(scs[2],variable=self.upchk)
        self.consf[0].config(text='是否区分大小写')
        for i in wid: self.consf[lcon]=concm[i[0]](int(i[1]),i[2:]); lcon+=1
        btncmd=[lambda: self.sch(dire=False),lambda: self.sch(dire=True),
                lambda: self.sch(dire=True,al=True),self.rplc,self.rplcal,
                lambda: (self.delmark(self.lastsc),self.winqut(schtl,'schgd'))]
        for i in range(6): self.consf[i+6].config(command=btncmd[i])
        pck=lambda tag: tag.pack(side='left',expand=True); list(map(pck,self.consf))
        for i in range(5): scs[i].pack(fill='both',expand=True)
    def slv(self):
        self.mzbtns[0].config(state='disabled')
        self.mzbtns[1].config(state='disabled')
        tmp=[[1,0],[-1,0],[0,1],[0,-1]]
        stk,top=numpy.zeros(shape=(self.ln*self.wd,3),dtype=int),0
        f=lambda j: tmp[i][j]+(tmp[i][j]<0); g=lambda j: tmp[i][j]*2+1-(tmp[i][j]<0)
        stk[top]=[self.bx*2-1,self.by*2-1,0]; flg=False
        while top>=0:
            x,y,i=stk[top]; self.maze[x][y]=0
            if flg:
                self.rt.after(0,self.mzshw,x+f(0),y+f(1),x+g(0),y+g(1),'#22cefc')
                top-=1; continue
            if i==4: top-=1; continue
            if not self.maze[x+tmp[i][0]][y+tmp[i][1]]: stk[top][2]=i+1; continue
            if self.maze[x+tmp[i][0]*2][y+tmp[i][1]*2]==2: flg=True; continue
            self.maze[x+tmp[i][0]][y+tmp[i][1]]=0
            self.rt.after(0,self.mzshw,x+f(0),y+f(1),x+g(0),y+g(1),'#ff00ff')
            if not self.maze[x+tmp[i][0]*2][y+tmp[i][1]*2]: stk[top][2]=i+1; continue
            top+=1; stk[top]=[x+tmp[i][0]*2,y+tmp[i][1]*2,0]
        self.mzbtns[0].config(state='normal')
    def style(self):
        ftsz=round(0.4*self.scr); stl=ttk.Style(self.rt)
        self.rt.config(bg=self.bg); self.sc.bgcolor(self.bg)
        fnt=(self.fnt,ftsz,self.fwgt); self.tetr.config(insertbackground=self.txchrc,font=fnt)
        for i in self.data['clr']: self.ls.tag_configure(i,foreground=i,background=self.bg)
        self.tetr.config(background=self.bg,foreground=self.txchrc)
        if self.bgidx: stl.theme_use('clam')
        stl.configure('.',background=self.bgin,fieldbackground=self.bg)
        stl.configure('.',foreground=self.txchrc,font=self.fnt)
        stl.configure('Treeview',font=fnt,rowheight=2.5*ftsz)
    def submt(self):
        stcd={'白天模式':0,'夜间模式':1,'流转模式':2}; self.subtn.config(state='disabled')
        self.cfg['bgidx']=stcd[self.datavar[0].get()]; self.cfg['font']=self.datavar[1].get()
        for i in range(4): self.cfg[self.fntkys[i]]=self.prevars[i].get()
        self.cfg['ani']=self.anivar.get()
        if self.mb('q','yn','需要重启','是否立即重启以应用设置?')=='yes':
            if self.ofl:
                if self.txflnm=='未命名文件': self.txflnm+='.txt'
                fl=open(self.txflnm,'w',encoding='utf-8')
                fl.write(self.tetr.get('1.0','end'))
                fl.close(); self.rbtarg=self.txflnm
            self.reboot=1; self.winqut(self.rt,'Fabits')
    def syn(self,k):
        if k=='M': self.m=self.res; return
        elif k=='=':
            self.thr(self.syncal(self.expsyn)); return
        if k=='AC': self.expidx,self.lexp=0,0
        elif k=='←':
            if self.expidx!=0:
                self.expidx-=1; self.lexp-=1
                for i in range(self.expidx,self.lexp): self.expsyn[i]=self.expsyn[i+1]
        elif k=='<':
            if self.expidx>0: self.expidx-=1
        elif k=='>':
            if self.expidx<self.lexp: self.expidx+=1
        elif k=='|x|':
            for i in range(self.lexp-1,self.expidx-1,-1): self.expsyn[i+2]=self.expsyn[i]
            self.expsyn[self.expidx]=self.expsyn[self.expidx+1]='|'
            self.expidx+=2; self.lexp+=2
        else:
            for i in range(self.lexp-1,self.expidx-1,-1): self.expsyn[i+1]=self.expsyn[i]
            self.expsyn[self.expidx]=k; self.expidx+=1; self.lexp+=1
        newexp=''.join(self.expsyn[:self.expidx]+['I']+self.expsyn[self.expidx:self.lexp])
        self.calshw[0].config(text=' '); self.calshw[1].config(text=newexp)
    def syncal(self,expsyn):
        if not expsyn: return
        try:
            res=round(self.cald(expsyn,self.lexp),self.acc)
            self.calshw[0].config(text=str(res)); self.res=res
        except OverflowError: self.calshw[0].config(text='堆栈错误')
        except ArithmeticError: self.calshw[0].config(text='数学错误')
        except ValueError: self.calshw[0].config(text='数学错误')
        except: self.calshw[0].config(text='语法错误')
    def txcbtb(self,byt,opn=0,clos=0,opnfl=None):
        if opn:
            if opnfl is None: flnm=self.dlg(1,'打开',('Nahida Data Assets','*.nda'))
            else: flnm=opnfl
            fl=open(flnm,'rb'); byt=fl.read(); fl.close()
        else: byt=byt.encode('utf-8')
        txlst=bytearray(byt); gn=self.hshgn()
        txlst=[i^next(gn) for i in txlst]; byt=bytes(txlst)
        if clos:
            if opn:
                flnm=self.dlg(2,'保存',('All text files','*.*'))
                if not self.tp.splitext(flnm)[1]: flnm+='.txt'
            else:
                flnm=self.dlg(2,'保存',('Nahida Data Assets','*.nda'))
                if not flnm.endswith('.nda'): flnm+='.nda'
            fl=open(flnm,'wb'); fl.write(byt); fl.close()
        else: return byt.decode('utf-8',errors='backslashreplace')
    def txdel(self):
        funfrm={'(处理方式)':lambda itxs: itxs,
                '编unicode':self.eucd,'生成组合字符':self.rndchr,
                '解unicode':self.ucd,'文本加解密':self.txcbtb}
        if not self.opclvr[0].get():
            itx=self.wids[1][1].get(); enc='utf-8'
            if not itx: self.mb('w','o','提示','请检查输入的内容'); return
        else:
            flnm=self.wids[2][1].get()
            try: fl=open(flnm,'rb')
            except: return
            data=fl.read(); fl.close(); enc=chardet.detect(data)['encoding']
            itx=data.decode(enc)
        otx=funfrm[self.funvar.get()](itx)
        if not self.opclvr[1].get():
            self.wids[4][1].delete(0,'end'); self.wids[4][1].insert('end',otx)
        else:
            new=self.wids[5][1].get()
            if not new: return
            if not self.tp.splitext(new)[1]: new+='.txt'
            fl=open(new,'w',encoding=enc); fl.write(otx); fl.close()
        self.rt.after(0,self.show,self.ls,'进程已结束','red')
        self.rt.after(0,self.show,self.ls,'>>>','purple')
    def txmng(self):
        mng=self.crttpl('文本处理',24,11,'txmng',0)
        self.opclvr=[tkinter.IntVar(value=0) for i in range(2)]
        mngemp=[ttk.Frame(mng) for i in range(7)]; self.funvar=tkinter.StringVar()
        self.wids=[['','',''] for i in range(7)]; mngbtn=[None]*2; mngtx=['生成','退出']
        args=['打开方式','文本输入','文件打开','保存方式','文本输出','文件保存']
        funs=['(处理方式)','编unicode','生成组合字符','解unicode','文本加解密']
        mngcmd=[lambda: self.thr(self.txdel),lambda: self.winqut(mng,'txmng')]
        for i in range(6):
            if i%3:
                mngrd=lambda k=i: self.mngrd(k); mngpth=lambda k=i: self.upth(k)
                mngscl=lambda k=i: self.scl(tag=self.wids[k][1])
                self.wids[i][0]=ttk.Radiobutton(mngemp[i],text=args[i])
                self.wids[i][0].config(variable=self.opclvr[i//3],value=i%3-1,command=mngrd)
                self.wids[i][1]=ttk.Entry(mngemp[i],width=30)
                self.wids[i][2]=ttk.Button(mngemp[i])
                if i%3-1: self.wids[i][2].config(text='浏览',command=mngpth)
                else: self.wids[i][2].config(text='全选',command=mngscl)
                self.wids[i][0].pack(side='left',expand=True)
                self.wids[i][1].pack(side='left',expand=True)
                self.wids[i][2].pack(side='left',expand=True)
            else:
                self.wids[i][0]=ttk.Label(mngemp[i],text=args[i])
                self.wids[i][0].pack(side='left',expand=True)
        self.wids[2][1].config(state='disabled'); self.wids[5][1].config(state='disabled')
        funop=ttk.OptionMenu(mngemp[6],self.funvar,funs[0],*funs)
        funop['menu'].configure(bg=self.bgin,fg=self.txchrc)
        funop.pack(side='left',expand=True)
        for i in range(2):
            mngbtn[i]=ttk.Button(mngemp[6],text=mngtx[i],command=mngcmd[i])
            mngbtn[i].pack(side='left',expand=True)
        for i in range(7): mngemp[i].pack(fill='both',expand=True)
    @staticmethod
    def ucd(itx):
        litx=len(itx); io,otx,i=0,['']*litx,0
        while i<litx:
            if litx-i>5 and itx[i:i+2]=='\\u': otx[io]=chr(int(itx[i+2:i+6],16)); i+=6
            else: otx[io]=itx[i]; i+=1
            io+=1
        return ''.join(otx)
    def undo(self):
        if self.ofl:
            try: self.tetr.edit_undo()
            except: self.rt.bell()
    def upd(self):
        try:
            resp=requests.get(self.data['new']); data=resp.json(); latvsn=data['tag_name']
            if latvsn==self.data['curvsn']: self.mb('i','o','提示','当前已经是最新版本')
            elif self.mb('i','yn','提示','有新版本!是否前往项目仓库下载?')=='yes':
                webbrowser.open(self.data['hub']+'/releases/latest')
        except:
            if self.mb('w','yn','无法连接服务器','是否重试?')=='yes': self.upd()
    def upgd(self):
        self.lvl[4]+=4
        if self.lvl[4]==20: self.itbtn[1].config(state='disabled')
        if self.sisl==3:
            while self.sisl!=4:
                si=random.choices(range(len(self.data['sipro'])),weights=self.data['sipro'])[0]
                if si not in self.sis and self.data['name'][si]!=self.mn:
                    self.lvl[self.sisl]=self.data['siup'][si]*random.choice(self.data['siupro'])
                    self.sis[self.sisl]=si; self.sisl+=1
            self.prit(st=3)
        else:
            up=random.randrange(4)
            self.lvl[up]+=self.data['siup'][self.sis[up]]*random.choice(self.data['siupro'])
            self.prit(st=up)
    def upth(self,p):
        arg=['打开','保存']; getpth=self.dlg(p//3+1,arg[p//3],('All text files','*.*'))
        if not getpth: return
        self.wids[p][1].delete(0,'end'); self.wids[p][1].insert(0,getpth)
    def winqut(self,arg,ky):
        a,b,c,d=arg.winfo_width(),arg.winfo_height(),arg.winfo_x(),arg.winfo_y()
        self.cfg[ky]=f'{a}x{b}+{c}+{d}'; arg.destroy()
if __name__=='__main__': fabits=Fabits()