'''
......................................................................................
..DDDD...EEEEE..IIIII..L.......OOO...PPPP...RRRR....OOO...X...X..IIIII..DDDD...EEEEE..
..D...D..E........I....L......O...O..P...P..R...R..O...O...X.X.....I....D...D..E......
..D...D..EEEEE....I....L......O...O..PPPP...RRRR...O...O....X......I....D...D..EEEEE..
..D...D..E........I....L......O...O..P......R...R..O...O...X.X.....I....D...D..E......
..DDDD...EEEEE..IIIII..LLLLL...OOO...P......R...R...OOO...X...X..IIIII..DDDD...EEEEE..
......................................................................................
'''
import hashlib,math,multiprocessing,json,os,random
import subprocess,sys,threading,time,tkinter,turtle,webbrowser
from numpy import array,bitwise_xor,mean,ones,uint8,zeros,zeros_like
from PIL.Image import fromarray,open as iopen
from tkinter import filedialog,messagebox,ttk,scrolledtext
from urllib.request import urlopen
def avgs(nm:str): return mean(array(iopen(nm).convert('L')))
if os.name=='nt':
    from ctypes import *
    from ctypes import wintypes
    style=['vista','winnative','xpnative']
    class Guid(Structure):
        _fields_=[("Data1",c_ulong),("Data2",c_ushort),
                  ("Data3",c_ushort),("Data4",c_ubyte*8)]
        def __init__(self,l,w1,w2,*b8)->None:
            '''initialize guid'''
            self.Data1,self.Data2,self.Data3=l,w1,w2
            for i in range(8): self.Data4[i]=b8[i]
    class Api:
        '''windows com api'''
        dpi=lambda: windll.shcore.SetProcessDpiAwareness(1)
        scfac=windll.shcore.GetScaleFactorForDevice(0)//5
        def __init__(self,wmid:int)->None:
            '''initialize com'''
            self.ptr,self.hwnd=c_void_p(),windll.user32.GetParent(wmid)
            clsid=Guid(0x56FDF344,0xFD6D,0x11d0,0x95,0x8A,0x00,0x60,0x97,0xC9,0xA0,0x90)
            iid=Guid(0xEA1AFB91,0x9E28,0x4B86,0x90,0xE9,0x9E,0x9F,0x8A,0x5E,0xEF,0xAF)
            windll.ole32.CoInitializeEx(None,2)
            windll.ole32.CoCreateInstance(byref(clsid),None,1,byref(iid),byref(self.ptr))
            vtable=cast(self.ptr,POINTER(c_void_p))[0]
            vpar=lambda par: vtable+par*sizeof(c_void_p)
            ptr=lambda *args: POINTER(WINFUNCTYPE(*args))
            rel=cast(vpar(2),ptr(c_ulong,c_void_p))[0]
            val=cast(vpar(9),ptr(HRESULT,c_void_p,wintypes.HWND,c_ulonglong,c_ulonglong))[0]
            chg=cast(vpar(10),ptr(HRESULT,c_void_p,wintypes.HWND,c_int))[0]
            self.state=lambda tbpf: chg(self.ptr,self.hwnd,tbpf)
            self.uninit=lambda: (rel(self.ptr),windll.ole32.CoUninitialize())
            self.value=lambda now,tol: val(self.ptr,self.hwnd,now,tol)
        @staticmethod
        def creblk(bgidx:int,wmid:int)->None:
            '''create black title bar'''
            hwnd=windll.user32.GetParent(wmid); val=c_int(bgidx)
            windll.dwmapi.DwmSetWindowAttribute(hwnd,20,byref(val),sizeof(val))
else:
    style=['aqua'] if sys.platform=='darwin' else []
    class Api:
        '''deal same api on mac or linux'''
        dpi=lambda *args: None; scfac=20
        def __init__(self,wmid:int)->None:
            '''deal same functions'''
            self.flash=self.state=self.uninit=self.value=lambda *args: None
        @staticmethod
        def creblk(bgidx:int,wmid:int)->None: pass
class Fabits:
    '''Fabits app main class shared data and io interface'''
    def __init__(self)->None:
        '''initialize app'''
        self.wmini(); self.stlchk(); self.adins(); self.funset()
        self.adconf(); self.style(); self.admenu()
    def adconf(self)->None:
        '''add main window widget and style'''
        self.wm.update_idletasks(); self.Api=Api(self.wm.winfo_id())
        self.sc=[self.scfac,self.wm.winfo_screenwidth(),self.wm.winfo_screenheight()]
        self.check=(self.cfg['sc']==self.sc); self.wm.geometry(self.calsz(64,36,'Fabits'))
        self.wm.title(self.data['tle']); self.wm.protocol('WM_DELETE_WINDOW',self.savcfg)
        self.wmain=ttk.Frame(self.wm); self.mnu=Navigation(self.wmain,self)
        self.wm.bind('<<style>>',self.mnu.bgs,'+')
        self.note=NotebookPlus(self.wmain,self); csl=ttk.Frame(self.wmain)
        self.csl=self.cretre(csl); self.clear(self.csl,1); ratio=[0.15,0.75]
        self.mnu.place(relx=0,rely=0,relwidth=ratio[0],relheight=1)
        self.note.place(relx=ratio[0],rely=0,relwidth=1-ratio[0],relheight=ratio[1])
        csl.place(relx=ratio[0],rely=ratio[1],relwidth=1-ratio[0],relheight=1-ratio[1])
        self.cvs=tkinter.Canvas(self.wm,highlightthickness=0)
        self.scrn=turtle.TurtleScreen(self.cvs)
        self.wm.bind('<<style>>',lambda *args: self.scrn.bgcolor(self.bg),'+')
        self.tul=turtle.RawTurtle(self.scrn)
    def adins(self)->None:
        '''add class instance'''
        self.adend=Adend(self); self.calc=Calc(self); self.cdmix=Cdmix(self)
        self.clrplc=Clrplc(self); self.cmdmng=Cmdmng(self); self.cmpil=Cmpil(self)
        self.hlp=Hlp(self); self.icon=Icon(self); self.imgsrt=Imgsrt(self)
        self.iso=Iso(self); self.itmsth=Itmsth(self); self.lnksrt=Lnksrt(self)
        self.mazen=Mazen(self); self.pgbar=Pgbar(self); self.piccpt=Piccpt(self)
        self.precfg=Precfg(self); self.pro=Pro(self); self.pul=Pul(self)
        self.rename=Rename(self); self.ring=Ring(self); self.rome=Rome(self)
        self.txmng=Txmng(self); self.update=Update(self)
    def admenu(self)->None:
        '''add menu to main window'''
        mnus={
        '文件(F)':{'新建':self.note.fnew,'打开':self.note.fopen,
            '保存':lambda: self.note.fsave(self.note.now),'全部保存':self.note.savall,
            '另存为':lambda: self.note.fsave(self.note.now,copy=1),
            '导入':lambda: self.note.fnew(''),'导出':self.note.ext,
            '查找与替换':self.note.schgd,'撤销':self.note.undo,'重做':self.note.redo,
            '关闭':lambda: self.note.fclose(self.note.now),
            '全部关闭':self.note.clsall,'退出':self.savcfg},
        '算法(A)':{'同分异构体数':self.iso.iso,'链表冒泡排序':self.lnksrt.lnksrt,
            '最大环长度':self.ring.ring,'求解罗马数字':self.rome.rome},
        '批处理(B)':{'缺失后缀修复':self.adend.adend,'图片颜色替换':self.clrplc.clrplc,
            '图片排序':self.imgsrt.imgsrt,'图片加解密':self.piccpt.piccpt},
        '网络(I)':{'项目仓库':lambda: self.web('proj'),'检查更新':self.update.update},
        '工具(T)':{'计算器':self.calc.calc,'代码混合器':self.cdmix.cdmix,
            '命令管理器':self.cmdmng.cmdmng,'编译链接库':self.cmpil.cmpil,
            '圣遗物强化':self.itmsth.itmsth,'迷宫可视化':self.mazen.mazen,
            '抽卡概率计算':self.pro.pro,'抽卡模拟器':self.pul.pul,
            '批量重命名':self.rename.rename,'文本处理':self.txmng.txmng},
        '设置(S)':{'清空控制台':lambda: self.clear(self.csl,1),'帮助':self.hlp.hlp,
            '图标':self.icon.icon,'选项':self.precfg.precfg}}
        sz=600//self.scfac
        for i in self.imgs:
            mnu=self.imgs[i][0]
            if mnu is not None:
                self.mnu.add_cascade(mnu,0.4,self.imgs[i][1],sz,self.scfac/2,self.scfac/2)
                for j in mnus[mnu]:
                    self.mnu.add_command(j,0.32,mnus[mnu][j],2.5*self.scfac,self.scfac/6)
    def calsz(self,w:int,h:int,key:str)->str:
        '''read last window info or make window center'''
        size=self.cfg.get(key,'')
        if size and self.check: return size
        wth,hgt=w*self.scfac,h*self.scfac
        posx,posy=(self.sc[1]-wth)//2,(self.sc[2]-hgt)//2
        return f'{wth}x{hgt}+{posx}+{posy}'
    def cinarg(self,tx:str)->str|None:
        '''input argument for command manager'''
        if 'cinarg' in self.tpls: return None
        cin,cinemp=self.cretpl('命令参数',18,6,'cinarg',4); self.val=None
        cinbtx=['文件夹打开','文件打开','文件保存','确认','跳过','取消']
        cinlb=ttk.Label(cinemp[0],text=tx); self.cinvar=tkinter.StringVar()
        cinet=ttk.Entry(cinemp[1],width=40,textvariable=self.cinvar)
        cinlb.pack(expand=1); cinet.pack(expand=1)
        cincmd=[lambda: self.cinpth(0),lambda: self.cinpth(1),lambda: self.cinpth(2),
                lambda: self.getvar(self.cinvar,cin,'cinarg',str),
                lambda: self.cinpas(cin),lambda: self.wmqut(cin,'cinarg')]
        for i in range(6):
            cinbtn=ttk.Button(cinemp[2+i//3],text=cinbtx[i],command=cincmd[i])
            cinbtn.pack(side='left',expand=1)
        for i in range(4): cinemp[i].pack(fill='both',expand=1)
        cin.protocol('WM_DELETE_WINDOW',lambda: self.wmqut(cin,'cinarg'))
        cin.wait_window(); return self.val
    def cinpas(self,tag:tkinter.Toplevel)->None: self.val=''; self.wmqut(tag,'cinarg')
    def cinpth(self,knd:int)->None:
        '''open or save path for command manager'''
        tles=['打开','打开','保存']; pth=self.dlg(knd,tles[knd],('All files','*.*'))
        if pth: self.cinvar.set(f'\"{pth}\"')
    def clear(self,tag:ttk.Treeview,flg:int=0)->None:
        '''clear treeview'''
        tag.delete(*tag.get_children())
        if flg:
            self.show(tag,'purple',f"Fabits {self.data['curvsn']}")
            self.show(tag,'purple',f'Based on Python {sys.version}')
            self.show(tag,'purple','>>>')
    def cpy(self,tag:ttk.Treeview)->str:
        '''treeview copy'''
        scl=tag.selection()
        if scl:
            val=tag.item(scl[0],'values'); self.wm.clipboard_clear()
            self.wm.clipboard_append(val)
        return 'break'
    def cretpl(self,tle:str,wth:int,hgt:int,tag:str,num:int)->tuple:
        '''create toplevel and frame'''
        tpl=tkinter.Toplevel(self.wm); self.tpls[tag]=tpl
        tpl.withdraw(); tpl.geometry(self.calsz(wth,hgt,tag))
        tpl.resizable(0,0); tpl.transient(self.wm); tpl.title(tle)
        tpl.protocol('WM_DELETE_WINDOW',lambda: self.wmqut(tpl,tag))
        tpl.update_idletasks(); self.Api.creblk(self.bgidx,tpl.winfo_id())
        tpl.deiconify(); emps=[ttk.Frame(tpl) for i in range(num)]; return tpl,emps
    def cretre(self,tag:ttk.Frame)->ttk.Treeview:
        '''create treeview with a xview side scrollbar'''
        slb=tkinter.Scrollbar(tag)
        tre=ttk.Treeview(tag,columns=('opt',),show='tree',yscrollcommand=slb.set)
        slb.config(command=tre.yview); tre.column('#0',width=0,stretch=0)
        for i in self.data['clr']: tre.tag_configure(i,foreground=i)
        tre.bind('<Control-c>',lambda *args: self.cpy(tre))
        slb.pack(side='right',fill='y'); tre.pack(fill='both',expand=1)
        return tre
    @staticmethod
    def decode(byt:bytes)->str:
        encs=['utf-8','gbk','gb2312','gb18030','latin1','iso-8859-1']
        for i in encs:
            try: res=byt.decode(i); return res
            except UnicodeDecodeError: continue
        return ''
    @staticmethod
    def dlg(knd:int,tl:str,*args)->str:
        '''open and save file or directory path'''
        if knd==0: pth=filedialog.askdirectory(title=tl)
        elif knd==1: pth=filedialog.askopenfilename(title=tl,filetypes=args)
        else: pth=filedialog.asksaveasfilename(title=tl,filetypes=args)
        return pth
    def funset(self)->None:
        '''initialize useful function'''
        self.clrtul=lambda: (self.tul.reset(),self.tul.ht(),self.tul.speed(0),self.tul.penup())
        self.fntl=lambda ftsz: (self.fnt,self.size(ftsz),'bold')
        self.fulnm=lambda pth,flnm: os.path.join(pth,flnm)
        self.notqut=lambda: self.note.fclose(self.note.now)
        self.pgqut=lambda: (self.Api.state(0),self.wmqut(self.pgbar.pg,'pgbar'))
        self.run=lambda: (self.wm.deiconify(),self.icon.icon(self.ani),self.wm.mainloop())
        self.show=lambda tag,clr,*args: tag.see(tag.insert('','end',values=args,tags=(clr,)))
        self.size=lambda x: round(x*self.scfac)
        self.title=lambda tle: self.wm.title(self.data['tle']+tle)
        self.thr=lambda fun,*args: lambda: threading.Thread(target=fun,args=args).start()
        self.thrpg=lambda tx,num: self.wm.after(0,self.pgbar.pgbar,tx,num)
        self.thrqut=lambda: self.wm.after(1000,self.pgqut)
        self.thrshw=lambda clr,*args: self.wm.after(0,self.show,self.csl,clr,*args)
        self.thrupd=lambda num,tx,clr: self.wm.after(0,self.pgbar.pgupd,num,tx,clr)
        self.web=lambda tag: webbrowser.open(self.data[tag])
    def getvar(self,var:tkinter.StringVar,tag:tkinter.Toplevel,arg:str,knd:type)->None:
        '''get value of entry string variable'''
        res=var.get()
        if not res: self.mb('w','o','提示','请检查输入的内容'); return
        try: self.val=knd(res); self.wmqut(tag,arg)
        except: self.mb('w','o','提示','请检查输入的内容')
    def hshgen(self)->int:
        '''generate crypted hash code'''
        licc,ltmp,lhdg,hsh=len(self.data['icc']),0,64,hashlib.sha256()
        while 1:
            if lhdg==64:
                lhdg=0; hsh.update(self.data['icc'][ltmp%licc].encode())
                ltmp+=1; hdg=hsh.hexdigest()
            yield int(hdg[lhdg:lhdg+2],16)
            lhdg+=2
    def mb(self,icn:str,tp:str,tle:str,msg:str)->str:
        '''create message box'''
        mbdata=self.data['mb']
        mbtmp=messagebox.Message(icon=mbdata[icn],type=mbdata[tp],title=tle,message=msg)
        res=mbtmp.show(); return res
    def misc(self)->None:
        '''create missing texture'''
        arr=zeros((1024,1024,3),dtype=uint8); arr[0:512,0:512]=[255,0,255]
        arr[512:1024,512:1024]=[255,0,255]; pic=fromarray(arr); pic.save('Img/misc.png')
    def notemp(self,num:int)->tuple[ttk.Frame,list[ttk.Frame]]:
        '''create window on notebook widget'''
        emp=ttk.Frame(self.note); emps=[ttk.Frame(emp) for i in range(num)]; return emp,emps
    def savcfg(self)->None:
        '''save configure after app closed'''
        self.Api.uninit(); self.note.clsall(); self.wmqut(self.wm,'Fabits')
        self.cfg['sc']=self.sc; fl=open('Json/Config.json','w',encoding='utf-8')
        json.dump(self.cfg,fl,ensure_ascii=0,indent=4); fl.close()
    def stlchk(self)->None:
        '''check cfg for default configure'''
        init={'font':'TkDefaultFont','knds':[0]*4,
              'ani':1,'bgidx':2,'style':'clam','sc':[0]*3}
        for i in init:
            if i not in self.cfg: self.cfg[i]=init[i]
    def style(self)->None:
        '''set widget style'''
        self.fnt=self.cfg['font']; self.knd=''
        knds=['bold','italic','underline','overstrike']
        for i in range(4): self.knd+=f'{knds[i]} ' if self.cfg['knds'][i] else ''
        if not self.knd: self.knd='normal'
        self.ani,self.bgidx=self.cfg['ani'],self.cfg['bgidx']
        if self.bgidx==2:
            self.bgidx=0 if 6<=time.localtime().tm_hour<18 else 1
        self.bg,self.fg,self.bgin=self.data['style'][self.bgidx]
        sty=ttk.Style(self.wm); self.fntx=(self.fnt,self.size(0.4),self.knd)
        self.stl=self.cfg['style']; sty.theme_use(self.stl)
        sty.configure('.',background=self.bgin,fieldbackground=self.bg)
        sty.configure('.',foreground=self.fg,font=self.fnt)
        sty.configure('Treeview',background=self.bg,font=self.fntx,rowheight=self.scfac)
        sty.layout('Treeview',[('Treeview.treearea',{'sticky':'nswe'})])
        sty.layout('TNotebook',[('TNotebook.Tab',{'sticky':'nswe'})])
        sty.map('TNotebook.Tab',background=[('selected',self.bg),('active',self.bg)])
        self.tplsty(); self.wm.event_generate('<<style>>')
    def tplsty(self)->None:
        '''change style for toplevel'''
        for i in self.tpls: self.Api.creblk(self.bgidx,self.tpls[i].winfo_id())
    def wmini(self)->None:
        '''initialize data and program necessarity'''
        self.scfac=Api.scfac; self.wm=tkinter.Tk(); self.wm.withdraw()
        self.tpls={'Fabits':self.wm}
        self.imgs={'Na':[None,None],'Fl':['文件(F)',None],'Al':['算法(A)',None],
                   'Ba':['批处理(B)',None],'In':['网络(I)',None],
                   'Tl':['工具(T)',None],'St':['设置(S)',None]}
        msgtx=['找不到{}','非法的{}\n请检查是否存在语法错误']
        fls=['Json/Data.json','Json/Config.json']; self.json=[{},{}]
        exist=lambda flnm: os.path.isfile(f'Img/{flnm}.png')
        for i in self.imgs:
            if exist(i): self.imgs[i][1]=tkinter.PhotoImage(file=f'Img/{i}.png')
            else:
                if not exist('misc'): self.misc()
                self.imgs[i][1]=tkinter.PhotoImage(file=f'Img/misc.png')
        self.wm.iconphoto(1,self.imgs['Na'][1])
        for i in range(2):
            try: fl=open(fls[i],'r',encoding='utf-8'); self.json[i]=json.load(fl); fl.close()
            except FileNotFoundError: messagebox.showerror('错误',msgtx[0].format(fls[i])); exit(0)
            except: messagebox.showerror('错误',msgtx[1].format(fls[i])); fl.close(); exit(0)
        self.data,self.cfg=self.json
    def wminp(self,st:str,knd:type=str,show:str='')->any:
        '''a simple variable input widget'''
        if 'wminp' in self.tpls: return None
        inp,inpemp=self.cretpl('',18,5,'wminp',3); self.val=None; inpbtx=['确认','取消']
        inplb=ttk.Label(inpemp[0],text=st); self.inpvar=tkinter.StringVar(value=show)
        inpet=ttk.Entry(inpemp[1],width=40,textvariable=self.inpvar)
        inpcmd=[lambda: self.getvar(self.inpvar,inp,'wminp',knd),
                lambda: self.wmqut(inp,'wminp')]
        for i in range(2):
            inpbtn=ttk.Button(inpemp[2],text=inpbtx[i],command=inpcmd[i])
            inpbtn.pack(side='left',expand=1)
        inplb.pack(expand=1); inpet.pack(expand=1)
        for i in range(3): inpemp[i].pack(fill='both',expand=1)
        inp.protocol('WM_DELETE_WINDOW',lambda: self.wmqut(inp,'wminp'))
        inp.wait_window(); return self.val
    def wmqut(self,arg:tkinter.Tk|tkinter.Toplevel,key:str)->None:
        '''window quit'''
        wth,hgt,posx,posy=arg.winfo_width(),arg.winfo_height(),arg.winfo_x(),arg.winfo_y()
        self.cfg[key]=f'{wth}x{hgt}+{posx}+{posy}'; self.tpls.pop(key); arg.destroy()
class Adend:
    '''add lack file end'''
    def __init__(self,io:Fabits)->None: self.io=io
    def adend(self)->None:
        '''directory input'''
        self.io.show(self.io.csl,'cyan','(1/2)打开')
        self.pth=self.io.dlg(0,'打开')
        self.io.thr(self.adfled)()
    def adfled(self)->None:
        '''add end to file without end'''
        try: flnms=[i for i in os.listdir(self.pth) if os.path.isfile(self.io.fulnm(self.pth,i))]
        except: return
        names=[i for i in flnms if not os.path.splitext(i)[1]]; hdnms=self.io.data['hdnms']
        self.io.thrshw('cyan','(2/2)转换'); lnm=len(names)
        if lnm:
            self.io.thrpg('查找添加缺失后缀',lnm)
            for i in range(lnm):
                nm=self.io.fulnm(self.pth,names[i]); fl=open(nm,'rb')
                cnt,tol,byte,chs=0,0,bytearray(fl.read()),[9,10,13]
                for k in byte:
                    tol+=1
                    if k<32 and k not in chs: cnt+=1
                if tol==0:
                    self.io.thrupd(i+1,f'{names[i]}为空文件 -> {names[i]}.txt','cyan')
                    fl.close(); os.rename(nm,nm+'.txt'); continue
                elif cnt/tol<0.001:
                    self.io.thrupd(i+1,f'{names[i]}可能为文本文件 -> {names[i]}.txt','cyan')
                    fl.close(); os.rename(nm,nm+'.txt'); continue
                fl.seek(0); head=fl.read(32)
                for j in hdnms:
                    if j.encode() in head:
                        self.io.thrupd(i+1,f'{names[i]} -> {names[i]+hdnms[j]}','cyan')
                        fl.close(); os.rename(nm,nm+hdnms[j]); break
                else: self.io.thrupd(i+1,f'未知文件类型: {names[i]}','red')
            self.io.thrqut()
        self.io.thrshw('red','进程已结束')
        self.io.thrshw('purple','>>>')
class Calc:
    '''scientific calculator'''
    def __init__(self,io:Fabits)->None:
        '''set initialize'''
        self.io=io; self.bgf=[]; self.io.wm.bind('<<style>>',self.bgs,'+')
    def bgs(self,*args)->None:
        '''set widget style'''
        for i in self.bgf: i()
    def cal(self)->None:
        '''deal calculate case for scientific calculator'''
        if not self.lexp: return
        try:
            res=round(self.calcon(),self.acc)
            self.calscl[0].config(text=str(res)); self.ressci=res
        except OverflowError: self.calscl[0].config(text='堆栈错误')
        except ArithmeticError: self.calscl[0].config(text='数学错误')
        except ValueError: self.calscl[0].config(text='数学错误')
        except: self.calscl[0].config(text='语法错误')
    def calc(self)->None:
        '''construct window'''
        relnm='计算器'
        if self.io.note.opened(relnm): return
        cal,self.calemp=self.io.notemp(2)
        self.io.note.add(cal,relnm,1,self); self.now=0
        self.mnu=Navigation(cal,self.io); self.bgf+=[self.mnu.bgs]
        mnus={'切换计算器(C)':{'科学计算器':lambda: self.calchg(0),'程序计算器':lambda: self.calchg(1)},
              '选项(O)':{'精度':self.calset,'退出':self.io.notqut}}
        for i in mnus:
            self.mnu.add_cascade(i,0.36,padx=self.io.scfac/3,pady=self.io.scfac/3)
            for j in mnus[i]:
                self.mnu.add_command(j,0.3,mnus[i][j],2*self.io.scfac,self.io.scfac/6)
        self.calsci(); self.calpgm()
        self.ratio=0.15; self.mnu.place(relx=0,rely=0,relwidth=self.ratio,relheight=1)
        self.calemp[0].place(relx=self.ratio,rely=0,relwidth=1-self.ratio,relheight=1)
    def calchg(self,knd:int)->None:
        '''change calculator'''
        if knd==self.now: return
        self.calemp[self.now].place_forget(); self.now=knd
        self.calemp[knd].place(relx=self.ratio,rely=0,relwidth=1-self.ratio,relheight=1)
    def calcon(self)->None:
        '''deal const for scientific calculator'''
        expsyn,lexp,dig,digs=['']*100,0,'',1
        nums,consts='0123456789.',{'m':self.msci,'ANS':self.ressci,'π':math.pi,'e':math.e}
        for i in range(self.lexp):
            if self.expsyn[i] in nums: dig+=self.expsyn[i]
            elif self.expsyn[i] in consts: digs*=consts[self.expsyn[i]]
            else:
                if dig or isinstance(digs,float):
                    digs*=float(dig) if dig else 1.0; expsyn[lexp]=digs; lexp+=1
                expsyn[lexp]=self.expsyn[i]; lexp+=1; dig,digs='',1
        if dig or isinstance(digs,float):
            digs*=float(dig) if dig else 1.0; expsyn[lexp]=digs; lexp+=1
        return self.calstk(expsyn,lexp,0,self.calsyn)
    def calcop(self)->int:
        '''deal const for program calculator'''
        expsyn,lexp,dig,digs,base=['']*100,0,'',None,10
        nums,consts='-0123456789ABCDEF',{'m':self.mpgm,'ANS':self.respgm}
        bases={'hex':16,'dec':10,'oct':8,'bin':2}
        for i in range(self.pexp):
            if self.pgmsyn[i] in bases: base=bases[self.pgmsyn[i]]
            elif self.pgmsyn[i] in nums: dig+=self.pgmsyn[i]
            elif self.pgmsyn[i] in consts:
                if digs==None: digs=1
                digs*=consts[self.pgmsyn[i]]
            else:
                if dig or digs is not None:
                    if digs is None: digs=1
                    if not dig: dig='1'
                    expsyn[lexp]=int(dig,base)*digs; lexp+=1
                expsyn[lexp]=self.pgmsyn[i]; lexp+=1; dig,digs='',None
        if dig or digs is not None:
            if digs is None: digs=1
            if not dig: dig='1'
            expsyn[lexp]=int(dig,base)*digs; lexp+=1
        return self.calstk(expsyn,lexp,1,self.calpyn)
    def calinp(self,tx:str)->None:
        '''input for scientific calculator'''
        match tx:
            case 'M': self.msci=self.ressci; return
            case '=': self.io.thr(self.cal)(); return
            case 'AC': self.expidx,self.lexp=0,0
            case '←':
                if self.expidx!=0:
                    self.expidx-=1; self.lexp-=1
                    for i in range(self.expidx,self.lexp): self.expsyn[i]=self.expsyn[i+1]
            case '<-':
                if self.expidx>0: self.expidx-=1
            case '->':
                if self.expidx<self.lexp: self.expidx+=1
            case '|x|':
                for i in range(self.lexp-1,self.expidx-1,-1): self.expsyn[i+2]=self.expsyn[i]
                self.expsyn[self.expidx]=self.expsyn[self.expidx+1]='|'
                self.expidx+=2; self.lexp+=2
            case _:
                for i in range(self.lexp-1,self.expidx-1,-1): self.expsyn[i+1]=self.expsyn[i]
                self.expsyn[self.expidx]=tx; self.expidx+=1; self.lexp+=1
        newexp=''.join(self.expsyn[:self.expidx]+['I']+self.expsyn[self.expidx:self.lexp])
        self.calscl[0].config(text=' '); self.calscl[1].config(text=newexp)
    def calp(self)->None:
        '''deal calculate case for program calculator'''
        if not self.pexp: return
        try:
            res=self.calcop(); const=int('0x'+'f'*8,16)
            hres=hex(res) if res>=0 else hex(const+res+1)
            ores=oct(res) if res>=0 else oct(const+res+1)
            bres=bin(res) if res>=0 else bin(const+res+1)
            tx=f'(Bool){bool(res)} (Hex){hres[2:]} (Dec){res} (Oct){ores[2:]} (Bin){bres[2:]}'
            self.calpgl[0].config(text=tx); self.respgm=res
        except OverflowError: self.calpgl[0].config(text='堆栈错误')
        except ArithmeticError: self.calpgl[0].config(text='数学错误')
        except ValueError: self.calpgl[0].config(text='数学错误')
        except: self.calpgl[0].config(text='语法错误')
    def calpnp(self,tx:str)->None:
        '''input for program calculator'''
        match tx:
            case 'M': self.mpgm=self.respgm; return
            case '=': self.io.thr(self.calp)(); return
            case 'AC': self.pgmidx,self.pexp=0,0
            case '←':
                if self.pgmidx!=0:
                    self.pgmidx-=1; self.pexp-=1
                    for i in range(self.pgmidx,self.pexp): self.pgmsyn[i]=self.pgmsyn[i+1]
            case '<-':
                if self.pgmidx>0: self.pgmidx-=1
            case '->':
                if self.pgmidx<self.lexp: self.pgmidx+=1
            case _:
                for i in range(self.pexp-1,self.pgmidx-1,-1): self.pgmsyn[i+1]=self.pgmsyn[i]
                self.pgmsyn[self.pgmidx]=tx; self.pgmidx+=1; self.pexp+=1
        newexp=''.join(self.pgmsyn[:self.pgmidx]+['I']+self.pgmsyn[self.pgmidx:self.pexp])
        self.calpgl[0].config(text=' '); self.calpgl[1].config(text=newexp)
    def calpgm(self)->None:
        '''program calculator'''
        self.calpgl,caltx=[ttk.Label]*2,[' ','I']; self.respgm=self.mpgm=0
        self.pgmsyn,self.pexp,self.pgmidx=['']*100,0,0
        self.funsp={'abs':abs,'bool':bool,'~':lambda a: ~a,'!':lambda a: not a}
        self.basp=[{'^':lambda a,b: int(a**b)},
                   {'*':lambda a,b: a*b,'/':lambda a,b: a//b,'%':lambda a,b: a%b},
                   {'+':lambda a,b=0: a+b,'-':lambda a,b=None: -a if b is None else a-b},
                   {'<<':lambda a,b: a<<b,'>>':lambda a,b: a>>b},
                   {'<':lambda a,b: a<b,'>':lambda a,b: a>b,
                    '<=':lambda a,b: a<=b,'>=':lambda a,b: a>=b},
                   {'==':lambda a,b: a==b,'!=':lambda a,b: a!=b},
                   {'&':lambda a,b: a&b},{'⊕':lambda a,b: a^b,
                    '⊙':lambda a,b: ~(a^b)},{'|':lambda a,b: a|b},
                   {'&&':lambda a,b: bool(a and b)},{'xor':lambda a,b: bool(a^b),
                    'nxor':lambda a,b: not a^b},{'||':lambda a,b: bool(a or b)}]
        calemp=[ttk.Frame(self.calemp[1]) for i in range(9)]; calbtx=self.io.data['calpgm']
        for i in range(2):
            self.calpgl[i]=ttk.Label(calemp[i],text=caltx[i],anchor='e')
            self.calpgl[i].pack(fill='both',expand=1,padx=self.io.scfac/3)
        for i in range(7):
            for j in range(8):
                calbtn=ttk.Button(calemp[i+2],text=calbtx[i][j])
                calbtn.config(command=lambda tx=calbtx[i][j]: self.calpnp(tx))
                calbtn.pack(side='left',fill='both',expand=1)
        for i in range(9): calemp[i].pack(fill='both',expand=1)
    def calpyn(self,expsyn:list,lexp:int)->int:
        '''calculate value of expresion for program calculator'''
        rl,tsyn,rsyn,chg=lexp,[any]*100,[any]*100,1
        for i in range(lexp): rsyn[i]=expsyn[i]
        while chg:
            tl,flg,chg=0,0,0
            for i in range(rl):
                if flg: flg=0; continue
                elif rsyn[i] in self.funsp:
                    if isinstance(rsyn[i+1],int):
                        tsyn[tl]=self.funsp[rsyn[i]](rsyn[i+1]); tl+=1; chg=flg=1
                    else: tsyn[tl]=rsyn[i]; tl+=1
                else: tsyn[tl]=rsyn[i]; tl+=1
            for i in range(tl): rsyn[i]=tsyn[i]
            rl=tl
        for i in self.basp:
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
    def calsci(self)->None:
        '''scientific calculator'''
        self.calscl,caltx=[ttk.Label]*2,[' ','I']; self.ressci=self.msci=0.0
        self.expsyn,self.lexp,self.expidx,self.acc=['']*100,0,0,12
        self.funs={'sin':math.sin,'cos':math.cos,'tan':math.tan,'arcsin':math.asin,
                   'arccos':math.acos,'arctan':math.atan,'mod':lambda a,b: a%b,
                   'log':lambda a,b=math.e: math.log(a,b),'√':lambda a,b=2: a**(1/b)}
        self.base=[{'C':lambda a,b: math.gamma(a+1)/math.gamma(b+1)/math.gamma(a-b+1),
                    'P':lambda a,b: math.gamma(a+1)/math.gamma(a-b+1)},
                   {'^':lambda a,b: a**b},{'×':lambda a,b: a*b,'÷':lambda a,b: a/b},
                   {'+':lambda a,b=0: a+b,'-':lambda a,b=None: -a if b is None else a-b}]
        calemp=[ttk.Frame(self.calemp[0]) for i in range(8)]; calbtx=self.io.data['calsci']
        for i in range(2):
            self.calscl[i]=ttk.Label(calemp[i],text=caltx[i],anchor='e')
            self.calscl[i].pack(fill='both',expand=1,padx=self.io.scfac/3)
        for i in range(6):
            for j in range(7):
                calbtn=ttk.Button(calemp[i+2],text=calbtx[i][j])
                calbtn.config(command=lambda tx=calbtx[i][j]: self.calinp(tx))
                calbtn.pack(side='left',fill='both',expand=1)
        for i in range(8): calemp[i].pack(fill='both',expand=1)
    def calset(self)->None:
        '''set remain digest decimal for scientific calculator'''
        acc=self.io.wminp(f'保留小数位数(当前为{self.acc}位)',int)
        if acc is None: return
        self.acc=acc
        if self.acc<0: self.acc=0
        if self.acc>15: self.acc=15
    def calstk(self,expsyn:list,lexp:int,deabs:int=0,fun=None)->any:
        '''deal bracket in expresion for calculator'''
        stk,top,res=[[0,[None]*100,0] for i in range(20)],0,0
        for i in range(lexp):
            if expsyn[i]=='(': top+=1; stk[top][0]=i
            elif expsyn[i]==')':
                if top>0 and expsyn[stk[top][0]]=='(':
                    res=fun(stk[top][1],stk[top][2]); stk[top][2]=0
                    top-=1; stk[top][1][stk[top][2]]=res; stk[top][2]+=1
                else: raise SyntaxError
            elif expsyn[i]=='|' and not deabs:
                if top>0 and expsyn[stk[top][0]]=='|':
                    res=abs(fun(stk[top][1],stk[top][2])); stk[top][2]=0
                    top-=1; stk[top][1][stk[top][2]]=res; stk[top][2]+=1
                else: top+=1; stk[top][0]=i
            else: stk[top][1][stk[top][2]]=expsyn[i]; stk[top][2]+=1
            if top>=20: raise OverflowError
        if top!=0: raise SyntaxError
        return fun(stk[top][1],stk[top][2])
    def calsyn(self,expsyn:list,lexp:int)->float|tuple:
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
    def clrbgf(self)->None: self.bgf=[]
class Cdmix:
    '''code mixer'''
    def __init__(self,io:Fabits)->None: self.io=io
    def cdchk(self)->None:
        '''check input for code mix'''
        self.fls=['']*3
        for i in range(3):
            fl=self.cdvar[i].get()
            if fl: self.fls[i]=fl
            else: self.io.mb('w','o','提示','请检查输入的内容'); return
        if not os.path.splitext(self.fls[2])[1]: self.fls[2]+='.cpy'
        self.io.thr(self.cdgen)()
    def cdcmd(self,knd:int)->None:
        '''open or save path for code mix'''
        tles=['打开','打开','保存']; knds=[('Python source files','*.py'),
            ('C/C++ source files','*.c *.cpp'),('All text files','*.*')]
        pth=self.io.dlg(knd//2+1,tles[knd],knds[knd])
        if not pth: return
        self.cdvar[knd].set(pth)
    def cdgen(self)->None:
        '''generate mixed code'''
        try:
            fpy=open(self.fls[0],'rb'); fcpp=open(self.fls[1],'rb')
            fcpy=open(self.fls[2],'w',encoding='utf-8')
        except: return
        pyb,cppb=fpy.read(),fcpp.read(); fpy.close(); fcpp.close()
        py,cpp=self.io.decode(pyb).splitlines(),self.io.decode(cppb).splitlines()
        fcpy.write('#if 0\n')
        for i in py: fcpy.write(i+'\n')
        fcpy.write('\n\'\'\'\n#else\n')
        for i in cpp: fcpy.write(i+'\n')
        fcpy.write('\n#endif\n////\'\'\''); fcpy.close()
        self.io.thrshw('red','进程已结束')
        self.io.thrshw('purple','>>>')
    def cdmix(self)->None:
        '''construct window'''
        relnm='代码混合器'
        if self.io.note.opened(relnm): return
        cd,cdemp=self.io.notemp(4); self.io.note.add(cd,relnm)
        self.cdvar=[tkinter.StringVar() for i in range(3)]
        cdtx,cdbtx=['Python源代码','C/C++源代码','生成到'],['生成','退出']
        cdcmd=[lambda: self.cdchk(),self.io.notqut]
        for i in range(3):
            cdlb=ttk.Label(cdemp[i],text=cdtx[i],width=12)
            cdet=ttk.Entry(cdemp[i],width=50,textvariable=self.cdvar[i])
            cdbtn=ttk.Button(cdemp[i],text='浏览',command=lambda p=i: self.cdcmd(p))
            cdlb.pack(side='left',padx=self.io.scfac/3)
            cdbtn.pack(side='right',padx=self.io.scfac/3)
            cdet.pack(side='right',padx=self.io.scfac/3)
        for i in range(1,-1,-1):
            cdbtn=ttk.Button(cdemp[3],text=cdbtx[i],command=cdcmd[i])
            cdbtn.pack(side='right',padx=self.io.scfac/3)
        for i in range(3): cdemp[i].pack(fill='x',pady=self.io.scfac/3)
        cdemp[3].pack(side='bottom',fill='x',pady=self.io.scfac/3)
class Clrplc:
    '''color replace'''
    def __init__(self,io:Fabits)->None: self.io=io
    def clrplc(self)->None:
        '''color input'''
        self.io.show(self.io.csl,'cyan','(1/4)打开')
        self.flnm=self.io.dlg(1,'打开',('All image files','*.*'))
        if not self.flnm: return
        convrt=lambda cl: [int(cl[:2],16),int(cl[2:4],16),int(cl[4:],16)]
        sclrs=self.io.wminp('输入被替换颜色(16进制表示)')
        if sclrs is None: return
        sclr=self.io.wminp('输入替换颜色(16进制表示)')
        if sclr is None: return
        try: self.clrs=list(map(convrt,sclrs.split())); self.clr=convrt(sclr)
        except: self.io.mb('w','o','提示','请检查输入的内容'); return
        self.io.thr(self.clrpld)()
    def clrpld(self)->None:
        '''image replace color'''
        self.io.thrshw('cyan','(2/4)转换'); pic=iopen(self.flnm)
        self.io.thrshw('cyan','(3/4)替换'); piarr=array(pic)
        for i in self.clrs: alc=(piarr[:,:,:3]==i).all(axis=-1); piarr[alc,:3]=self.clr
        self.io.thrshw('cyan','(4/4)保存'); pic=fromarray(piarr)
        flnew=self.io.dlg(2,'保存',('Image files','*.png'))
        if not flnew: return
        if not flnew.endswith('.png'): flnew+='.png'
        pic.save(flnew); self.io.thrshw('red','进程已结束')
        self.io.thrshw('purple','>>>')
class Cmdmng:
    '''command manager'''
    def __init__(self,io:Fabits)->None:
        '''set initialize'''
        self.io=io; self.bgf=[]; self.io.wm.bind('<<style>>',self.bgs,'+')
    def bgs(self,*args)->None:
        '''set widget style'''
        for i in self.bgf: i()
    def clrbgf(self)->None: self.bgf=[]
    def cmdadd(self)->None:
        '''add new command for command manager'''
        nm=self.io.wminp('新名称')
        if nm is None: return
        if nm in self.cfg:
            if self.io.mb('q','yn','命令重复','是否替换')=='no': return
            cmd=self.io.wminp('输入命令,占位参数用{变量名}表示')
            if cmd is None: return
            for i in self.cmdtre.get_children():
                if self.cmdtre.item(i,'values')[0]==nm:
                    self.cmdtre.set(i,column='cmd',value=cmd)
                    self.cmdtre.see(i); break
        else:
            cmd=self.io.wminp('输入命令,占位参数用{变量名}表示')
            if cmd is None: return
            self.io.show(self.cmdtre,'green',nm,cmd)
        self.cfg[nm]=cmd
    def cmddel(self)->None:
        '''delete command for command manager'''
        scl=self.cmdtre.selection()
        if not scl: return
        if self.io.mb('q','yn','','确认删除?')=='yes':
            lnm,lcmd=self.cmdtre.item(scl,'values')
            self.cmdtre.delete(scl); self.cfg.pop(lnm)
    def cmdmdf(self)->None:
        '''modify command for command manager'''
        scl=self.cmdtre.selection()
        if not scl: return
        lnm,lcmd=self.cmdtre.item(scl,'values')
        nm=self.io.wminp('新名称',show=lnm)
        if nm is None: return
        cmd=self.io.wminp('输入命令,占位参数用{变量名}表示',show=lcmd)
        if cmd is None: return
        self.cmdtre.set(scl,column='nm',value=nm)
        self.cmdtre.set(scl,column='cmd',value=cmd)
        self.cfg.pop(lnm); self.cfg[nm]=cmd
    def cmdmng(self)->None:
        '''construct window'''
        relnm='命令管理器'
        if self.io.note.opened(relnm): return
        cmd,cmdemp=self.io.notemp(1); self.io.note.add(cmd,relnm,1,self)
        cmdmnu={'命令(C)':{'添加':self.cmdadd,'修改':self.cmdmdf,'删除':self.cmddel},
                '运行(R)':{'预览':lambda: self.cmdrun(pre=1),'运行':self.cmdrun},
                '选项(O)':{'退出':self.io.notqut}}
        self.mnu=Navigation(cmd,self.io); self.bgf+=[self.mnu.bgs]
        for i in cmdmnu:
            self.mnu.add_cascade(i,0.36,padx=self.io.scfac/3,pady=self.io.scfac/3)
            for j in cmdmnu[i]:
                self.mnu.add_command(j,0.3,cmdmnu[i][j],2*self.io.scfac,self.io.scfac/6)
        self.cmdtre=ttk.Treeview(cmdemp[0],columns=('nm','cmd'),show='headings')
        self.cmdtre.heading('nm',text='名称'); self.cmdtre.heading('cmd',text='命令')
        self.cmdtre.column('nm',width=3*self.io.scfac,anchor='w')
        self.cmdtre.column('cmd',width=12*self.io.scfac,anchor='w')
        cmdslb=tkinter.Scrollbar(cmdemp[0]); self.cmdtre.config(yscrollcommand=cmdslb.set)
        cmdslb.config(command=self.cmdtre.yview)
        for i in self.io.data['clr']: self.cmdtre.tag_configure(i,foreground=i)
        cmdslb.pack(side='right',fill='y'); self.cmdtre.pack(fill='both',expand=1)
        if 'cmds' not in self.io.cfg: self.io.cfg['cmds']={}
        self.cfg=self.io.cfg['cmds']
        for i in self.cfg:
            self.io.show(self.cmdtre,'green',i,self.cfg[i])
        ratio=0.15; self.mnu.place(relx=0,rely=0,relwidth=ratio,relheight=1)
        cmdemp[0].place(relx=ratio,rely=0,relwidth=1-ratio,relheight=1)
    def cmdout(self,cmd:str)->None:
        '''print command line message'''
        pipe=subprocess.Popen(cmd,shell=1,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=1)
        for i in iter(pipe.stdout.readline,''):
            self.io.wm.after(0,self.cmdprt,i,'purple')
        out,err=pipe.communicate()
        if out: self.io.wm.after(0,self.cmdprt,out,'yellow')
        if err: self.io.wm.after(0,self.cmdprt,err,'red')
        self.io.wm.after(0,self.cmdprt,'>>>','purple')
    def cmdprt(self,tx:str,cl:str)->None:
        '''multiline print'''
        idx=0; tmptx=tx[idx:idx+100]
        while tmptx: self.io.show(self.io.csl,cl,tmptx); idx+=100; tmptx=tx[idx:idx+100]
    def cmdrun(self,pre:int=0)->None:
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
            args[i]=self.io.cinarg(f'参数{args[i]}的值')
            if args[i] is None: return
        exe=form.format(*args)
        self.cmdprt(exe,'green')
        if pre and self.io.mb('q','yn','预览','是否运行?')=='no': return
        self.io.thr(self.cmdout,exe)()
class Cmpil:
    '''command compile'''
    def __init__(self,io:Fabits)->None: self.io=io
    def cmpadd(self)->None:
        '''open or save path for command compile'''
        pth=self.io.dlg(1,'打开',('C/C++ source files','*.c *.cpp'))
        if not pth: return
        self.cmpvar[0].set(pth)
    def cmpchk(self,pre:int=0)->None:
        '''check input and run compile for command compile'''
        pth=self.cmpvar[0].get()
        if not pth: self.io.mb('w','o','提示','请检查输入的内容'); return
        flnm,ext=os.path.splitext(pth); args=self.cmpvar[1].get()
        if ext=='.c': gcc='gcc'
        elif ext=='.cpp': gcc='g++'
        else: self.io.mb('w','o','提示','请检查输入的内容'); return
        cmd=f'{gcc} \"{pth}\" -o \"{flnm}\" {args}'
        if not self.cmpknd.get(): cmd+=' -shared'
        self.io.wm.after(0,self.cmpprt,cmd,'green')
        if pre: return
        self.cmpout(cmd)
    def cmpil(self)->None:
        '''construct window'''
        relnm='编译链接库'
        if self.io.note.opened(relnm): return
        cmp,cmpemp=self.io.notemp(4); self.io.note.add(cmp,relnm)
        cmptx,cmpbtx=['编译类型','选择文件','其它参数'],['预览','开始','退出']
        cmpcmd=[self.io.thr(self.cmpchk,1),self.io.thr(self.cmpchk,0),self.io.notqut]
        self.cmpknd=tkinter.IntVar(value=0)
        self.cmpvar=[tkinter.StringVar() for i in range(2)]; cmpknd=['.dll','.exe']
        for i in range(3):
            cmplb=ttk.Label(cmpemp[i],text=cmptx[i]); cmplb.pack(side='left',padx=self.io.scfac/3)
        cmpbtn=ttk.Button(cmpemp[1],text='浏览',command=self.cmpadd)
        cmpbtn.pack(side='right',padx=self.io.scfac/3)
        for i in range(1,-1,-1):
            cmprdb=ttk.Radiobutton(cmpemp[0],text=cmpknd[i],width=28)
            cmprdb.config(variable=self.cmpknd,value=i)
            cmpet=ttk.Entry(cmpemp[i+1],textvariable=self.cmpvar[i],width=50+i*14)
            cmprdb.pack(side='right',padx=self.io.scfac/3)
            cmpet.pack(side='right',padx=self.io.scfac/3)
        for i in range(2,-1,-1):
            cmpbtn=ttk.Button(cmpemp[3],text=cmpbtx[i],command=cmpcmd[i])
            cmpbtn.pack(side='right',padx=self.io.scfac/3)
        for i in range(3): cmpemp[i].pack(fill='x',pady=self.io.scfac/3)
        cmpemp[3].pack(fill='x',side='bottom',pady=self.io.scfac/3)
    def cmpout(self,cmd:str)->None:
        '''print command line message'''
        pipe=subprocess.Popen(cmd,shell=1,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=1)
        for i in iter(pipe.stdout.readline,''):
            self.io.wm.after(0,self.cmpprt,i,'purple')
        out,err=pipe.communicate()
        if out: self.io.wm.after(0,self.cmpprt,out,'yellow')
        if err: self.io.wm.after(0,self.cmpprt,err,'red')
        self.io.wm.after(0,self.cmpprt,'>>>','purple')
    def cmpprt(self,tx:str,cl:str)->None:
        '''multiline print'''
        idx=0; tmptx=tx[idx:idx+80]
        while tmptx: self.io.show(self.io.csl,cl,tmptx); idx+=80; tmptx=tx[idx:idx+80]
class Hlp:
    '''help page'''
    def __init__(self,io:Fabits)->None:
        '''set initialize'''
        self.io=io; self.bgf=[]; self.io.wm.bind('<<style>>',self.bgs,'+')
    def bgs(self,*args)->None:
        '''set widget style'''
        for i in self.bgf: i()
    def clrbgf(self)->None: self.bgf=[]
    def hlp(self)->None:
        '''construct window'''
        relnm='帮助'
        if self.io.note.opened(relnm): return
        hlp,hlpemp=self.io.notemp(1)
        self.io.note.add(hlp,relnm,1,self); hlptx=self.io.data['hlp']
        hlpmnu={'帮助内容(I)':{hlptx[i]:lambda knd=i: self.hlpshw(knd) for i in hlptx},
                '选项(O)':{'退出':self.io.notqut}}
        self.mnu=Navigation(hlp,self.io); self.bgf+=[self.mnu.bgs]
        for i in hlpmnu:
            self.mnu.add_cascade(i,0.36,padx=self.io.scfac/3,pady=self.io.scfac/3)
            for j in hlpmnu[i]:
                self.mnu.add_command(j,0.3,hlpmnu[i][j],2*self.io.scfac,self.io.scfac/6)
        self.hlptre=self.io.cretre(hlpemp[0]); self.hlpshw('F')
        ratio=0.15; self.mnu.place(relx=0,rely=0,relwidth=ratio,relheight=1)
        hlpemp[0].place(relx=ratio,rely=0,relwidth=1-ratio,relheight=1)
    def hlpshw(self,knd:str)->None:
        '''print help message'''
        self.io.clear(self.hlptre); mdfls={'D':'Help.md','N':'NEW.md'}
        if knd in mdfls:
            try: fl=open(mdfls[knd],'r',encoding='utf-8')
            except: self.io.mb('e','o','错误',f'{mdfls[knd]}不存在'); return
            self.hlptre.column('opt',anchor='w'); ln=fl.readline(); flg=0
            while ln:
                if ln=='\n' or ln.startswith('!'): ln=fl.readline(); continue 
                elif ln.startswith('```'): flg=1-flg
                elif flg: self.io.show(self.hlptre,'green',ln)
                else:
                    tx=''
                    for i in ln:
                        if i in '#*`- ': continue
                        tx+=i
                    self.io.show(self.hlptre,'green',tx)
                ln=fl.readline()
            fl.close()
        else:
            self.hlptre.column('opt',anchor='c')
            for i in self.io.data['hlps'][knd]: self.io.show(self.hlptre,'green',i)
class Icon:
    '''display begin icon'''
    def __init__(self,io:Fabits)->None: self.io=io
    def icc(self)->None:
        '''display icon icc'''
        if not self.show: self.ice(); return
        self.io.wmain.pack_forget()
        self.io.clrtul(); self.io.cvs.pack(fill='both',expand=1)
        self.ico(self.io.data['icc'],60,self.io.size(0.5),iter('d'))
        self.io.wm.after(500,self.icd)
    def icd(self)->None:
        '''display icon icd'''
        self.io.clrtul(); self.ico('l041r24l30',45,self.io.size(0.6),iter('d'))
        self.ico(self.io.data['icd'],90,self.io.scfac,iter('dwdwd'))
        self.io.tul.rt(45); self.io.tul.fd(12*self.io.scfac)
        chrc,chre='圣·西门科技股份有限公司 出品','Sig·WestGate Tech. L.C.D. present.'
        self.io.tul.write(chrc,align='center',font=('华文行楷',self.io.size(0.8)))
        self.io.tul.fd(self.io.size(2.2))
        self.io.tul.write(chre,align='center',font=('Consolas',self.io.size(0.7),'bold'))
        self.io.wm.after(1200,self.ice)
    def ice(self)->None:
        '''deal system argument'''
        self.io.cvs.pack_forget(); self.io.clrtul()
        self.io.wmain.pack(fill='both',expand=1)
    def ico(self,iccd:str,ang:int,sz:int,clr)->None:
        '''use python turtle to draw icon'''
        cmds={'b':lambda a: (self.io.tul.begin_fill(),self.io.tul.pendown()),
              'e':lambda a: (self.io.tul.end_fill(),self.io.tul.penup()),
              'l':lambda a: (self.io.tul.lt(int(a[0])*ang),self.io.tul.fd(int(a[1:])*sz)),
              'r':lambda a: (self.io.tul.rt(int(a[0])*ang),self.io.tul.fd(int(a[1:])*sz)),
              'c':lambda a: self.io.tul.color(clrs[next(clr)])}
        clrs={'d':'#22cefc','w':self.io.bg}; cmd,dig=cmds['c'],''
        for i in range(len(iccd)):
            if iccd[i].isdigit(): dig+=iccd[i]
            else: cmd(dig); dig,cmd='',cmds[iccd[i]]
        cmd(dig)
    def icon(self,show:int=1)->None: self.show=show; self.io.wm.after(0,self.icc)
class Imgsrt:
    '''image sort'''
    def __init__(self,io:Fabits)->None: self.io=io
    def imgren(self)->None:
        '''multiprocess sort'''
        try:
            getext=lambda fl: os.path.splitext(fl)[-1]
            names=[i for i in os.listdir(self.pth) if getext(i).lower() in self.imgext]
        except: return
        self.io.thrshw('cyan','(2/3)排序'); self.lnm=len(names)
        if self.lnm:
            lnmr,cnt=range(self.lnm),multiprocessing.cpu_count()
            res,pol=[[None,0,'',''] for i in lnmr],multiprocessing.Pool(processes=cnt)
            self.io.thrpg('图片排序',self.lnm); self.picnt=0; calbk=lambda *args: self.imgupd()
            try:
                for i in lnmr:
                    nm=self.io.fulnm(self.pth,names[i])
                    tsk=pol.apply_async(avgs,args=(nm,),callback=calbk)
                    res[i][0]=tsk; res[i][2]=nm
            except Exception as err:
                self.io.thrqut(); pol.close(); self.io.mb('e','o','错误',str(err)); return
            pol.close(); pol.join(); self.io.thrqut()
            for i in lnmr: res[i][1]=res[i][0].get()
            res=sorted(res,key=lambda i:i[1])
            self.io.thrshw('cyan','(3/3)整理')
            for i in lnmr:
                res[i][3]=f'{i:04}{getext(res[i][2])}'
                os.rename(self.io.fulnm(self.pth,res[i][2]),self.io.fulnm(self.pth,res[i][3]))
            for i in lnmr:
                os.rename(self.io.fulnm(self.pth,res[i][3]),self.io.fulnm(self.pth,f'pic{res[i][3]}'))
        self.io.thrshw('red','进程已结束')
        self.io.thrshw('purple','>>>')
    def imgsrt(self)->None:
        '''directory input'''
        self.io.show(self.io.csl,'cyan','(1/3)打开')
        self.imgext=['.png','.jpg','.jpeg','.bmp','.gif','.ico','.ico']
        self.pth=self.io.dlg(0,'打开'); self.io.thr(self.imgren)()
    def imgupd(self)->None:
        '''update progressbar for image sort multiprocessing callback'''
        self.picnt+=1
        if not self.picnt%2:
            self.io.thrupd(self.picnt,f'已完成({self.picnt}/{self.lnm})','cyan')
class Iso:
    '''calculate iso'''
    def __init__(self,io:Fabits)->None: self.io=io
    def iso(self)->None:
        '''input for iso calculate'''
        self.num=self.io.wminp('基团-CnH2n+1,输入n值',int)
        if self.num is None: return
        self.io.thr(self.isocal)()
    def isocal(self)->None:
        '''begin calculate'''
        isonum,liso=zeros(self.num+1,dtype=int),1; isonum[0]=1
        for i in range(self.num):
            isob,isoc,isotmp=0,0,0; isoa=i-2*isoc
            while isoc<=isoa:
                isotmp+=isonum[isoa]*isonum[isob]*isonum[isoc]; isoa-=1; isob+=1
                if isoa<isob: isoc+=1; isoa,isob=i-2*isoc,isoc
            isonum[liso],liso=isotmp,liso+1
        self.io.thrshw('green',f'{isonum[self.num]}')
        self.io.thrshw('purple','>>>')
class Itmsth:
    '''item strength tool for Genshin Impact'''
    def __init__(self,io:Fabits)->None:
        '''set initialize'''
        self.io=io; self.bgf=[]; self.io.wm.bind('<<style>>',self.bgs,'+')
    def bgs(self,*args)->None:
        '''set widget style'''
        for i in self.bgf: i()
    def clrbgf(self)->None: self.bgf=[]
    def itmadd(self)->None:
        '''add item to treeview'''
        if self.itmnum==-1: return
        itmk=f"{self.io.data['itmknd'][self.itknd]}(+{self.pptlvls[4]})"
        itmm=f'-{self.mn}'; itmp='-'
        for i in range(self.lppts):
            ppt=self.io.data['name'][self.ppts[i]]
            if ppt[-1]==' ': itmp+=f'{ppt[:-1]}+{round(self.pptlvls[i]+0.05,1)} '
            else: itmp+=f'{ppt}+{round(self.pptlvls[i]+0.05,1)}% '
        if self.itmnum not in self.res:
            item=self.itmtre.insert('','end',values='',tags=('cyan',))
            self.res[self.itmnum]=item
        self.itmtre.set(self.res[self.itmnum],column='opt',value=f'{itmk}{itmm}{itmp}')
    def itmclr(self)->None:
        '''clear item result'''
        self.io.clear(self.itmtre); self.res={}
    def itmgen(self)->None:
        '''generate item'''
        self.ppts,self.pptlvls,self.itknd=[0]*4,[0]*5,random.randint(0,4)
        mns=self.io.data['mns'][self.itknd]
        self.mn=random.choices(mns[0],weights=mns[1])[0]
        if self.mn==-1: self.mn=random.randint(0,2)
        if self.mn==-2:
            self.mn=random.choice(self.io.data['elmnkd'])
            if self.mn==' ': self.mn='物理'
            else: self.mn+='元素'
            self.mn+='伤害加成'
        else: self.mn=self.io.data['name'][self.mn]
        self.lppts,self.nm=0,random.choices((3,4),weights=(4,1))[0]
        while self.lppts<self.nm:
            lst=range(len(self.io.data['pptpro']))
            ppt=random.choices(lst,weights=self.io.data['pptpro'])[0]
            if ppt not in self.ppts and self.io.data['name'][ppt]!=self.mn:
                upd=random.choice(self.io.data['pptupd'])
                self.pptlvls[self.lppts]=self.io.data['pptmax'][ppt]*upd
                self.ppts[self.lppts]=ppt; self.lppts+=1
        self.itmnum+=1; self.itmprt()
    def itmprt(self,pptidx=-1)->None:
        '''print item for item strength tool'''
        knd=f"{self.io.data['itmknd'][self.itknd]}(+{self.pptlvls[4]})"
        self.io.show(self.io.csl,'cyan',knd)
        self.io.show(self.io.csl,'blue',self.mn)
        for i in range(self.lppts):
            ppt=self.io.data['name'][self.ppts[i]]
            if pptidx!=-1 and i==pptidx: clr='green'
            else: clr='red'
            if ppt[-1]==' ':
                self.io.show(self.io.csl,clr,f'{ppt[:-1]}+{round(self.pptlvls[i]+0.05,1)}')
            else: self.io.show(self.io.csl,clr,f'{ppt}+{round(self.pptlvls[i]+0.05,1)}%')
        self.io.show(self.io.csl,'purple','>>>')
    def itmsth(self)->None:
        '''construct window'''
        relnm='圣遗物强化'
        if self.io.note.opened(relnm): return
        itm,itmemp=self.io.notemp(1)
        self.io.note.add(itm,relnm,1,self); self.itmnum,self.res=-1,{}
        itmmnu={'圣遗物(I)':{'获取':self.itmgen,'强化':self.itmupd,'入库':self.itmadd},
                '选项(O)':{'清空':self.itmclr,'退出':self.io.notqut}}
        self.mnu=Navigation(itm,self.io); self.bgf+=[self.mnu.bgs]
        for i in itmmnu:
            self.mnu.add_cascade(i,0.36,padx=self.io.scfac/3,pady=self.io.scfac/3)
            for j in itmmnu[i]:
                self.mnu.add_command(j,0.3,itmmnu[i][j],2*self.io.scfac,self.io.scfac/6)
        itmlb=ttk.Label(itmemp[0],text='强化结果:'); itmlb.pack(pady=self.io.scfac/3)
        self.itmtre=self.io.cretre(itmemp[0])
        ratio=0.15; self.mnu.place(relx=0,rely=0,relwidth=ratio,relheight=1)
        itmemp[0].place(relx=ratio,rely=0,relwidth=1-ratio,relheight=1)
    def itmupd(self)->None:
        '''upgrage item for item strength tool'''
        if self.itmnum==-1 or self.pptlvls[4]==20: return
        self.pptlvls[4]+=4
        if self.lppts==3:
            while self.lppts!=4:
                lst=range(len(self.io.data['pptpro']))
                ppt=random.choices(lst,weights=self.io.data['pptpro'])[0]
                if ppt not in self.ppts and self.io.data['name'][ppt]!=self.mn:
                    sth=random.choice(self.io.data['pptupd'])
                    self.pptlvls[self.lppts]=self.io.data['pptmax'][ppt]*sth
                    self.ppts[self.lppts]=ppt; self.lppts+=1
            self.itmprt(pptidx=3)
        else:
            pptup=random.randint(0,3); sth=random.choice(self.io.data['pptupd'])
            self.pptlvls[pptup]+=self.io.data['pptmax'][self.ppts[pptup]]*sth
            self.itmprt(pptidx=pptup)
class Lnksrt:
    '''link sort class'''
    def __init__(self,io:Fabits)->None: self.io=io
    def lnkcal(self)->None:
        '''link bubble sort'''
        lnk=json.loads(self.lnks); llnk,cur=0,self.head
        while cur!=-1: llnk+=1; cur=lnk[cur][1]
        for i in range(llnk-1,-1,-1):
            p,q=self.head,-1; r=lnk[p][1]
            for j in range(i):
                if lnk[p][0]>lnk[r][0]:
                    if q==-1: head=r
                    else: lnk[q][1]=r
                    lnk[p][1],lnk[r][1]=lnk[r][1],p; p,r=r,p
                p,q,r=r,p,lnk[r][1]
        self.io.thrshw('green',f'{lnk},head={self.head}')
        self.io.thrshw('purple','>>>')
    def lnksrt(self)->None:
        '''input for link bubble sort'''
        self.lnks=self.io.wminp('输入链表')
        if self.lnks is None: return
        self.head=self.io.wminp('输入头地址',int)
        if self.head is None: return
        self.io.thr(self.lnkcal)()
class Mazen:
    '''visual maze'''
    def __init__(self,io:Fabits)->None: self.io=io
    def mazen(self)->None:
        '''construct window'''
        if 'mzgd' in self.io.tpls: return
        self.mz,mzemp=self.io.cretpl('迷宫可视化',20,8,'mzgd',5)
        mzlb=ttk.Label(mzemp[0],text='迷宫设置'); mzlb.pack(expand=1)
        mztx,mzbtx=['迷宫长','迷宫宽','起点x','起点y','终点x','终点y'],['生成','解','退出']
        self.mzbtn=[ttk.Button]*3; self.mzvars=[tkinter.StringVar(value=1) for i in range(6)]
        mzcmd=[self.mzchk,self.io.thr(self.mzslv),self.mzclr]
        for i in range(6):
            mzlb=ttk.Label(mzemp[i//2+1],text=mztx[i],width=8)
            mzsp=ttk.Spinbox(mzemp[i//2+1],width=12,textvariable=self.mzvars[i],from_=1,to=100)
            mzlb.pack(side='left',expand=1); mzsp.pack(side='left',expand=1)
        for i in range(3):
            self.mzbtn[i]=ttk.Button(mzemp[4],text=mzbtx[i],command=mzcmd[i])
            self.mzbtn[i].pack(side='left',expand=1)
        self.mzbtn[1].config(state='disabled')
        for i in range(5): mzemp[i].pack(fill='both',expand=1)
    def mzchk(self)->None:
        '''check input for visual maze'''
        args=[0]*6
        try:
            for i in range(6): args[i]=int(self.mzvars[i].get())
            self.io.wmain.pack_forget(); self.io.cvs.pack(fill='both',expand=1)
            self.io.clrtul(); self.mzbtn[0].config(state='disabled')
            self.io.thr(self.mzgen,args)()
        except: self.io.mb('w','o','提示','请检查输入的内容'); return
    def mzclr(self)->None:
        '''clear and quit for visual maze'''
        self.io.wmqut(self.mz,'mzgd'); self.io.cvs.pack_forget(); self.io.clrtul()
        self.io.wmain.pack(fill='both',expand=1)
    def mzgen(self,args:list[int])->None:
        '''gen maze for visual maze'''
        self.hgt,self.wth,self.bgx,self.bgy,self.edx,self.edy=args
        self.sz=min(12*self.io.scfac/self.hgt,12*self.io.scfac/self.wth)
        self.maze=ones(shape=(self.hgt*2+1,self.wth*2+1),dtype=int)
        for i in range(self.hgt*2+1):
            for j in range(self.wth*2+1):
                if i in [0,self.hgt*2] or j in [0,self.wth*2]: self.maze[i,j]=0
        self.mzshw(0,0,self.hgt*2+1,self.wth*2+1,self.io.fg)
        self.mzshw(1,1,self.hgt*2,self.wth*2,self.io.bg)
        stk,top=zeros(shape=(self.hgt*self.wth,4),dtype=int),0
        stk[top]=[1,1,self.hgt*2-1,self.wth*2-1]; top+=1
        while top>0:
            top-=1; ltx,lty,rtx,rty=stk[top]
            if rtx-ltx<2 or rty-lty<2: continue
            wllx=random.randint(ltx+1,rtx-1)//2*2; wlly=random.randint(lty+1,rty-1)//2*2
            stk[top]=[wllx+1,wlly+1,rtx,rty]; top+=1; stk[top]=[wllx+1,lty,rtx,wlly-1]; top+=1
            stk[top]=[ltx,lty,wllx-1,wlly-1]; top+=1; stk[top]=[ltx,wlly+1,wllx-1,rty]; top+=1
            for i in range(ltx,rtx+1): self.maze[i,wlly]=0
            for i in range(lty,rty+1): self.maze[wllx,i]=0
            self.mzshw(ltx,wlly,rtx+1,wlly+1,self.io.fg)
            self.mzshw(wllx,lty,wllx+1,rty+1,self.io.fg)
            holes=[(random.randint(ltx,wllx-1)//2*2+1,wlly),
                  (random.randint(wllx+1,rtx)//2*2+1,wlly),
                  (wllx,random.randint(lty,wlly-1)//2*2+1),
                  (wllx,random.randint(wlly+1,rty)//2*2+1)]
            hole=random.randint(0,3)
            for i in range(4):
                if hole-i:
                    emp=holes[i]; self.maze[emp[0],emp[1]]=1
                    self.mzshw(emp[0],emp[1],emp[0]+1,emp[1]+1,self.io.bg)
        self.maze[self.bgx*2-1,self.bgy*2-1]=1; self.maze[self.edx*2-1,self.edy*2-1]=2
        self.mzshw(self.bgx*2-1,self.bgy*2-1,self.bgx*2,self.bgy*2,'#22cefc')
        self.mzshw(self.edx*2-1,self.edy*2-1,self.edx*2,self.edy*2,'#00ff00')
        self.mzbtn[0].config(state='normal')
        self.mzbtn[1].config(state='normal')
    def mzshw(self,ltx:int,lty:int,rtx:int,rty:int,clr:str)->None:
        '''draw rec for generate maze and solve maze'''
        tpx,tpy=(ltx-self.hgt)*self.sz+22*self.io.scfac,(lty-self.wth)*self.sz-12*self.io.scfac
        self.io.tul.teleport(tpx,tpy); self.io.tul.fillcolor(clr); self.io.tul.begin_fill()
        for i in range(2):
            self.io.tul.fd((rtx-ltx)*self.sz); self.io.tul.lt(90)
            self.io.tul.fd((rty-lty)*self.sz); self.io.tul.lt(90)
        self.io.tul.end_fill()
    def mzslv(self)->None:
        '''solve maze for visual maze'''
        self.mzbtn[0].config(state='disabled')
        self.mzbtn[1].config(state='disabled')
        dires=[[1,0],[-1,0],[0,1],[0,-1]]
        stk,top=zeros(shape=(self.hgt*self.wth,3),dtype=int),0
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
class Navigation(ttk.Frame):
    '''navigation menu widget'''
    def __init__(self,master:ttk.Frame,io:Fabits)->None:
        '''initialize navigation widget'''
        super().__init__(master); self.io=io; self.bgf=[]
        self.state:dict[str:list[tkinter.PhotoImage,int]]={}
    def add_cascade(self,tx:str,ftsz:float,ico=None,size=1,padx=0,pady=0)->None:
        '''add top menu'''
        item=ttk.Frame(self); main=tkinter.Frame(item,padx=padx,pady=pady)
        text=tkinter.Label(main,text=tx); dire=tkinter.Label(main,text='▶')
        text.config(bg=self.io.bgin,fg=self.io.fg,font=self.io.fntl(ftsz))
        dire.config(bg=self.io.bgin,fg=self.io.fg); main.config(bg=self.io.bgin)
        self.bgf+=[lambda mn=main: mn.config(bg=self.io.bgin),
            lambda tx=text,sz=ftsz: tx.config(font=self.io.fntl(sz)),
            lambda tx=text: tx.config(bg=self.io.bgin,fg=self.io.fg),
            lambda dr=dire: dr.config(bg=self.io.bgin,fg=self.io.fg)]
        self.subs=ttk.Frame(item)
        show=lambda arg,text=tx,subs=self.subs,dirl=dire: self.disp(text,subs,dirl)
        if ico:
            self.state[tx]=[ico.subsample(size),0]
            icon=tkinter.Label(main,image=self.state[tx][0],bg=self.io.bgin)
            self.bgf+=[lambda ic=icon: ic.config(bg=self.io.bgin)]
            icon.pack(side='left')
            on=lambda arg,args=[main,icon,text,dire]: self.light(args,1)
            off=lambda arg,args=[main,icon,text,dire]: self.light(args,0)
        else:
            self.state[tx]=[None,0]
            on=lambda arg,args=[main,text,dire]: self.light(args,1)
            off=lambda arg,args=[main,text,dire]: self.light(args,0)
        text.pack(side='left'); dire.pack(side='right')
        self.rebind(main,'<ButtonRelease-1>',show)
        self.rebind(main,'<Enter>',on); self.rebind(main,'<Leave>',off)
        main.pack(fill='x'); item.pack(fill='x')
    def add_command(self,tx:str,ftsz:float,cmd=None,padx=0,pady=0)->None:
        '''add second menu'''
        sub=tkinter.Label(self.subs,text=tx,padx=padx,pady=pady,anchor='w')
        sub.config(bg=self.io.bgin,fg=self.io.fg,font=self.io.fntl(ftsz))
        self.bgf+=[lambda su=sub,sz=ftsz: su.config(font=self.io.fntl(sz)),
            lambda su=sub: su.config(bg=self.io.bgin,fg=self.io.fg)]
        if cmd: sub.bind('<ButtonRelease-1>',lambda *args: cmd())
        sub.bind('<Enter>',lambda arg,subl=sub: self.light([subl],1))
        sub.bind('<Leave>',lambda arg,subl=sub: self.light([subl],0)); sub.pack(fill='x')
    def bgs(self,*args)->None:
        '''set widget style'''
        for i in self.bgf: i()
    def disp(self,text:str,subs:ttk.Frame,dire:ttk.Label)->None:
        '''display submenu'''
        if self.state[text][1]:
            dire.config(text='▶'); subs.pack_forget(); self.state[text][1]=0
        else: dire.config(text='▼'); subs.pack(fill='x'); self.state[text][1]=1
    def light(self,args:list,flag:int)->None:
        '''highlight menu'''
        bg=self.io.bg if flag else self.io.bgin
        for i in args: i.config(bg=bg)
    def rebind(self,tag,event:str,fun)->None:
        '''recusion bind function'''
        tag.bind(event,fun)
        for i in tag.winfo_children(): self.rebind(i,event,fun)
class NotebookPlus(ttk.Notebook):
    '''notebook widget with some function'''
    def __init__(self,master,io:Fabits)->None:
        '''construct window'''
        self.io=io; super().__init__(master)
        self.now=self.cur=None; self.count,self.emp,self.card=1,'未命名文件',[]
        self.funset(); self.adarg(); self.menu=tkinter.Menu(self,tearoff=0)
        self.menu.add_command(label='关闭',command=lambda: self.fclose(self.cur))
        self.menu.add_command(label='全部关闭',command=self.clsall)
        self.io.wm.bind('<<style>>',self.bgs,'+')
        self.bind('<ButtonRelease-3>',lambda arg: self.right(arg))
        self.bind('<<NotebookTabChanged>>',lambda arg: self.change())
    def adarg(self)->None:
        '''add file when open with a file'''
        if len(sys.argv)>1:
            fl=sys.argv[1].strip('\"')
            if fl.endswith('.nda'): self.fnew(fl)
            else: self.fopen(fl)
        else: self.fnew()
    def add(self,child,text:str,flg:int=0,tag=None)->None:
        '''open window'''
        self.now=len(self.card); self.card+=[[text,None,flg,tag,child]]
        super().add(child,text=text); super().select(super().tabs()[self.now])
    def bgs(self,*args)->None:
        '''set widget style'''
        self.menu.config(bg=self.io.bg,fg=self.io.fg)
        if 'schgd' in self.io.tpls:
            self.schtg.config(bg=self.io.bgin)
        for i in range(len(self.card)):
            if self.isfl(i):
                self.card[i][4].config(bg=self.io.bg,fg=self.io.fg,font=self.io.fntx)
    def change(self)->None:
        '''change title when change notebook tab'''
        cur=super().select(); tle=''
        for i in range(len(self.card)):
            if super().tabs()[i]==cur:
                self.now=i; tle=f' - {self.getuid(i)}'; break
        self.io.title(tle)
    def ext(self)->None:
        '''text encrypt nda and export'''
        if not self.isfl(self.now): return
        flnm=self.io.dlg(2,'保存',('Nahida Data Assets','*.nda'))
        if not flnm: return
        byte=self.card[self.now][4].get('1.0','end').encode('utf-8')
        bytarr=bytearray(byte); gn=self.io.hshgen()
        bytarr=[i^next(gn) for i in bytarr]; byte=bytes(bytarr)
        if not flnm.endswith('.nda'): flnm+='.nda'
        fl=open(flnm,'wb'); fl.write(byte); fl.close()
    def fclose(self,idx:int,force:int=0)->None:
        '''file close'''
        if idx is None: return
        if self.isfl(idx):
            if force: self.fsave(idx,force=1)
            elif self.card[idx][3]:
                state=self.io.mb('q','ync','关闭文件时保存','未保存的内容将会丢失,是否保存?')
                if state=='yes':
                    if self.card[idx][2]:
                        flnm=self.io.dlg(2,'保存',('All text files','*.*'))
                        if not flnm: return
                        if not os.path.splitext(flnm)[1]: flnm+='.txt'
                    fl=open(flnm,'w',encoding='utf-8',newline='\n')
                    tx=self.card[idx][4].get('1.0','end'); fl.write(tx); fl.close()
                elif state=='cancel': return
        elif self.card[idx][2]: self.card[idx][3].clrbgf()
        super().forget(idx); self.card[idx][4].destroy()
        self.card=self.card[:idx]+self.card[idx+1:]
        if len(self.card)<=self.now: self.now=len(self.card)-1
        if self.now<0: self.now=None
    def fnew(self,flnm:str=None)->None:
        '''new text file or import'''
        if flnm is not None:
            if not flnm: flnm=self.io.dlg(1,'打开',('Nahida Data Assets','*.nda'))
            try: fl=open(flnm,'rb')
            except: return
            byte=fl.read(); fl.close(); bytarr=bytearray(byte); gn=self.io.hshgen()
            bytarr=[i^next(gn) for i in bytarr]; datas=bytes(bytarr)
            dataln=datas.decode('utf-8',errors='backslashreplace').splitlines()
            ldt=len(dataln); text=scrolledtext.ScrolledText(self,undo=1)
            for i in range(ldt):
                if i==ldt-1: text.insert('end',dataln[i])
                else: text.insert('end',dataln[i]+'\n')
        else: text=scrolledtext.ScrolledText(self,undo=1)
        text.bind('<Key>',lambda arg: self.modify()); nm=f'{self.emp}-{self.count}'
        self.now=len(self.card); self.card+=[[nm,nm,1,0,text]]; self.count+=1
        super().add(text,text=nm); super().select(super().tabs()[self.now])
    def fopen(self,flnm:str=None)->None:
        '''open text file'''
        if not flnm: flnm=self.io.dlg(1,'打开',('All text files','*.*'))
        if self.istx(flnm) or self.opened(flnm): return
        fl=open(flnm,'rb'); datas=fl.read(); fl.close()
        dataln=self.io.decode(datas).splitlines()
        text=scrolledtext.ScrolledText(self,undo=1); ldt=len(dataln)
        for i in range(ldt):
            if i==ldt-1: text.insert('end',dataln[i])
            else: text.insert('end',dataln[i]+'\n')
        text.bind('<Key>',lambda arg: self.modify()); nm=os.path.basename(flnm)
        self.now=len(self.card); self.card+=[[nm,flnm,0,0,text]]
        super().add(text,text=nm); super().select(super().tabs()[self.now])
    def fsave(self,idx:int,copy:int=0,force:int=0)->None:
        '''save file'''
        if not self.isfl(idx): return
        flnm=self.card[idx][1]
        if self.card[idx][3]==0: return
        if force and not os.path.splitext(flnm)[1]: flnm+='.txt'
        elif self.card[idx][2] or copy:
            flnm=self.io.dlg(2,'保存',('All text files','*.*'))
            if not flnm: return
            if not os.path.splitext(flnm)[1]: flnm+='.txt'
            self.card[idx][0]=os.path.basename(flnm)
            self.card[idx][1]=flnm; self.card[idx][2]=0
            if self.now==idx: self.change()
            super().tab(super().tabs()[idx],text=os.path.basename(flnm))
        fl=open(flnm,'w',encoding='utf-8',newline='\n')
        tx=self.card[idx][4].get('1.0','end'); fl.write(tx); fl.close()
        self.card[idx][3]=0; return
    def funset(self)->None:
        '''initialize useful function'''
        self.clsall=lambda: [self.fclose(i,1) for i in range(len(self.card)-1,-1,-1)]
        self.delmk=lambda: self.remove() if self.last[0] else None
        self.isfl=lambda idx: None if idx is None else self.card[idx][1]
        self.remove=lambda: self.nowsch.tag_remove('match',self.last[0],self.last[1])
        self.savall=lambda: [self.fsave(i,force=1) for i in range(len(self.card))]
    def getuid(self,idx:int)->str:
        '''get window tag'''
        if idx is None: return None
        if self.isfl(idx): return self.card[idx][1]
        else: return self.card[idx][0]
    def isrt(self,tx:str)->None:
        '''insert line'''
        if not self.isfl(self.now): return
        idx=self.card[self.now][4].index('insert')
        self.card[self.now][4].insert(idx,tx); self.modify(self.now)
    def istx(self,flnm:str)->int:
        '''judge text file or binary file'''
        try: fl=open(flnm,'rb')
        except: return -1
        cnt,tol,byte,chs=0,0,bytearray(fl.read()),[9,10,13]; fl.close()
        for i in byte:
            tol+=1
            if i<32 and i not in chs: cnt+=1
        if tol==0 or cnt/tol<0.001: return 0
        else: self.io.mb('w','o','文件类型不正确','可能是非文本文件'); return -1
    def modify(self,idx:int=None)->None:
        '''change tab title when file modify'''
        if idx is None: idx=self.now
        if not self.card[idx][3]:
            self.card[idx][3]=1
            tab=super().tabs()[idx]
            super().tab(tab,text=f'{self.card[idx][0]}*')
    def opened(self,name:str)->int:
        '''judge window is opened'''
        for i in range(len(self.card)):
            if name==self.getuid(i):
                super().select(super().tabs()[i]); return 1
        return 0
    def redo(self)->None:
        '''redo operation for text editor'''
        if self.isfl(self.now) and self.card[self.now][1]:
            try: self.card[self.now][4].edit_redo()
            except: self.io.wm.bell()
    def right(self,arg)->None:
        '''summon menu on right click'''
        posx,posy=arg.x,arg.y; idx=super().index(f'@{posx},{posy}')
        if idx!=-1: self.cur=idx; self.menu.post(arg.x_root,arg.y_root)
    def rplc(self,al:int=0)->None:
        '''text replace for text editor'''
        schtx,rplctx=self.schvars[0].get(),self.schvars[1].get()
        ncas,cnt=not self.case.get(),0; super().select(super().tabs()[self.nsch])
        if not (schtx and rplctx): self.io.mb('w','o','提示','请检查输入的内容'); return
        cur=self.nowsch.index('insert'); pos=self.nowsch.search(schtx,cur,'end',nocase=ncas)
        if not pos: pos=self.nowsch.search(schtx,'1.0',cur,nocase=ncas)
        while pos:
            self.nowsch.delete(pos,f'{pos}+{len(schtx)}c'); self.nowsch.insert(pos,rplctx)
            aled=f'{pos}+{len(rplctx)}c'; self.nowsch.mark_set('insert',aled); cnt+=1
            cur=self.nowsch.index('insert'); pos=self.nowsch.search(schtx,cur,'end',nocase=ncas)
            if not pos: pos=self.nowsch.search(schtx,'1.0',cur,nocase=ncas)
            if not al: break
        if cnt:
            self.modify(self.nsch)
            if al: self.io.mb('i','o','替换',f'已成功替换{cnt}处文本')
        else: self.io.mb('i','o','提示','找不到相应的文本')
    def sch(self,dire:int=1,al:int=0)->None:
        '''search text for text editor'''
        schtx=self.schvars[0].get(); super().select(super().tabs()[self.nsch])
        if not schtx: self.io.mb('w','o','提示','请检查输入的内容'); return
        st,ed,cur,ncas='1.0','end',self.nowsch.index('insert'),not self.case.get()
        if al: pos=self.nowsch.search(schtx,st,ed,nocase=ncas)
        elif dire:
            pos=self.nowsch.search(schtx,cur+'+1c',ed,nocase=ncas)
            if not pos: pos=self.nowsch.search(schtx,st,cur+'+1c',nocase=ncas)
        else:
            pos=self.nowsch.search(schtx,cur,st,backwards=1,nocase=ncas)
            if not pos: pos=self.nowsch.search(schtx,ed,cur,backwards=1,nocase=ncas)
        if pos:
            self.delmk(); self.nowsch.see(pos); self.nowsch.mark_set('insert',pos)
            aled=f'{pos}+{len(schtx)}c'; self.nowsch.tag_add('match',pos,aled)
            self.nowsch.tag_config('match',background='yellow'); self.last=pos,aled
        else: self.io.mb('i','o','提示','找不到相应的文本')
    def schgd(self)->None:
        '''search and replace text for text editor'''
        if not self.isfl(self.now): return
        if 'schgd' in self.io.tpls: return
        sch,schemp=self.io.cretpl('查找与替换',18,7,'schgd',5); self.last=('','')
        self.nsch,self.nowsch=self.now,self.card[self.now][4]; self.case=tkinter.BooleanVar(value=0)
        self.schvars=[tkinter.StringVar() for i in range(2)]
        schtx,schbtx=['查找','替换为'],['向上查找','向下查找','从头查找','替换','全部替换','退出']
        schqut=lambda: (self.delmk(),self.io.wmqut(sch,'schgd'))
        schcmd=[lambda: self.sch(dire=0),self.sch,lambda: self.sch(al=1),
                self.rplc,lambda: self.rplc(al=1),schqut]
        for i in range(2):
            schlb=ttk.Label(schemp[i],text=schtx[i],width=8)
            schet=ttk.Entry(schemp[i],width=30,textvariable=self.schvars[i])
            schlb.pack(side='left',expand=1); schet.pack(side='left',expand=1)
        self.schtg=Toggle(schemp[2],self.io,self.case)
        schlb=ttk.Label(schemp[2],text='区分大小写',width=32)
        schlb.pack(side='left',expand=1); self.schtg.pack(side='left',expand=1)
        for i in range(6):
            schbtn=ttk.Button(schemp[3+i//3],text=schbtx[i],command=schcmd[i])
            schbtn.pack(side='left',expand=1)
        sch.protocol('WM_DELETE_WINDOW',schqut)
        for i in range(5): schemp[i].pack(fill='both',expand=1)
    def undo(self)->None:
        '''undo operation for text editor'''
        if self.isfl(self.now) and self.card[self.now][1]:
            try: self.card[self.now][4].edit_undo()
            except: self.io.wm.bell()
class Pgbar:
    '''progressbar window'''
    def __init__(self,io:Fabits)->None: self.io=io
    def pgbar(self,tle:str,tol:int)->None:
        '''progress bar initialize'''
        if 'pgbar' in self.io.tpls: return
        self.pg,pgemp=self.io.cretpl('',16,13,'pgbar',3)
        self.pglb=ttk.Label(pgemp[0],text='0.00%')
        self.pgpgb=ttk.Progressbar(pgemp[1],maximum=tol)
        self.pgtre=self.io.cretre(pgemp[2]); self.tol=tol
        self.pg.update_idletasks(); self.io.Api.state(2)
        self.pg.title(tle); self.pglb.pack(expand=1)
        self.pgpgb.pack(fill='both',expand=1,padx=self.io.scfac//2,pady=self.io.scfac//4)
        for i in range(3): pgemp[i].pack(fill='both',expand=1)
    def pgupd(self,num:int,tx:str,clr:str)->None:
        '''update progress bar'''
        self.pglb.config(text=f'{100*num/self.tol:.2f}%')
        self.io.show(self.pgtre,clr,tx); self.pgpgb['value']=num
        self.io.Api.value(num,self.tol)
class Piccpt:
    '''picture encrypt'''
    def __init__(self,io:Fabits)->None: self.io=io
    def piccpt(self)->None:
        '''directory input'''
        self.io.show(self.io.csl,'cyan','(1/3)打开')
        self.flnm=self.io.dlg(1,'打开',('All image files','*.*'))
        self.io.thr(self.pichsh)()
    def pichsh(self)->None:
        '''hash encrypt'''
        try: pic=iopen(self.flnm)
        except: return
        piarr,hgt,wth=array(pic),pic.height,pic.width
        self.io.thrshw('cyan','(2/3)加密')
        lclr=len(piarr[0,0]); hsh=self.io.hshgen()
        imgmsk=zeros_like(piarr); self.io.thrpg('图片加密',hgt)
        for i in range(hgt):
            for j in range(wth):
                for k in range(lclr): imgmsk[i,j,k]=next(hsh)
            if i%2: self.io.thrupd(i+1,f'已加密{i+1}/{hgt}','cyan')
        pic=fromarray(bitwise_xor(piarr,imgmsk))
        self.io.thrqut()
        self.io.thrshw('cyan','(3/3)保存')
        new=self.io.dlg(2,'保存',('Image files','*.png'))
        if not new: return
        if new.endswith('.png'): pic.save(new)
        else: pic.save(f'{new}.png')
        self.io.thrshw('red','进程已结束')
        self.io.thrshw('purple','>>>')
class Precfg:
    '''preference setting'''
    def __init__(self,io:Fabits)->None:
        '''set initialize'''
        self.io=io; self.bgf=[]; self.io.wm.bind('<<style>>',self.bgs,'+')
    def bgs(self,*args)->None:
        '''set widget style'''
        for i in self.bgf: i()
    def clrbgf(self)->None: self.bgf=[]
    def preapy(self)->None:
        '''confirm and reboot for preference setting'''
        state={'白天模式':0,'夜间模式':1,'流转模式':2}
        self.aply.config(state='disabled')
        self.cfg['bgidx']=state[self.stlvar[0].get()]
        self.cfg['style'],self.cfg['font']=self.stlvar[1].get(),self.stlvar[2].get()
        self.cfg['knds']=[self.fntvar[i].get() for i in range(4)]
        self.cfg['ani']=self.fntvar[4].get()
        self.io.style()
    def precfg(self)->None:
        '''construct window'''
        relnm='选项'
        if self.io.note.opened(relnm): return
        pre,preemp=self.io.notemp(9)
        self.io.note.add(pre,relnm,1,self); self.cfg=self.io.cfg
        pretx=['UI显示模式','主题','字体']; preotx=[self.io.data['modes'],
            style+self.io.data['styles'],self.io.data['fonts']]
        optshw=[preotx[0][self.cfg['bgidx']],self.cfg['style'],self.cfg['font']]
        prebtx=['粗体','斜体','下划线','删除线','是否启用动画']
        self.stlvar=[tkinter.StringVar(value=optshw[i]) for i in range(3)]
        self.fntvar=[tkinter.IntVar(value=self.cfg['knds'][i]) for i in range(4)]
        self.fntvar+=[tkinter.IntVar(value=self.io.ani)]
        enable=lambda *args: self.aply.config(state='normal')
        for i in range(3):
            prelb=ttk.Label(preemp[i],text=pretx[i],width=15)
            preopt=ttk.OptionMenu(preemp[i],self.stlvar[i],optshw[i],*preotx[i])
            preopt['menu'].configure(bg=self.io.bg,fg=self.io.fg)
            self.bgf+=[lambda mnu=preopt['menu']: mnu.configure(bg=self.io.bg,fg=self.io.fg)]
            preopt.config(width=30); prelb.pack(side='left',padx=self.io.scfac/3)
            preopt.pack(side='right',padx=self.io.scfac/3); self.stlvar[i].trace('w',enable)
        for i in range(5):
            pretg=Toggle(preemp[i+3],self.io,self.fntvar[i],enable)
            self.bgf+=[lambda tg=pretg: tg.config(bg=self.io.bgin)]
            prelb=ttk.Label(preemp[i+3],text=prebtx[i],width=32)
            prelb.pack(side='left',padx=self.io.scfac/3)
            pretg.pack(side='right',padx=self.io.scfac/3)
        self.aply=ttk.Button(preemp[8],text='应用',command=self.preapy,state='disabled')
        clrbtn=ttk.Button(preemp[8],text='退出',command=self.io.notqut)
        clrbtn.pack(side='right',padx=self.io.scfac/3)
        self.aply.pack(side='right',padx=self.io.scfac/3)
        for i in range(8): preemp[i].pack(fill='x',pady=self.io.scfac/3)
        preemp[8].pack(fill='x',side='bottom',pady=self.io.scfac/3)
class Pro:
    '''pull for probility tool for Genshin Impact'''
    def __init__(self,io:Fabits)->None:
        self.io=io; self.protmp=zeros(shape=(52,91,5,2))
        self.pullst=zeros(shape=(38000,4),dtype=int); self.prolst=zeros(38000)
    def pro(self)->None:
        '''construct window'''
        relnm='抽卡概率计算'
        if self.io.note.opened(relnm): return
        pro,proemp=self.io.notemp(6)
        self.io.note.add(pro,relnm); limit=[1000000,5000,89,3,1]
        self.provars=[tkinter.StringVar(value=0) for i in range(5)]
        probtx=['原石数','粉球数','垫池数(0-89)','已经连歪数(0-3)','是否大保底(0/1)']
        for i in range(5):
            prolb=ttk.Label(proemp[i],text=probtx[i],width=15)
            prolb.pack(side='left',padx=self.io.scfac/3)
            prosp=ttk.Spinbox(proemp[i],width=40,textvariable=self.provars[i],from_=0,to=limit[i])
            prosp.pack(side='right',padx=self.io.scfac/3)
        self.procfm=ttk.Button(proemp[5],text='确认',command=self.prochk)
        probtn=ttk.Button(proemp[5],text='退出',command=self.io.notqut)
        probtn.pack(side='right',padx=self.io.scfac/3)
        self.procfm.pack(side='right',padx=self.io.scfac/3)
        for i in range(5): proemp[i].pack(fill='x',pady=self.io.scfac/3)
        proemp[5].pack(fill='x',side='bottom',pady=self.io.scfac/3)
    def procal(self,args:list[int])->None:
        '''calculate pull for probility'''
        respro=zeros(52,dtype=float)
        stn,pbl,puts,fu,tu=args; self.procfm.config(state='disabled')
        lpro,st,ed=0,0,50; pbl+=stn//160; self.pullst[lpro]=[0,puts,fu,tu]
        self.prolst[lpro]=1; lpro+=1; self.io.thrpg('抽卡模拟',pbl)
        for i in range(pbl):
            for j in range(lpro):
                upnum,put,false_up,true_up=self.pullst[j]; lstpro=self.prolst[j]
                upnum=min(upnum,50); putpro=self.io.data['lst5'][put]
                tu_pro=self.io.data['tu_lst'][false_up]
                self.protmp[upnum,put+1,false_up,true_up]+=lstpro*(1-putpro)
                if true_up: self.protmp[upnum+1,0,false_up,0]+=lstpro*putpro
                else:
                    self.protmp[upnum,0,false_up+1,1]+=lstpro*putpro*(1-tu_pro)
                    self.protmp[upnum+1,0,0,0]+=lstpro*putpro*tu_pro
            lpro=0
            for j in range(52):
                for t in range(90):
                    for p in range(4):
                        for k in range(2):
                            if self.protmp[j,t,p,k]!=0:
                                self.pullst[lpro]=[j,t,p,k]; self.prolst[lpro]=self.protmp[j,t,p,k]
                                lpro+=1; self.protmp[j,t,p,k]=0
            if i%2: self.io.thrupd(i+1,f'已完成{i+1}抽','cyan')
        for i in range(lpro): respro[self.pullst[i,0]]+=self.prolst[i]*100
        for i in range(ed+1):
            if respro[i]>0.1: st=i; break
        for i in range(ed,0,-1):
            if respro[i]<0.1: respro[i-1]+=respro[i]
            else: ed=i; break
        self.io.thrqut(); self.io.thrshw('purple','UP数 概率')
        for i in range(st,ed+1):
            self.io.thrshw('purple',f'{i:>2d}{respro[i]:7.2f}%')
        self.io.thrshw('purple','>>>')
        self.procfm.config(state='normal')
    def prochk(self)->None:
        '''check input for pull for probility'''
        limit=[89,3,1]; args=[0]*5
        for i in range(5):
            val=self.provars[i].get()
            if (not val.isdigit()) or int(val)<0:
                self.io.mb('w','o','提示','请检查输入的内容'); return
            if i>1 and int(val)>limit[i-2]:
                self.io.mb('w','o','提示','请检查输入的内容'); return
            args[i]=int(val)
        self.io.thr(self.procal,args)()
class Pul:
    '''pull for tools for Genshin Impact'''
    def __init__(self,io:Fabits)->None:
        '''set initialize'''
        self.io=io; self.bgf=[]; self.io.wm.bind('<<style>>',self.bgs,'+')
    def bgs(self,*args)->None:
        '''set widget style'''
        for i in self.bgf: i()
    def clrbgf(self)->None: self.bgf=[]
    def pul(self)->None:
        '''construct window'''
        relnm='抽卡模拟器'
        if self.io.note.opened(relnm): return
        pul,pulwm=self.io.notemp(1)
        self.io.note.add(pul,relnm,1,self); self.res={}
        pulemp=[ttk.Frame(pulwm[0]) for i in range(5)]
        pultx=['五星UP','四星UP1','四星UP2','四星UP3']
        pulmnu={'祈愿(W)':{'确认':self.pulchk,'祈愿一次':lambda: self.pulcal(1),
                '祈愿十次':lambda: self.pulcal(10)},'选项(O)':{'清空':self.pulclr,
                '重置':self.pulset,'退出':self.io.notqut}}
        puldtx=['ups5','ups4','fups5','wpns5','wpns4','wpns3']
        self.ups,self.put5,self.put4,self.true_up5,self.true_up4,self.fu=['']*4,0,0,0,0,0
        self.pulvar=[tkinter.StringVar() for i in range(4)]
        ups5,ups4=self.io.data['ups5'],self.io.data['ups4']
        self.menu=Navigation(pul,self.io)
        for i in pulmnu:
            self.menu.add_cascade(i,0.36,padx=self.io.scfac/3,pady=self.io.scfac/3)
            for j in pulmnu[i]:
                self.menu.add_command(j,0.3,pulmnu[i][j],2*self.io.scfac,self.io.scfac/6)
        for i in range(4):
            pullb=ttk.Label(pulemp[i],text=pultx[i])
            if i: pulopt=ttk.OptionMenu(pulemp[i],self.pulvar[i],ups4[0],*ups4)
            else: pulopt=ttk.OptionMenu(pulemp[i],self.pulvar[i],ups5[0],*ups5)
            pulopt['menu'].configure(bg=self.io.bg,fg=self.io.fg)
            self.bgf+=[lambda mnu=pulopt['menu']: mnu.configure(bg=self.io.bg,fg=self.io.fg)]
            pulopt.config(width=20); pullb.pack(side='left',padx=self.io.scfac/3)
            pulopt.pack(side='right',padx=self.io.scfac/3)
        self.pullb=ttk.Label(pulemp[4],text='祈愿结果'); self.pullb.pack(expand=1)
        ratio=0.15; self.menu.place(relx=0,rely=0,relwidth=ratio,relheight=1)
        pulwm[0].place(relx=ratio,rely=0,relwidth=1-ratio,relheight=1)
        for i in range(5): pulemp[i].pack(fill='x',pady=self.io.scfac/3)
        self.pultre=self.io.cretre(pulwm[0])
    def puladd(self,knd:int,up:str)->None:
        '''add result to treeview'''
        clr=['yellow','purple','blue']
        if knd==3: up='三星武器'
        if up not in self.res:
            item=self.pultre.insert('','end',values='',tags=(clr[5-knd],))
            self.res[up]=[0,item]
        self.res[up][0]+=1
        self.pultre.set(self.res[up][1],column='opt',value=f'{up}:{self.res[up][0]}')
    def pulcal(self,num:int)->None:
        '''generate pull'''
        if not self.ups[0]: return
        for i in range(num):
            kndpro,trupro=random.random(),random.random()
            if kndpro<=self.io.data['lst5'][self.put5]:
                if self.true_up5:
                    self.io.show(self.io.csl,'yellow',self.ups[0])
                    self.true_up5=0; self.puladd(5,self.ups[0])
                elif trupro<=self.io.data['tu_lst'][self.fu]:
                    self.io.show(self.io.csl,'yellow',self.ups[0])
                    self.true_up5=self.fu=0; self.puladd(5,self.ups[0])
                else:
                    fal_up5=random.choice(self.io.data['fups5']+self.io.data['wpns5'])
                    self.io.show(self.io.csl,'yellow',fal_up5); self.io.show(self.io.csl,'red','歪')
                    self.true_up5,self.fu=1,self.fu+1; self.puladd(5,fal_up5)
                self.put5,self.put4=0,self.put4+1
            elif kndpro<=self.io.data['lst5'][self.put5]+self.io.data['lst4'][self.put4]:
                if trupro<=0.5 or self.true_up4:
                    up4=random.choice(self.ups[1:])
                    self.io.show(self.io.csl,'purple',up4)
                    self.true_up4=0; self.puladd(4,up4)
                else:
                    fal_up4=random.choice(self.io.data['ups4']+self.io.data['wpns4'])
                    self.io.show(self.io.csl,'purple',fal_up4)
                    self.true_up4=1; self.puladd(4,fal_up4)
                self.put5,self.put4=self.put5+1,0
            else:
                up3=random.choice(self.io.data['wpns3'])
                self.io.show(self.io.csl,'blue',up3)
                self.put5,self.put4=self.put5+1,self.put4+1; self.puladd(3,up3)
        self.io.show(self.io.csl,'cyan',f'垫{self.put5}发')
        self.io.show(self.io.csl,'purple','>>>')
    def pulchk(self)->None:
        '''add up pull for'''
        resups=['']*4
        for i in range(4):
            up=self.pulvar[i].get()
            if up in resups: self.io.mb('w','o','选择角色重复','请重新选择'); return
            resups[i]=up
        for i in range(4):
            self.ups[i]=resups[i]; self.io.show(self.io.csl,'red',f'角色{self.ups[i]}添加成功!')
        upstx=f'当前角色:{self.ups[0]},{self.ups[1]},{self.ups[2]},{self.ups[3]}'
        self.pullb.config(text=f'祈愿结果({upstx})')
    def pulclr(self)->None:
        '''clear pul result'''
        self.io.clear(self.pultre); self.res={}
    def pulset(self)->None:
        '''clear pul data'''
        self.ups,self.put5,self.put4,self.true_up5,self.true_up4,self.fu=['']*4,0,0,0,0,0
        self.pulclr(); self.pullb.config(text='祈愿结果')
class Rename:
    '''file rename tool'''
    def __init__(self,io:Fabits)->None:
        '''set initialize'''
        self.io=io; self.bgf=[]; self.io.wm.bind('<<style>>',self.bgs,'+')
    def bgs(self,*args)->None:
        '''set widget style'''
        for i in self.bgf: i()
    def clrbgf(self)->None: self.bgf=[]
    def recmd(self,knd:int)->None:
        '''command for file rename tool'''
        if knd==0:
            exts=self.revars[0].get().split()
            flnm=self.io.dlg(1,'打开',('All files','*.*'))
            if not flnm: return
            ext=os.path.splitext(flnm)[1]
            if ext in exts: return
            exts+=[ext]; self.revars[0].set(' '.join(exts))
        elif knd==1:
            pth=self.io.dlg(0,'打开')
            if not pth: return
            self.revars[1].set(pth)
    def rename(self)->None:
        '''construct window'''
        relnm='批量重命名'
        if self.io.note.opened(relnm): return
        re,reemp=self.io.notemp(4); self.io.note.add(re,relnm,1,self)
        revar=tkinter.StringVar(); self.revars=[tkinter.StringVar() for i in range(3)]
        retx,rebtx=['文件后缀','目录','命名模板'],['重命名','预览','退出']
        recmds=[self.io.thr(self.renm),self.io.thr(self.renm,1),self.io.notqut]
        refun=lambda *args: self.revars[2].set(self.io.data['tmplts'][int(revar.get()[0])-1])
        for i in range(3):
            relb=ttk.Label(reemp[i],text=retx[i],width=16)
            reet=ttk.Entry(reemp[i],width=50,textvariable=self.revars[i])
            relb.pack(side='left',padx=self.io.scfac/3)
            if i-2:
                recmd=lambda k=i: self.recmd(k); tx='浏览'
                rebtn=ttk.Button(reemp[i],text=tx,command=recmd,width=15)
                rebtn.pack(side='right',padx=self.io.scfac/3)
            else:
                tmplt=self.io.data['tmplt']
                reopt=ttk.OptionMenu(reemp[2],revar,tmplt[0],*tmplt)
                reopt['menu'].configure(bg=self.io.bg,fg=self.io.fg)
                self.bgf+=[lambda mnu=reopt['menu']: mnu.configure(bg=self.io.bg,fg=self.io.fg)]
                reopt.config(width=13); revar.trace('w',refun)
                reopt.pack(side='right',padx=self.io.scfac/3)
            reet.pack(side='right',padx=self.io.scfac/3)
        for i in range(2,-1,-1):
            rebtn=ttk.Button(reemp[3],text=rebtx[i],command=recmds[i])
            rebtn.pack(side='right',padx=self.io.scfac/3)
        for i in range(3): reemp[i].pack(fill='x',pady=self.io.scfac/3)
        reemp[3].pack(fill='x',side='bottom',pady=self.io.scfac/3)
    def renm(self,show:int=0)->None:
        '''generate template and file rename'''
        exts,pth=self.revars[0].get().split(),self.revars[1].get()
        tmplt=self.revars[2].get(); ltpl=len(tmplt)
        if not (pth and tmplt): self.io.mb('w','o','提示','请检查输入的内容'); return
        try:
            if not exts: names=[i for i in os.listdir(pth)]
            else: names=[i for i in os.listdir(pth) if os.path.splitext(i)[1] in exts]
        except: return
        names=[[i,''] for i in names if os.path.isfile(self.io.fulnm(pth,i))]
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
            fltime={'a':time.localtime(os.path.getatime(self.io.fulnm(pth,nm))),
                    'm':time.localtime(os.path.getmtime(self.io.fulnm(pth,nm))),
                    'c':time.localtime(os.path.getctime(self.io.fulnm(pth,nm)))}
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
            if self.io.mb('q','yn','模板预览',tx)=='no': return
        if lnms:
            self.io.thrpg('视频重命名',lnms); cnt=0
            for i in range(lnms):
                try:
                    os.rename(self.io.fulnm(pth,names[i][0]),self.io.fulnm(pth,names[i][1]))
                    self.io.thrupd(i+1,f'{names[i][0]} -> {names[i][1]}','cyan')
                except: cnt+=1
            self.io.thrqut()
            if cnt: self.io.mb('w','o','重命名',self.io.data['flmsg'].format(lnms-cnt,cnt))
        self.io.thrshw('red','进程已结束')
        self.io.thrshw('purple','>>>')
class Ring:
    '''calculate ring number'''
    def __init__(self,io:Fabits)->None: self.io=io
    def ring(self)->None:
        '''input for calculate ring number'''
        self.num=self.io.wminp('输入n值(对)',int)
        if self.num is None: return
        self.io.thr(self.ringcal)()
    def ringcal(self)->None:
        '''begin calculate'''
        rmax,flg=0,[1]*(2*self.num)
        for i in range(2*self.num):
            tmp,lring=i,0
            while flg[tmp]:
                flg[tmp],lring=0,lring+1
                if tmp<self.num: tmp*=2
                else: tmp=2*(tmp-self.num)+1
            rmax=max(rmax,lring)
        self.io.thrshw('green',f'{rmax}')
        self.io.thrshw('purple','>>>')
class Rome:
    '''calculate rome number'''
    def __init__(self,io:Fabits)->None: self.io=io
    def rome(self)->None:
        '''input for calculate rome number'''
        self.chs=self.io.wminp('输入罗马数字')
        if self.chs is None: return
        self.io.thr(self.romecal)()
    def romecal(self)->None:
        '''begin calculate'''
        num,stk,top=0,[0]*len(self.chs),0
        for i in self.chs:
            if i not in self.io.data['rome']:
                self.io.mb('w','o','提示','请检查输入的内容'); return
            while top>0 and self.io.data['rome'][i]>stk[top-1]: top-=1; num-=stk[top]
            stk[top]=self.io.data['rome'][i]; top+=1
        while top>0: top-=1; num+=stk[top]
        self.io.thrshw('green',f'{num}')
        self.io.thrshw('purple','>>>')
class Toggle(tkinter.Canvas):
    '''modern widget with dynamic animation'''
    _count=0
    def __init__(self,master:ttk.Frame,io:Fabits,var:tkinter.BooleanVar,cmd=None)->None:
        '''initialize toggle widget'''
        wth,hgt=2*io.scfac,io.scfac
        super().__init__(master,width=wth+1,height=hgt+1,bg=io.bgin,highlightthickness=0)
        self.wth,self.hgt,self.rad=wth,hgt,0.375*hgt
        self.sc,self.on,self.off='#ffffff','#4CAF50','#848484'
        self.var,self.cmd,self.items=var,cmd,[None]*4
        self.onani,self.state,self.fx=0,self.var.get(),lambda x: 1-(1-x)**3
        self.draw(self.state); self.bind('<ButtonRelease-1>',self.toggle)
    def ani(self,crd)->None:
        '''play animation for toggle switch move'''
        try: cd=next(crd)
        except: self.onani=0; return
        scx,scy=self.hgt/2-self.rad,self.hgt/2+self.rad
        if self.state: self.coords(self.items[3],cd-self.rad,scx,cd+self.rad,scy)
        else: self.coords(self.items[3],self.wth-cd-self.rad,scx,self.wth-cd+self.rad,scy)
        self.after(15,self.ani,crd)
    def draw(self,state:int)->None:
        '''begin draw toggle'''
        par,bg=self.wth-self.hgt,self.on if state else self.off
        scx,scy=self.hgt/2-self.rad,self.hgt/2+self.rad
        self.items[0]=self.create_arc(0,0,self.hgt,self.hgt,start=90,
                                      extent=180,fill=bg,outline='')
        self.items[1]=self.create_arc(par,0,self.wth,self.hgt,start=270,
                                      extent=180,fill=bg,outline='')
        self.items[2]=self.create_rectangle(self.hgt/2,0,self.wth-self.hgt/2,
                                            self.hgt+1,fill=bg,outline='')
        if state: self.items[3]=self.create_oval(scx+par,scx,scy+par,scy,fill=self.sc,outline='')
        else: self.items[3]=super().create_oval(scx,scx,scy,scy,fill=self.sc,outline='')
    def toggle(self,*args)->None:
        '''prepare to play animation'''
        if self.onani: return
        self.onani,self.state=1,1-self.state; bg=self.on if self.state else self.off
        if self.var: self.var.set(self.state)
        if self.cmd: self.cmd(self.state)
        for i in range(3): self.itemconfig(self.items[i],fill=bg)
        crd=(self.fx(i/12)*(self.wth-self.hgt)+self.hgt/2 for i in range(13))
        self.after(0,self.ani,crd)
class Txmng:
    '''text manager'''
    def __init__(self,io:Fabits)->None:
        '''set initialize'''
        self.io=io; self.bgf=[]; self.io.wm.bind('<<style>>',self.bgs,'+')
    def bgs(self,*args)->None:
        '''set widget style'''
        for i in self.bgf: i()
    def clrbgf(self)->None: self.bgf=[]
    def encucd(self,tx:str)->str:
        '''unicode encoder for text manager'''
        ltx=len(tx); res=['']*ltx
        for i in range(ltx): res[i]=f'\\u{ord(tx[i]):04x}'
        return ''.join(res)
    def rndchr(self,tx:str,num:int)->str:
        '''generate random combinate character for text manager'''
        slst=list(range(768,880))+list(range(1155,1162))
        lres,res=0,['']*len(tx)*(num+1)
        for i in tx:
            res[lres]=i; lres+=1; chs=map(chr,random.choices(slst,k=num))
            for j in chs: res[lres]=j; lres+=1
        return ''.join(res)
    def txcmd(self,knd:int,idx:int)->None:
        '''open or save file for text manager'''
        args=['打开','保存']; pth=self.io.dlg(knd+1,args[knd],('All text files','*.*'))
        if not pth: return
        self.txet[knd][idx].delete(0,'end'); self.txet[knd][idx].insert(0,pth)
    def txcpt(self,tx:str)->str:
        '''text encrypt for text manager'''
        byte=tx.encode('utf-8')
        bytarr=bytearray(byte); gn=self.io.hshgen()
        bytarr=[i^next(gn) for i in bytarr]; byte=bytes(bytarr)
        return byte.decode('utf-8',errors='backslashreplace')
    def txinp(self)->None:
        '''input for text manager'''
        tx,new,num=self.txet[0][1].get(),'',0
        if not self.txvars[0].get():
            tx=self.txet[0][0].get()
            if not tx: self.io.mb('w','o','提示','请检查输入的内容'); return
        if self.txvars[1].get():
            new=self.txet[1][1].get()
            if not new: return
        funknd=int(self.txfun.get()[0])-1
        if funknd==1:
            num=self.io.wminp('输入字符密度',int)
            if num is None: return
        self.io.thr(self.txpre,tx,new,num,funknd)()
    def txmng(self)->None:
        '''construct window'''
        relnm='文本处理'
        if self.io.note.opened(relnm): return
        tx,txemp=self.io.notemp(7); self.io.note.add(tx,relnm,1,self)
        self.txet=[[ttk.Entry]*2,[ttk.Entry]*2]
        self.txvars=[tkinter.IntVar(value=0) for i in range(2)]
        self.txfun=tkinter.StringVar(); txbtx=['生成','退出']
        txtx=['打开方式','文本输入','文件打开','保存方式','文本输出','文件保存']
        txfun=['1.编unicode','2.生成组合字符','3.解unicode','4.文本加解密']
        txcmd=[self.txinp,self.io.notqut]
        for i in range(2):
            txlb=ttk.Label(txemp[3*i],text=txtx[3*i])
            txlb.pack(side='left',padx=self.io.scfac/3)
            for j in range(2):
                mngrd=lambda knd=i,idx=j: self.txrdc(knd,idx)
                txbtn=ttk.Radiobutton(txemp[3*i+j+1],text=txtx[3*i+j+1])
                txbtn.config(variable=self.txvars[i],value=j,command=mngrd)
                txbtn.pack(side='left',padx=self.io.scfac/3)
                self.txet[i][j]=ttk.Entry(txemp[3*i+j+1],width=50)
                if j: btx='浏览'; cmd=lambda knd=i,idx=j: self.txcmd(knd,idx)
                else: btx='全选'; cmd=lambda tag=self.txet[i][j]: tag.selection_range(0,'end')
                txbtn=ttk.Button(txemp[3*i+j+1],text=btx,command=cmd)
                txbtn.pack(side='right',padx=self.io.scfac/3)
                self.txet[i][j].pack(side='right',padx=self.io.scfac/3)
            self.txet[i][1].config(state='disabled')
        txopt=ttk.OptionMenu(txemp[6],self.txfun,txfun[0],*txfun)
        txopt['menu'].configure(bg=self.io.bg,fg=self.io.fg)
        self.bgf+=[lambda: txopt['menu'].configure(bg=self.io.bg,fg=self.io.fg)]
        for i in range(1,-1,-1):
            txbtn=ttk.Button(txemp[6],text=txbtx[i],command=txcmd[i])
            txbtn.pack(side='right',padx=self.io.scfac/3)
        txopt.pack(side='right',padx=self.io.scfac/3)
        for i in range(6): txemp[i].pack(fill='x',pady=self.io.scfac/3)
        txemp[6].pack(fill='x',side='bottom',pady=self.io.scfac/3)
    def txpre(self,tx:str,new:str,num:int,funknd:int)->None:
        '''set open and close format for text manager'''
        funs=[self.encucd,lambda tx: self.rndchr(tx,num),self.ucd,self.txcpt]
        if self.txvars[0].get():
            try: fl=open(tx,'rb')
            except: return
            datas=fl.read(); fl.close(); tx=self.io.decode(datas)
        else: enc='utf-8'
        res=funs[funknd](tx)
        if self.txvars[1].get():
            if not os.path.splitext(new)[1]: new+='.txt'
            fl=open(new,'w',encoding=enc); fl.write(res); fl.close()
        else:
            self.txet[1][0].delete(0,'end'); self.txet[1][0].insert('end',res)
        self.io.thrshw('red','进程已结束')
        self.io.thrshw('purple','>>>')
    def txrdc(self,idx:int,knd:int)->None:
        '''command for text manager radiobutton'''
        self.txet[idx][knd].config(state='normal')
        self.txet[idx][1-knd].config(state='disabled')
    def ucd(self,tx:str)->str:
        '''decode unicode for text manager'''
        ltx=len(tx); lres,res,i=0,['']*ltx,0
        while i<ltx:
            if ltx-i>5 and tx[i:i+2]=='\\u': res[lres]=chr(int(tx[i+2:i+6],16)); i+=6
            else: res[lres]=tx[i]; i+=1
            lres+=1
        return ''.join(res)
class Update:
    '''check update for app'''
    def __init__(self,io:Fabits)->None: self.io=io
    def update(self)->None:
        '''thread check'''
        self.io.thr(self.updchk())
    def updchk(self)->None:
        '''send request'''
        try:
            resp=urlopen(self.io.data['latest'],timeout=30)
            latvsn=json.loads(self.io.decode(resp.read()))['tag_name']
            if latvsn==self.io.data['curvsn']:
                self.io.mb('i','o','提示','当前已经是最新版本')
            elif self.io.mb('i','yn','提示','有新版本!是否前往项目仓库下载?')=='yes':
                webbrowser.open(self.io.data['proj']+'/releases/latest')
        except:
            if self.io.mb('w','yn','无法连接服务器','是否重试?')=='yes': self.update()
if __name__=='__main__':
    multiprocessing.freeze_support()
    Api.dpi(); Fabits().run()