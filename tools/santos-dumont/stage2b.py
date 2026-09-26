import sys; sys.path.insert(0,__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from lib2 import *
import rh, time
t0=time.time()
bpy.ops.wm.open_mainfile(filepath=S+'stage2a.blend')
body=bpy.data.objects['body']; proxy=bpy.data.objects['proxy']
JJ=json.load(open(S+'joints1.json'))['joints']
B=Body(body,JJ); BP=Body(proxy,JJ); bi=B.bi; J=B.J
def bid(n): return bi[n]
V=B.V; fd=B.fdom; fc=B.fc
Z_W=0.905; Z_HEM=0.645; Z_V0=1.075; NY=-0.012

def obj_bvh(names):
    Vs=[];Fs=[];off=0
    for n in names:
        o=bpy.data.objects[n]; me=o.data
        Vs+= [tuple(v.co) for v in me.vertices]; Fs+=[tuple(i+off for i in p.vertices) for p in me.polygons]; off+=len(me.vertices)
    return BVHTree.FromPolygons(Vs,Fs)
def raycast(bvh,o,d,far=1.0):
    loc,nrm,fi,dist=bvh.ray_cast(Vector(o),Vector(d).normalized(),far); return loc,nrm,dist
def grid_faces(R,C,closed=False):
    F=[]
    for r in range(R-1):
        for c in range(C if closed else C-1):
            c2=(c+1)%C; F.append((r*C+c,r*C+c2,(r+1)*C+c2,(r+1)*C+c))
    return F
def ellipsoid(center,axes,frame,nu=10,nv=7):
    X,Y,Zz=[np.array(a) for a in frame]; Vv=[];F=[]
    for i in range(nv+1):
        th=math.pi*i/nv
        for j in range(nu):
            ph=2*math.pi*j/nu
            Vv.append(np.array(center)+X*axes[0]*math.sin(th)*math.cos(ph)+Y*axes[1]*math.sin(th)*math.sin(ph)+Zz*axes[2]*math.cos(th))
    for i in range(nv):
        for j in range(nu):
            a=i*nu+j; b=i*nu+(j+1)%nu; F.append((a,a+nu,b+nu,b))
    return np.array(Vv),F
def box(center,half,frame):
    X,Y,Zz=[np.array(a) for a in frame]; c=np.array(center); Vv=[]
    for sx in (-1,1):
        for sy in (-1,1):
            for sz in (-1,1): Vv.append(c+X*half[0]*sx+Y*half[1]*sy+Zz*half[2]*sz)
    F=[(0,1,3,2),(4,6,7,5),(0,4,5,1),(2,3,7,6),(0,2,6,4),(1,5,7,3)]
    return np.array(Vv),F
def frame_from(n,up=(0,0,1)):
    n=Vector(n).normalized(); u=Vector(up); x=u.cross(n)
    if x.length<1e-4: x=Vector((1,0,0))
    x.normalize(); y=n.cross(x); return (tuple(x),tuple(y),tuple(n))
def merge(parts):
    Vv=np.concatenate([p[0] for p in parts]); F=[];off=0
    for p in parts: F+=[tuple(i+off for i in f) for f in p[1]]; off+=len(p[0])
    return Vv,F

# ---------- CAMISA (peito visível no V) ----------
mk=np.array([(fd[f] in (bid('chest'),bid('neck'),bid('spine'))) and 1.03<fc[f][2]<1.285 and fc[f][1]<-0.02 and abs(fc[f][0])<0.056 for f in range(len(fd))])
bm=bm_from_faces(proxy,mk); shell(bm,BP,lambda P:np.full(len(P),0.006),iters=12)
to_obj('shirt',bm,'shirt',(0.95,0.94,0.9,1))

# ---------- COLARINHO ALTO (engomado, pontas arredondadas) ----------
ZC0=1.238
def ztop(th):
    a=abs(math.atan2(math.sin(th),math.cos(th)))
    return 1.301+0.031*float(ss(0.3,1.3,a))-0.004*float(ss(1.8,3.0,a))
def zbot(th):
    a=abs(math.atan2(math.sin(th),math.cos(th)))
    return 1.236+0.050*float(ss(0.35,1.35,a))-0.010*float(ss(1.8,3.0,a))
def neck_r(th,z):
    loc,nrm,dist=raycast(B.bvh,(0,NY,z),(math.sin(th),-math.cos(th),0),0.2)
    return dist if dist else 0.05
thg=np.linspace(0,2*math.pi,181)
Rmax=np.array([neck_r(th,ztop(th)-0.004) for th in thg])
Rmax=np.convolve(np.pad(Rmax[:-1],3,mode='wrap'),np.ones(7)/7,mode='valid'); Rmax=np.r_[Rmax,Rmax[0]]
def rcol(th,z):
    i=int(round((th%(2*math.pi))/(2*math.pi)*180))%181; return Rmax[i]+0.0015*max(0,(1.27-z)/0.03)
NCOL=56; rows=9; Vc=[]; gtop=0.20; gbot=0.055
for r_ in range(rows):
    v=r_/(rows-1); g=gbot+(gtop-gbot)*v
    for th in np.linspace(g,2*math.pi-g,NCOL):
        zt=ztop(th); a=min(th,2*math.pi-th); cr=1-float(ss(g,g+0.22,a)); zt-=0.008*cr*cr
        zb=zbot(th); z=zb+v*(zt-zb); rr=rcol(th,z)+0.0055+0.0035*(1-v)
        Vc.append((math.sin(th)*rr,NY-math.cos(th)*rr,z))
to_obj('collar',(np.array(Vc),[f[::-1] for f in grid_faces(rows,NCOL)]),'shirt')

# ---------- GRAVATA (xadrez, como nas fotos do 14-bis) ----------
shirt_bvh=obj_bvh(['shirt'])
rk=neck_r(0.0,1.259)
kc=np.array((0,NY-rk-0.0118,1.257))
Vt,Ft=ellipsoid(kc,(1,1,1),((1,0,0),(0,1,0),(0,0,1)),16,10)
for p in Vt:      # nó de gravata: bloco trapezoidal arredondado
    d_=p-kc; e_=np.sign(d_)*np.abs(d_)**0.55
    t=(e_[2]+1)/2; hw=0.0068+0.0062*t
    p[:]=kc+np.array((e_[0]*hw,e_[1]*0.0058*(0.8+0.2*t),e_[2]*0.0115))
    p[1]-=0.0022*(1-e_[0]**2)*(e_[1]<0)
to_obj('tieknot',(Vt,Ft),'tie',(0.2,0.2,0.3,1))
Vb=[]; NR=18; NC=5
for i in range(NR):
    z=1.249-i*(1.249-1.035)/(NR-1); hw=0.0075+0.0085*(i/(NR-1))
    for j in range(NC):
        x=-hw+2*hw*j/(NC-1)
        loc,nrm,dist=raycast(shirt_bvh,(x,-0.5,z),(0,1,0))
        if loc is None: loc,nrm,dist=raycast(BP.bvh,(x,-0.5,z),(0,1,0))
        Vb.append(np.array(loc)+np.array(nrm)*(0.0022+0.0012*(1-abs(2*j/(NC-1)-1))))
to_obj('tieblade',(np.array(Vb),[f[::-1] for f in grid_faces(NR,NC)]),'tie')

# ---------- BOTÕES e BOLSOS ----------
jb=obj_bvh(['jacket','skirt'])
parts=[]
for z in (1.068,1.001,0.934,0.867):
    loc,nrm,dist=raycast(jb,(0,-0.5,z),(0,1,0))
    parts.append(ellipsoid(np.array(loc)+np.array(nrm)*0.0012,(0.0068,0.0068,0.0022),frame_from(nrm),10,5))
to_obj('buttons',merge(parts),'button',(0.05,0.04,0.035,1))
def patch(bvh,cx,cz,w,h,t,nx=8,nz=3):
    P=[]
    for i in range(nz):
        for j in range(nx):
            x=cx-w/2+w*j/(nx-1); z=cz+h/2-h*i/(nz-1)
            loc,nrm,dist=raycast(bvh,(x,-0.5,z),(0,1,0)); P.append((np.array(loc),np.array(nrm)))
    top=[p+n*t for p,n in P]; bot=[p+n*0.0003 for p,n in P]
    Vout=np.array(top+bot); F=[f[::-1] for f in grid_faces(nz,nx)]; N=nz*nx
    bnd=[(0,j) for j in range(nx)]+[(i,nx-1) for i in range(1,nz)]+[(nz-1,j) for j in range(nx-2,-1,-1)]+[(i,0) for i in range(nz-2,0,-1)]
    ids=[i*nx+j for i,j in bnd]
    for k in range(len(ids)):
        a=ids[k]; b=ids[(k+1)%len(ids)]; F.append((b+N,b,a,a+N))
    return Vout,F
pk=[patch(jb,sg*0.088,0.737,0.108,0.034,0.0016) for sg in (1,-1)]
pk.append(patch(jb,0.07,1.128,0.066,0.011,0.0012,8,2))
to_obj('pockets',merge(pk),'suit')

# ---------- PUNHOS DA CAMISA + RELÓGIO CARTIER SANTOS (pulso esquerdo) ----------
def arm_frame(s):
    e,w=J['forearm.'+s]; ax=(w-e).normalized(); x=Vector((1,0,0)); u=(x-ax*x.dot(ax)).normalized(); v=ax.cross(u); return e,w,ax,u,v
def arm_ring(s,t,off,n=20):
    e,w,ax,u,v=arm_frame(s); c=e+(w-e)*t; pts=[]
    for k in range(n):
        a=2*math.pi*k/n; d=u*math.cos(a)+v*math.sin(a)
        loc,nrm,dist=raycast(B.bvh,c,d,0.1); pts.append(np.array(c+d*((dist or 0.025)+off)))
    return np.array(pts)
cuffs=[loft([arm_ring(s,t,0.0048) for t in (0.955,0.93,0.905,0.88)],True) for s in ('L','R')]
to_obj('cuffs',merge(cuffs),'shirt')
e,w,ax,u,v=arm_frame('L')
to_obj('strap',loft([arm_ring('L',t,0.0016,24) for t in (0.998,0.985,0.972)],True),'strapmat',(0.08,0.05,0.03,1))
hv=V[B.dom==bid('hand.L')]; hc=hv.mean(0); U_,Sv,Vt_=np.linalg.svd(hv-hc); dn=Vector(Vt_[2])
if dn.x<0: dn=-dn
dn=(dn-ax*dn.dot(ax)).normalized()
c=e+(w-e)*0.985
loc,nrm,dist=raycast(B.bvh,c,dn,0.1)
wc=np.array(c+dn*((dist or 0.022)+0.0045))
fx=tuple(ax); fz=tuple(dn); fy=tuple(dn.cross(ax))
to_obj('watchcase',box(wc,(0.0105,0.0098,0.0028),(fx,fy,fz)),'gold',(0.83,0.69,0.3,1))
to_obj('watchdial',box(wc+np.array(dn)*0.0026,(0.0082,0.0076,0.0004),(fx,fy,fz)),'dial',(0.95,0.94,0.9,1))
to_obj('watchcrown',ellipsoid(wc+np.array(dn)*0.0005+np.array(Vector(fy))*0.0112,(0.0016,0.0016,0.0016),(fx,fy,fz),6,4),'gold')
print('watch dorsal',tuple(round(x,3) for x in dn))

# ---------- ARNÊS DE VOO (nov/1906): os ailerons octogonais eram comandados por cabos presos aos ombros ----------
# do paletó; inclinando o corpo ele puxava um cabo e soltava o outro. Alças de couro + cinto no peito + argolas de aço
jk=obj_bvh(['jacket','sleeve.L','sleeve.R'])
def hit(o,d,off=0.0032):
    loc,nrm,dist=raycast(jk,o,d,1.0)
    return None if loc is None else (np.array(loc)+np.array(nrm)*off,np.array(nrm))
def strap_mesh(P,N,w,t=0.0022,closed=False):
    P=np.array(P); N=np.array(N)
    T=np.gradient(P,axis=0) if len(P)>2 else np.tile(P[1]-P[0],(len(P),1))
    if closed: T=np.roll(P,-1,0)-np.roll(P,1,0)
    T/=np.linalg.norm(T,axis=1)[:,None]
    Bn=np.cross(T,N); Bn/=np.linalg.norm(Bn,axis=1)[:,None]
    rings_=[np.array([p+b*w/2+n*t,p-b*w/2+n*t,p-b*w/2-n*0.0006,p+b*w/2-n*0.0006]) for p,n,b in zip(P,N,Bn)]
    Vv,F=loft(rings_,True)
    if not closed: pass
    else:
        n=len(rings_); m=4
        F+=[(( n-1)*m+i,(n-1)*m+(i+1)%m,(i+1)%m,i) for i in range(m)]
    return Vv,F,T
hparts=[]; hrings=[]; attach={}
for sg in (1,-1):                                    # sg=+1: ombro esquerdo (Blender +x)
    P=[];N=[]
    for z in np.linspace(0.975,1.12,8):              # frente
        r=hit((sg*0.078,-0.5,z),(0,1,0)); P.append(r[0]);N.append(r[1])
    C=np.array((sg*0.088,0.0,1.12))
    for th in np.linspace(0.12,math.pi-0.12,22):      # por cima do ombro
        d=np.array((0,-math.cos(th),math.sin(th))); r=hit(C+d*0.4,-d); P.append(r[0]);N.append(r[1])
    for z in np.linspace(1.12,0.975,8):              # costas
        r=hit((sg*0.078,0.5,z),(0,-1,0)); P.append(r[0]);N.append(r[1])
    P=np.array(P);N=np.array(N)
    # alisa o caminho (sem degraus entre os trechos)
    for it in range(6):
        P[1:-1]=P[1:-1]*0.5+(P[:-2]+P[2:])*0.25
        N[1:-1]=N[1:-1]*0.5+(N[:-2]+N[2:])*0.25; N/=np.linalg.norm(N,axis=1)[:,None]
    Vv,F,T=strap_mesh(P,N,0.026); hparts.append((Vv,F))
    # argola em D atrás do alto do ombro, onde engata o cabo do aileron
    k=8+int(22*0.66); p=P[k]; n=N[k]; t=T[k]
    rc=p+n*0.010; rr=0.0105; tube=0.0021; Vr=[];Fr=[]; NU,NV=16,6
    b=np.cross(t,n); b/=np.linalg.norm(b)
    for i in range(NU):
        a=2*math.pi*i/NU; ctr=rc+(n*math.cos(a)+t*math.sin(a))*rr; rd=(n*math.cos(a)+t*math.sin(a))
        for j in range(NV):
            c_=2*math.pi*j/NV; Vr.append(ctr+(rd*math.cos(c_)+b*math.sin(c_))*tube)
    for i in range(NU):
        for j in range(NV):
            a_=i*NV+j; b_=((i+1)%NU)*NV+j; c2=((i+1)%NU)*NV+(j+1)%NV; d_=i*NV+(j+1)%NV; Fr.append((a_,b_,c2,d_))
    hrings.append((np.array(Vr),Fr)); attach['L' if sg>0 else 'R']=(rc+n*rr).tolist()
# cinto no peito, por baixo dos braços
P=[];N=[]
for a in np.linspace(0,2*math.pi,48,endpoint=False):
    d=np.array((math.sin(a),-math.cos(a),0)); r=hit((0,0.0,0.975),d,0.0034)
    if r is None: continue
    P.append(r[0]);N.append(r[1])
P=np.array(P);N=np.array(N)
for it in range(3):
    P=P*0.5+(np.roll(P,1,0)+np.roll(P,-1,0))*0.25
Vv,F,T=strap_mesh(P,N,0.028,closed=True); hparts.append((Vv,F))
to_obj('harness',merge(hparts),'harnessmat',(0.3,0.19,0.11,1))
to_obj('hrings',merge(hrings),'hringmat',(0.6,0.62,0.65,1))
json.dump(attach,open(S+'harness.json','w'))
print('harness attach',{k:[round(x,3) for x in v] for k,v in attach.items()})

# ---------- PÁLPEBRAS QUE PISCAM: calotas de pele entre o globo ocular e a pele da pálpebra; abertas ficam escondidas ----
# sob a pálpebra de cima; o jogo gira os ossos lid.L/lid.R para baixo e a calota cobre o olho (com a linha dos cílios)
lids=[];lidc={}
for en,side in (('eyeL','L'),('eyeR','R')):
    pe=verts(bpy.data.objects[en]); c=pe.mean(0); r=np.linalg.norm(pe-c,axis=1).max()
    rr=r+0.0007; NA=18; NE=10; Vv=[]; Cc=[]
    for i in range(NE+1):
        el=math.radians(36+74*i/NE)                    # elevação (0 = olhando para a frente, −y no Blender)
        for j in range(NA+1):
            az=math.radians(-82+164*j/NA)
            d=np.array((math.sin(az)*math.cos(el),-math.cos(az)*math.cos(el),math.sin(el)))
            Vv.append(c+d*rr)
    F=[]
    for i in range(NE):
        for j in range(NA):
            a_=i*(NA+1)+j; F.append((a_,a_+1,a_+NA+2,a_+NA+1))
    o=to_obj('lid'+side,(np.array(Vv),F),'lidmat',(0.8,0.6,0.5,1))
    lids.append(o.name); lidc[side]=c.tolist()
json.dump({'centers':lidc,'NA':18,'NE':10},open(S+'lids.json','w'))
print('lids',{k:[round(x,4) for x in v] for k,v in lidc.items()})

# ---------- CABELO: repartido ao meio, emplastrado ----------
def hairline(phi):
    a=abs(phi)
    pts=[(0,1.468),(0.55,1.462),(0.85,1.445),(1.02,1.402),(1.22,1.398),(1.34,1.432),(1.75,1.432),(2.1,1.392),(2.6,1.362),(math.pi,1.356)]
    for (a0,z0),(a1,z1) in zip(pts,pts[1:]):
        if a<=a1: t=(a-a0)/(a1-a0); return z0+(z1-z0)*t
    return pts[-1][1]
ears=np.zeros(len(V),bool)
vs=vert_sets(body)
for sid in (4,5): ears[list(vs[sid])]=True
def is_hair(i):
    p=V[i]
    if ears[i]: return False
    if B.dom[i] not in (bid('head'),bid('neck')): return False
    phi=math.atan2(p[0],-(p[1]+0.025))
    return p[2]>hairline(phi)
hv_=np.array([is_hair(i) for i in range(len(V))])
mk=np.array([all(hv_[j] for j in B.polys[f]) for f in range(len(fd))])
bm=bm_from_faces(body,mk)
shell(bm,B,lambda P:np.full(len(P),0.0024),iters=10,lam=0.5)
for vv in bm.verts:        # risca ao meio
    c=vv.co
    if c.z>1.465 and c.y<0.03:
        g=math.exp(-(c.x/0.0028)**2)
        vv.co-=vv.normal*0.0022*g
to_obj('hair',bm,'hair',(0.06,0.045,0.035,1))

# ---------- SOBRANCELHAS ----------
brows=[]
for sg in (1,-1):
    NRb=4; NCb=12; Vv=[]
    for i in range(NRb):
        vq=-0.5+i/(NRb-1)
        for j in range(NCb):
            t=j/(NCb-1); x=sg*(0.0105+0.040*t)
            zc=1.4207+0.0142+0.0042*math.sin(math.pi*min(1,t*1.15))-0.0045*t**3
            h=0.0072*(1-0.55*t); z=zc-vq*h
            loc,nrm,dist=raycast(B.bvh,(x,-0.5,z),(0,1,0))
            Vv.append(np.array(loc)+np.array(nrm)*(0.00025+0.0008*(1-4*vq*vq)))
    F=grid_faces(NRb,NCb)
    if sg<0: F=[f[::-1] for f in F]
    brows.append((np.array(Vv),F))
to_obj('brows',merge(brows),'hair')

# ---------- BIGODE (farto, pontas caídas além dos cantos da boca) ----------
prof=[]
for z in np.arange(1.345,1.40,0.0005):
    loc,nrm,dist=raycast(B.bvh,(0,-0.5,z),(0,1,0)); prof.append((z,loc.y))
prof=np.array(prof)
ylip=prof[(prof[:,0]>1.358)&(prof[:,0]<1.366)][:,1].min()
nose=prof[prof[:,1]<ylip-0.006]; zsn=nose[:,0].min()-0.0015
mouth=prof[(prof[:,0]>1.35)&(prof[:,0]<1.362)]; zm=mouth[np.argmax(mouth[:,1])][0]
print('subnasale',zsn,'mouth',zm)
NU=19; NV=8; Vm=[]
for i in range(NV):
    vq=i/(NV-1)
    for j in range(NU):
        u=-1+2*j/(NU-1); au=abs(u)
        hw=0.019+0.012*vq
        ztp=zsn-0.004*au**2
        zbt=zm+0.0010-0.0075*au**2.4
        z=ztp+(zbt-ztp)*vq
        x=u*hw*(1-0.10*(1-math.sin(math.pi*vq))*au**4)
        loc,nrm,dist=raycast(B.bvh,(x,-0.5,z),(0,1,0))
        th=0.0038*(1-au**2.2)**0.7*(0.35+0.65*math.sin(math.pi*(0.12+0.88*vq)))+0.0006
        p=np.array(loc)+np.array(nrm)*th
        if i==NV-1: p[2]-=0.0006*(1-au)
        Vm.append(p)
to_obj('mustache',(np.array(Vm),[f[::-1] for f in grid_faces(NV,NU)]),'hair')

# ---------- CHAPÉU PANAMÁ (copa em sino com cumeeira, aba caída ondulada) ----------
yF,zF=-0.12,1.481; yB,zB=0.075,1.452
k=(zB-zF)/(yB-yF)
O=Vector((0,-0.022,zF+k*(-0.022-yF)))
Xh=Vector((1,0,0)); Yh=Vector((0,1,k)).normalized(); Uh=Xh.cross(Yh).normalized()
hair_bvh=obj_bvh(['hair','body'])
NP=64
phis=np.linspace(math.pi,math.pi+2*math.pi,NP+1)   # costura atrás
def head_r(phi):
    d=(Xh*math.sin(phi)-Yh*math.cos(phi)).normalized()
    loc,nrm,dist=raycast(hair_bvh,O+Uh*0.004,d,0.2)
    return (dist or 0.085)
RB=np.array([head_r(p) for p in phis[:-1]])+0.0045
RB=np.convolve(np.pad(RB,2,mode='wrap'),np.ones(5)/5,mode='valid'); RB=np.r_[RB,RB[0]]
def P(phi,r,h): return O+(Xh*math.sin(phi)-Yh*math.cos(phi))*r+Uh*h
rows=[]; vcoord=[]
Wb=lambda ph:0.049+0.005*math.cos(ph)**2*(1 if math.cos(ph)>0 else 1.3)
droop=lambda ph:0.86 if math.cos(ph)>0.3 else (1.0 if math.cos(ph)>-0.3 else 1.05)
for b in np.linspace(1,0,8):   # aba (de fora para dentro)
    rows.append([P(ph,RB[i]+Wb(ph)*b,-Wb(ph)*(0.34*b+0.66*b*b)*(0.62+0.38*(1-math.cos(ph))/2)+b*b*(0.0042*math.sin(3*ph+0.6)+0.0026*math.sin(5*ph+1.9))) for i,ph in enumerate(phis)])
HS=0.086
for s in np.linspace(0,1,10)[1:]:   # lateral da copa
    rows.append([P(ph,RB[i]*(1-0.19*s**1.5),HS*s) for i,ph in enumerate(phis)])
for q in np.linspace(0,1,8)[1:]:    # topo com cumeeira frente-trás
    rows.append([P(ph,RB[i]*0.81*(1-q)+1e-4,HS+0.028*math.sqrt(max(0,1-(1-q)**2))*(0.62+0.38*math.cos(ph)**2)) for i,ph in enumerate(phis)])
HV=np.array([[tuple(p) for p in r] for r in rows]).reshape(-1,3)
Fh=grid_faces(len(rows),NP+1)
hat=to_obj('hat',(HV,Fh),'straw',(0.86,0.78,0.6,1))
band=[[P(ph,RB[i]*(1-0.19*s**1.5)+0.0013,HS*s) for i,ph in enumerate(phis)] for s in np.linspace(0,0.30,4)]
BV=np.array([[tuple(p) for p in r] for r in band]).reshape(-1,3)
to_obj('hatband',(BV,grid_faces(4,NP+1)),'band',(0.03,0.03,0.03,1))
# inclinação "de lado" (desabado)
R=Matrix.Rotation(math.radians(-4.0),4,Vector((0,-1,0)))@Matrix.Rotation(math.radians(1.5),4,Vector((1,0,0)))
T=Matrix.Translation(O)@R@Matrix.Translation(-O)
for n in ('hat','hatband'):
    bpy.data.objects[n].data.transform(T)
# ---------- SOLA GROSSA + SALTO ----------
def clip(poly,y0,keep_greater):
    out=[]; n=len(poly)
    for i in range(n):
        a=poly[i]; b=poly[(i+1)%n]
        ina=(a[1]>=y0) if keep_greater else (a[1]<=y0); inb=(b[1]>=y0) if keep_greater else (b[1]<=y0)
        if ina: out.append(a)
        if ina!=inb:
            t=(y0-a[1])/(b[1]-a[1]); out.append(a+(b-a)*t)
    return np.array(out)
def prism(poly,z0,z1,spring=None):
    n=len(poly); Vv=[]
    for p in poly: Vv.append((p[0],p[1],z0+(spring(p) if spring else 0)))
    for p in poly: Vv.append((p[0],p[1],z1))
    F=[tuple(range(n))[::-1],tuple(range(n,2*n))]
    for i in range(n):
        j=(i+1)%n; F.append((i,j,n+j,n+i))
    return np.array(Vv),F
SOLE=0.022
soles=[]
for s_ in ('L','R'):
    bv=verts(bpy.data.objects['boot.'+s_]); low=bv[bv[:,2]<0.012][:,:2]
    H=hull2d(low); c=H.mean(0)
    H=np.array([p+(p-c)/np.linalg.norm(p-c)*0.0032 for p in H])
    y0,y1=H[:,1].min(),H[:,1].max(); L=y1-y0
    soles.append(prism(H,-0.0065,0.0))
    soles.append(prism(clip(H,y1-0.27*L,True),-SOLE,-0.0065))
    soles.append(prism(clip(H,y0+0.60*L,False),-SOLE,-0.0065,spring=lambda p,y0=y0,L=L:0.007*max(0,1-(p[1]-y0)/(0.22*L))**2))
to_obj('soles',merge(soles),'solemat',(0.05,0.04,0.035,1))
json.dump({'SOLE':SOLE},open(S+'sole.json','w'))
json.dump({'hatO':list(O),'NP':NP,'rows':len(rows)},open(S+'hatinfo.json','w'))
print('hat ok',time.time()-t0)
bpy.ops.wm.save_as_mainfile(filepath=S+'stage2b.blend')
rh.setup('BLENDER_WORKBENCH',(700,700))
for n,c in (('suit',(0.2,0.21,0.26,1)),('body',(0.85,0.68,0.57,1))):
    if n in bpy.data.materials: bpy.data.materials[n].diffuse_color=c
for m in body.data.materials: m.diffuse_color=(0.85,0.68,0.57,1)
rh.cam_shot(S+"s3_front.png",(0,0,0.80),4.3,0,4,50)
rh.cam_shot(S+"s3_q.png",(0,0,0.80),4.3,35,6,50)
rh.cam_shot(S+"s3_back.png",(0,0,0.80),4.3,180,6,50)
rh.cam_shot(S+"s3_head.png",(0,-0.03,1.38),0.9,20,4,85)
rh.cam_shot(S+"s3_headside.png",(0,-0.03,1.38),0.9,80,4,85)
