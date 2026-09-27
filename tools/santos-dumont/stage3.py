import sys; sys.path.insert(0,__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from lib2 import *
import base64, time
t0=time.time()
OUT=sys.argv[-1] if sys.argv[-1].endswith('.js') else S+'santos-dumont.js'
bpy.ops.wm.open_mainfile(filepath=S+'stage2b.blend')
body=bpy.data.objects['body']; proxy=bpy.data.objects['proxy']
J1=json.load(open(S+'joints1.json')); JJ=J1['joints']; FAX=J1.get('fingers',{})
SOLE=json.load(open(S+'sole.json'))['SOLE']
B=Body(body,JJ); BP=Body(proxy,JJ); bi=B.bi; J=B.J; BONES=B.bones
V=B.V; fd=B.fdom; fc=B.fc
PARENT={'hips':None,'spine':'hips','chest':'spine','neck':'chest','head':'neck'}
for s in ('L','R'):
    PARENT.update({f'upperarm.{s}':'chest',f'forearm.{s}':f'upperarm.{s}',f'hand.{s}':f'forearm.{s}',
                   f'thigh.{s}':'hips',f'shin.{s}':f'thigh.{s}',f'foot.{s}':f'shin.{s}'})
    for f in ('thumb','index','middle','ring','pinky'):
        PARENT.update({f'{f}1.{s}':f'hand.{s}',f'{f}2.{s}':f'{f}1.{s}',f'{f}3.{s}':f'{f}2.{s}'})
FINGER=tuple(n for n in FAX)

# ---------- corpo: mantém só o que aparece (cabeça, pescoço acima do colarinho, pulsos e mãos) ----------
def ft(s,P):
    e,w=J['forearm.'+s]; return seg_t(P,np.array(e),np.array(w))
def ztop(th):
    a=abs(math.atan2(math.sin(th),math.cos(th)))
    return 1.301+0.031*float(ss(0.3,1.3,a))-0.004*float(ss(1.8,3.0,a))
keep=np.zeros(len(fd),bool)
tL=ft('L',fc); tR=ft('R',fc)
for f in range(len(fd)):
    n=BONES[fd[f]]; z=fc[f][2]
    if n=='head' and z<1.505: keep[f]=True
    elif n=='neck' and z>ztop(math.atan2(fc[f][0],-(fc[f][1]+0.012)))-0.008: keep[f]=True
    elif n.startswith('hand') or n in FAX: keep[f]=True
    elif n=='forearm.L' and tL[f]>0.88: keep[f]=True
    elif n=='forearm.R' and tR[f]>0.88: keep[f]=True
bm=bm_from_faces(body,keep); bm.to_mesh(body.data); bm.free(); body.data.update()
# cabelo dentro da copa do chapéu não aparece
h=bpy.data.objects['hair']; bm=bmesh.new(); bm.from_mesh(h.data)
bmesh.ops.delete(bm,geom=[f for f in bm.faces if f.calc_center_median().z>1.505],context='FACES'); bm.to_mesh(h.data); bm.free()

def split_obj(src,name,pred):
    o=src.copy(); o.data=src.data.copy(); o.name=name; bpy.context.scene.collection.objects.link(o)
    bm=bmesh.new(); bm.from_mesh(o.data)
    bmesh.ops.delete(bm,geom=[f for f in bm.faces if not pred(f.calc_center_median())],context='FACES'); bm.to_mesh(o.data); bm.free()
    return o
split_obj(body,'head',lambda c:c.z>1.0); split_obj(body,'hands',lambda c:c.z<=1.0)
def decimate(o,ratio):
    m=o.modifiers.new('dec','DECIMATE'); m.ratio=ratio; m.use_collapse_triangulate=True
    if o.name=='head':   # protege olhos, pálpebras, nariz, boca e orelhas
        g=o.vertex_groups.new(name='keep'); P_=np.array([v.co[:] for v in o.data.vertices])
        x,y,z=P_[:,0],P_[:,1],P_[:,2]
        w=np.zeros(len(P_))
        for sg in (1,-1):
            w=np.maximum(w,np.exp(-(((x-sg*0.0295)/0.02)**2+((z-1.421)/0.014)**2))*(y<-0.07))
            w=np.maximum(w,np.exp(-(((x-sg*0.07)/0.02)**2+((z-1.40)/0.03)**2)))
        w=np.maximum(w,np.exp(-((x/0.025)**2+((z-1.375)/0.03)**2))*(y<-0.08))
        for i,wi in enumerate(w):
            if wi>0.05: g.add([i],float(min(1,wi*1.3)),'REPLACE')
        m.vertex_group='keep'; m.vertex_group_factor=8.0
    with ctx(o): bpy.ops.object.modifier_apply(modifier=m.name)

PARTS=[ # objeto, material, pesos, decimação
 ('head','skin','xfer',0.45),('hands','skin','xfer',0.42),('eyeL','eye','head',1),('eyeR','eye','head',1),
 ('hair','hair','xfer',0.5),('brows','hair','xfer',1),('mustache','hair','xfer',1),
 ('jacket','suit','torsoW',0.38),('sleeve.L','suit','sleeve.L',1),('sleeve.R','suit','sleeve.R',1),('skirt','suit','skirt',1),('pockets','suit','torsoW',1),
 ('trousers.P','suit','xfer',1),('trousers.L','suit','xfer',1),('trousers.R','suit','xfer',1),
 ('shirt','shirt','torsoW',0.6),('collar','shirt','xfer',1),('cuffs','shirt','xfer',1),
 ('tieknot','tie','torsoW',1),('tieblade','tie','torsoW',1),
 ('buttons','dark','torsoW',1),('hatband','dark','head',1),
 ('hat','straw','head',1),
 ('boot.L','leather','xfer',1),('boot.R','leather','xfer',1),('soles','sole','xfer',1),
 ('strap','leather','rigid',1),('harness','harness','harnessW',1),('lidL','skin','lid.L',1),('lidR','skin','lid.R',1),('hrings','hring','chest',1),('watchcase','gold','rigid',1),('watchcrown','gold','rigid',1),('watchdial','dial','rigid',1),
]
for n,m,wm,r in PARTS:
    o=bpy.data.objects[n]
    if r<1: decimate(o,r)
# ---------- cores ----------
def srgb(c): return np.array(c,float)
SKIN=srgb((0.86,0.68,0.57))
vsets=vert_sets(bpy.data.objects['proxy'])   # mesmos índices do corpo original
def skin_colors(P):
    C=np.tile(SKIN,(len(P),1))
    def mix(w,col):
        nonlocal C; w=np.clip(w,0,1)[:,None]; C=C*(1-w)+np.array(col)*w
    x,y,z=P[:,0],P[:,1],P[:,2]
    # lábios
    lip=np.exp(-((x/0.022)**2+((z-1.356)/0.0075)**2))*ss(-0.10,-0.12,y)
    mix(lip*0.75,(0.70,0.44,0.41))
    for sg in (1,-1):
        mix(0.22*np.exp(-(((x-sg*0.045)/0.02)**2+((z-1.39)/0.02)**2))*ss(-0.06,-0.09,y),(0.88,0.58,0.50))   # maçãs
        d=np.sqrt((x-sg*0.0295)**2+((y+0.1096)*0.8)**2+((z-1.4207)*1.1)**2)
        mix(0.45*np.clip(1-d/0.024,0,1)**1.5,(0.58,0.42,0.37))                                              # olheiras
        mix(0.30*np.exp(-(((x-sg*0.075)/0.012)**2+((z-1.40)/0.03)**2)),(0.86,0.58,0.50))                    # orelhas
    beard=ss(1.372,1.35,z)*ss(-0.05,-0.08,y)*(z>1.25)
    mix(0.13*beard,(0.55,0.52,0.52))
    return C
def eye_colors(P,c):
    D=P-c; D/=np.linalg.norm(D,axis=1)[:,None]; a=np.arccos(np.clip(-D[:,1],-1,1))
    C=np.tile(np.array((0.92,0.89,0.84)),(len(P),1))
    C[:]=(0.86,0.83,0.78)
    iris=a<0.52; C[iris]=(0.22,0.13,0.07)
    C[(a<0.52)&(a>0.45)]=(0.10,0.06,0.04)
    C[a<0.19]=(0.015,0.012,0.01)
    lid=np.clip((D[:,2]+0.05)/0.5,0,1)[:,None]*(~iris)[:,None]      # sombra da pálpebra superior
    C=C*(1-0.45*lid)+np.array((0.55,0.45,0.40))*0.45*lid
    corner=np.clip((a-1.0)/0.6,0,1)[:,None]*(~iris)[:,None]
    C=C*(1-0.25*corner)+np.array((0.85,0.6,0.55))*0.25*corner
    return C
# ---------- montagem ----------
def tri_mesh(o):
    me=o.data; me.calc_loop_triangles()
    P=np.array([v.co[:] for v in me.vertices]); N=np.array([v.normal[:] for v in me.vertices])
    T=np.array([t.vertices[:] for t in me.loop_triangles],np.int64)
    TP=np.array([t.polygon_index for t in me.loop_triangles])
    PN=np.array([p.normal[:] for p in me.polygons])
    return P,N,T,PN[TP] if len(TP) else np.zeros((0,3))
MATS=['skin','eye','hair','suit','shirt','tie','dark','straw','leather','sole','gold','dial','harness','hring']
hatinfo=json.load(open(S+'hatinfo.json'))
geo={m:{'P':[],'N':[],'UV':[],'C':[],'W':[],'T':[],'n':0} for m in MATS}
EXTRA=['lid.L','lid.R']                                   # ossos extras (pálpebras), filhos da cabeça
LIDS=json.load(open(S+'lids.json'))
def weights_for(n,mode,P):
    W=_weights_for(n,mode,P)
    if W.shape[1]==len(BONES): W=np.hstack([W,np.zeros((len(W),len(EXTRA)))])
    return W
def _weights_for(n,mode,P):
    if mode in EXTRA:
        W=np.zeros((len(P),len(BONES)+len(EXTRA))); W[:,len(BONES)+EXTRA.index(mode)]=1; return W
    if mode=='head':
        W=np.zeros((len(P),len(BONES))); W[:,bi['head']]=1; return W
    if mode=='xfer': return B.xfer(P)
    if mode=='xferP': return BP.xfer(P)
    if mode.startswith('sleeve'):                         # manga: braço rígido, dobra só no cotovelo
        sd=mode[-1];A,E=(np.array(v) for v in J['upperarm.'+sd]);W_=np.zeros((len(P),len(BONES)))
        t=seg_t(P,A,E)*np.linalg.norm(E-A);Lu=np.linalg.norm(E-A);k=np.clip((t-(Lu-0.035))/0.07,0,1)
        W_[:,bi['upperarm.'+sd]]=1-k;W_[:,bi['forearm.'+sd]]=k;return W_
    if mode=='chest':
        W=np.zeros((len(P),len(BONES))); W[:,bi['chest']]=1; return W
    if mode=='torsoW':     # peças do tronco: só tronco e pescoço (o braço não puxa o paletó — nada de "pé de pato")
        W=BP.xfer(P); keep_=[bi['hips'],bi['spine'],bi['chest'],bi['neck']]
        M_=np.zeros(len(BONES)); M_[keep_]=1; W=W*M_; W[W.sum(1)<1e-6,bi['chest']]=1
        return W/W.sum(1,keepdims=True)
    if mode=='harnessW':   # arnês segue só o tronco (argolas presas ao peito)
        W=BP.xfer(P); keep_=[bi['hips'],bi['spine'],bi['chest']]
        M_=np.zeros(len(BONES)); M_[keep_]=1; W=W*M_; W[W.sum(1)<1e-6,bi['chest']]=1
        return W/W.sum(1,keepdims=True)
    if mode=='rigid':
        W=B.xfer(np.array([P.mean(0)])); return np.repeat(W,len(P),0)
    if mode=='skirt':
        W=np.zeros((len(P),len(BONES))); t=np.clip((0.935-P[:,2])/(0.935-0.645),0,1)
        leg=0.42*t**1.3; side=ss(-0.05,0.05,P[:,0])
        W[:,bi['hips']]=1-leg; W[:,bi['thigh.L']]=leg*side; W[:,bi['thigh.R']]=leg*(1-side)
        top=t<0.12; W[top]=BP.xfer(P[top])*(1-t[top,None]/0.12)+W[top]*(t[top,None]/0.12)
        return W
for n,mat,mode,r in PARTS:
    o=bpy.data.objects[n]; P,N,T,FN=tri_mesh(o)
    if len(T)==0: print('vazio',n); continue
    W=weights_for(n,mode,P)
    UV=np.zeros((len(P),2)); C=np.ones((len(P),3))
    if mat=='skin' and n.startswith('lid'):            # pálpebra: pele um pouco mais rosada, cílios escuros na borda
        NA=LIDS['NA']+1; row=np.arange(len(P))//NA
        C=np.tile(np.array((0.8,0.6,0.5)),(len(P),1)); C[row==0]=(0.08,0.06,0.05); C[row==1]=(0.45,0.32,0.27)
    elif mat=='skin': C=skin_colors(P)
    if mat=='eye':
        ec=P.mean(0)+np.array((0,0.0012,0)); C=eye_colors(P,ec); Dd=P-ec; Dd/=np.linalg.norm(Dd,axis=1)[:,None]
        UV=np.stack([0.5+Dd[:,0]*0.5,0.5+Dd[:,2]*0.5],1); UV[Dd[:,1]>0]=(0.03,0.03)
        C=np.where((np.arccos(np.clip(-Dd[:,1],-1,1))<0.62)[:,None],np.maximum(C,0.999),C)
    if mat=='tie': UV=P[:,[0,2]].copy()
    if n=='hair':
        ang=np.arctan2(P[:,0],-(P[:,1]+0.025)); UV=np.stack([ang*0.085,P[:,2]],1)
    if n=='mustache':
        NU,NV=19,8; j=np.arange(len(P))%NU; i_=np.arange(len(P))//NU; UV=np.stack([j/(NU-1)*0.065,i_/(NV-1)*0.03],1)
    if n=='brows':
        NCb,NRb=12,4; k_=np.arange(len(P))%(NCb*NRb); j=k_%NCb; i_=k_//NCb; UV=np.stack([i_/(NRb-1)*0.009,j/(NCb-1)*0.045],1)
    if n in ('hat','hatband'):
        NP=hatinfo['NP']; cols=NP+1; rows=len(P)//cols
        G=P.reshape(rows,cols,3); dv=np.linalg.norm(np.diff(G,axis=0),axis=2).mean(1); vv=np.concatenate([[0],np.cumsum(dv)])
        circ=np.linalg.norm(np.diff(G[rows//2],axis=0),axis=1).sum()
        U=np.tile(np.arange(cols)/NP*circ,(rows,1)); VV=np.tile(vv[:,None],(1,cols))
        UV=np.stack([U.ravel(),VV.ravel()],1)
    if n.startswith('sleeve'):                          # risca-de-giz ao longo da manga
        sd=n[-1];A,E=(np.array(v) for v in J['upperarm.'+sd]);E2,Wr=(np.array(v) for v in J['forearm.'+sd])
        tu=seg_t(P,A,E);up=tu<1.0;ax=np.where(up[:,None],(E-A)/np.linalg.norm(E-A),(Wr-E)/np.linalg.norm(Wr-E))
        base=np.where(up[:,None],A,E);vv=np.where(up,np.clip(tu,-0.3,1)*np.linalg.norm(E-A),np.linalg.norm(E-A)+seg_t(P,E,Wr)*np.linalg.norm(Wr-E))
        d=P-base;d-=ax*(d*ax).sum(1)[:,None];r0=np.array((0,1.0,0));e1=r0-ax*(ax@r0)[:,None];e1/=np.linalg.norm(e1,axis=1)[:,None];e2=np.cross(ax,e1)
        UV=np.stack([np.arctan2((d*e2).sum(1),(d*e1).sum(1))*0.05,vv],1)
    if mat=='suit' and not n.startswith('sleeve'):   # risca-de-giz: projeção por face (frente/costas usa x, laterais usa y)
        grp=(np.abs(FN[:,0])>np.abs(FN[:,1])).astype(int)
        key={}; P2=[];N2=[];W2=[];C2=[];UV2=[];T2=[]
        for ti,tr in enumerate(T):
            g=grp[ti]; nt=[]
            for vi in tr:
                k=(vi,g)
                if k not in key:
                    key[k]=len(P2); P2.append(P[vi]); N2.append(N[vi]); W2.append(W[vi]); C2.append(C[vi])
                    UV2.append((P[vi][1] if g else P[vi][0],P[vi][2]))
                nt.append(key[k])
            T2.append(nt)
        P,N,W,C,UV,T=np.array(P2),np.array(N2),np.array(W2),np.array(C2),np.array(UV2),np.array(T2)
    G_=geo[mat]; off=G_['n']
    G_['P'].append(P);G_['N'].append(N);G_['UV'].append(UV);G_['C'].append(C);G_['W'].append(W);G_['T'].append(T+off);G_['n']+=len(P)
    print('%-12s %-8s v=%5d t=%5d'%(n,mat,len(P),len(T)))
# ---------- converte para o espaço do three.js: x=-bx, y=bz+SOLE, z=by ----------
def to3(P): return np.stack([-P[:,0],P[:,2]+SOLE,P[:,1]],1)
def to3n(N): return np.stack([-N[:,0],N[:,2],N[:,1]],1)
allP=[];allN=[];allUV=[];allC=[];allW=[];allT=[];groups=[];base=0;ti=0
for m in MATS:
    G_=geo[m]
    if G_['n']==0: continue
    P=to3(np.concatenate(G_['P'])); N=to3n(np.concatenate(G_['N'])); T=np.concatenate(G_['T'])+base
    allP.append(P);allN.append(N);allUV.append(np.concatenate(G_['UV']));allC.append(np.concatenate(G_['C']));allW.append(np.concatenate(G_['W']));allT.append(T)
    groups.append([m,ti*3,len(T)*3]); ti+=len(T); base+=G_['n']
P=np.concatenate(allP);N=np.concatenate(allN);UV=np.concatenate(allUV);C=np.concatenate(allC);W=np.concatenate(allW);T=np.concatenate(allT)
# 4 maiores pesos
idx=np.argsort(-W,axis=1)[:,:4]; ww=np.take_along_axis(W,idx,1); ww/=np.maximum(ww.sum(1,keepdims=True),1e-9)
wq=np.round(ww*255).astype(int); wq[:,0]+=255-wq.sum(1)
print('total verts',len(P),'tris',len(T))
def b64(a): return base64.b64encode(np.ascontiguousarray(a).tobytes()).decode()
pmin=P.min(0); pmax=P.max(0); ps=(pmax-pmin)/65535
q=np.round((P-pmin)/ps).astype(np.uint16)
uvmin=UV.min(0); uvmax=UV.max(0); uvs=np.maximum(uvmax-uvmin,1e-6)/65535
quv=np.round((UV-uvmin)/uvs).astype(np.uint16)
Nn=N/np.maximum(np.linalg.norm(N,axis=1,keepdims=True),1e-9); qn=np.round(Nn*127).astype(np.int8)
qc=np.round(np.clip(C,0,1)*255).astype(np.uint8)
bones=[]
for n in BONES+EXTRA:
    h=np.array(J[n][0]) if n in J else np.array(LIDS['centers']['L' if n=='lid.L' else 'R']); h3=[-h[0],h[2]+SOLE,h[1]]
    bo={'n':n,'p':PARENT.get(n,'head'),'h':[round(float(x),5) for x in h3]}
    if n in FAX:                                          # dedos: eixo de flexão (+ = fecha para a palma) e ponta da falange
        a=FAX[n]['ax']; t=np.array(J[n][1]); bo['ax']=[round(-a[0],4),round(a[2],4),round(a[1],4)]; bo['t']=[round(float(-t[0]),5),round(float(t[2]+SOLE),5),round(float(t[1]),5)]
    bones.append(bo)
HA=json.load(open(S+'harness.json'))
harness={k:[round(-v[0],5),round(v[2]+SOLE,5),round(v[1],5)] for k,v in HA.items()}
data={'v':1,'harness':harness,'count':int(len(P)),'pmin':pmin.round(6).tolist(),'ps':ps.tolist(),'uvmin':uvmin.round(6).tolist(),'uvs':uvs.tolist(),
      'bones':bones,'groups':groups,
      'pos':b64(q),'nrm':b64(qn),'uv':b64(quv),'col':b64(qc),'si':b64(idx.astype(np.uint8)),'sw':b64(wq.astype(np.uint8)),
      'idx':b64(T.astype(np.uint16 if len(P)<65536 else np.uint32)),'i32':int(len(P)>=65536)}
hdr=('/* Santos Dumont (1,52 m) para "14 Bis do Dumont" — malha com esqueleto gerada no Blender a partir do\n'
     '   "Human Base Meshes" (Blender Studio, CC0), esculpida e vestida por script: terno risca-de-giz, colarinho alto,\n'
     '   gravata xadrez, panamá desabado, bigode, relógio Cartier Santos no pulso esquerdo. Gerado automaticamente. */\n')
open(OUT,'w',encoding='utf-8').write(hdr+'window.SD_MODEL='+json.dumps(data,separators=(',',':'))+';\n')
import os; print('wrote',OUT,os.path.getsize(OUT)//1024,'KB',time.time()-t0)
