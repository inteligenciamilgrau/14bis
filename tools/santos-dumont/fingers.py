# dedos: ossos, pesos e eixos de flexão a partir dos face sets de cada falange do "Human Base Meshes"
# (cada falange e cada unha é um face set próprio na malha realista masculina: 3 por dedo + unha)
import numpy as np, math
from mathutils import Vector, Matrix
FS={'L':{'hand':9,'thumb':(80,81,82,83),'index':(76,77,78,79),'middle':(72,73,74,75),'ring':(68,69,70,71),'pinky':(64,65,66,67)},
    'R':{'hand':10,'thumb':(84,85,86,87),'index':(88,89,90,91),'middle':(92,93,94,95),'ring':(96,97,98,99),'pinky':(100,101,102,103)}}
NAMES=('thumb','index','middle','ring','pinky')
# o nó do dedo fica dentro da mão, antes da membrana entre os dedos (onde o face set da falange começa);
# o polegar gira desde a base, junto do pulso (articulação carpo-metacarpal)
BACK={'thumb':1.1,'index':0.45,'middle':0.45,'ring':0.45,'pinky':0.45}
def bone_names(sd): return [f'{f}{k}.{sd}' for f in NAMES for k in (1,2,3)]
def _ring(V,vs,a,b):
    s=vs.get(a,set())&vs.get(b,set())
    return V[sorted(s)].mean(0) if s else None
def chains(V,vs):
    """(lado,dedo) -> dict(j=[base,j1,j2,ponta], ax=eixo de flexão (+ = dobra para a palma), pw=direção da palma)"""
    out={}
    for sd in ('L','R'):
        H=FS[sd]['hand']
        for f in NAMES:
            s1,s2,s3,nl=FS[sd][f]
            j0=_ring(V,vs,H,s1); j1=_ring(V,vs,s1,s2); j2=_ring(V,vs,s2,s3)
            if j0 is None:                      # sem fronteira com a palma: usa a borda da falange mais próxima do pulso
                P1=V[sorted(vs[s1])]; d=(j2-j1)/np.linalg.norm(j2-j1); j0=j1-d*((j1-P1)@d).max()
            d=(j2-j1)/np.linalg.norm(j2-j1)
            P=V[sorted(vs[s3]|vs[nl])]; tip=j2+d*((P-j2)@d).max()
            j0=j0+(j0-j1)*BACK[f]
            nail=V[sorted(vs[nl])].mean(0); dist=V[sorted(vs[s3])].mean(0)
            dr=(tip-j1)/np.linalg.norm(tip-j1)
            pw=dist-nail; pw=pw-dr*pw.dot(dr); pw/=np.linalg.norm(pw)
            ax=np.cross(dr,pw); ax/=np.linalg.norm(ax)
            out[(sd,f)]=dict(j=[np.array(j0),np.array(j1),np.array(j2),np.array(tip)],ax=ax,pw=pw,dr=dr)
        # unha e ponta do dedo ficam a 4 mm: a direção da palma de um dedo só é ruidosa → média dos quatro dedos
        n=sum(out[(sd,f)]['pw'] for f in NAMES[1:]); n/=np.linalg.norm(n)
        for f in NAMES[1:]:
            c=out[(sd,f)]; pw=n-c['dr']*n.dot(c['dr']); pw/=np.linalg.norm(pw)
            ax=np.cross(c['dr'],pw); c['pw']=pw; c['ax']=ax/np.linalg.norm(ax)
    return out
def ss(e0,e1,x):
    t=np.clip((np.asarray(x,float)-e0)/(e1-e0),0,1); return t*t*(3-2*t)
def _chain_param(P,Q):
    """posição ao longo da cadeia (s, o primeiro segmento se estende para trás) e distância radial"""
    L=[np.linalg.norm(Q[k+1]-Q[k]) for k in range(3)]; cum=[0,L[0],L[0]+L[1]]
    best_d=np.full(len(P),1e9); best_s=np.zeros(len(P))
    for k in range(3):
        A=Q[k]; D=Q[k+1]-A; t=((P-A)@D)/D.dot(D); t=np.clip(t,-9 if k==0 else 0,1)
        C=A+t[:,None]*D; d=np.linalg.norm(P-C,axis=1); m=d<best_d
        best_d[m]=d[m]; best_s[m]=cum[k]+t[m]*L[k]
    return best_s,best_d,cum,L
def weights(V,vs,CH,W_hand):
    """reparte o peso da mão entre a palma e as 15 falanges. W_hand: {lado: pesos (n,)} → {nome do osso: pesos (n,)}"""
    out={}
    for sd in ('L','R'):
        wh=W_hand[sd]; cand=np.where(wh>1e-4)[0]; P=V[cand]
        own=np.full(len(V),-1)
        for fi,f in enumerate(NAMES):
            for s_ in FS[sd][f]: own[sorted(vs[s_])]=fi
        own=own[cand]
        res=[];
        for fi,f in enumerate(NAMES):
            Q=CH[(sd,f)]['j']; s,d,cum,L=_chain_param(P,Q); res.append((s,d,cum,L))
        # palma: o dedo mais próximo (pela distância radial); falange: o dedo dono do face set
        D=np.stack([r[1] for r in res],1); near=D.argmin(1); fsel=np.where(own>=0,own,near)
        wpalm=np.ones(len(cand)); wb={n:np.zeros(len(cand)) for n in bone_names(sd)}
        for fi,f in enumerate(NAMES):
            m=fsel==fi
            if not m.any(): continue
            s,d,cum,L=res[fi]; s=s[m]; d=d[m]
            hw=[max(0.0035,0.22*L[0]) if f!='thumb' else max(0.006,0.3*L[0]),max(0.003,0.2*min(L[0],L[1])),max(0.003,0.2*min(L[1],L[2]))]
            u0=ss(cum[0]-hw[0],cum[0]+hw[0],s); u1=ss(cum[1]-hw[1],cum[1]+hw[1],s); u2=ss(cum[2]-hw[2],cum[2]+hw[2],s)
            w1=np.clip(u0-u1,0,1); w2=np.clip(u1-u2,0,1); w3=u2
            r0,r1=((0.011,0.024) if f=='thumb' else (0.007,0.013))
            g=np.where(own[m]>=0,1.0,1-ss(r0,r1,d))            # na palma, só perto do dedo
            wf=g*(w1+w2+w3); wpalm[m]=1-wf
            wb[f'{f}1.{sd}'][m]=g*w1; wb[f'{f}2.{sd}'][m]=g*w2; wb[f'{f}3.{sd}'][m]=g*w3
        full=lambda a:(lambda z:(z.__setitem__(cand,a),z)[1])(np.zeros(len(V)))
        out['hand.'+sd]=full(wh[cand]*wpalm)
        for n,a in wb.items(): out[n]=full(wh[cand]*a)
    return out
def rot_about(pb,axis,ang,pivot=None):
    """gira o pose bone em torno de um eixo do espaço da armature, pelo próprio head"""
    import bpy
    M=pb.matrix.copy(); h=(pivot if pivot is not None else M.translation).copy()
    pb.matrix=Matrix.Translation(h)@Matrix.Rotation(ang,4,Vector(axis))@Matrix.Translation(-h)@M
    bpy.context.view_layer.update()
