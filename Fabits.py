import chardet,ctypes,hashlib,json,numpy,os,random,requests
import subprocess,sys,threading,time,tkinter,turtle,webbrowser
from tkinter import filedialog,ttk
from PIL import Image
lst=numpy.zeros(shape=(38000,4),dtype=int); tp=os.path
proes=numpy.zeros(38000); dic=numpy.zeros(shape=(52,91,5,2))
hdnms={b'PNG':'.png',b'GIF8':'.gif',b'PDF':'.pdf',b'Rar!':'.rar',
       b'FLV':'.flv',b'BM':'.bmp',b'AVI LIST':'.avi',b'8BPS':'.psd',
       b'WAVEfmt':'.wav',b'MZ':'.exe',b'ftypmp':'.mp4',b'ftypM4':'.m4a',
       b'\xff\xd8\xff':'.jpg',b'\x49\x49\x2a\x00':'.tiff',b'\x1f\x8b':'.gz',
       b'PK\x03\x04':'.zip',b'7Z\xBC\xAF\x27':'.7z',b'\x49\x44\x33':'.mp3'}
class Fabits:
    def __init__(self):
        if self.preset()==-1: return
        self.rt=tkinter.Tk(); self.check();
        self.rt.geometry(self.calsz(64,36,'Fabits'))
        self.rt.iconphoto(True,tkinter.PhotoImage(file='Na.png'))
        self.rt.title(self.cfg['til']); self.rt.config(bg=self.bgin)
        self.adcon(); self.admnu(); self.style(); self.prefn()
        self.ics(); self.rt.mainloop(); self.savcfg()
    def adcon(self):
        self.memp1=ttk.Frame(self.rt)
        self.ls=ttk.Treeview(self.memp1,columns=('opt',),show='tree')
        self.slb=tkinter.Scrollbar(self.memp1); self.cvs=tkinter.Canvas(self.rt)
        self.sc=turtle.TurtleScreen(self.cvs); self.tl=turtle.RawTurtle(self.sc)
        self.sc.bgcolor(self.bg); self.ls.column('#0',width=0,stretch=False)
        self.ls.column('opt',width=30*self.scr,anchor='w')
        self.ls.config(yscrollcommand=self.slb.set)
        self.slb.config(command=self.ls.yview); self.memp2=ttk.Frame(self.rt)
        self.tetr=tkinter.Text(self.memp2,undo=True); self.slb2=tkinter.Scrollbar(self.memp2)
        self.tetr.config(yscrollcommand=self.slb2.set,background=self.bg,foreground=self.txchrc)
        self.slb2.config(command=self.tetr.yview); self.show(self.ls,'>>>','purple')
        self.tetr.config(font=('TkDefaultFont',12))
        self.tetr.bind('<Key>',lambda s: self.cchg())
        self.ofl=self.nfl=self.chg=0; self.txflnm='未命名文件'
        self.slb.pack(side='right',fill='y'); self.ls.pack(fill='both',expand=True)
        self.slb2.pack(side='right',fill='y'); self.tetr.pack(fill='both',expand=True)
    def adfun(self,lbl,knd):
        mntmp=tkinter.Menu(self.mnu,tearoff=0,bg=self.bgin,fg=self.txchrc)
        self.mnu.add_cascade(label=lbl,menu=mntmp)
        for i in knd: mntmp.add_command(label=i,command=knd[i])
    def adlsnd(self):
        self.show(self.ls,'(1/2)打开','cyan')
        self.pth=self.dlg(0,'打开',('Text files','*.txt'))
        if not self.pth: return
        fnames=[i for i in os.listdir(self.pth) if tp.isfile(self.pnm(i))]
        names=[i for i in fnames if not tp.splitext(i)[1]]
        self.show(self.ls,'(2/2)转换','cyan'); lnm=len(names)
        if lnm:
            self.pginit('查找添加缺失后缀',lnm)
            for i in range(lnm):
                nm=self.pnm(names[i]); fl=open(nm,'rb'); hd=fl.read(32); fl.close()
                for j in hdnms:
                    if j in hd:
                        self.pgu(i+1,f"{nm} -> {nm+hdnms[j]}",'cyan')
                        os.rename(nm,nm+hdnms[j]); break
                else: self.pgu(i+1,f'未知文件类型: {self.cfg['name']}','red')
            self.rt.after(250); self.winqut(self.pgm,'pginit')
        self.show(self.ls,'进程已结束','red'); self.show(self.ls,'>>>','purple')
    def admnu(self):
        self.clr={'black','red','green','yellow','blue','purple','cyan','grey','white'}
        self.funknd={
        '文件(F)':{'新建':self.opnf,'打开':lambda: self.opnf(1),'保存':self.savf,
            '另存为':lambda: self.savf(1),'导入':lambda: self.opnf(nda=1),
            '导出':lambda: self.savf(nda=1),'查找与替换':self.schgd,'撤销':self.undo,
            '重做':self.redo,'关闭':self.clsf,
            '退出':lambda: None if self.clsf() else self.winqut(self.rt,'Fabits')},
        '算法(A)':{'同分异构体数量':lambda: self.thr(self.iso),
            '链表冒泡排序':lambda: self.thr(self.lnksrt),'最大环长度':lambda: self.thr(self.ring),
            '求解罗马数字':lambda: self.thr(self.rome)},
        '批处理(B)':{'补齐缺失后缀':lambda: self.thr(self.adlsnd),
            '图片颜色替换':lambda: self.thr(self.clrplc),'图片排序':lambda: self.thr(self.imgsrt),
            '图片加解密':lambda: self.thr(self.picpt),'生成组合字符':lambda: self.txmng(self.rndchr),
            '解unicode':lambda: self.txmng(self.ucd),'视频重命名':lambda: self.thr(self.vdornm),
            '文本加解密':lambda: self.txmng(lambda itx: self.txcbtb(itx,0,0,0))},
        '网络(I)':{'官网':lambda: webbrowser.open('https://nahida520.love'),
            '项目仓库':lambda: webbrowser.open(self.cfg['urp1'].format(self.cfg['urp2'])),'版本检测':self.upd},
        '工具(T)':{'抽卡模拟器':self.conpuw,'圣遗物强化':self.itsth,'迷宫可视化':self.mazepl,
            '抽卡概率计算':self.pulprogd},
        '设置(S)':{'清屏':self.clear,'帮助':lambda: self.thr(self.hlp),'图标':self.ics,'选项':self.prefr}}
        self.mnu=tkinter.Menu(self.rt)
        for i in self.clr: self.ls.tag_configure(i,foreground=i,background=self.bg)
        for i in self.funknd: self.adfun(i,self.funknd[i])
        self.rt.config(menu=self.mnu)
    def adups(self,i,n):
        if i in self.ups: self.mb('w','o','选择角色重复','请重新选择')
        else: self.ups[n]=i; self.show(self.et,f'角色{i}添加成功!','red')
        for i in self.ups:
            if not i: return
        self.btn1.config(state='normal'); self.btn2.config(state='normal')
    def calsz(self,w,h,ky):
        size=self.cfg.get(ky,'')
        if size: return size
        a,b=w*self.scr,h*self.scr; c,d=(self.scwth-a)//2,(self.schgt-b)//2
        return f'{a}x{b}+{c}+{d}'
    def cchg(self):
        if not self.chg: self.chg=1; self.rt.title(f"{self.cfg['til']} - {self.txflnm}*")
    def check(self):
        self.scwth,self.schgt=self.rt.winfo_screenwidth(),self.rt.winfo_screenheight()
        self.chek=self.cfg.get('scr','')==self.scr; self.reboot=0
        self.chek=self.chek and self.cfg.get('scwth','')==self.scwth
        self.chek=self.chek and self.cfg.get('schgt','')==self.schgt
        srckys=['schgd','txmng','conpuw','inp','itsth','mazepl','pulprogd','Fabits','pginit','prefr']
        if not self.chek:
            for i in srckys: self.cfg.pop(i,None)
        self.bgidx=self.cfg['bgidx']
        if self.bgidx==2:
            lctme=time.localtime()
            if 6<=lctme.tm_hour<18: self.bgidx=0
            else: self.bgidx=1
        self.bg=self.cfg['bg'][self.bgidx]; self.txchrc=self.cfg['chr'][self.bgidx]
        self.bgin=self.cfg['bgin'][self.bgidx]
    def clear(self):
        self.ls.delete(*self.ls.get_children()); self.show(self.ls,'>>>','purple')
    def clrplc(self):
        self.show(self.ls,'(1/4)打开','cyan')
        pnm=self.dlg(1,'打开',('All image files','*.*'))
        if not pnm: return
        pic=Image.open(pnm)
        fm=lambda cl: (int(cl[:2],16),int(cl[2:4],16),int(cl[4:],16))
        nclr=list(map(fm,self.inp('输入多个被替换颜色(16进制表示)').split()))
        clr=fm(self.inp('输入替换颜色(16进制表示)'))
        self.show(self.ls,'(2/4)转换','cyan'); pix=numpy.array(pic)
        self.show(self.ls,'(3/4)替换','cyan')
        for i in nclr: alc=(pix[:,:,:3]==i).all(axis=-1); pix[alc,:3]=clr
        self.show(self.ls,'(4/4)保存','cyan'); pic=Image.fromarray(pix)
        new=self.dlg(2,'保存',('Image files','*.png'))
        if not new: return
        if not new.endswith('.png'): new+='.png'
        pic.save(new); self.show(self.ls,'进程已结束','red'); self.show(self.ls,'>>>','purple')
    def clsf(self):
        if not self.ofl: return
        if self.chg:
            svst=self.mb('q','ync','关闭文件时保存','未保存的内容将会丢失,是否保存?')
            if svst=='yes':
                if self.savf(): return -1
                else: self.tetr.delete('1.0','end')
            elif svst=='cancel': return -1
        else: self.tetr.delete('1.0','end')
        self.memp2.pack_forget(); self.ofl=0; self.rt.title(self.cfg['til'])
    def conpuw(self):
        self.puw=tkinter.Toplevel(self.rt); self.puw.transient(self.rt)
        self.puw.title('抽卡模拟器'); self.puw.geometry(self.calsz(16,14,'conpuw'))
        self.pu=ttk.Frame(self.puw); self.pum=tkinter.Menu(self.pu)
        self.puw.config(menu=self.pum)
        self.ups5=tkinter.Menu(self.pum,tearoff=0,bg=self.bgin,fg=self.txchrc)
        self.ups41=tkinter.Menu(self.pum,tearoff=0,bg=self.bgin,fg=self.txchrc)
        self.ups42=tkinter.Menu(self.pum,tearoff=0,bg=self.bgin,fg=self.txchrc)
        self.ups43=tkinter.Menu(self.pum,tearoff=0,bg=self.bgin,fg=self.txchrc)
        self.pum.add_cascade(label='五星UP',menu=self.ups5)
        self.pum.add_cascade(label='四星UP1',menu=self.ups41)
        self.pum.add_cascade(label='四星UP2',menu=self.ups42)
        self.pum.add_cascade(label='四星UP3',menu=self.ups43)
        dtm=['ups5','ups4','fups5','wpns5','wpns4','wpns3']
        self.ups,self.put5,self.put4,self.true_up4,self.true_up5,self.fu=['']*4,0,0,0,0,0
        for i in dtm:
            for j in self.cfg[i]:
                if i=='ups5':
                    self.ups5.add_command(label=j,command=lambda k=j: self.adups(k,0))
                elif i=='ups4':
                    self.ups41.add_command(label=j,command=lambda k=j: self.adups(k,1))
                    self.ups42.add_command(label=j,command=lambda k=j: self.adups(k,2))
                    self.ups43.add_command(label=j,command=lambda k=j: self.adups(k,3))
        self.lb=ttk.Label(self.pu,text='祈愿结果')
        self.et=ttk.Treeview(self.pu,columns=('opt',),show='tree')
        self.slet=tkinter.Scrollbar(self.pu); self.emp=ttk.Frame(self.pu)
        self.btn1=ttk.Button(self.emp,text='祈愿一次',command=lambda: self.pul(1))
        self.btn2=ttk.Button(self.emp,text='祈愿十次',command=lambda: self.pul(10))
        self.btn3=ttk.Button(self.emp,text='退出',command=lambda: self.winqut(self.puw,'conpuw'))
        self.btn1.config(width=8,state='disabled'); self.btn2.config(width=8,state='disabled')
        self.btn3.config(width=8); self.et.column('#0',width=0,stretch=False)
        self.et.column('opt',width=15*self.scr,anchor='w')
        self.et.config(yscrollcommand=self.slet.set); self.slet.config(command=self.et.yview)
        for i in self.clr: self.et.tag_configure(i, foreground=i,background=self.bg)
        self.slet.pack(side='right',fill='y'); self.lb.pack(expand=True)
        self.et.pack(fill='both',expand=True); self.emp.pack(fill='x',expand=True)
        self.btn1.pack(side='left',expand=True); self.btn2.pack(side='left',expand=True)
        self.btn3.pack(side='left',expand=True); self.pu.pack(fill='both',expand=True)
    def delmark(self):
        if self.lastsc[0]: self.tetr.tag_remove('match',self.lastsc[0],self.lastsc[1])
    @staticmethod
    def dlg(n,tle,flt):
        if n==0: dl=filedialog.askdirectory(title=tle)
        elif n==1: dl=filedialog.askopenfilename(title=tle,filetypes=(flt,))
        else: dl=filedialog.asksaveasfilename(title=tle,filetypes=(flt,))
        return dl
    def gen(self):
        self.ln,self.wd=map(int,self.inp('输入迷宫的长和宽').split())
        self.bx,self.by=map(int,self.inp('输入迷宫起始点x,y').split())
        self.ex,self.ey=map(int,self.inp('输入迷宫终点x,y').split())
        self.restul(); self.btn4.config(state='disabled')
        self.sz=min(12*self.scr/self.ln,12*self.scr/self.wd)
        self.maze=numpy.ones(shape=(self.ln*2+1,self.wd*2+1),dtype=int)
        for i in range(self.ln*2+1):
            for j in range(self.wd*2+1):
                if i in [0,self.ln*2] or j in [0,self.wd*2]: self.maze[i,j]=0
        self.mzshw(0,0,self.ln*2+1,self.wd*2+1,self.txchrc)
        self.mzshw(1,1,self.ln*2,self.wd*2,self.bg)
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
            self.mzshw(lx,y,rx+1,y+1,self.txchrc); self.mzshw(x,ly,x+1,ry+1,self.txchrc)
            rtmp=[(random.randint(lx,x-1)//2*2+1,y),(random.randint(x+1,rx)//2*2+1,y),
                  (x,random.randint(ly,y-1)//2*2+1),(x,random.randint(y+1,ry)//2*2+1)]
            k=random.randrange(4)
            for i in range(4):
                if k-i:
                    self.maze[rtmp[i][0],rtmp[i][1]]=1
                    self.mzshw(rtmp[i][0],rtmp[i][1],rtmp[i][0]+1,rtmp[i][1]+1,self.bg)
        self.maze[self.bx*2-1,self.by*2-1]=1; self.maze[self.ex*2-1,self.ey*2-1]=2
        self.mzshw(self.bx*2-1,self.by*2-1,self.bx*2,self.by*2,'#22cefc')
        self.mzshw(self.ex*2-1,self.ey*2-1,self.ex*2,self.ey*2,'#00ff00')
        self.btn4.config(state='normal'); self.btn5.config(state='normal')
    def getit(self):
        self.sis,self.lvl,self.kd=[0]*4,[0]*5,random.randrange(5)
        self.mn=random.choices(self.cfg['mnpro'][self.kd][0],weights=self.cfg['mnpro'][self.kd][1])[0]
        if self.mn==-1: self.mn=random.randint(0,2)
        if self.mn==-2:
            self.mn=random.choice(self.cfg['elmnkd'])
            if self.mn==' ': self.mn='物理'
            else: self.mn+='元素'
            self.mn+='伤害加成'
        else: self.mn=self.cfg['name'][self.mn]
        self.sisl,self.nm=0,random.choices((3,4),weights=(4,1))[0]
        while self.sisl in range(self.nm):
            si=random.choices(range(len(self.cfg['sipro'])),weights=self.cfg['sipro'])[0]
            if si not in self.sis and self.cfg['name'][si]!=self.mn:
                self.lvl[self.sisl]=self.cfg['siup'][si]*random.choice(self.cfg['siupro'])
                self.sis[self.sisl]=si; self.sisl+=1
        self.btn2.config(state='normal')
        self.et.delete(*self.et.get_children()); self.prit()
    def getvar(self):
        self.var=self.etr.get()
        if self.var: self.winqut(self.tmp,'inp')
        else: self.mb('w','o','提示','请检查输入的内容'); return
    def hlp(self):
        fl=open('README.md','r',encoding='utf-8');
        ln=fl.readline(); flg=0
        while ln:
            if ln=='\n' or ln.startswith('![]'): ln=fl.readline(); continue 
            elif ln.startswith('```'): flg=1-flg
            elif flg: self.show(self.ls,ln,'green')
            else:
                tmp=''
                for i in ln:
                    if i in '#*` ': continue
                    tmp+=i;
                self.show(self.ls,tmp,'green')
            ln=fl.readline()
        fl.close()
        self.show(self.ls,'>>>','purple')
    def hshgn(self):
        licc,lictmp,hdgl,hsh=len(self.cfg['icc']),0,64,hashlib.sha256()
        while True:
            if hdgl==64:
                hdgl=0; hsh.update(self.cfg['icc'][lictmp%licc].encode())
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
        i,j,cmd,dig=0,len(icx),cmds['c'],''
        while i<j:
            if icx[i].isdigit(): dig+=icx[i]
            else: cmd(dig); dig,cmd='',cmds[icx[i]]
            i+=1
        cmd(dig)
    def ics(self):
        self.memp1.pack_forget(); sztmp=lambda x: round(x*self.scr)
        self.restul(); self.cvs.pack(fill='both',expand=True)
        self.ico(self.cfg['icc'],60,sztmp(0.5),iter('d'))
        self.rt.after(500); self.restul()
        self.ico('l041r24l30',45,sztmp(0.6),iter('d'))
        self.ico(self.cfg['icd'],90,self.scr,iter('dwdwd'))
        self.tl.rt(45); self.tl.fd(11*self.scr)
        icm1,icm2='圣·西门科技股份有限公司 出品','Sig·WestGate Tech. L.C.D. present.'
        self.tl.write(icm1,align='center',font=('TkDefaultFont',sztmp(0.6),'bold'))
        self.tl.fd(sztmp(2.2))
        self.tl.write(icm2,align='center',font=('TkDefaultFont',sztmp(0.6),'bold'))
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
        self.rt.after(250); self.winqut(self.pgm,'pginit'); self.pginit('图片排序',ln)
        self.show(self.ls,'(3/4)排序','cyan')
        sort=[[numpy.mean(pis[i][0]),names[i],msg('完成',i)] for i in lnr]
        self.rt.after(250); self.winqut(self.pgm,'pginit')
        sort=sorted(sort,key=lambda i:i[0]); self.show(self.ls,'(4/4)整理','cyan')
        for i in lnr: os.rename(self.pnm(sort[i][1]),self.pnm(f'pix{i:04d}.png'))
        names=[i for i in os.listdir(self.pth) if i.lower().endswith('.png')]
        for i in lnr: os.rename(self.pnm(names[i]),self.pnm(f'pic{i:04d}.png'))
        self.show(self.ls,'进程已结束','red'); self.show(self.ls,'>>>','purple')
    def inp(self,st):
        self.tmp=tkinter.Toplevel(self.rt)
        self.tmp.title(''); self.tmp.geometry(self.calsz(16,5,'inp'))
        self.inemp=ttk.Label(self.tmp); self.lb=ttk.Label(self.inemp,text=st)
        self.etr=ttk.Entry(self.inemp,width=40); self.emp=ttk.Frame(self.tmp)
        self.btn1=ttk.Button(self.emp,text='全选',command=lambda: self.scl(self.etr))
        self.btn2=ttk.Button(self.emp,text='确认',command=self.getvar)
        self.btn1.config(width=10); self.btn2.config(width=10)
        self.lb.pack(expand=True); self.inemp.pack(fill='both',expand=True)
        self.etr.pack(expand=True); self.emp.pack(fill='both',expand=True)
        self.btn1.pack(side='left',expand=True); self.btn2.pack(side='left',expand=True)
        self.tmp.grab_set(); self.tmp.wait_window(); return self.var
    def iso(self):
        n=int(self.inp('基团-CnH2n+1,输入n值'))
        hm,isol=numpy.zeros(n+1,dtype=int),1; hm[0]=1
        for i in range(n):
            b,c,res=0,0,0; a=i-2*c
            while c<=a:
                res+=hm[a]*hm[b]*hm[c]; a,b=a-1,b+1
                if a<b: c+=1; a,b=i-2*c,c
            hm[isol],isol=res,isol+1
        self.show(self.ls,f'{hm[n]}','green'); self.show(self.ls,'>>>','purple')
    def itsth(self):
        self.itw=tkinter.Toplevel(self.rt); self.itw.transient(self.rt)
        self.itw.title('圣遗物强化'); self.itw.geometry(self.calsz(16,14,'itsth'))
        self.it=ttk.Frame(self.itw); self.lb=ttk.Label(self.it,text='强化结果:')
        self.et=ttk.Treeview(self.it,columns=('opt',),show='tree')
        self.slet=tkinter.Scrollbar(self.it); self.emp=ttk.Frame(self.it)
        self.btn1=ttk.Button(self.emp,text='获取',command=self.getit)
        self.btn2=ttk.Button(self.emp,text='强化',command=self.upgd)
        self.btn3=ttk.Button(self.emp,text='退出',command=lambda: self.winqut(self.itw,'itsth'))
        self.btn1.config(width=8); self.btn2.config(width=8,state='disabled')
        self.btn3.config(width=8); self.et.column('#0',width=0,stretch=False)
        self.et.column('opt',width=15*self.scr,anchor='w')
        self.et.config(yscrollcommand=self.slet.set); self.slet.config(command=self.et.yview)
        for i in self.clr: self.et.tag_configure(i, foreground=i,background=self.bg)
        self.slet.pack(side='right',fill='y'); self.lb.pack(expand=True)
        self.et.pack(fill='both',expand=True); self.emp.pack(fill='x',expand=True)
        self.btn1.pack(side='left',expand=True); self.btn2.pack(side='left',expand=True)
        self.btn3.pack(side='left',expand=True); self.it.pack(fill='both',expand=True)
    def lnksrt(self):
        arr,hd=eval(self.inp('输入链表')),int(self.inp('输入头地址')); lnkl,cur=0,hd
        while cur!=-1: lnkl+=1; cur=arr[cur][1]
        for i in range(lnkl-1,-1,-1):
            p,q=hd,-1; r=arr[p][1]
            for j in range(i):
                if arr[p][0]>arr[r][0]:
                    if q==-1: hd=r
                    else: arr[q][1]=r
                    arr[p][1],arr[r][1]=arr[r][1],p; p,r=r,p
                p,q,r=r,p,arr[r][1]
        self.show(self.ls,f'{arr},head={hd}','green'); self.show(self.ls,'>>>','purple')
    def mazepl(self):
        self.mz=tkinter.Toplevel(self.rt); self.mz.title('迷宫可视化')
        self.mz.transient(self.rt); self.mz.geometry(self.calsz(16,4,'mazepl'))
        self.mzemp=ttk.Frame(self.mz); self.lb=ttk.Label(self.mzemp,text='迷宫设置')
        self.emp=ttk.Frame(self.mz); self.btn4=ttk.Button(self.emp,text='生成',command=self.gen)
        self.btn5=ttk.Button(self.emp,text='解',command=self.slv)
        self.btn6=ttk.Button(self.emp,text='退出',command=lambda: self.winqut(self.mz,'mazepl'))
        self.btn4.config(width=8); self.btn5.config(width=8,state='disabled')
        self.btn6.config(width=8); self.memp1.pack_forget()
        self.cvs.pack(fill='both',expand=True); self.lb.pack(expand=True)
        self.mzemp.pack(fill='both',expand=True); self.emp.pack(fill='both',expand=True)
        self.btn4.pack(side='left',expand=True); self.btn5.pack(side='left',expand=True)
        self.btn6.pack(side='left',expand=True); self.mz.grab_set(); self.mz.wait_window()
        self.cvs.pack_forget(); self.restul(); self.memp1.pack(side='bottom',fill='both',expand=True)
    def mb(self,icn,tp,tle,msg):
        mbt=tkinter.messagebox.Message(icon=self.cfg['mb'][icn],type=self.cfg['mb'][tp],title=tle,message=msg)
        res=mbt.show(); return res
    def mngrd(self,i):
        j=i-1 if i%2 else i+1
        self.wids[i][1].config(state='normal')
        self.wids[j][1].config(state='disabled')
    def mzshw(self,lx,ly,rx,ry,clr):
        self.tl.teleport((lx-self.ln)*self.sz+22*self.scr,(ly-self.wd)*self.sz-12*self.scr)
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
                self.rt.title(f"{self.cfg['til']} - {self.txflnm}*"); return
        if ext:
            self.rsflnm=self.dlg(1,'打开',('All text files','*.*'))
            if self.rsflnm:
                self.tetr.delete('1.0','end')
                self.txflnm=self.rsflnm; fl=open(self.txflnm,'rb')
                data=fl.read(1024); enc=chardet.detect(data)['encoding']
                fl.seek(0); data=fl.readlines()
                for i in data: self.tetr.insert('insert',i.decode(enc))
                fl.close(); self.nfl=0
                self.rt.title(f"{self.cfg['til']} - {self.txflnm}")
            else: self.rt.title(f"{self.cfg['til']} - {self.txflnm}"); return
        else:
            self.nfl=1; self.txflnm='未命名文件'; self.tetr.delete('1.0','end')
            if nda:
                byt=self.txcbtb(None,1,0,1)
                if byt!=-1: self.tetr.insert('insert',byt)
        self.chg=0; self.rt.title(f"{self.cfg['til']} - {self.txflnm}")
    def pginit(self,tx,tol):
        self.pgm=tkinter.Toplevel(self.rt); self.pgm.geometry(self.calsz(16,14,'pginit'))
        self.pgm.transient(self.rt); self.pgm.title(tx);
        self.pgf=ttk.Frame(self.pgm); self.pgl=ttk.Label(self.pgf,text='0.00%')
        self.pgb=ttk.Progressbar(self.pgf,length=15*self.scr)
        self.pgsb=tkinter.Scrollbar(self.pgf)
        self.pgt=ttk.Treeview(self.pgf,columns=('opt',),show='tree')
        self.pgt.column('#0',width=0,stretch=False)
        self.pgt.column('opt',width=15*self.scr,anchor='w')
        self.pgt.config(yscrollcommand=self.pgsb.set)
        self.pgsb.config(command=self.pgt.yview)
        for i in self.clr: self.pgt.tag_configure(i,foreground=i,background=self.bg)
        self.pgb['maximum']=tol; self.tol=tol/100
        self.pgl.pack(); self.pgb.pack(); self.pgsb.pack(side='right',fill='y')
        self.pgt.pack(fill='both',expand=True); self.pgf.pack(fill='both',expand=True)
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
        self.rt.after(250); self.winqut(self.pgm,'pginit')
        self.show(self.ls,'(3/3)保存','cyan')
        new=self.dlg(2,'保存',('Image files','.png'))
        if not new: return
        if new.endswith('.png'): pic.save(new)
        else: pic.save(f'{new}.png')
        self.show(self.ls,'进程已结束','red'); self.show(self.ls,'>>>','purple')
    def prconf(self):
        lim=[89,3,1]; res=[0]*5
        for i in range(5):
            val=self.proinp[i].get()
            if (not val.isdigit()) or int(val)<0:
                self.mb('w','o','提示','请检查输入内容'); return
            if i>1 and int(val)>lim[i-2]:
                self.mb('w','o','提示','请检查输入内容'); return
            res[i]=int(val)
        self.winqut(self.progd,'pulprogd'); self.thr(lambda: self.pulpro(res))
    def prefn(self):
        self.pnm=lambda fn: tp.join(self.pth,fn)
        self.scl=lambda tag: (tag.focus_set(),tag.selection_range(0,'end'))
    def prefr(self):
        prf=tkinter.Toplevel(self.rt); prf.transient(self.rt); prf.geometry(self.calsz(16,6,'prefr'))
        prf.title('选项'); self.fui=tkinter.IntVar(value=self.cfg['bgidx'])
        prfemp=[ttk.Frame(prf) for i in range(4)]
        prfl=ttk.Label(prfemp[0],text='部分选项需要重启后生效')
        prfui=ttk.Label(prfemp[1],text='UI流转(夜间模式)显示模式')
        rdbs=['']*3; lan=['白天模式','夜间模式','流转模式']
        for i in range(3):
            rdbs[i]=ttk.Radiobutton(prfemp[2],text=lan[i],variable=self.fui,value=i)
            rdbs[i].pack(side='left',expand=True)
        subtn=ttk.Button(prfemp[3],text='应用',command=self.submt)
        canbtn=ttk.Button(prfemp[3],text='取消',command=lambda: self.winqut(prf,'prefr'))
        prfl.pack(expand=True); prfui.pack(expand=True)
        subtn.pack(side='left',expand=True); canbtn.pack(side='left',expand=True)
        for i in range(4): prfemp[i].pack(fill='both',expand=True)
    def preset(self):
        try:
            self.scr=ctypes.windll.shcore.GetScaleFactorForDevice(0)//5
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except: self.scr=20
        try:
            fl=open('Config.json','r',encoding='utf-8')
            self.cfg=json.load(fl); fl.close()
        except: tkinter.messagebox.showerror('错误','无效的Config.json'); return -1
    def prit(self,st=[]):
        self.show(self.et,f"{self.cfg['knd'][self.kd]}(+{self.lvl[4]})",'cyan')
        self.show(self.et,self.mn,'blue')
        for i in range(self.sisl):
            nm=self.cfg['name'][self.sis[i]]; clr='red' if i in st else 'green'
            if nm[-1]==' ':
                self.show(self.et,f'{nm[:-1]}+{round(self.lvl[i]+0.05,1)}',clr)
            else: self.show(self.et,f'{nm}+{round(self.lvl[i]+0.05,1)}%',clr)
        self.show(self.et,'>>>','purple')
    def pul(self,n):
        for i in range(n):
            ran,tup=random.random(),random.random()
            if ran<=self.cfg['pro_lst5'][self.put5]:
                if self.true_up5: self.show(self.et,self.ups[0],'yellow'); self.true_up5=0
                elif tup<=self.cfg['tu_lst'][self.fu]:
                    self.show(self.et,self.ups[0],'yellow'); self.true_up5,self.fu=0,0
                else:
                    it=random.choice(self.cfg['fups5']+self.cfg['wpns5'])
                    self.show(self.et,it,'yellow'); self.show(self.et,'歪','red')
                    self.true_up5,self.fu=1,self.fu+1
                self.put5,self.put4=0,self.put4+1
            elif ran<=self.cfg['pro_lst5'][self.put5]+self.cfg['pro_lst4'][self.put4]:
                if tup<=0.5 or self.true_up4:
                    self.show(self.et,random.choice(self.ups[1:]),'purple')
                    self.true_up4=0
                else:
                    it=random.choice(self.cfg['ups4']+self.cfg['wpns4'])
                    self.show(self.et,it,'purple'); self.true_up4=1
                self.put5,self.put4=self.put5+1,0
            else:
                self.show(self.et,random.choice(self.cfg['wpns3']),'blue')
                self.put5,self.put4=self.put5+1,self.put4+1
        self.show(self.et,f'垫{self.put5}发','cyan'); self.show(self.et,'>>>','purple')
    def pulpro(self,vals):
        global dic,lst; res=numpy.zeros(52,dtype=float)
        s,pb,put,fu,tu=vals
        _len,st,ed=0,0,50; pb+=s//160; lst[_len]=[0,put,fu,tu]
        proes[_len]=1; _len+=1; self.pginit('抽卡模拟',pb)
        for i in range(pb):
            for j in range(_len):
                ups,puts,false_up,true_up=lst[j]; pro=proes[j]
                ups=min(ups,50); pros=self.cfg['pro_lst5'][puts]; tu_pro=self.cfg['tu_lst'][false_up]
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
        self.rt.after(250); self.winqut(self.pgm,'pginit')
        self.show(self.ls,'UP数 概率','purple')
        for i in range(st,ed+1): self.show(self.ls,f'{i:>2d}{res[i]:7.2f}%','purple')
        self.show(self.ls,'>>>','purple')
    def pulprogd(self):
        self.progd=tkinter.Toplevel(self.rt); self.progd.transient(self.rt)
        self.progd.geometry(self.calsz(24,9,'pulprogd')); self.progd.title('抽卡概率计算')
        probtntx=['原石数'+' '*13,'粉球数'+' '*13,'垫池数(0-89)    ','已经连歪数(0-3)','是否大保底(0/1)']
        self.prem=[ttk.Frame(self.progd) for i in range(6)]
        self.prolb,self.proinp=['']*5,['']*5
        for i in range(5):
            self.prolb[i]=ttk.Label(self.prem[i],text=probtntx[i])
            self.proinp[i]=ttk.Entry(self.prem[i],width=30)
            self.prolb[i].pack(side='left',expand=True)
            self.proinp[i].pack(side='left',expand=True)
        self.proys=ttk.Button(self.prem[5]); self.prono=ttk.Button(self.prem[5])
        self.proys.config(text='确认',command=self.prconf)
        self.prono.config(text='退出',command=lambda: self.winqut(self.progd,'pulprogd'))
        self.proys.pack(side='left',expand=True); self.prono.pack(side='left',expand=True)
        for i in range(6): self.prem[i].pack(fill='both',expand=True)
    def putvar(self,val): self.var=val; self.tmp.destroy()
    def redo(self):
        if self.ofl:
            try: self.tetr.edit_redo()
            except: self.mb('w','o','提示','已经是最后一层')
    def restul(self): self.tl.reset(); self.tl.ht(); self.tl.speed(0); self.tl.penup()
    def ring(self):
        n=int(self.inp('输入n值(对)')); m,flg=0,[1]*(2*n)
        for i in range(2*n):
            k,rngl=i,0
            while flg[k]: flg[k],rngl=0,rngl+1; k=k*2 if k<n else 2*(k-n)+1
            m=max(m,rngl)
        self.show(self.ls,f'{m}','green'); self.show(self.ls,'>>>','purple')
    def rndchr(self,itx):
        n=int(self.inp('输入字符密度'))
        lst=list(range(768,880))+list(range(1155,1162)); io,otx=0,['']*len(itx)*(n+1)
        for i in itx:
            otx[io]=i; io+=1; chs=map(chr,random.choices(lst,k=n))
            for j in chs: otx[io]=j; io+=1
        return ''.join(otx)
    def rome(self):
        ch=self.inp('输入罗马数字'); num,stk,top=0,[0]*len(ch),0
        dic={'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000,
             'i':1,'v':5,'x':10,'l':50,'c':100,'d':500,'m':1000}
        for i in ch:
            while top>0 and dic[i]>stk[top-1]: top-=1; num-=stk[top]
            stk[top]=dic[i]; top+=1
        while top>0: top-=1; num+=stk[top]
        self.show(self.ls,f'{num}','green'); self.show(self.ls,'>>>','purple')
    def rplc(self):
        schtx=self.consf[2].get(); rplctx=self.consf[4].get(); ncs=not self.upchk
        if not (schtx and rplctx): self.mb('w','o','提示','请检查输入的内容'); return
        cur=self.tetr.index('insert'); pos=self.tetr.search(schtx,cur,'end',nocase=ncs)
        if not pos: pos=self.tetr.search(schtx,'1.0',cur,nocase=ncs)
        if pos:
            self.tetr.delete(pos,f'{pos}+{len(schtx)}c'); self.delmark()
            self.tetr.insert(pos,rplctx); aled=f'{pos}+{len(rplctx)}c'
            self.tetr.mark_set('insert',aled); self.tetr.tag_add('match',pos,aled)
            self.tetr.tag_config('match',background='yellow')
            self.lastsc=pos,aled; self.cchg()
        else: self.mb('i','o','提示','找不到相应的文本')
    def rplcal(self):
        schtx=self.consf[2].get(); rplctx=self.consf[4].get(); ncs=not self.upchk; cnt=0
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
        self.cfg['scr']=self.scr; self.cfg['scwth']=self.scwth
        self.cfg['schgt']=self.schgt; fl=open('Config.json','w',encoding='utf-8')
        json.dump(self.cfg,fl,indent=4,ensure_ascii=False); fl.close()
        if self.reboot: now=sys.executable; subprocess.Popen([now]+sys.argv); sys.exit(0)
    def savf(self,at=0,nda=0):
        if not self.ofl: return
        if nda: ot=self.txcbtb(self.tetr.get('1.0','end'),0,1,0); return
        if self.nfl or at:
            self.rsflnm=self.dlg(2,'保存',('All text files','*.*'))
            if not self.rsflnm: return -1
            if not tp.splitext(self.rsflnm)[1]: self.rsflnm+='.txt'
            self.txflnm=self.rsflnm; self.rt.title(f"{self.cfg['til']} - {self.txflnm}")
        fl=open(self.txflnm,'w',encoding='utf-8',newline='\n'); self.nfl=self.chg=0
        txres=self.tetr.get('1.0','end'); fl.write(txres); fl.close()
    def sch(self,dire,al=False):
        schtx=self.consf[2].get()
        if not schtx: self.mb('w','o','提示','请检查输入的内容'); return
        st,ed,cur,ncs='1.0','end',self.tetr.index('insert'),not self.upchk
        if al: pos=self.tetr.search(schtx,st,ed,nocase=ncs)
        elif dire:
            pos=self.tetr.search(schtx,cur+'+1c',ed,nocase=ncs)
            if not pos: pos=self.tetr.search(schtx,st,cur,nocase=ncs)
        else:
            pos=self.tetr.search(schtx,cur,st,backwards=True,nocase=ncs)
            if not pos: pos=self.tetr.search(schtx,ed,cur,backwards=True,nocase=ncs)
        if pos:
            self.delmark(); self.tetr.see(pos); self.tetr.mark_set('insert',pos)
            aled=f'{pos}+{len(schtx)}c'; self.tetr.tag_add('match',pos,aled)
            self.tetr.tag_config('match',background='yellow'); self.lastsc=pos,aled
        else: self.mb('i','o','提示','找不到相应的文本')
    def schgd(self):
        if not self.ofl: return
        self.schtl=tkinter.Toplevel(self.rt); self.schtl.transient(self.rt)
        self.schtl.geometry(self.calsz(18,7,'schgd')); self.schtl.title('查找与替换')
        scs=[ttk.Frame(self.schtl) for i in range(5)]; self.lastsc=('','')
        concm={'l':lambda idx,arg: ttk.Label(scs[idx],text=arg),
               'e':lambda idx,arg: ttk.Entry(scs[idx],width=30),
               'b':lambda idx,arg: ttk.Button(scs[idx],text=arg)}
        wid=['l0查找   ','e0','l1替换为','e1','l2 ','b3向上查找',
             'b3向下查找','b3从头查找','b4替换','b4全部替换','b4退出']
        self.consf=['']*12; lcon=1; self.uptmp=tkinter.BooleanVar(); self.upchk=False
        self.consf[0]=ttk.Checkbutton(scs[2],variable=self.uptmp,command=self.uppchk)
        self.consf[0].config(text='是否区分大小写')
        for i in wid: self.consf[lcon]=concm[i[0]](int(i[1]),i[2:]); lcon+=1
        btncmd=[lambda: self.sch(dire=False),lambda: self.sch(dire=True),
                lambda: self.sch(dire=True,al=True),self.rplc,self.rplcal,
                lambda: (self.delmark(),self.winqut(self.schtl,'schgd'))]
        for i in range(6): self.consf[i+6].config(command=btncmd[i])
        pck=lambda tag: tag.pack(side='left',expand=True); list(map(pck,self.consf))
        for i in range(5): scs[i].pack(fill='both',expand=True)
    @staticmethod
    def show(arg,st,cl): itm=arg.insert('','end',values=(st,),tags=(cl,)); arg.see(itm)
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
    def style(self):
        ftsz=round(0.4*self.scr); stl=ttk.Style(self.rt)
        if self.bgidx: stl.theme_use('clam')
        stl.configure('.',background=self.bgin,fieldbackground=self.bg,foreground=self.txchrc)
        stl.configure('Treeview',font=('TkDefaultFont',ftsz,'bold'),rowheight=2.5*ftsz)
    def submt(self):
        self.cfg['bgidx']=self.fui.get()
        if self.mb('q','yn','需要重启','是否立即重启以应用设置?')=='yes':
            if self.clsf()==-1: return
            self.reboot=1; self.winqut(self.rt,'Fabits')
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
    def txdel(self,fun):
        if not self.opclvr[0].get():
            itx=self.wids[0][1].get(); enc='utf-8'
            if not itx: self.mb('w','o','提示','请检查输入的内容'); return
        else:
            flnm=self.wids[1][1].get()
            if not flnm: return
            fl=open(flnm,'rb'); data=fl.read(1024)
            enc=chardet.detect(data)['encoding']; fl.seek(0)
            itx=fl.read().decode(enc); fl.close()
        otx=fun(itx)
        if not self.opclvr[1].get(): self.wids[2][1].insert('end',otx)
        else:
            new=self.wids[3][1].get()
            if not new: return
            if not tp.splitext(new)[1]: new+='.txt'
            fl=open(new,'w',encoding=enc); fl.write(otx); fl.close()
        self.show(self.ls,'进程已结束','red'); self.show(self.ls,'>>>','purple')
    def txmng(self,fun):
        self.mng=tkinter.Toplevel(self.rt); self.mng.transient(self.rt)
        self.mng.title('文本处理'); self.mng.geometry(self.calsz(24,10,'txmng'))
        self.opclvr=[tkinter.IntVar(value=0),tkinter.IntVar(value=0)]
        mngemp=[ttk.Frame(self.mng) for i in range(5)]
        self.wids=[['','',''] for i in range(4)]
        lbemp=[ttk.Label(self.mng),ttk.Label(self.mng)]
        mainlb1,mainlb2=ttk.Label(lbemp[0],text='打开方式'),ttk.Label(lbemp[1],text='保存方式')
        mainlb1.pack(); mainlb2.pack(); self.args=['文本输入','文件打开','文本输出','文件保存']
        for i in range(4):
            mngrd=lambda k=i: self.mngrd(k)
            mngscl=lambda k=i: self.scl(tag=self.wids[k][1])
            mngpth=lambda k=i: self.upth(k)
            self.wids[i][0]=ttk.Radiobutton(mngemp[i],text=self.args[i])
            self.wids[i][0].config(variable=self.opclvr[i//2],value=i%2,command=mngrd)
            self.wids[i][1]=ttk.Entry(mngemp[i],width=30)
            self.wids[i][2]=ttk.Button(mngemp[i])
            if i%2: self.wids[i][2].config(text='...',command=mngpth)
            else: self.wids[i][2].config(text='全选',command=mngscl)
        for i in self.wids:
            for j in range(3): i[j].pack(side='left',expand=True)
        mngbtn1=ttk.Button(mngemp[4],text='生成',command=lambda: self.txdel(fun))
        mngbtn2=ttk.Button(mngemp[4],text='退出',command=lambda: self.winqut(self.mng,'txmng'))
        mngbtn1.pack(side='left',expand=True); mngbtn2.pack(side='left',expand=True)
        for i in range(5):
            if i in [0,2]: lbemp[i//2].pack(fill='both',expand=True)
            mngemp[i].pack(fill='both',expand=True)
        self.wids[1][1].config(state='disabled')
        self.wids[3][1].config(state='disabled')
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
            except: self.mb('w','o','提示','已经是最后一层')
    def upd(self):
        lvurl=self.cfg['urp1'].format(f"api.{self.cfg['urp2']}/repos")+'releases/latest'
        try:
            resp=requests.get(lvurl)
            if resp.status_code==200:
                data=resp.json(); latvsn=data['tag_name']
                if latvsn==self.cfg['curvsn']: self.mb('i','o','提示','当前已经是最新版本')
                elif self.mb('i','yn','提示','有新版本!是否前往项目仓库下载?')=='yes':
                    webbrowser.open(self.cfg['urp1'].format(self.cfg['urp2'])+'releases')
            elif self.mb('w','yn','无法连接服务器','是否重试?')=='yes': self.upd()
        except OSError as e:
            if self.mb('w','yn','网络连接中断','是否重试?')=='yes': self.upd()
    def upgd(self):
        self.lvl[4]+=4
        if self.lvl[4]==20: self.btn2.config(state='disabled')
        if self.sisl==3:
            while self.sisl!=4:
                si=random.choices(range(len(self.cfg['sipro'])),weights=self.cfg['sipro'])[0]
                if si not in self.sis and self.cfg['name'][si]!=self.mn:
                    self.lvl[self.sisl]=self.cfg['siup'][si]*random.choice(self.cfg['siupro'])
                    self.sis[self.sisl]=si; self.sisl+=1
            self.prit(st=[3])
        else:
            up=random.randrange(4)
            self.lvl[up]+=self.cfg['siup'][self.sis[up]]*random.choice(self.cfg['siupro'])
            self.prit(st=[up])
    def upth(self,p):
        getpth=self.dlg((p+1)//2,self.args[p][2:],('All text files','*.*'))
        if getpth: self.wids[p][1].delete(0,'end'); self.wids[p][1].insert(0,getpth)
    def uppchk(self): self.upchk=self.uptmp.get()
    def vdornm(self):
        self.show(self.ls,'(1/2)打开','cyan')
        self.pth=self.dlg(0,'打开',('Text files','*.txt'))
        if not self.pth: return
        names=[i for i in os.listdir(self.pth) if i.lower().endswith('.mp4')]
        self.show(self.ls,'(2/2)重命名','cyan'); lnms=len(names)
        if lnms:
            self.pginit('视频重命名',lnms)
            for i in range(lnms):
                t=time.localtime(tp.getctime(self.pnm(names[i])))
                new=f"{time.strftime('%Y%m%d_%H%M%S',t)}A.mp4"
                self.pgu(i+1,f'{names[i]} -> {new}','cyan')
                os.rename(self.pnm(names[i]),self.pnm(new))
            self.rt.after(250); self.winqut(self.pgm,'pginit')
        self.show(self.ls,'进程已结束','red'); self.show(self.ls,'>>>','purple')
    def winqut(self,arg,ky):
        a,b,c,d=arg.winfo_width(),arg.winfo_height(),arg.winfo_x(),arg.winfo_y()
        self.cfg[ky]=f'{a}x{b}+{c}+{d}'; arg.destroy()
if __name__=='__main__': fabits=Fabits()