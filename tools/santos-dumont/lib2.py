# utilidades do estágio 2 (roupas / acessórios)
import sys; sys.path.insert(0,__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from common import *
import json
from mathutils.bvhtree import BVHTree
from mathutils.interpolate import poly_3d_calc

def ss(e0,e1,x):
    t=np.clip((np.asarray(x,float)-e0)/(e1-e0),0,1); return t*t*(3-2*t)

class Body:
    def __init__(s,obj,joints):
        s.obj=obj; me=obj.data
        s.V=verts(obj); s.polys=[tuple(p.vertices) for p in me.polygons]
        s.bvh=BVHTree.FromPolygons([tuple(v) for v in s.V],s.polys)
        s.bones=list(joints.keys()); s.bi={n:i for i,n in enumerate(s.bones)}
        s.J={k:(Vector(h),Vector(t)) for k,(h,t) in joints.items()}
        gi={g.index:g.name for g in obj.vertex_groups}
        W=np.zeros((len(s.V),len(s.bones)))
        for v in me.vertices:
            for g in v.groups:
                n=gi[g.group]
                if n in s.bi: W[v.index,s.bi[n]]=g.weight
        z=W.sum(1)==0
        if z.any():   # sem peso: osso mais próximo
            for i in np.where(z)[0]:
                p=Vector(s.V[i]); best=min(s.bones,key=lambda n:seg_dist(p,*s.J[n])); W[i,s.bi[best]]=1
        s.W=W/W.sum(1,keepdims=True); s.dom=s.W.argmax(1)
        fs=face_sets(obj); s.fs=fs
        s.fc=np.array([p.center[:] for p in me.polygons])
        s.fdom=np.array([s.dom[p[0]] for p in s.polys])
    def domname(s,i): return s.bones[s.dom[i]]
    def xfer(s,P):
        out=np.zeros((len(P),len(s.bones)))
        for i,p in enumerate(P):
            loc,nrm,fi,d=s.bvh.find_nearest(Vector(p))
            pv=s.polys[fi]; w=poly_3d_calc([Vector(s.V[j]) for j in pv],loc)
            for j,wj in zip(pv,w): out[i]+=wj*s.W[j]
        return out/np.maximum(out.sum(1,keepdims=True),1e-9)
    def ray(s,o,d,far=1.0):
        loc,nrm,fi,dist=s.bvh.ray_cast(Vector(o),Vector(d).normalized(),far)
        return loc,nrm
    def near(s,p):
        loc,nrm,fi,d=s.bvh.find_nearest(Vector(p)); return loc,nrm

def seg_dist(p,a,b):
    ab=b-a; t=max(0,min(1,(p-a).dot(ab)/ab.length_squared)); return (a+ab*t-p).length
def seg_t(P,a,b):
    a=np.array(a); b=np.array(b); ab=b-a
    return ((P-a)@ab)/ab.dot(ab)

def bm_from_faces(obj,mask):
    bm=bmesh.new(); bm.from_mesh(obj.data); bm.faces.ensure_lookup_table()
    bmesh.ops.delete(bm,geom=[f for f in bm.faces if not mask[f.index]],context='FACES')
    bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table(); bm.faces.ensure_lookup_table()
    return bm

def shell(bm,B,dfun,iters=20,lam=0.55,extra=0.0):
    """desloca a região para fora e alisa, mantendo distância mínima do corpo (pano esticado)"""
    bm.normal_update(); bm.verts.ensure_lookup_table()
    P=np.array([v.co[:] for v in bm.verts]); N=np.array([v.normal[:] for v in bm.verts])
    d=dfun(P); P=P+N*d[:,None]
    E=np.array([[e.verts[0].index,e.verts[1].index] for e in bm.edges])
    deg=np.bincount(E.ravel(),minlength=len(P)).astype(float)
    for it in range(iters):
        Sm=np.zeros_like(P); np.add.at(Sm,E[:,0],P[E[:,1]]); np.add.at(Sm,E[:,1],P[E[:,0]])
        P=P+lam*(Sm/np.maximum(deg,1)[:,None]-P)
        for i in range(len(P)):
            loc,nrm,fi,dist=B.bvh.find_nearest(Vector(P[i]))
            sd=(Vector(P[i])-loc).dot(nrm)
            if sd<d[i]: P[i]+=np.array(nrm)*(d[i]-sd)
    for v,p in zip(bm.verts,P): v.co=p
    bm.normal_update()
    if extra:
        for v in bm.verts: v.co+=v.normal*extra
    return bm

def bisect_keep(bm,co,no):
    """corta pelo plano e apaga o lado positivo (na direção da normal)"""
    geom=bm.verts[:]+bm.edges[:]+bm.faces[:]
    bmesh.ops.bisect_plane(bm,geom=geom,dist=1e-6,plane_co=co,plane_no=no,clear_outer=True)
    bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table()

def to_obj(name,bm_or_data,mat=None,col=(0.5,0.5,0.5,1)):
    me=bpy.data.meshes.new(name)
    if isinstance(bm_or_data,bmesh.types.BMesh): bm_or_data.to_mesh(me)
    else:
        Vv,F=bm_or_data; me.from_pydata([tuple(map(float,v)) for v in Vv],[],[tuple(map(int,f)) for f in F])
    me.update()
    o=bpy.data.objects.new(name,me); bpy.context.scene.collection.objects.link(o)
    m=bpy.data.materials.get(mat or name)
    if not m:
        m=bpy.data.materials.new(mat or name); m.diffuse_color=col
    me.materials.append(m)
    for p in me.polygons: p.use_smooth=True
    return o

def hull2d(P):
    P=np.unique(np.round(P,6),axis=0)
    if len(P)<3: return P
    P=P[np.lexsort((P[:,1],P[:,0]))]
    def cross(o,a,b): return (a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0])
    lo=[];up=[]
    for p in P:
        while len(lo)>=2 and cross(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(tuple(p))
    for p in P[::-1]:
        while len(up)>=2 and cross(up[-2],up[-1],p)<=0: up.pop()
        up.append(tuple(p))
    return np.array(lo[:-1]+up[:-1])

def poly_radius(H,c,ang):
    """raio do polígono convexo H a partir de c na direção ang (0 = frente -y, pi/2 = +x)"""
    d=np.array([math.sin(ang),-math.cos(ang)]); best=0
    n=len(H)
    for i in range(n):
        a=H[i]-c; b=H[(i+1)%n]-c; e=b-a
        den=d[0]*(-e[1])-d[1]*(-e[0])
        if abs(den)<1e-12: continue
        t=(a[0]*(-e[1])-a[1]*(-e[0]))/den
        u=(d[0]*a[1]-d[1]*a[0])/den
        if t>0 and -1e-9<=u<=1+1e-9: best=max(best,t)
    return best

def loft(rings,closed=True):
    """rings: lista de arrays (n,3) com mesmo n; retorna verts, faces"""
    R=len(rings); n=len(rings[0]); Vv=np.concatenate(rings); F=[]
    m=n if closed else n-1
    for r in range(R-1):
        for i in range(m):
            j=(i+1)%n
            F.append((r*n+i,r*n+j,(r+1)*n+j,(r+1)*n+i))
    return Vv,F
