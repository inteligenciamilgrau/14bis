import sys; sys.path.insert(0,__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from lib2 import *
import rh, time
t0=time.time()
bpy.ops.wm.open_mainfile(filepath=S+'stage1.blend')
body=bpy.data.objects['body']
JJ=json.load(open(S+'joints1.json'))['joints']
B0=Body(body,JJ); bi=B0.bi; J=B0.J
# ---- proxy do corpo com tronco 'estruturado' (sem peitorais/abdômen/escápulas) ----
PV=B0.V.copy(); TW=B0.W[:,[bi['spine'],bi['chest'],bi['hips']]].sum(1)
tor=TW>0.6
for z in np.arange(0.80,1.27,0.004):
    m=tor&(np.abs(PV[:,2]-z)<0.0022)
    if m.sum()<8: continue
    H=hull2d(B0.V[tor&(np.abs(B0.V[:,2]-z)<0.004)][:,:2]); c=np.array([(H[:,0].max()+H[:,0].min())/2,(H[:,1].max()+H[:,1].min())/2])
    for i in np.where(m)[0]:
        w=float(ss(0.80,0.85,z)*((1-ss(1.16,1.25,z)) if PV[i,1]<0.0 else (1-ss(1.22,1.28,z))))
        d=PV[i,:2]-c; rv=np.linalg.norm(d)
        if rv<1e-6: continue
        a=math.atan2(d[0],-d[1]); rh_=poly_radius(H,c,a)
        PV[i,:2]=c+d/rv*(rv+(max(rh_,rv)-rv)*w*min(1,(TW[i]-0.6)/0.3))
Ed=np.array([e.vertices[:] for e in body.data.edges]); deg=np.bincount(Ed.ravel(),minlength=len(PV)).astype(float)
sm=tor&(PV[:,2]>0.80)&(PV[:,2]<1.24+0.04*(PV[:,1]>0))
for it in range(25):
    Sm=np.zeros_like(PV); np.add.at(Sm,Ed[:,0],PV[Ed[:,1]]); np.add.at(Sm,Ed[:,1],PV[Ed[:,0]])
    PV[sm]+=0.5*(Sm[sm]/deg[sm][:,None]-PV[sm])
# costas do paletó caem retas das escápulas ao quadril: preenche a lombar (envoltória traseira em cada coluna x)
AW=B0.W[:,[bi[n] for n in B0.bones if n.startswith(('upperarm','forearm','hand','thumb','index','middle','ring','pinky'))]].sum(1)
bk=(AW<0.3)&(PV[:,1]>0.0)&(PV[:,2]>0.66)&(PV[:,2]<1.24)&(np.abs(PV[:,0])<0.17)
_fill=[]
for xb in np.arange(-0.16,0.16,0.01):
    m=bk&(np.abs(PV[:,0]-xb-0.005)<0.0075)
    if m.sum()<6: continue
    H=hull2d(PV[m][:,[2,1]]); H=H[np.argsort(H[:,0])]
    zs_=np.linspace(PV[m][:,2].min(),PV[m][:,2].max(),60)
    top=[]
    for zq in zs_:   # borda de trás (y máximo) da envoltória convexa em (z,y)
        ys=[]
        for i in range(len(H)):
            a_=H[i]; b_=H[(i+1)%len(H)]
            if (a_[0]-zq)*(b_[0]-zq)<=0 and a_[0]!=b_[0]: ys.append(a_[1]+(b_[1]-a_[1])*(zq-a_[0])/(b_[0]-a_[0]))
        top.append(max(ys) if ys else -1)
    top=np.array(top)
    for i in np.where(m)[0]:
        yh=np.interp(PV[i,2],zs_,top); w=float(ss(0.68,0.74,PV[i,2])*(1-ss(1.16,1.24,PV[i,2])))
        if yh>PV[i,1]: _fill.append((yh-PV[i,1])*w); PV[i,1]+=(yh-PV[i,1])*w
bsm=bk|((AW<0.3)&(PV[:,2]>0.64)&(PV[:,2]<1.26)&(np.abs(PV[:,0])<0.17)&(PV[:,1]>-0.02))
for it in range(30):   # alisa o tronco depois do preenchimento (sem estrias)
    Sm=np.zeros_like(PV); np.add.at(Sm,Ed[:,0],PV[Ed[:,1]]); np.add.at(Sm,Ed[:,1],PV[Ed[:,0]])
    PV[bsm]+=0.5*(Sm[bsm]/deg[bsm][:,None]-PV[bsm])
print('lombar: max preenchimento %.3f m em %d verts'%(max(_fill) if _fill else 0,len(_fill)))
proxy=body.copy(); proxy.data=body.data.copy(); bpy.context.scene.collection.objects.link(proxy); proxy.name='proxy'
set_verts(proxy,PV); proxy.hide_render=True
B=Body(proxy,JJ)
def bid(n): return bi[n]
fd=B.fdom; fc=B.fc; V=B.V
Z_W=0.905; Z_HEM=0.645; Z_V0=1.075
torso={bid('spine'),bid('chest'),bid('hips')}
def is_arm(i):
    n=B.bones[i]; return n.startswith('upperarm') or n.startswith('forearm')
def cut(bm,co,no,filt=lambda c:True):
    co=Vector(co); no=Vector(no).normalized()
    bmesh.ops.bisect_plane(bm,geom=bm.verts[:]+bm.edges[:]+bm.faces[:],dist=1e-6,plane_co=co,plane_no=no)
    bm.faces.ensure_lookup_table()
    dl=[f for f in bm.faces if (f.calc_center_median()-co).dot(no)>0 and filt(f.calc_center_median())]
    bmesh.ops.delete(bm,geom=dl,context='FACES')
    bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table()
# ---------- PALETÓ (parte de cima): fatias horizontais em volta do tronco (envoltória convexa, SEM os braços) ----------
# o braço nunca entra na casca do tronco: embaixo do braço fica o lado do paletó, e a manga é peça própria
PV2=B.V;selJ=np.isin(B.dom,[bid('hips'),bid('spine'),bid('chest'),bid('neck')])|(
     np.isin(B.dom,[bid('upperarm.L'),bid('upperarm.R')])&(PV2[:,2]>1.1)&(np.abs(PV2[:,0])<0.125))      # topo do ombro até a articulação
NSJ=64;angJ=np.linspace(0,2*math.pi,NSJ,endpoint=False);zsJ=np.linspace(Z_W-0.04,1.30,46);RJ=[];CJ=[]
for z in zsJ:
    m=selJ&(np.abs(PV2[:,2]-z)<0.008);H=hull2d(PV2[m][:,:2]);c=np.array([0.0,(H[:,1].max()+H[:,1].min())/2])
    RJ.append([poly_radius(H,c,a) for a in angJ]);CJ.append(c)
RJ=np.array(RJ);CJ=np.array(CJ)
for it in range(2):RJ=(np.roll(RJ,1,1)+RJ*2+np.roll(RJ,-1,1))/4
RJ=np.array([RJ[max(0,i-3):i+4].mean(0) for i in range(len(RJ))]);CJ=np.array([CJ[max(0,i-2):i+3].mean(0) for i in range(len(CJ))])
front=np.maximum(0,np.cos(angJ))
rings=[]
for i,z in enumerate(zsJ):
    r=RJ[i]+0.0135+0.004*math.exp(-((z-1.12)/0.09)**2)*front
    rings.append(np.stack([CJ[i][0]+np.sin(angJ)*r,CJ[i][1]-np.cos(angJ)*r,np.full(NSJ,z)],1))
VJ,FJ=loft(rings,True);ct=len(VJ);VJ=np.vstack([VJ,[[CJ[-1][0],CJ[-1][1],zsJ[-1]+0.01]]])
FJ+=[(ct,(len(zsJ)-1)*NSJ+(k+1)%NSJ,(len(zsJ)-1)*NSJ+k) for k in range(NSJ)]
bm=bmesh.new()
for v in VJ:bm.verts.new(tuple(v))
bm.verts.ensure_lookup_table()
for f in FJ:bm.faces.new([bm.verts[i] for i in f])
bmesh.ops.recalc_face_normals(bm,faces=bm.faces[:]);bm.normal_update()
# gola do paletó: elipse em volta do pescoço (mais alta atrás)
NY=-0.012
def neck_r(th,z):
    loc,nrm,fi,dist=B0.bvh.ray_cast(Vector((0,NY,z)),Vector((math.sin(th),-math.cos(th),0)),0.2)
    return dist if dist else 0.05
_thg=np.linspace(0,2*math.pi,91); _zz=np.array([1.245,1.26,1.275,1.29,1.30]); _A=np.vstack([_zz,np.ones_like(_zz)]).T
_Rf=[np.linalg.lstsq(_A,np.array([neck_r(th,z) for z in _zz]),rcond=None)[0] for th in _thg]
def rcol(th,z):
    i=int(round((th%(2*math.pi))/(2*math.pi)*90))%91; a,b=_Rf[i]; return a*z+b
def ztop(th):
    a=abs(math.atan2(math.sin(th),math.cos(th)))
    return 1.301+0.031*float(ss(0.3,1.3,a))-0.004*float(ss(1.8,3.0,a))
def zjack(th):
    a=abs(math.atan2(math.sin(th),math.cos(th))); return 1.250+0.050*float(ss(0.35,1.35,a))-0.010*float(ss(1.8,3.0,a))
def polar(c):
    th=math.atan2(c.x,-(c.y-NY)); r=math.hypot(c.x,c.y-NY); return th,r
dl=[]
for f in bm.faces:
    c=f.calc_center_median(); th,r=polar(c)
    if c.z>1.19 and r<0.105 and c.z>zjack(th): dl.append(f)
bmesh.ops.delete(bm,geom=dl,context='FACES')
bm.verts.ensure_lookup_table()
for v in bm.verts:
    if v.is_boundary and v.co.z>1.19:
        th,r=polar(v.co)
        if r<0.105 and v.co.z>zjack(th)-0.02:
            v.co.z=zjack(th); rc=neck_r(th,ztop(th)-0.004)+0.0155
            v.co.x=math.sin(th)*rc; v.co.y=NY-math.cos(th)*rc
# decote em V
def vhalf(z): return 0.004+(z-Z_V0)*(0.046/(1.265-Z_V0))
for sg in (1,-1):
    cut(bm,(sg*0.004,0,Z_V0),(sg*0.19,0,-0.046),lambda c:False)
dl=[f for f in bm.faces if (lambda c:c.z>Z_V0 and c.y<-0.01 and abs(c.x)<vhalf(c.z))(f.calc_center_median())]
bmesh.ops.delete(bm,geom=dl,context='FACES')
bm.verts.ensure_lookup_table()
# alisa bordas (neck) um pouco
bm.normal_update()
for v in bm.verts:
    c=v.co
    if c.z>Z_V0-0.01 and c.y<-0.01 and c.z<1.27:
        d=abs(c.x)-vhalf(c.z)
        lw=0.006+0.030*float(ss(Z_V0,Z_V0+0.12,c.z))
        lw*=1-0.75*math.exp(-((c.z-1.212)/0.007)**2)
        if -0.001<d<lw+0.002:
            pr=float(ss(-0.001,0.004,d))*(1-float(ss(lw-0.003,lw+0.001,d)))
            v.co+=v.normal*0.003*pr
jacket=to_obj('jacket',bm,'suit',(0.13,0.13,0.16,1))
jbvh=BVHTree.FromPolygons([tuple(v.co) for v in jacket.data.vertices],[tuple(p.vertices) for p in jacket.data.polygons])
print('jacket verts',len(bm.verts),time.time()-t0)
# ---------- MANGAS: tubo do ombro ao punho + bola de ombro (hemisfério) centrada na articulação ----------
def sleeve(s):
    A,E=(np.array(v) for v in J['upperarm.'+s]);E2,Wr=(np.array(v) for v in J['forearm.'+s])
    st=[A+(E-A)*t for t in np.linspace(0,1,10)]+[E+(Wr-E)*t for t in np.linspace(0.1,0.9,9)]
    st=np.array(st);T=np.gradient(st,axis=0);T/=np.linalg.norm(T,axis=1)[:,None]
    ref=np.array((0,1.0,0));U=[];Vv=[]
    for t in T:                                               # referenciais sem torção (transporte paralelo)
        u=ref-t*ref.dot(t);u/=np.linalg.norm(u);v=np.cross(t,u);U.append(u);Vv.append(v);ref=u
    NA=20;ang=np.linspace(0,2*math.pi,NA,endpoint=False);Rr=np.zeros((len(st),NA))
    for i,(c,u,v) in enumerate(zip(st,U,Vv)):
        for k,a in enumerate(ang):
            d=u*math.cos(a)+v*math.sin(a);loc,nrm,fi,dist=B0.bvh.ray_cast(Vector(c),Vector(d),0.12)
            Rr[i,k]=dist if dist else 0.035
    i3=3                                                      # perto do ombro o raio pega o tronco: usa o do 1/3 do braço
    for i in range(i3):Rr[i]=Rr[i3]
    Rr=np.minimum(Rr,np.median(Rr,axis=1,keepdims=True)*1.25)
    for it in range(2):Rr=(np.roll(Rr,1,1)+Rr*2+np.roll(Rr,-1,1))/4
    Rr=np.array([Rr[max(0,i-1):i+2].mean(0) for i in range(len(Rr))])
    off=np.array([0.0105]*10+[0.0092]*9)[:,None];Rr=Rr+off
    rb=float(Rr[0].max())
    rings=[]
    for ph in np.linspace(math.pi/2*0.97,0.12,6):             # hemisfério (do topo para a boca do tubo)
        rings.append(np.array([A-T[0]*rb*math.sin(ph)+(U[0]*math.cos(a)+Vv[0]*math.sin(a))*rb*math.cos(ph) for a in ang]))
    for i in range(len(st)):
        r_=np.maximum(Rr[i],rb*(1-float(ss(0,0.35,i/9))*0.35)) if i<4 else Rr[i]
        rings.append(np.array([st[i]+(U[i]*math.cos(a)+Vv[i]*math.sin(a))*r_[k] for k,a in enumerate(ang)]))
    Vs,Fs=loft(rings,True)
    top=np.array(A-T[0]*rb);Vs=np.vstack([Vs,top]);ti=len(Vs)-1
    Fs+=[(ti,(k+1)%NA,k) for k in range(NA)]
    o=to_obj('sleeve.'+s,(Vs,Fs),'suit')
    me=o.data;bm2=bmesh.new();bm2.from_mesh(me);bmesh.ops.recalc_face_normals(bm2,faces=bm2.faces[:]);bm2.to_mesh(me);bm2.free()
    return o
for s in ('L','R'):sleeve(s)
# ---------- SAIA DO PALETÓ ----------
NS=72
legtorso=[bid('hips'),bid('spine'),bid('thigh.L'),bid('thigh.R')]
def slice_hull(z,bones,side=0,h=0.006):
    m=(np.abs(V[:,2]-z)<h)&np.isin(B.dom,bones)
    if side>0: m&=V[:,0]>0.004
    if side<0: m&=V[:,0]<-0.004
    return hull2d(V[m][:,:2])
def gap(z): return 0.008+0.24*float(ss(0.86,Z_HEM,z))**1.3
zs=np.linspace(Z_HEM,Z_W+0.03,26); rings=[]
for z in zs:
    H=slice_hull(z,legtorso); c=np.array([0.0,(H[:,1].max()+H[:,1].min())/2])
    tt=(z-Z_HEM)/(Z_W+0.03-Z_HEM)
    infl=0.022*(1-float(ss(0.0,1.0,tt)))+0.0085*float(ss(0,1,tt))
    g=gap(z); angs=np.linspace(g,2*math.pi-g,NS)
    r=np.array([poly_radius(H,c,a) for a in angs])
    r=np.convolve(np.pad(r,3,mode='wrap'),np.ones(7)/7,mode='valid')+infl
    ZB=Z_W-0.04                       # borda de baixo da parte de cima do paletó
    if z>ZB-0.07:                     # a saia nasce da borda: casa o raio e entra por dentro acima dela
        for q,a in enumerate(angs):
            zq=max(z,ZB+0.004)
            loc,nrm,fi,dist=jbvh.ray_cast(Vector((c[0],c[1],zq)),Vector((math.sin(a),-math.cos(a),0)),0.4)
            if not dist: continue
            if z>ZB: r[q]=min(r[q],dist-0.0025)
            else:
                w_=float(ss(ZB-0.07,ZB,z)); r[q]=r[q]*(1-w_)+(dist-0.0012)*w_
    rings.append(np.stack([c[0]+np.sin(angs)*r,c[1]-np.cos(angs)*r,np.full(NS,z)],1))
RG=np.array(rings); CZ=RG.copy()
for i in range(len(RG)): CZ[i]=RG[max(0,i-2):i+3].mean(0)
CZ[:,:,2]=RG[:,:,2]; rings=list(CZ)
Vs,Fs=loft(rings,closed=False)
to_obj('skirt',(Vs,Fs),'suit')
# ---------- CALÇA: parte da bacia ----------
rings=[]
for z in np.linspace(0.69,Z_W+0.01,14):
    H=slice_hull(z,legtorso); c=np.array([0.0,(H[:,1].max()+H[:,1].min())/2])
    angs=np.linspace(0,2*math.pi,48,endpoint=False)
    r=np.array([poly_radius(H,c,a) for a in angs])+0.008
    rings.append(np.stack([c[0]+np.sin(angs)*r,c[1]-np.cos(angs)*r,np.full(48,z)],1))
Vp,Fp=loft(rings,closed=True); to_obj('trousers.P',(Vp,Fp),'suit')
# ---------- CALÇAS: pernas ----------
for s,sg in (('L',1),('R',-1)):
    NT=28; bl=[bid('thigh.'+s),bid('shin.'+s),bid('foot.'+s),bid('hips')]
    zs=np.arange(0.035,0.80,0.02); knee=J['shin.'+s][0].z
    Hs=[]; Cs=[]
    for z in zs:
        H=slice_hull(max(z,0.115),bl,sg); Hs.append(H)
        Cs.append([(H[:,0].max()+H[:,0].min())/2,(H[:,1].max()+H[:,1].min())/2])
    Cs=np.array(Cs); k=5
    Cs=np.array([Cs[max(0,i-k):i+k+1].mean(0) for i in range(len(Cs))])
    angs=np.linspace(0,2*math.pi,NT,endpoint=False)+math.pi*0.5*sg
    Rr=np.array([[poly_radius(H,c,a) for a in angs] for H,c in zip(Hs,Cs)])+0.011
    ik=int(np.argmin(np.abs(zs-knee)))
    for i in range(ik): Rr[i]=np.maximum(Rr[i],Rr[ik]*0.93)
    Rr=np.array([Rr[max(0,i-2):i+3].mean(0) for i in range(len(Rr))])
    Rh=np.array([[poly_radius(H,c,a) for a in angs] for H,c in zip(Hs,Cs)])+0.007
    Rr=np.maximum(Rr,Rh)
    for i,z in enumerate(zs):
        if z<0.07: Rr[i]+=0.0022
    rings=[np.stack([Cs[i,0]+np.sin(angs)*Rr[i],Cs[i,1]-np.cos(angs)*Rr[i],np.full(NT,z)],1) for i,z in enumerate(zs)]
    Vt,Ft=loft(rings,closed=True); to_obj('trousers.'+s,(Vt,Ft),'suit')
# ---------- BOTINAS (loft ao longo do pé: bico arredondado, sem dedos) ----------
for s,sg in (('L',1),('R',-1)):
    a_,t_=J['foot.'+s]; d=np.array([t_.x-a_.x,t_.y-a_.y]); d/=np.linalg.norm(d); w_=np.array([-d[1],d[0]])
    m=np.isin(B0.dom,[bid('foot.'+s)])|(np.isin(B0.dom,[bid('shin.'+s)])&(V[:,2]<0.135))
    Pf=V[m]; tt=Pf[:,:2]@d; ww=Pf[:,:2]@w_
    t0_,t1_=tt.min(),tt.max(); NSL=24; NA=22
    ts=np.linspace(t0_+0.002,t1_+0.006,NSL); rings=[]; cen=[]
    for k,tq in enumerate(ts):
        mm=np.abs(tt-min(tq,t1_-0.003))<0.007
        H=hull2d(np.stack([ww[mm],Pf[mm][:,2]],1)); c=np.array([(H[:,0].max()+H[:,0].min())/2,(H[:,1].max()+H[:,1].min())/2])
        angs=np.linspace(0,2*math.pi,NA,endpoint=False)
        r=np.array([poly_radius(H,c,a) for a in angs])+0.0045
        if tq>t1_-0.003: r*=max(0.25,1-(tq-(t1_-0.003))/0.012)
        rings.append((c,r)); cen.append(c)
    R=np.array([r for c,r in rings]); C=np.array(cen)
    R=np.array([R[max(0,i-1):i+2].mean(0) for i in range(len(R))]); C=np.array([C[max(0,i-1):i+2].mean(0) for i in range(len(C))])
    Vb=[]
    for k,tq in enumerate(ts):
        for q,a in enumerate(np.linspace(0,2*math.pi,NA,endpoint=False)):
            wv=C[k,0]+math.sin(a)*R[k,q]; zv=max(0.0,C[k,1]-math.cos(a)*R[k,q])
            xy=d*tq+w_*wv; Vb.append((xy[0],xy[1],zv))
    Vb=np.array(Vb); F=[]
    for k in range(NSL-1):
        for q in range(NA):
            q2=(q+1)%NA; F.append((k*NA+q,k*NA+q2,(k+1)*NA+q2,(k+1)*NA+q))
    Vb=np.vstack([Vb,[np.r_[d*ts[0]+w_*C[0,0],C[0,1]]],[np.r_[d*ts[-1]+w_*C[-1,0],C[-1,1]]]]); a0=len(Vb)-2; a1=len(Vb)-1
    for q in range(NA):
        q2=(q+1)%NA; F.append((a0,q2,q)); F.append((a1,(NSL-1)*NA+q,(NSL-1)*NA+q2))
    o=to_obj('boot.'+s,(Vb,F),'leather',(0.03,0.03,0.03,1))
    me=o.data; bm=bmesh.new(); bm.from_mesh(me); bmesh.ops.recalc_face_normals(bm,faces=bm.faces); bm.to_mesh(me); bm.free()
print('done',time.time()-t0)
bpy.ops.wm.save_as_mainfile(filepath=S+'stage2a.blend')
rh.setup('BLENDER_WORKBENCH',(700,700))
bpy.data.materials['suit'].diffuse_color=(0.25,0.27,0.34,1)
rh.cam_shot(S+"s2_front.png",(0,0,0.77),4.2,0,4,50)
rh.cam_shot(S+"s2_side.png",(0,0,0.77),4.2,90,4,50)
rh.cam_shot(S+"s2_back.png",(0,0,0.77),4.2,200,8,50)
rh.cam_shot(S+"s2_torso.png",(0,0,1.0),2.0,25,5,50)
