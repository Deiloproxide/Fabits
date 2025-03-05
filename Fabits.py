import chardet,hashlib,numpy,os,random,requests,threading,time,tkinter,turtle,webbrowser
from tkinter import filedialog,ttk
from PIL import Image
til='自制小工具集合 By——红石社Deiloproxide'; tp=os.path; curvsn='v1.3.0'
urp1='https://{}/Deiloproxide/Fabits/'; urp2='github.com'
pro_lst5=[0.006]*73+[0.06*i+0.006 for i in range(16)]+[1]
pro_lst4=[0.051]*8+[0.51*i+0.051 for i in range(4)]
tu_lst=[0.5,0.55,0.75,1]; dic=numpy.zeros(shape=(52,91,5,2))
lst=numpy.zeros(shape=(38000,4),dtype=int); proes=numpy.zeros(38000)
name=['生命值','攻击力','防御力','生命值 ','攻击力 ','防御力 ',
      '元素充能效率','暴击率','暴击伤害','元素精通 ','治疗加成']
mnpro=[[[3],[1]],[[4],[1]],[[-1,6,9],[8,1,1]],[[-1,-2,9],[23,16,1]],
       [[-1,7,8,10,9],[33,5,5,5,2]]]
sipro=[4,4,4,6,6,6,4,3,3,4]; siupro=[0.7,0.8,0.9,1]
siup=[5.83,5.83,7.29,298.75,19.45,23.15,6.48,3.89,7.77,23.31]
knd=['生之花','死之羽','时之沙','空之杯','理之冠']; elmnkd='火水风雷草冰岩 '
hdnms={b'PNG':'.png',b'GIF8':'.gif',b'PDF':'.pdf',b'Rar!':'.rar',
       b'FLV':'.flv',b'BM':'.bmp',b'AVI LIST':'.avi',b'8BPS':'.psd',
       b'WAVEfmt':'.wav',b'MZ':'.exe',b'ftypmp':'.mp4',b'ftypM4':'.m4a',
       b'\xff\xd8\xff':'.jpg',b'\x49\x49\x2a\x00':'.tiff',b'\x1f\x8b':'.gz',
       b'PK\x03\x04':'.zip',b'7Z\xBC\xAF\x27':'.7z',b'\x49\x44\x33':'.mp3'}
icc=('r117l117br26l22r24l24l12l22r24l22r24l22el111l23br22l24l12l24er28r13br22'
     'l22r24l23r22r12l12l27l12l23r24l23r22r17r26l22l16r111r24l22r24l22l14r12'
     'l23r13l227el14l215br26l22l16l22el32r22bl23r22r13l12l25l16l25l12el27l17'
     'br12l12l22l12el28l11bl34r12l12l22r24r12l12l27l12l23r24r12l12l22r24l22e')
icd=('bl13l13l12r16l18r11r12l11l13l13l12r16l18r11r12l11el28bcl15l15l15l1'
     '5el14l14bcl13l13l13l13el12l12bcl11l11l11l11el01l11cbl01r11ebl11l11'
     'l11l11el11l11bl11r11el02l12bl01r11ebl11l11l11l11el11l11bl11r11el11')
mb={'o':'ok','a':'abort','r':'retry','c':'cancel','y':'yes','n':'no',
    'oc':'okcancel','yn':'yesno','ync':'yesnocancel','rc':'retrycancel',
    'arc':'abortretrycancel','e':'error','i':'info','q':'question','w':'warning'}
class Fabits:
    def __init__(self):
        self.rt=tkinter.Tk(); self.rt.geometry('1440x810+120+120')
        self.rt.iconphoto(True,tkinter.PhotoImage(file='Na.png'))
        self.rt.title(til); self.adcon(); self.admnu()
        self.prefn(); self.ics(); self.rt.mainloop()
    def adcon(self):
        self.memp1=tkinter.Frame(self.rt)
        self.ls=ttk.Treeview(self.memp1,columns=('opt',),show='tree')
        self.slb=tkinter.Scrollbar(self.memp1); self.cvs=tkinter.Canvas(self.rt)
        self.sc=turtle.TurtleScreen(self.cvs); self.tl=turtle.RawTurtle(self.sc)
        self.ls.column("#0",width=0,stretch=False)
        self.ls.column('opt',width=200,anchor='w'); stl=ttk.Style()
        stl.configure("Treeview",font=("TkDefaultFont",12,'bold'),rowheight=20)
        self.ls.config(yscrollcommand=self.slb.set)
        self.slb.config(command=self.ls.yview)
        self.memp2=tkinter.Frame(self.rt)
        self.tetr=tkinter.Text(self.memp2); self.slb2=tkinter.Scrollbar(self.memp2)
        self.tetr.config(yscrollcommand=self.slb2.set)
        self.slb2.config(command=self.tetr.yview)
        self.tetr.config(font=("TkDefaultFont",12))
        self.tetr.bind('<Key>',lambda s: self.cchg())
        self.ofl=self.nfl=self.chg=0; self.txflnm='未命名文件'
        self.slb.pack(side='right',fill='y'); self.ls.pack(fill='both',expand=True)
        self.slb2.pack(side='right',fill='y'); self.tetr.pack(fill='both',expand=True)
    def adfun(self,lbl,knd):
        mntmp=tkinter.Menu(self.mnu,tearoff=0)
        self.mnu.add_cascade(label=lbl,menu=mntmp)
        for i in knd: mntmp.add_command(label=i,command=knd[i])
    def admnu(self):
        self.clr={'black','red','green','yellow','blue','purple','cyan','grey','white'}
        self.funknd={
        '文件(F)':{'新建':self.opnf,'打开':lambda: self.opnf(1),'保存':self.savf,
            '另存为':lambda: self.savf(1),'导入':lambda: self.opnf(nda=1),
            '导出':lambda: self.savf(nda=1),'关闭':self.clsf,'退出':lambda: self.winqut(self.rt)},
        '算法(A)':{'同分异构体数量':lambda: self.thr(self.iso),
            '链表冒泡排序':lambda: self.thr(self.lnksrt),'最大环长度':lambda: self.thr(self.ring),
            '求解罗马数字':lambda: self.thr(self.rome)},
        '批处理(B)':{'补齐缺失后缀':lambda: self.thr(self.adlsnd),
            '图片颜色替换':lambda: self.thr(self.clrplc),'图片排序':lambda: self.thr(self.imgsrt),
            '图片加解密':lambda: self.thr(self.picpt),'生成组合字符':lambda: self.txmng(self.rndchr),
            '解unicode':lambda: self.txmng(self.ucd),'视频重命名':lambda: self.thr(self.vdornm),
            '文本加解密':lambda: self.txmng(lambda itx: self.txcbtb(itx,0,0,0))},
        '网络(I)':{'官网':lambda: webbrowser.open('https://nahida520.love'),
            '项目仓库':lambda: webbrowser.open(urp1.format(urp2)),'版本检测':self.upd},
        '工具(T)':{'抽卡模拟器':self.conpuw,'圣遗物强化':self.itsth,'迷宫可视化':self.mazepl,
            '抽卡概率计算':lambda: self.thr(self.pulpro)},
        '设置(S)':{'清屏':self.clear,'帮助':lambda: self.thr(self.hlp),'图标':self.ics}}
        self.mnu=tkinter.Menu(self.rt)
        for i in self.clr: self.ls.tag_configure(i,foreground=i)
        for i in self.funknd: self.adfun(i,self.funknd[i])
        self.rt.config(menu=self.mnu)
    def adlsnd(self):
        self.show(self.ls,'(1/2)打开','cyan')
        self.pth=self.dlg(0,'打开',('Text files','*.txt'))
        if not self.pth: return
        fnames=[i for i in os.listdir(self.pth) if tp.isfile(self.pnm(i))]
        names=[i for i in fnames if not tp.splitext(i)[1]]
        self.show(self.ls,'(2/2)转换','cyan'); lnm=len(names)
        if names: self.pginit('查找添加缺失后缀',lnm)
        for i in range(lnm):
            nm=self.pnm(names[i]); fl=open(nm,'rb'); hd=fl.read(32); fl.close()
            for j in hdnms:
                if j in hd:
                    self.pgu(i+1,f"{name} -> {name+hdnms[j]}",'cyan')
                    os.rename(nm,nm+hdnms[j]); break
            else: self.pgu(i+1,f'未知文件类型: {name}','red')
        self.show(self.ls,'进程已结束','red')
        self.rt.after(250); self.winqut(self.pgm,ask=False)
    def adups(self,i,n):
        if i in self.ups: self.mb('w','o','选择角色重复','请重新选择')
        else: self.ups[n]=i; self.show(self.et,f'角色{i}添加成功!','red')
        for i in self.ups:
            if not i: return
        self.btn1.config(state='normal'); self.btn2.config(state='normal')
    def cchg(self):
        if not self.chg: self.chg=1; self.rt.title(f'{til} - {self.txflnm}*')
    def clear(self): self.ls.delete(*self.ls.get_children())
    def clrplc(self):
        self.show(self.ls,'(1/4)打开','cyan')
        pnm=self.dlg(1,'打开',('All image files','*.*'))
        if not pnm: return
        pic=Image.open(pnm)
        fm=lambda cl: (int(cl[:2],16),int(cl[2:4],16),int(cl[4:],16))
        nclr=list(map(fm,self.lmd('输入多个被替换颜色(16进制表示)').split()))
        clr=fm(self.lmd('输入替换颜色(16进制表示)'))
        self.show(self.ls,'(2/4)转换','cyan'); pix=numpy.array(pic)
        self.show(self.ls,'(3/4)替换','cyan')
        for i in nclr: alc=(pix[:,:,:3]==i).all(axis=-1); pix[alc,:3]=clr
        self.show(self.ls,'(4/4)保存','cyan'); pic=Image.fromarray(pix)
        new=self.dlg(2,'保存',('Image files','*.png'))
        if not new: return
        if not new.endswith('.png'): new+='.png'
        pic.save(new); self.show(self.ls,'进程已结束','red')
    def clsf(self):
        if not self.ofl: return
        if self.chg:
            svst=self.mb('q','ync','关闭文件时保存','未保存的内容将会丢失,是否保存?')
            if svst=='yes':
                if self.savf(): return
                else: self.tetr.delete('1.0','end')
            elif svst=='cancel': return
        else: self.tetr.delete('1.0','end')
        self.memp2.pack_forget(); self.ofl=0; self.rt.title(til)
    def conpuw(self):
        self.pu=tkinter.Toplevel(self.rt)
        self.pu.title('抽卡模拟器'); self.pu.geometry('400x450')
        self.pum=tkinter.Menu(self.pu); self.pu.config(menu=self.pum)
        self.ups5=tkinter.Menu(self.pum,tearoff=0)
        self.ups41=tkinter.Menu(self.pum,tearoff=0)
        self.ups42=tkinter.Menu(self.pum,tearoff=0)
        self.ups43=tkinter.Menu(self.pum,tearoff=0)
        self.pum.add_cascade(label='五星UP',menu=self.ups5)
        self.pum.add_cascade(label='四星UP1',menu=self.ups41)
        self.pum.add_cascade(label='四星UP2',menu=self.ups42)
        self.pum.add_cascade(label='四星UP3',menu=self.ups43)
        self.dtm={'ups5':None,'ups4':None,'fups5':None,
                  'wpns5':None,'wpns4':None,'wpns3':None}
        itm,litm,ctm,self.put5,self.put4,self.true_up5,self.true_up4=['']*100,0,'',0,0,0,0
        self.fu,self.ups=0,['']*4
        libf=self.txcbtb('',1,0,1,frmopn='PulChrLibs.nda'); libs=libf.split('\r\n')
        for i in libs:
            if not ctm: ctm=i
            elif i in self.dtm: self.dtm[ctm]=itm[:litm]; litm=0; ctm=i
            else:
                for j in i.split():
                    if ctm=='ups5':
                        self.ups5.add_command(label=j,command=lambda k=j: self.adups(k,0))
                    elif ctm=='ups4':
                        self.ups41.add_command(label=j,command=lambda k=j: self.adups(k,1))
                        self.ups42.add_command(label=j,command=lambda k=j: self.adups(k,2))
                        self.ups43.add_command(label=j,command=lambda k=j: self.adups(k,3))
                    itm[litm]=j; litm+=1
        self.dtm[ctm]=itm[:litm]; self.lb=tkinter.Label(self.pu,text='祈愿结果:')
        self.et=ttk.Treeview(self.pu,columns=('opt',),show='tree')
        self.slet=tkinter.Scrollbar(self.pu); self.emp=tkinter.Frame(self.pu)
        self.btn1=tkinter.Button(self.emp,text='祈愿一次',command=lambda: self.pul(1))
        self.btn2=tkinter.Button(self.emp,text='祈愿十次',command=lambda: self.pul(10))
        self.btn3=tkinter.Button(self.emp,text='退出',command=lambda: self.winqut(self.pu))
        self.btn1.config(width=8,state='disabled')
        self.btn2.config(width=8,state='disabled')
        self.btn3.config(width=8)
        self.et.column("#0",width=0,stretch=False)
        self.et.column('opt',width=200,anchor='w')
        self.et.config(yscrollcommand=self.slet.set)
        self.slet.config(command=self.et.yview)
        for i in self.clr: self.et.tag_configure(i, foreground=i)
        self.slet.pack(side='right',fill='y'); self.lb.pack(expand=True)
        self.et.pack(fill='both',expand=True); self.emp.pack(fill='x',expand=True)
        self.btn1.pack(side='left',expand=True)
        self.btn2.pack(side='left',expand=True)
        self.btn3.pack(side='left',expand=True)
        self.pu.grab_set(); self.pu.wait_window()
    @staticmethod
    def dlg(n,tle,flt):
        if n==0: dl=filedialog.askdirectory(title=tle)
        elif n==1: dl=filedialog.askopenfilename(title=tle,filetypes=(flt,))
        else: dl=filedialog.asksaveasfilename(title=tle,filetypes=(flt,))
        return dl
    def gen(self):
        self.ln,self.wd=map(int,self.lmd('输入迷宫的长和宽').split())
        self.bx,self.by=map(int,self.lmd('输入迷宫起始点x,y').split())
        self.ex,self.ey=map(int,self.lmd('输入迷宫终点x,y').split())
        self.restul(); self.btn4.config(state='disabled')
        self.sz=min(250/self.ln,250/self.wd)
        self.maze=numpy.ones(shape=(self.ln*2+1,self.wd*2+1),dtype=int)
        for i in range(self.ln*2+1):
            for j in range(self.wd*2+1):
                if i in [0,self.ln*2] or j in [0,self.wd*2]: self.maze[i,j]=0
        self.mzshw(0,0,self.ln*2+1,self.wd*2+1,'#000000')
        self.mzshw(1,1,self.ln*2,self.wd*2,'#ffffff')
        stk,top=numpy.zeros(shape=(self.ln*self.wd,4),dtype=int),0
        stk[top]=[1,1,self.ln*2-1,self.wd*2-1]; top+=1
        while top>0:
            top-=1; lx,ly,rx,ry=stk[top]
            if rx-lx<2 or ry-ly<2: continue
            x=random.randint(lx+1,rx-1)//2*2; y=random.randint(ly+1,ry-1)//2*2
            stk[top]=[lx,y+1,x-1,ry]; top+=1; stk[top]=[lx,ly,x-1,y-1]; top+=1
            stk[top]=[x+1,ly,rx,y-1]; top+=1; stk[top]=[x+1,y+1,rx,ry]; top+=1
            for i in range(lx,rx+1): self.maze[i][y]=0
            for i in range(ly,ry+1): self.maze[x][i]=0
            self.mzshw(lx,y,rx+1,y+1,'#000000'); self.mzshw(x,ly,x+1,ry+1,'#000000')
            rtmp=[(random.randint(lx,x-1)//2*2+1,y),(random.randint(x+1,rx)//2*2+1,y),
                  (x,random.randint(ly,y-1)//2*2+1),(x,random.randint(y+1,ry)//2*2+1)]
            k=random.randrange(4)
            for i in range(4):
                if k-i:
                    self.maze[rtmp[i][0],rtmp[i][1]]=1
                    self.mzshw(rtmp[i][0],rtmp[i][1],rtmp[i][0]+1,rtmp[i][1]+1,'#ffffff')
        self.maze[self.bx*2-1,self.by*2-1]=1; self.maze[self.ex*2-1,self.ey*2-1]=2
        self.mzshw(self.bx*2-1,self.by*2-1,self.bx*2,self.by*2,'#22cefc')
        self.mzshw(self.ex*2-1,self.ey*2-1,self.ex*2,self.ey*2,'#00ff00')
        self.btn4.config(state='normal'); self.btn5.config(state='normal')
    def getit(self):
        self.sis,self.lvl,self.kd=[0]*4,[0]*5,random.randrange(5)
        self.mn=random.choices(mnpro[self.kd][0],weights=mnpro[self.kd][1])[0]
        if self.mn==-1: self.mn=random.randint(0,2)
        if self.mn==-2:
            self.mn=random.choice(elmnkd)
            if self.mn==' ': self.mn='物理'
            else: self.mn+='元素'
            self.mn+='伤害加成'
        else: self.mn=name[self.mn]
        self.sisl,self.nm=0,random.choices((3,4),weights=(4,1))[0]
        while self.sisl in range(self.nm):
            si=random.choices(range(len(sipro)),weights=sipro)[0]
            if si not in self.sis and name[si]!=self.mn:
                self.lvl[self.sisl]=siup[si]*random.choice(siupro)
                self.sis[self.sisl]=si; self.sisl+=1
        self.btn2.config(state='normal')
        self.et.delete(*self.et.get_children()); self.prit()
    def getvar(self):
        self.var=self.etr.get()
        if self.var: self.tmp.destroy()
    def hlp(self):
        fl=open('README.md','r',encoding='utf-8'); lns=fl.readlines()
        for i in lns:
            if i!='\n': self.show(self.ls,i,'green')
    @staticmethod
    def hshgn():
        licc,lictmp,hdgl,hsh=len(icc),0,64,hashlib.sha256()
        while True:
            if hdgl==64:
                hdgl=0; hsh.update(icc[lictmp%licc].encode())
                lictmp+=1; hdg=hsh.hexdigest()
            yield int(hdg[hdgl:hdgl+2],16)
            hdgl+=2
    def ico(self,icx,ang,sz,clr):
        cmds={'b':lambda a: (self.tl.begin_fill(),self.tl.pendown()),
              'e':lambda a: (self.tl.end_fill(),self.tl.penup()),
              'l':lambda a: (self.tl.lt(int(a[0])*ang),self.tl.fd(int(a[1:])*sz)),
              'r':lambda a: (self.tl.rt(int(a[0])*ang),self.tl.fd(int(a[1:])*sz)),
              'c':lambda a: self.tl.color(cmds[next(clr)]),
              'd':'#22cefc','w':'#ffffff'}
        i,j,cmd,dig=0,len(icx),cmds['c'],''
        while i<j:
            if icx[i].isdigit(): dig+=icx[i]
            else: cmd(dig); dig,cmd='',cmds[icx[i]]
            i+=1
        cmd(dig)
    def ics(self):
        self.memp1.pack_forget()
        self.restul(); self.cvs.pack(fill='both',expand=True)
        self.ico(icc,60,12,iter('d')); self.rt.after(500); self.restul()
        self.ico('r0114r212l30',45,5,iter('d'))
        self.ico(icd,90,22,iter('dwdwd')); self.tl.rt(45); self.tl.fd(255)
        icm1,icm2='圣·西门科技股份有限公司 出品','Sig·WestGate Tech. L.C.D. present.'
        self.tl.write(icm1,align='center',font=("TkDefaultFont",25,'bold'))
        self.tl.fd(50); self.tl.write(icm2,align='center',font=("TkDefaultFont",20,'bold'))
        self.rt.after(1250); self.cvs.pack_forget()
        self.restul(); self.memp1.pack(side='bottom',fill='both',expand=True)
    def imgsrt(self):
        self.show(self.ls,'(1/4)打开','cyan')
        self.pth=self.dlg(0,'打开',('Text files','*.txt'))
        if not self.pth: return
        names=[i for i in os.listdir(self.pth) if i.lower().endswith('.png')]
        ln=len(names); lnr=range(ln); self.pginit('图片排序',ln)
        msg=lambda tx,x: self.pgu(x+1,f'已{tx}{x+1}/{len(names)}','cyan')
        self.show(self.ls,'(2/4)转换','cyan')
        pis=[[numpy.array(Image.open(self.pnm(names[i])))[:,:3],msg('转换',i)] for i in lnr]
        self.rt.after(250); self.winqut(self.pgm,ask=False); self.pginit('图片排序',ln)
        self.show(self.ls,'(3/4)排序','cyan')
        sort=[[numpy.mean(pis[i][0]),names[i],msg('完成',i)] for i in lnr]
        self.rt.after(250); self.winqut(self.pgm,ask=False)
        sort=sorted(sort,key=lambda i:i[0]); self.show(self.ls,'(4/4)整理','cyan')
        for i in lnr: os.rename(self.pnm(sort[i][1]),self.pnm(f'pix{i:04d}.png'))
        names=[i for i in os.listdir(self.pth) if i.lower().endswith('.png')]
        for i in lnr: os.rename(self.pnm(names[i]),self.pnm(f'pic{i:04d}.png'))
        self.show(self.ls,'进程已结束','red')
    def inp(self,st,tx,ab,tx1,tx2,cmd1,cmd2,shw=''):
        self.tmp=tkinter.Toplevel(self.rt)
        self.tmp.title(''); self.tmp.geometry('220x100')
        self.lb=tkinter.Label(self.tmp,text=st)
        if shw: self.etr=tkinter.Entry(self.tmp,show=shw)
        else: self.etr=tkinter.Entry(self.tmp)
        self.etr.insert('end',tx); self.emp=tkinter.Frame(self.tmp)
        self.btn1=tkinter.Button(self.emp,text=tx1,command=cmd1)
        self.btn2=tkinter.Button(self.emp,text=tx2,command=cmd2)
        self.btn1.config(width=10); self.btn2.config(width=10)
        self.lb.pack(expand=True)
        if ab: self.etr.pack(expand=True)
        self.emp.pack(fill='x',expand=True)
        self.btn1.pack(side='left',expand=True)
        self.btn2.pack(side='right',expand=True)
        self.tmp.grab_set(); self.tmp.wait_window()
        return self.var
    def iso(self):
        n=int(self.lmd('基团-CnH2n+1,输入n值'))
        hm,isol=numpy.zeros(n+1,dtype=int),1; hm[0]=1
        for i in range(n):
            b,c,res=0,0,0; a=i-2*c
            while c<=a:
                res+=hm[a]*hm[b]*hm[c]; a,b=a-1,b+1
                if a<b: c+=1; a,b=i-2*c,c
            hm[isol],isol=res,isol+1
        self.show(self.ls,f'{hm[n]}','green')
    def itsth(self):
        self.it=tkinter.Toplevel(self.rt)
        self.it.title('圣遗物强化'); self.it.geometry('400x450')
        self.lb=tkinter.Label(self.it,text='强化结果:')
        self.et=ttk.Treeview(self.it,columns=('opt',),show='tree')
        self.slet=tkinter.Scrollbar(self.it)
        self.emp=tkinter.Frame(self.it)
        self.btn1=tkinter.Button(self.emp,text='获取',command=self.getit)
        self.btn2=tkinter.Button(self.emp,text='强化',command=self.upgd)
        self.btn3=tkinter.Button(self.emp,text='退出',command=lambda: self.winqut(self.it))
        self.btn1.config(width=8)
        self.btn2.config(width=8,state='disabled')
        self.btn3.config(width=8)
        self.et.column("#0",width=0,stretch=False)
        self.et.column('opt',width=200,anchor='w')
        self.et.config(yscrollcommand=self.slet.set)
        self.slet.config(command=self.et.yview)
        for i in self.clr: self.et.tag_configure(i, foreground=i)
        self.slet.pack(side='right',fill='y'); self.lb.pack(expand=True)
        self.et.pack(fill='both',expand=True); self.emp.pack(fill='x',expand=True)
        self.btn1.pack(side='left',expand=True)
        self.btn2.pack(side='left',expand=True)
        self.btn3.pack(side='left',expand=True)
        self.it.grab_set(); self.it.wait_window()
    def lnksrt(self):
        arr,hd=eval(self.lmd('输入链表')),int(self.lmd('输入头地址')); lnkl,cur=0,hd
        while cur!=-1: lnkl+=1; cur=arr[cur][1]
        for i in range(lnkl-1,-1,-1):
            p,q=hd,-1; r=arr[p][1]
            for j in range(i):
                if arr[p][0]>arr[r][0]:
                    if q==-1: hd=r
                    else: arr[q][1]=r
                    arr[p][1],arr[r][1]=arr[r][1],p; p,r=r,p
                p,q,r=r,p,arr[r][1]
        self.show(self.ls,f'{arr},head={hd}','green')
    def mazepl(self):
        self.mz=tkinter.Toplevel(self.rt); self.mz.title('迷宫可视化')
        self.mz.geometry('300x100'); self.lb=tkinter.Label(self.mz,text='迷宫设置')
        self.emp=tkinter.Frame(self.mz)
        self.btn4=tkinter.Button(self.emp,text='生成',command=self.gen)
        self.btn5=tkinter.Button(self.emp,text='解',command=self.slv)
        self.btn6=tkinter.Button(self.emp,text='退出',command=lambda: self.winqut(self.mz))
        self.btn4.config(width=8); self.btn5.config(width=8,state='disabled')
        self.btn6.config(width=8); self.memp1.pack_forget()
        self.cvs.pack(fill='both',expand=True); self.lb.pack(expand=True)
        self.emp.pack(fill='x',expand=True); self.btn4.pack(side='left',expand=True)
        self.btn5.pack(side='left',expand=True); self.btn6.pack(side='left',expand=True)
        self.mz.grab_set(); self.mz.wait_window(); self.cvs.pack_forget(); self.restul()
        self.memp1.pack(side='bottom',fill='both',expand=True)
    @staticmethod
    def mb(icn,tp,tle,msg):
        mbt=tkinter.messagebox.Message(icon=mb[icn],type=mb[tp],title=tle,message=msg)
        res=mbt.show(); return res
    def mzshw(self,lx,ly,rx,ry,clr):
        self.tl.teleport((lx-self.ln)*self.sz+515,(ly-self.wd)*self.sz-275)
        self.tl.fillcolor(clr); self.tl.begin_fill()
        for i in range(2):
            self.tl.fd((rx-lx)*self.sz); self.tl.lt(90)
            self.tl.fd((ry-ly)*self.sz); self.tl.lt(90)
        self.tl.end_fill()
    def opnf(self,ext=0,nda=0):
        self.ofl=1; self.memp2.pack(fill='both',expand=True)
        if self.chg:
            svst=self.mb('q','ync','关闭文件时保存','上一个未保存的内容将会丢失,是否保存?')
            if svst=='cancel' or (svst=='yes' and self.savf()):
                self.rt.title(f'{til} - {self.txflnm}*'); return
        if ext:
            self.rsflnm=self.dlg(1,'打开',('All text files','*.*'))
            if self.rsflnm:
                self.tetr.delete('1.0','end')
                self.txflnm=self.rsflnm; fl=open(self.txflnm,'rb')
                data=fl.read(1024); enc=chardet.detect(data)['encoding']
                fl.seek(0); data=fl.readlines()
                for i in data: self.tetr.insert('insert',i.decode(enc))
                fl.close(); self.nfl=0
                self.rt.title(f'{til} - {self.txflnm}')
            else: self.rt.title(f'{til} - {self.txflnm}'); return
        else:
            self.nfl=1; self.txflnm='未命名文件'; self.tetr.delete('1.0','end')
            if nda:
                byt=self.txcbtb(None,1,0,1)
                if byt!=-1: self.tetr.insert('insert',byt)
        self.chg=0; self.rt.title(f'{til} - {self.txflnm}')
    def pginit(self,tx,tol):
        self.pgm=tkinter.Toplevel(self.rt); self.pgm.title(tx)
        self.pgm.geometry('400x250'); self.pgl=tkinter.Label(self.pgm,text='0.00%')
        self.pgb=ttk.Progressbar(self.pgm); self.pgsb=tkinter.Scrollbar(self.pgm)
        self.pgt=ttk.Treeview(self.pgm,columns=('opt',),show='tree')
        self.pgt.column("#0",width=0,stretch=False)
        self.pgt.column('opt',width=200,anchor='w')
        self.pgt.config(yscrollcommand=self.pgsb.set)
        self.pgsb.config(command=self.pgt.yview)
        for i in self.clr: self.pgt.tag_configure(i,foreground=i)
        self.pgb['maximum']=tol; self.tol=tol/100; self.pgb.config(length=350)
        self.pgl.pack(); self.pgb.pack()
        self.pgsb.pack(side='right',fill='y'); self.pgt.pack(fill='both',expand=True)
    def pgu(self,num,tx,clr):
        self.pgl.config(text=f'{num/self.tol:.2f}%'); self.pgb['value']=num
        if tx: self.show(self.pgt,tx,clr)
    def picpt(self):
        self.show(self.ls,'(1/3)打开','cyan')
        fl=self.dlg(1,'打开',('All image files','*.*'))
        if not fl: return
        pic=Image.open(fl); pix,h,w=numpy.array(pic),pic.height,pic.width
        self.show(self.ls,'(2/3)加密','cyan'); ln=len(pix[0,0])
        gn=self.hshgn(); immsk=numpy.zeros_like(pix); self.pginit('图片加密',h)
        for i in range(h):
            for j in range(w):
                for k in range(ln): immsk[i,j,k]=next(gn)
            self.pgu(i+1,f'已加密{i+1}/{h}','cyan')
        pic=Image.fromarray(numpy.bitwise_xor(pix,immsk))
        self.rt.after(250); self.winqut(self.pgm,ask=False)
        self.show(self.ls,'(3/3)保存','cyan')
        new=self.dlg(2,'保存',('Image files','.png'))
        if not new: return
        if new.endswith('.png'): pic.save(new)
        else: pic.save(f'{new}.png')
        self.show(self.ls,'进程已结束','red')
    def prefn(self):
        self.pnm=lambda fn: tp.join(self.pth,fn)
        self.scl=lambda: self.etr.selection_range(0,'end')
        self.tru=lambda: self.putvar(True); self.fls=lambda: self.putvar(False)
        self.lmd=lambda ch,show='': self.inp(ch,'',True,'全选','确认',self.scl,self.getvar,shw=show)
    def prit(self,st=[]):
        self.show(self.et,f'{knd[self.kd]}(+{self.lvl[4]})','cyan')
        self.show(self.et,self.mn,'blue')
        for i in range(self.sisl):
            nm=name[self.sis[i]]; clr='red' if i in st else 'green'
            if nm[-1]==' ':
                self.show(self.et,f'{nm[:-1]}+{round(self.lvl[i]+0.05,1)}',clr)
            else: self.show(self.et,f'{nm}+{round(self.lvl[i]+0.05,1)}%',clr)
        self.show(self.et,'','black')
    def pul(self,n):
        for i in range(n):
            ran,tup=random.random(),random.random()
            if ran<=pro_lst5[self.put5]:
                if self.true_up5: self.show(self.et,self.ups[0],'yellow'); self.true_up5=0
                elif tup<=tu_lst[self.fu]:
                    self.show(self.et,self.ups[0],'yellow'); self.true_up5,self.fu=0,0
                else:
                    it=random.choice(self.dtm['fups5']+self.dtm['wpns5'])
                    self.show(self.et,it,'yellow'); self.show(self.et,'歪','red')
                    self.true_up5,self.fu=1,self.fu+1
                self.put5,self.put4=0,self.put4+1
            elif ran<=pro_lst5[self.put5]+pro_lst4[self.put4]:
                if tup<=0.5 or self.true_up4:
                    self.show(self.et,random.choice(self.ups[1:]),'purple')
                    self.true_up4=0
                else:
                    it=random.choice(self.dtm['ups4']+self.dtm['wpns4'])
                    self.show(self.et,it,'purple'); self.true_up4=1
                self.put5,self.put4=self.put5+1,0
            else:
                self.show(self.et,random.choice(self.dtm['wpns3']),'blue')
                self.put5,self.put4=self.put5+1,self.put4+1
        self.show(self.et,f'垫{self.put5}发','cyan')
    def pulpro(self):
        global dic,lst; res=numpy.zeros(52,dtype=float); s=int(self.lmd('原石数'))
        pb=int(self.lmd('粉球数')); put=int(self.lmd('垫池数(0-89)'))
        fu,tu=int(self.lmd('已经连歪数')),int(self.lmd('是否大保底(0/1)'))
        _len,st,ed=0,0,50; pb+=s//160; lst[_len]=[0,put,fu,tu]
        proes[_len]=1; _len+=1; self.pginit('抽卡模拟',pb)
        for i in range(pb):
            for j in range(_len):
                ups,puts,false_up,true_up=lst[j]; pro=proes[j]
                ups=min(ups,50); pros=pro_lst5[puts]; tu_pro=tu_lst[false_up]
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
            self.pgu(i+1,f'已完成{i+1}抽','cyan')
        for i in range(_len): res[lst[i,0]]+=proes[i]*100
        for i in range(ed+1):
            if res[i]>0.1: st=i; break
        for i in range(ed,0,-1):
            if res[i]<0.1: res[i-1]+=res[i]
            else: ed=i; break
        self.rt.after(250); self.winqut(self.pgm,ask=False)
        self.show(self.ls,'UP数 概率','purple')
        for i in range(st,ed+1): self.show(self.ls,f'{i:>2d}{res[i]:7.2f}%','purple')
    def putvar(self,val): self.var=val; self.tmp.destroy()
    def restul(self): self.tl.reset(); self.tl.ht(); self.tl.speed(0); self.tl.penup()
    def ring(self):
        n=int(self.lmd('输入n值(对)')); m,flg=0,[1]*(2*n)
        for i in range(2*n):
            k,rngl=i,0
            while flg[k]: flg[k],rngl=0,rngl+1; k=k*2 if k<n else 2*(k-n)+1
            m=max(m,rngl)
        self.show(self.ls,f'{m}','green')
    def rndchr(self,itx):
        n=int(self.inp('输入字符密度','',True,'全选','确认',self.scl,self.getvar))
        lst=list(range(768,880))+list(range(1155,1162)); io,otx=0,['']*len(itx)*(n+1)
        for i in itx:
            otx[io]=i; io+=1; chs=map(chr,random.choices(lst,k=n))
            for j in chs: otx[io]=j; io+=1
        return ''.join(otx)
    def rome(self):
        ch=self.lmd('输入罗马数字'); num,stk,top=0,[0]*len(ch),0
        dic={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000,
             'i':1,'v':5,'x':10,'l':50,'c':100,'d':500,'m':1000}
        for i in ch:
            while top>0 and dic[i]>stk[top-1]: top-=1; num-=stk[top]
            stk[top]=dic[i]; top+=1
        while top>0: top-=1; num+=stk[top]
        self.show(self.ls,f'{num}','green')
    def savf(self,at=0,nda=0):
        if not self.ofl: return
        if nda: ot=self.txcbtb(self.tetr.get('1.0','end'),0,1,0); return
        if self.nfl or at:
            self.rsflnm=self.dlg(2,'保存',('All text files','*.*'))
            if not self.rsflnm: return -1
            if not tp.splitext(self.rsflnm)[1]: self.rsflnm+='.txt'
            self.txflnm=self.rsflnm; self.rt.title(f'{til} - {self.txflnm}')
        fl=open(self.txflnm,'w',encoding='utf-8'); self.nfl=self.chg=0
        txres=self.tetr.get('1.0','end'); fl.write(txres); fl.close()
    @staticmethod
    def show(arg,st,cl):
        itm=arg.insert('','end',values=(st,),tags=(cl,)); arg.see(itm)
    def slv(self):
        self.btn4.config(state='disabled'); self.btn5.config(state='disabled')
        tmp=[[1,0],[-1,0],[0,1],[0,-1]]
        stk,top=numpy.zeros(shape=(self.ln*self.wd,3),dtype=int),0
        f=lambda j: tmp[i][j]+(tmp[i][j]<0); g=lambda j: tmp[i][j]*2+1-(tmp[i][j]<0)
        stk[top]=[self.bx*2-1,self.by*2-1,0]; flg=False
        while top>=0:
            x,y,i=stk[top]; self.maze[x][y]=0
            if flg:
                self.mzshw(x+f(0),y+f(1),x+g(0),y+g(1),'#22cefc')
                top-=1; continue
            if i==4: top-=1; continue
            if not self.maze[x+tmp[i][0]][y+tmp[i][1]]: stk[top][2]=i+1; continue
            if self.maze[x+tmp[i][0]*2][y+tmp[i][1]*2]==2: flg=True; continue
            self.maze[x+tmp[i][0]][y+tmp[i][1]]=0
            self.mzshw(x+f(0),y+f(1),x+g(0),y+g(1),'#ff00ff')
            if not self.maze[x+tmp[i][0]*2][y+tmp[i][1]*2]: stk[top][2]=i+1; continue
            top+=1; stk[top]=[x+tmp[i][0]*2,y+tmp[i][1]*2,0]
        self.btn4.config(state='normal')
    @staticmethod
    def thr(fun): tsk=threading.Thread(target=fun); tsk.start()
    def txcbtb(self,byt,opn,clos,ecpt,frmopn=''):
        if opn:
            if frmopn: flnm=frmopn
            elif ecpt: flnm=self.dlg(1,'打开',('Nahida Data Assets','*.nda'))
            else: flnm=self.dlg(1,'打开',('All text files','*.*'))
            if not flnm: return -1
            fl=open(flnm,'rb'); byt=fl.read(); fl.close()
        else: byt=byt.encode('utf-8')
        txlst=bytearray(byt); gn=self.hshgn()
        txlst=[i^next(gn) for i in txlst]; byt=bytes(txlst)
        if clos:
            if ecpt:
                flnm=self.dlg(2,'保存',('All text files','*.*'))
                if not flnm: return -1
                if not tp.splitext(flnm)[1]: flnm+='.txt'
            else:
                flnm=self.dlg(2,'保存',('Nahida Data Assets','*.nda'))
                if not flnm: return -1
                if not flnm.endswith('.nda'): flnm+='.nda'
            fl=open(flnm,'wb'); fl.write(byt); fl.close()
        else: return byt.decode('utf-8',errors='backslashreplace')
    def txmng(self,fun):
        self.show(self.ls,'(1/3)打开','cyan')
        if self.inp('打开方式','',False,'文本输入','文件打开',self.tru,self.fls):
            itx=self.lmd('输入你的文本'); enc='utf-8'
        else:
            flnm=self.dlg(1,'打开',('All text files','*.*'))
            if not flnm: return
            fl=open(flnm,'rb')
            if flnm.endswith('.nda'): enc='utf-8'
            else: data=fl.read(1024); enc=chardet.detect(data)['encoding']; fl.seek(0)
            itx=fl.read().decode(enc); fl.close()
        self.show(self.ls,'(2/3)处理','cyan')
        otx=fun(itx)
        self.show(self.ls,'(3/3)保存','cyan')
        if self.inp('保存方式','',False,'文本输出','文件保存',self.tru,self.fls):
            self.inp('生成结果',otx,True,'全选','确认',self.scl,self.getvar)
        else:
            new=self.dlg(2,'保存',('All text files','*.*'))
            if not new: return
            if not tp.splitext(new)[1]: new+='.txt'
            fl=open(new,'w',encoding=enc); fl.write(otx); fl.close()
        self.show(self.ls,'进程已结束','red')
    @staticmethod
    def ucd(itx):
        litx=len(itx); io,otx,i=0,['']*litx,0
        while i<litx:
            if litx-i>5 and itx[i:i+2]=='\\u': otx[io]=chr(int(itx[i+2:i+6],16)); i+=6
            else: otx[io]=itx[i]; i+=1
            io+=1
        return ''.join(otx)
    def upd(self):
        lvurl=urp1.format(f'api.{urp2}/repos')+'releases/latest'
        resp=requests.get(lvurl)
        if resp.status_code==200:
            data=resp.json(); latvsn=data["tag_name"]
            if latvsn==curvsn: self.mb('i','o','提示','当前已经是最新版本')
            elif self.mb('i','yn','提示','有新版本!是否前往项目仓库下载?')=='yes':
                webbrowser.open(urp1.format(urp2)+'releases')
        elif self.mb('q','yn','网络连接中断','无法连接服务器,是否重试?')=='yes': self.upd()
    def upgd(self):
        self.lvl[4]+=4
        if self.lvl[4]==20: self.btn2.config(state='disabled')
        if self.sisl==3:
            while self.sisl!=4:
                si=random.choices(range(len(sipro)),weights=sipro)[0]
                if si not in self.sis and name[si]!=self.mn:
                    self.lvl[self.sisl]=siup[si]*random.choice(siupro)
                    self.sis[self.sisl]=si; self.sisl+=1
            self.prit(st=[3])
        else:
            up=random.randrange(4)
            self.lvl[up]+=siup[self.sis[up]]*random.choice(siupro)
            self.prit(st=[up])
    def vdornm(self):
        self.show(self.ls,'(1/2)打开','cyan')
        self.pth=self.dlg(0,'打开',('Text files','*.txt'))
        if not self.pth: return
        names=[i for i in os.listdir(self.pth) if i.lower().endswith('.mp4')]
        self.show(self.ls,'(2/2)重命名','cyan'); lnms=len(names)
        if names: self.pginit('视频重命名',lnms)
        for i in range(lnms):
            t=time.localtime(tp.getctime(self.pnm(names[i])))
            new=f'{time.strftime("%Y%m%d_%H%M%S",t)}A.mp4'
            self.pgu(i+1,f'{names[i]} -> {new}','cyan')
            os.rename(self.pnm(names[i]),self.pnm(new))
        self.rt.after(250); self.winqut(self.pgm,ask=False)
        self.show(self.ls,'进程已结束','red')
    def winqut(self,tlk,ask=True):
        if not ask: tlk.destroy()
        elif self.mb('q','yn','退出','确认退出?')=='yes': tlk.destroy()
if __name__=='__main__': fabits=Fabits()