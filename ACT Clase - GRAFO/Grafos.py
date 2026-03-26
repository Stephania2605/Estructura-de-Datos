"""
TDA Grafo — Diseño CYBER/NEON
Estética: terminal retro-futurista, verde neón sobre negro profundo
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import math, random, time


BG        = "#050a05"
BG2       = "#080f08"
PANEL     = "#0b160b"
BORDER    = "#1a3d1a"
NEON      = "#00ff41"       # verde matrix
NEON_DIM  = "#00882a"
NEON2     = "#ff00ff"       # magenta
NEON3     = "#00e5ff"       # cyan
WARN      = "#ffcc00"
ERR       = "#ff3333"
TXT       = "#c8ffc8"
TXT_DIM   = "#3a6b3a"
EDGE_COL  = "#ff00ff"
VERT_FILL = "#050a05"
SEL       = "#ffcc00"

FONT_TITLE = ("Courier New", 13, "bold")
FONT_MONO  = ("Courier New", 9)
FONT_MONO_B= ("Courier New", 9, "bold")
FONT_SMALL = ("Courier New", 8)
FONT_BIG   = ("Courier New", 15, "bold")


class Vertice:
    def __init__(self, idx, info):
        self.idx = idx; self.info = info

class Arista:
    def __init__(self, idx, u, v, info=None):
        self.idx = idx; self.u = u; self.v = v; self.info = info

class Grafo:
    def __init__(self):
        self._V: dict[int, Vertice] = {}
        self._E: dict[int, Arista]  = {}
        self._vid = 0; self._eid = 0

    def numVertices(self):      return len(self._V)
    def numAristas(self):       return len(self._E)
    def vertices(self):         return list(self._V)
    def aristas(self):          return list(self._E)
    def grado(self, v):         return sum(1 for e in self._E.values() if e.u==v or e.v==v)
    def verticesAdyacentes(self,v): return [e.v if e.u==v else e.u for e in self._E.values() if e.u==v or e.v==v]
    def aristasIncidentes(self,v):  return [e.idx for e in self._E.values() if e.u==v or e.v==v]
    def verticesFinales(self,e):
        a=self._E.get(e); return [a.u,a.v] if a else None
    def opuesto(self,v,e):
        a=self._E.get(e)
        if not a: return None
        return a.v if a.u==v else (a.u if a.v==v else None)
    def esAdyacente(self,v,w):  return any((e.u==v and e.v==w)or(e.u==w and e.v==v) for e in self._E.values())
    def tamano(self):           return self.numVertices()+self.numAristas()
    def estaVacio(self):        return not self._V
    def elementos(self):        return [v.info for v in self._V.values()]+[a.info for a in self._E.values()]
    def posiciones(self):       return list(self._V)+list(self._E)
    def reemplazar(self,p,r,es_v=True):
        obj=(self._V if es_v else self._E).get(p)
        if obj: obj.info=r; return True
        return False
    def intercambiar(self,p,q,es_v=True):
        d=self._V if es_v else self._E
        a,b=d.get(p),d.get(q)
        if a and b: a.info,b.info=b.info,a.info; return True
        return False
    def agregarVertice(self,info):
        self._vid+=1; self._V[self._vid]=Vertice(self._vid,info); return self._vid
    def agregarArista(self,u,v,info=None):
        self._eid+=1; self._E[self._eid]=Arista(self._eid,u,v,info); return self._eid
    def eliminarVertice(self,v):
        if v not in self._V: return False
        for eid in self.aristasIncidentes(v): self._E.pop(eid,None)
        del self._V[v]; return True
    def eliminarArista(self,e):
        if e not in self._E: return False
        del self._E[e]; return True
    def getV(self,v): return self._V.get(v)
    def getE(self,e): return self._E.get(e)



class App(tk.Tk):
    R = 24

    def __init__(self):
        super().__init__()
        self.title("TDA::GRAFO")
        self.configure(bg=BG)
        self.minsize(1150, 720)
        try: self.state("zoomed")
        except: self.attributes("-zoomed", True)

        self.grafo   = Grafo()
        self._pos    = {}
        self._drag   = {}
        self._hl_v   = []
        self._hl_e   = []
        self._log    = []

        self._build()
        self._demo()

    
    def _build(self):
        
        bar = tk.Frame(self, bg=BG, bd=0)
        bar.pack(fill="x")
        tk.Frame(bar, bg=NEON, height=2).pack(fill="x")
        inner = tk.Frame(bar, bg=BG)
        inner.pack(fill="x", padx=16, pady=6)

        tk.Label(inner, text="▓▓ TDA::GRAFO", font=("Courier New",16,"bold"),
                 fg=NEON, bg=BG).pack(side="left")
        tk.Label(inner, text=" // VISUALIZADOR DE TIPO DE DATO ABSTRACTO",
                 font=FONT_MONO, fg=NEON_DIM, bg=BG).pack(side="left", pady=2)

        self._clock_lbl = tk.Label(inner, text="", font=FONT_MONO, fg=TXT_DIM, bg=BG)
        self._clock_lbl.pack(side="right")
        self._tick_clock()

        tk.Frame(bar, bg=BORDER, height=1).pack(fill="x")

       
        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True)

       
        self._sidebar = tk.Frame(main, bg=PANEL, width=230)
        self._sidebar.pack(side="left", fill="y")
        self._sidebar.pack_propagate(False)
        self._build_sidebar()

       
        center = tk.Frame(main, bg=BG)
        center.pack(side="left", fill="both", expand=True)

        self.canvas = tk.Canvas(center, bg=BG2, highlightthickness=0, cursor="crosshair")
        self.canvas.pack(fill="both", expand=True, padx=6, pady=6)
        self.canvas.bind("<Button-1>",        self._c_click)
        self.canvas.bind("<B1-Motion>",       self._c_drag)
        self.canvas.bind("<ButtonRelease-1>", self._c_release)
        self.canvas.bind("<Configure>",       lambda e: self._redraw())

        
        log_frame = tk.Frame(center, bg=PANEL, height=120)
        log_frame.pack(fill="x", padx=6, pady=(0,6))
        log_frame.pack_propagate(False)
        tk.Frame(log_frame, bg=NEON, height=1).pack(fill="x")
        hdr = tk.Frame(log_frame, bg=PANEL)
        hdr.pack(fill="x", padx=8, pady=2)
        tk.Label(hdr, text="◉ LOG", font=FONT_MONO_B, fg=NEON, bg=PANEL).pack(side="left")
        tk.Label(hdr, text="(últimas operaciones)", font=FONT_SMALL, fg=TXT_DIM, bg=PANEL).pack(side="left", padx=6)
        self._log_txt = tk.Text(log_frame, bg=PANEL, fg=TXT_DIM, font=FONT_SMALL,
                                relief="flat", state="disabled", height=5,
                                insertbackground=NEON, bd=0)
        self._log_txt.pack(fill="both", expand=True, padx=8, pady=(0,4))

     
        right = tk.Frame(main, bg=PANEL, width=270)
        right.pack(side="right", fill="y")
        right.pack_propagate(False)
        self._build_right(right)
    def _build_sidebar(self):
        s = self._sidebar
        tk.Frame(s, bg=BORDER, height=1).pack(fill="x")

        self._section_lbl = {}

        def section(title):
            f = tk.Frame(s, bg=PANEL)
            f.pack(fill="x", pady=(8,0))
            tk.Label(f, text=title, font=("Courier New",8,"bold"),
                     fg=NEON_DIM, bg=PANEL).pack(anchor="w", padx=10, pady=(4,2))
            tk.Frame(f, bg=BORDER, height=1).pack(fill="x", padx=6)
            return f

        def btn(parent, label, cmd, color=NEON):
            b = tk.Button(parent, text=label, command=cmd,
                          font=("Courier New",8,"bold"), fg=BG, bg=color,
                          activebackground=TXT, activeforeground=BG,
                          relief="flat", bd=0, pady=4, padx=6,
                          cursor="hand2", anchor="w")
            b.pack(fill="x", padx=8, pady=1)
           
            b.bind("<Enter>", lambda e,b=b,c=color: b.config(bg=TXT))
            b.bind("<Leave>", lambda e,b=b,c=color: b.config(bg=c))
            return b

        p = section("// MUTADORES")
        btn(p, "[+] Agregar Vértice",  self._agregar_v,  NEON)
        btn(p, "[+] Agregar Arista",   self._agregar_e,  NEON)
        btn(p, "[-] Eliminar Vértice", self._eliminar_v, NEON2)
        btn(p, "[-] Eliminar Arista",  self._eliminar_e, NEON2)

        p2 = section("// OPERACIONES GENERALES")
        ops = [
            ("numVertices()",         self._numV),
            ("numAristas()",          self._numE),
            ("vertices()",            self._vs),
            ("aristas()",             self._es),
            ("grado(v)",              self._grado),
            ("verticesAdyacentes(v)", self._vadj),
            ("aristasIncidentes(v)",  self._einc),
            ("verticesFinales(e)",    self._vfin),
            ("opuesto(v, e)",         self._opuesto),
            ("esAdyacente(v, w)",     self._esadj),
        ]
        for lbl, cmd in ops:
            btn(p2, lbl, cmd, NEON3)

        p3 = section("// OPERACIONES POSICIONALES")
        pos_ops = [
            ("tamano()",          self._tamano),
            ("estaVacio()",       self._vacio),
            ("elementos()",       self._elems),
            ("posiciones()",      self._poss),
            ("reemplazar(p,r)",   self._reemplazar),
            ("intercambiar(p,q)", self._intercambiar),
        ]
        for lbl, cmd in pos_ops:
            btn(p3, lbl, cmd, WARN)

        p4 = section("// UTILIDADES")
        btn(p4, "[RND] Grafo Aleatorio", self._random, NEON)
        btn(p4, "[CLR] Limpiar Todo",    self._clear,  ERR)

    def _build_right(self, r):
        tk.Frame(r, bg=BORDER, height=1).pack(fill="x")
        tk.Label(r, text="◈ OUTPUT", font=FONT_TITLE, fg=NEON2, bg=PANEL).pack(anchor="w", padx=12, pady=8)

        self._out = tk.Text(r, bg=BG, fg=NEON, font=("Courier New",10),
                            relief="flat", state="disabled", wrap="word",
                            insertbackground=NEON, bd=0, selectbackground=NEON_DIM)
        self._out.pack(fill="both", expand=True, padx=8)

        tk.Frame(r, bg=BORDER, height=1).pack(fill="x", pady=6)
        tk.Label(r, text="◈ ESTADO DEL GRAFO", font=FONT_MONO_B, fg=NEON2, bg=PANEL).pack(anchor="w", padx=12)

        self._state = tk.Text(r, bg=BG, fg=TXT, font=FONT_SMALL,
                              relief="flat", state="disabled", wrap="word",
                              height=14, insertbackground=NEON, bd=0)
        self._state.pack(fill="x", padx=8, pady=(4,8))


    def _show(self, fn, result):
        ts = time.strftime("%H:%M:%S")
        self._out.config(state="normal")
        self._out.delete("1.0","end")
        self._out.insert("end", f"┌─ {fn}\n", "fn")
        self._out.insert("end", f"│\n")
        lines = str(result).split("\n")
        for l in lines:
            self._out.insert("end", f"│  {l}\n")
        self._out.insert("end", f"└─ [{ts}]\n")
        self._out.tag_config("fn", foreground=NEON2, font=("Courier New",10,"bold"))
        self._out.config(state="disabled")

        self._log.append(f"[{ts}] {fn}")
        self._log = self._log[-40:]
        self._log_txt.config(state="normal")
        self._log_txt.delete("1.0","end")
        for entry in reversed(self._log[-5:]):
            self._log_txt.insert("end", entry+"\n")
        self._log_txt.config(state="disabled")

        self._update_state()

    def _update_state(self):
        g = self.grafo
        lines = [
            f"VÉRTICES  : {g.numVertices()}",
            f"ARISTAS   : {g.numAristas()}",
            f"TAMAÑO    : {g.tamano()}",
            f"VACÍO     : {'SÍ' if g.estaVacio() else 'NO'}",
            "─"*28,
        ]
        for vid in g.vertices():
            v = g.getV(vid)
            lines.append(f" v{vid:<3} '{v.info}'  g={g.grado(vid)}")
        lines.append("─"*28)
        for eid in g.aristas():
            a = g.getE(eid)
            lines.append(f" e{eid:<3} v{a.u}─v{a.v}  [{a.info}]")
        self._state.config(state="normal")
        self._state.delete("1.0","end")
        self._state.insert("end", "\n".join(lines))
        self._state.config(state="disabled")

    def _ask(self, p, d=""):
        return simpledialog.askstring("INPUT", p, initialvalue=d, parent=self)
    def _askint(self, p):
        return simpledialog.askinteger("INPUT", p, parent=self)

    def _agregar_v(self):
        info = self._ask("Nombre del vértice:","V")
        if info is None: return
        vid = self.grafo.agregarVertice(info)
        w,h = max(self.canvas.winfo_width(),600), max(self.canvas.winfo_height(),400)
        self._pos[vid] = (random.randint(70,w-70), random.randint(70,h-70))
        self._show("agregarVertice()", f"v{vid} = '{info}' ✓")
        self._redraw()

    def _agregar_e(self):
        if self.grafo.numVertices()<2:
            messagebox.showinfo("","Necesitas ≥2 vértices."); return
        u = self._askint(f"Índice u {self.grafo.vertices()}:")
        if u is None: return
        v = self._askint(f"Índice v {self.grafo.vertices()}:")
        if v is None: return
        if u not in self.grafo.vertices() or v not in self.grafo.vertices():
            messagebox.showerror("Error","Vértices inválidos."); return
        info = self._ask("Peso/info:","1")
        eid = self.grafo.agregarArista(u,v,info)
        self._show("agregarArista()", f"e{eid}: v{u}─v{v}  [{info}] ✓")
        self._redraw()

    def _eliminar_v(self):
        v = self._askint(f"Índice vértice {self.grafo.vertices()}:")
        if v is None: return
        ok = self.grafo.eliminarVertice(v); self._pos.pop(v,None)
        self._show("eliminarVertice()", f"v{v} {'eliminado ✓' if ok else 'no encontrado ✗'}")
        self._redraw()

    def _eliminar_e(self):
        e = self._askint(f"Índice arista {self.grafo.aristas()}:")
        if e is None: return
        ok = self.grafo.eliminarArista(e)
        self._show("eliminarArista()", f"e{e} {'eliminada ✓' if ok else 'no encontrada ✗'}")
        self._redraw()

    def _numV(self): self._show("numVertices()", self.grafo.numVertices())
    def _numE(self): self._show("numAristas()",  self.grafo.numAristas())

    def _vs(self):
        vs = self.grafo.vertices()
        detail = "\n".join(f"  v{i}: '{self.grafo.getV(i).info}'" for i in vs)
        self._show("vertices()", f"{vs}\n{detail}")

    def _es(self):
        es = self.grafo.aristas()
        detail = "\n".join(f"  e{i}: v{self.grafo.getE(i).u}─v{self.grafo.getE(i).v} [{self.grafo.getE(i).info}]" for i in es)
        self._show("aristas()", f"{es}\n{detail}")

    def _grado(self):
        v = self._askint(f"Vértice {self.grafo.vertices()}:")
        if v is None: return
        self._show("grado(v)", f"grado(v{v}) = {self.grafo.grado(v)}")
        self._hl_v=[v]; self._redraw()

    def _vadj(self):
        v = self._askint(f"Vértice {self.grafo.vertices()}:")
        if v is None: return
        adj = self.grafo.verticesAdyacentes(v)
        detail = "\n".join(f"  v{w}: '{self.grafo.getV(w).info}'" for w in adj)
        self._show("verticesAdyacentes(v)", f"adj(v{v}) = {adj}\n{detail}")
        self._hl_v=adj; self._redraw()

    def _einc(self):
        v = self._askint(f"Vértice {self.grafo.vertices()}:")
        if v is None: return
        inc = self.grafo.aristasIncidentes(v)
        self._show("aristasIncidentes(v)", f"inc(v{v}) = {inc}")
        self._hl_e=inc; self._redraw()

    def _vfin(self):
        e = self._askint(f"Arista {self.grafo.aristas()}:")
        if e is None: return
        vf = self.grafo.verticesFinales(e)
        self._show("verticesFinales(e)", f"vf(e{e}) = {vf}")
        if vf: self._hl_v=vf; self._redraw()

    def _opuesto(self):
        v = self._askint(f"Vértice {self.grafo.vertices()}:")
        if v is None: return
        e = self._askint(f"Arista {self.grafo.aristas()}:")
        if e is None: return
        op = self.grafo.opuesto(v,e)
        self._show("opuesto(v,e)", f"opuesto(v{v},e{e}) = {'v'+str(op) if op is not None else 'None'}")
        if op is not None: self._hl_v=[op]; self._redraw()

    def _esadj(self):
        v = self._askint(f"Vértice v {self.grafo.vertices()}:")
        if v is None: return
        w = self._askint(f"Vértice w {self.grafo.vertices()}:")
        if w is None: return
        r = self.grafo.esAdyacente(v,w)
        self._show("esAdyacente(v,w)", f"esAdyacente(v{v},v{w}) = {r}")

    def _tamano(self):   self._show("tamano()",   self.grafo.tamano())
    def _vacio(self):    self._show("estaVacio()", self.grafo.estaVacio())
    def _elems(self):    self._show("elementos()", "\n".join(f"  {i}: {e}" for i,e in enumerate(self.grafo.elementos())))
    def _poss(self):     self._show("posiciones()", self.grafo.posiciones())

    def _reemplazar(self):
        t = messagebox.askquestion("Tipo","¿Vértice? (No=Arista)")
        ev = t=="yes"
        col = self.grafo.vertices() if ev else self.grafo.aristas()
        p = self._askint(f"Índice p {col}:")
        if p is None: return
        r = self._ask("Nuevo valor r:")
        if r is None: return
        ok = self.grafo.reemplazar(p,r,es_v=ev)
        self._show("reemplazar(p,r)", "✓ OK" if ok else "✗ No encontrado")
        self._redraw()

    def _intercambiar(self):
        t = messagebox.askquestion("Tipo","¿Vértices? (No=Aristas)")
        ev = t=="yes"
        col = self.grafo.vertices() if ev else self.grafo.aristas()
        p = self._askint(f"Índice p {col}:")
        if p is None: return
        q = self._askint(f"Índice q {col}:")
        if q is None: return
        ok = self.grafo.intercambiar(p,q,es_v=ev)
        self._show("intercambiar(p,q)", "✓ OK" if ok else "✗ No encontrado")
        self._redraw()

    def _random(self):
        n = self._askint("¿Cuántos vértices? (2-12):") or 7
        n = max(2,min(12,n))
        self.grafo=Grafo(); self._pos.clear()
        names=list("ABCDEFGHIJKL")
        for i in range(n): self.grafo.agregarVertice(names[i])
        self.update_idletasks()
        w,h=max(self.canvas.winfo_width(),700),max(self.canvas.winfo_height(),450)
        cx,cy,r=w/2,h/2,min(w,h)*0.34
        for i,vid in enumerate(self.grafo.vertices()):
            ang=2*math.pi*i/n - math.pi/2
            self._pos[vid]=(cx+r*math.cos(ang),cy+r*math.sin(ang))
        vids=self.grafo.vertices()
        for i in range(n-1): self.grafo.agregarArista(vids[i],vids[i+1],random.randint(1,9))
        for _ in range(random.randint(1,n)):
            u,v=random.sample(vids,2)
            if not self.grafo.esAdyacente(u,v): self.grafo.agregarArista(u,v,random.randint(1,9))
        self._hl_v=[]; self._hl_e=[]
        self._show("random()",f"{n} vértices generados ✓")
        self._redraw()

    def _clear(self):
        self.grafo=Grafo(); self._pos.clear(); self._hl_v=[]; self._hl_e=[]
        self._show("clear()","Grafo limpiado ✓"); self._redraw()

    # ─── canvas ───────────────────────────────
    def _redraw(self):
        c=self.canvas; c.delete("all")
        self._draw_bg()
        for eid in self.grafo.aristas():
            a=self.grafo.getE(eid)
            pu,pv=self._pos.get(a.u),self._pos.get(a.v)
            if pu and pv:
                col = SEL if eid in self._hl_e else EDGE_COL
                self._draw_edge(pu,pv,a,col)
        for vid in self.grafo.vertices():
            p=self._pos.get(vid)
            if p:
                col = SEL if vid in self._hl_v else NEON
                self._draw_vertex(p,vid,self.grafo.getV(vid).info,col)

    def _draw_bg(self):
        c=self.canvas
        w,h=c.winfo_width(),c.winfo_height()
        # dot grid
        step=32
        for x in range(0,w,step):
            for y in range(0,h,step):
                c.create_oval(x-1,y-1,x+1,y+1,fill="#0d200d",outline="")
        # corner label
        c.create_text(w-8,h-8,text=f"V={self.grafo.numVertices()} E={self.grafo.numAristas()}",
                      anchor="se",fill=TXT_DIM,font=FONT_SMALL)

    def _draw_edge(self,pu,pv,a,col):
        c=self.canvas
        x1,y1=pu; x2,y2=pv
        # glow (múltiples líneas anchas→estrechas)
        for w,alpha in [(7,"#1a001a"),(4,"#3d003d"),(2,col)]:
            c.create_line(x1,y1,x2,y2,fill=alpha,width=w,capstyle="round")
        # peso
        mx,my=(x1+x2)/2,(y1+y2)/2
        c.create_rectangle(mx-12,my-8,mx+12,my+8,fill=BG2,outline=col,width=1)
        c.create_text(mx,my,text=str(a.info),fill=col,font=("Courier New",8,"bold"))
        # label arista
        dx,dy=y2-y1,x1-x2
        d=math.hypot(dx,dy) or 1
        off=14
        c.create_text(mx+dx/d*off,my+dy/d*off,text=f"e{a.idx}",fill=TXT_DIM,font=("Courier New",7))

    def _draw_vertex(self,pos,vid,info,col):
        c=self.canvas; x,y=pos; R=self.R
        # outer glow rings
        for r,clr in [(R+10,"#001500"),(R+6,"#003300"),(R+3,NEON_DIM)]:
            c.create_oval(x-r,y-r,x+r,y+r,fill="",outline=clr,width=1)
        # fill circle
        c.create_oval(x-R,y-R,x+R,y+R,fill=BG,outline=col,width=2,tags=(f"v{vid}",))
        # label
        s=info[:3] if len(info)>3 else info
        c.create_text(x,y,text=s,fill=col,font=("Courier New",9,"bold"),tags=(f"v{vid}",))
        # index below
        c.create_text(x,y+R+9,text=f"v{vid}",fill=TXT_DIM,font=("Courier New",7))

    # ─── drag ─────────────────────────────────
    def _c_click(self,e):
        vid=self._find_v(e.x,e.y)
        if vid: self._drag={"vid":vid}
        else: self._drag={}

    def _c_drag(self,e):
        if "vid" in self._drag:
            self._pos[self._drag["vid"]]=(e.x,e.y)
            self._redraw()

    def _c_release(self,e): self._drag={}

    def _find_v(self,x,y):
        for vid,(vx,vy) in self._pos.items():
            if math.hypot(x-vx,y-vy)<=self.R+4: return vid
        return None

    # ─── clock ────────────────────────────────
    def _tick_clock(self):
        self._clock_lbl.config(text=time.strftime("SYS::%H:%M:%S"))
        self.after(1000,self._tick_clock)

    # ─── demo ─────────────────────────────────
    def _demo(self):
        self.update_idletasks()
        w=max(self.canvas.winfo_width(),700)
        h=max(self.canvas.winfo_height(),450)
        for n in ["NEO","MOR","TRI","AGT","ORK"]:
            self.grafo.agregarVertice(n)
        vids=self.grafo.vertices()
        cx,cy,r=w/2,h/2,min(w,h)*0.28
        for i,vid in enumerate(vids):
            ang=2*math.pi*i/len(vids)-math.pi/2
            self._pos[vid]=(cx+r*math.cos(ang),cy+r*math.sin(ang))
        for u,v,w_ in [(1,2,9),(2,3,3),(3,4,7),(4,5,1),(5,1,5),(1,3,4)]:
            self.grafo.agregarArista(u,v,w_)
        self._show("INIT","Sistema iniciado.\nGrafo de ejemplo cargado.\nUsa los botones del panel\npara ejecutar operaciones.")
        self._redraw()


if __name__=="__main__":
    App().mainloop()