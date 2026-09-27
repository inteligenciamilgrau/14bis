import sys; sys.path.insert(0,__import__("os").path.dirname(__import__("os").path.abspath(__file__)))
from common import *
import rh
import fingers as FG
body,eL,eR=load_base(1)
V=verts(body); vs=vert_sets(body)
LID=[np.array(sorted(vs[2])),np.array(sorted(vs[3]))]      # pálpebras (2: +x = olho esquerdo)
LID0=[V[i].mean(0) for i in LID]
def ss(e0,e1,x):
    t=np.clip((x-e0)/(e1-e0),0,1); return t*t*(3-2*t)
X,Y,Z=V[:,0].copy(),V[:,1].copy(),V[:,2].copy()
headw=ss(1.40,1.47,Z)
# --- rosto de Santos Dumont: estreito e comprido ---
V[:,0]*=1-0.05*headw                                   # cabeça mais estreita
jaw=ss(1.43,1.47,Z)*(1-ss(1.50,1.545,Z))
V[:,0]*=1-0.09*jaw                                     # mandíbula fina
front=ss(-0.03,-0.09,Y)
V[:,2]-=0.007*ss(1.535,1.465,Z)*front*headw            # terço inferior mais longo (queixo desce)
chin=np.exp(-((X/0.03)**2+((Z-1.462)/0.02)**2))*front
V[:,1]-=0.003*chin                                     # queixo levemente projetado/pontudo
# nariz longo e proeminente
nose=np.exp(-(X/0.02)**2)*ss(-0.118,-0.15,Y)*ss(1.51,1.525,Z)*(1-ss(1.575,1.595,Z))
V[:,1]-=0.005*nose
tip=np.exp(-((X/0.018)**2+((Z-1.537)/0.012)**2))*ss(-0.13,-0.16,Y)
V[:,2]-=0.003*tip; V[:,1]-=0.001*tip
bridge=np.exp(-((X/0.012)**2+((Z-1.575)/0.012)**2))*ss(-0.11,-0.135,Y)
V[:,1]-=0.002*bridge
# bochechas magras
for sg in (1,-1):
    ck=np.exp(-(((sg*X)-0.052)/0.016)**2-((Z-1.515)/0.022)**2)*ss(-0.05,-0.10,Y)
    V[:,0]-=sg*0.0035*ck; V[:,1]+=0.0015*ck
# lábios mais finos (bigode cobre o superior)
lip=np.exp(-((X/0.03)**2+((Z-1.49)/0.01)**2))*ss(-0.12,-0.14,Y)
V[:,1]+=0.0025*lip
# orelhas de abano
for sid,sg in ((4,1),(5,-1)):
    idx=np.array(sorted(vs[sid]))
    p=V[idx]; c=p.mean(0)
    w=np.clip((sg*p[:,0]-0.064)/0.014,0,1)
    a=-sg*math.radians(20)*w
    dx=p[:,0]-(sg*0.066); dy=p[:,1]-(-0.04)
    nx=dx*np.cos(a)-dy*np.sin(a); ny=dx*np.sin(a)+dy*np.cos(a)
    p2=p.copy(); p2[:,0]=sg*0.066+nx; p2[:,1]=-0.04+ny
    sc=1+0.12*w[:,None]; p2=c+(p2-c)*sc
    V[idx]=p2
set_verts(body,V)
# --- esqueleto provisório para repor pose e afinar ---
J={'hips':(0,0,0.86),'spine':(0,-0.02,0.95),'chest':(0,-0.02,1.12),'neck':(0,-0.015,1.41),'head':(0,-0.01,1.51),'headtop':(0,-0.01,1.68),
   'shoulder.L':(0.165,0.0,1.35),'elbow.L':(0.294,0.0,1.09),'wrist.L':(0.376,-0.064,0.882),'handtip.L':(0.405,-0.075,0.79),
   'hip.L':(0.09,0.0,0.85),'knee.L':(0.139,0.017,0.45),'ankle.L':(0.172,0.035,0.075),'toe.L':(0.2,-0.13,0.015)}
for k in list(J):
    if k.endswith('.L'): x,y,z=J[k]; J[k[:-2]+'.R']=(-x,y,z)
bones=[('hips','hips','spine',None),('spine','spine','chest','hips'),('chest','chest','neck','spine'),('neck','neck','head','chest'),('head','head','headtop','neck')]
for s in ('L','R'):
    bones+= [(f'upperarm.{s}',f'shoulder.{s}',f'elbow.{s}','chest'),(f'forearm.{s}',f'elbow.{s}',f'wrist.{s}',f'upperarm.{s}'),(f'hand.{s}',f'wrist.{s}',f'handtip.{s}',f'forearm.{s}'),
             (f'thigh.{s}',f'hip.{s}',f'knee.{s}','hips'),(f'shin.{s}',f'knee.{s}',f'ankle.{s}',f'thigh.{s}'),(f'foot.{s}',f'ankle.{s}',f'toe.{s}',f'shin.{s}')]
# --- dedos: 3 falanges por dedo (o polegar começa no pulso), juntas tiradas dos face sets de cada falange ---
CH=FG.chains(V,vs)
for s in ('L','R'):
    for f in FG.NAMES:
        j=CH[(s,f)]['j']
        for k in range(3): J[f'{f}{k+1}.{s}']=tuple(j[k])
        J[f'{f}tip.{s}']=tuple(j[3])
        bones+=[(f'{f}1.{s}',f'{f}1.{s}',f'{f}2.{s}',f'hand.{s}'),(f'{f}2.{s}',f'{f}2.{s}',f'{f}3.{s}',f'{f}1.{s}'),(f'{f}3.{s}',f'{f}3.{s}',f'{f}tip.{s}',f'{f}2.{s}')]
FINGER=set(n for s in ('L','R') for n in FG.bone_names(s))
ad=bpy.data.armatures.new('rig'); arm=bpy.data.objects.new('rig',ad); bpy.context.scene.collection.objects.link(arm)
bpy.context.view_layer.objects.active=arm
with ctx(arm): bpy.ops.object.mode_set(mode='EDIT')
for n,h,t,p in bones:
    eb=ad.edit_bones.new(n); eb.head=J[h]; eb.tail=J[t]; eb.roll=0
    if p: eb.parent=ad.edit_bones[p]
    eb.inherit_scale='FULL' if n in FINGER else 'NONE'     # dedos acompanham a mão afinada
with ctx(arm): bpy.ops.object.mode_set(mode='OBJECT')
# pesos automáticos (calor)
for o in bpy.context.view_layer.objects: o.select_set(False)
body.select_set(True); arm.select_set(True); bpy.context.view_layer.objects.active=arm
with bpy.context.temp_override(object=arm,active_object=arm,selected_objects=[body,arm],selected_editable_objects=[body,arm]):
    bpy.ops.object.parent_set(type='ARMATURE_AUTO')
# dedos: o calor decide só quanto é "mão" (contra o antebraço); a divisão palma/falanges vem da geometria de cada falange
def vg_array(o,name):
    g=o.vertex_groups.get(name); a=np.zeros(len(o.data.vertices))
    if g is None: return a
    gi=g.index
    for v in o.data.vertices:
        for e in v.groups:
            if e.group==gi: a[v.index]=e.weight
    return a
WH={s:vg_array(body,'hand.'+s)+sum(vg_array(body,n) for n in FG.bone_names(s)) for s in ('L','R')}
FW=FG.weights(V,vs,CH,WH)
for n,a in FW.items():
    g=body.vertex_groups.get(n) or body.vertex_groups.new(name=n)
    g.remove(list(range(len(a))))
    nz=np.where(a>1e-4)[0]
    for i in nz: g.add([int(i)],float(a[i]),'REPLACE')
print("vgroups",[g.name for g in body.vertex_groups])
for e in (eL,eR):
    g=e.vertex_groups.new(name='head'); g.add(list(range(len(e.data.vertices))),1.0,'REPLACE')
    m=e.modifiers.new('arm','ARMATURE'); m.object=arm
# --- pose: braços caídos, pernas juntas, corpo franzino ---
pbs=arm.pose.bones
for pb in pbs: pb.rotation_mode='QUATERNION'
def sc(n,s): pbs[n].scale=s
for n in ('hips',): sc(n,(0.92,1,0.9))
for n in ('spine','chest'): sc(n,(0.88,1,0.88))
sc('neck',(0.86,1,0.86))
for s in ('L','R'):
    sc(f'upperarm.{s}',(0.84,1,0.84)); sc(f'forearm.{s}',(0.86,1,0.86)); sc(f'hand.{s}',(0.92,0.95,0.92))
    sc(f'thigh.{s}',(0.86,1,0.86)); sc(f'shin.{s}',(0.88,1,0.88))
bpy.context.view_layer.update()
def rotw(n,axis,deg):
    pb=pbs[n]; M=pb.matrix.copy(); h=M.translation.copy()
    pb.matrix=Matrix.Translation(h)@Matrix.Rotation(math.radians(deg),4,axis)@Matrix.Translation(-h)@M
    bpy.context.view_layer.update()
for s,sg in (('L',1),('R',-1)):
    rotw(f'upperarm.{s}','Y',sg*14.5)
    rotw(f'forearm.{s}','Y',-sg*2.5)
    rotw(f'forearm.{s}','X',8)      # cotovelo levemente dobrado (mão à frente)
    rotw(f'thigh.{s}','Y',sg*4.2)
    rotw(f'foot.{s}','Y',-sg*4.2)
# ombros estreitos: desloca o braço para dentro
for s,sg in (('L',1),('R',-1)):
    pb=pbs[f'upperarm.{s}']; M=pb.matrix.copy(); M.translation.x-=sg*0.014; M.translation.z-=0.006; pb.matrix=M
    bpy.context.view_layer.update()
# --- mãos relaxadas: os dedos dobram nos próprios ossos (eixo de flexão de cada dedo levado junto com a mão) ---
FAX={}
for s in ('L','R'):
    pbh=pbs['hand.'+s]; Rh=(pbh.matrix.to_3x3()@ad.bones['hand.'+s].matrix_local.to_3x3().inverted())
    for f in FG.NAMES:
        ax=(Rh@Vector(CH[(s,f)]['ax'])).normalized(); pw=(Rh@Vector(CH[(s,f)]['pw'])).normalized()
        for k in (1,2,3): FAX[f'{f}{k}.{s}']={'ax':tuple(ax),'pw':tuple(pw)}
REST={'thumb':(0.05,0.12,0.12),'index':(0.12,0.22,0.12),'middle':(0.16,0.26,0.14),'ring':(0.2,0.3,0.16),'pinky':(0.24,0.34,0.18)}
for s in ('L','R'):
    for f in FG.NAMES:
        for k in (1,2,3): FG.rot_about(pbs[f'{f}{k}.{s}'],FAX[f'{f}{k}.{s}']['ax'],REST[f][k-1])
# juntas finais (espaço da armature)
JP={}
for pb in pbs: JP[pb.name]=(tuple(pb.head),tuple(pb.tail))
for o in (body,eL,eR):
    for m in o.modifiers:
        if m.type=='ARMATURE':
            with ctx(o): bpy.ops.object.modifier_apply(modifier=m.name)
body.parent=None; body.matrix_world=Matrix.Identity(4)
_V1=verts(body)
for e,i,c0 in ((eL,LID[0],LID0[0]),(eR,LID[1],LID0[1])):   # olhos acompanham as pálpebras (escultura + pose)
    pe=verts(e); pe+=(_V1[i].mean(0)-c0)*np.array((1,1,1)); set_verts(e,pe)
# --- escala para 1,52 m ---
zmin=verts(body)[:,2].min(); zmax=verts(body)[:,2].max()
k=1.52/(zmax-zmin); T=Matrix.Translation((0,0,0))@Matrix.Scale(k,4)@Matrix.Translation((0,0,-zmin))
for o in (body,eL,eR): o.data.transform(T); o.data.update()
JS={n:(tuple(T@Vector(h)),tuple(T@Vector(t))) for n,(h,t) in JP.items()}
bpy.data.objects.remove(arm,do_unlink=True)
import json; json.dump({'k':k,'zmin':zmin,'joints':JS,'fingers':FAX},open(S+'joints1.json','w'),indent=1)
print("scale",k,"height",verts(body)[:,2].max())
bpy.ops.wm.save_as_mainfile(filepath=S+'stage1.blend')
rh.setup('BLENDER_WORKBENCH',(600,600))
rh.cam_shot(S+"s1_head_front.png",(0,-0.03,1.40),0.75,0,3,85)
rh.cam_shot(S+"s1_head_side.png",(0,-0.03,1.40),0.75,75,3,85)
rh.cam_shot(S+"s1_body_front.png",(0,0,0.77),4.2,0,4,50)
rh.cam_shot(S+"s1_body_side.png",(0,0,0.77),4.2,90,4,50)
_hc=JS['middle1.L'][0]
rh.cam_shot(S+"s1_hand_side.png",(_hc[0],_hc[1],_hc[2]-0.03),0.5,90,5,50)
rh.cam_shot(S+"s1_hand_front.png",(_hc[0],_hc[1],_hc[2]-0.03),0.5,0,5,50)
