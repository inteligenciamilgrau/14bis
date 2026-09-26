import bpy, bmesh, numpy as np, math, mathutils, sys
from mathutils import Vector, Matrix
import os
# pasta de trabalho (blends intermediários, json de juntas, saída .js): SD_WORK ou ./build ao lado dos scripts
S=os.environ.get("SD_WORK") or os.path.join(os.path.dirname(os.path.abspath(__file__)),"build")
os.makedirs(S,exist_ok=True); S=S.replace("\\","/").rstrip("/")+"/"
def ctx(o):
    return bpy.context.temp_override(object=o, active_object=o, selected_objects=[o], selected_editable_objects=[o])
def load_base(level=1):
    keep={'GEO-body_male_realistic','GEO-body_male_realistic.eye.L','GEO-body_male_realistic.eye.R'}
    for o in list(bpy.data.objects):
        if o.name not in keep: bpy.data.objects.remove(o,do_unlink=True)
    for c in list(bpy.data.collections):
        bpy.data.collections.remove(c)
    body=bpy.data.objects['GEO-body_male_realistic']; body.name='body'
    eL=bpy.data.objects['GEO-body_male_realistic.eye.L']; eL.name='eyeL'
    eR=bpy.data.objects['GEO-body_male_realistic.eye.R']; eR.name='eyeR'
    dx=-body.location.x
    for o in (body,eL,eR):
        if o.name not in bpy.context.scene.collection.objects: bpy.context.scene.collection.objects.link(o)
        o.animation_data_clear()
        mw=o.matrix_world.copy(); o.parent=None; o.matrix_world=mw
    for o in (body,eL,eR):
        for m in list(o.modifiers):
            if m.type=='MULTIRES':
                m.levels=level
                with ctx(o): bpy.ops.object.modifier_apply(modifier=m.name)
            else: o.modifiers.remove(m)
        o.data=o.data.copy()
        o.data.transform(Matrix.Translation((dx,0,0))@o.matrix_world); o.matrix_world=Matrix.Identity(4)
    return body,eL,eR
def verts(o):
    me=o.data; a=np.empty(len(me.vertices)*3,np.float64); me.vertices.foreach_get('co',a); return a.reshape(-1,3)
def set_verts(o,a):
    o.data.vertices.foreach_set('co',a.astype(np.float64).ravel()); o.data.update()
def face_sets(o):
    me=o.data; fs=me.attributes['.sculpt_face_set']; a=np.zeros(len(me.polygons),np.int32); fs.data.foreach_get('value',a); return a
def vert_sets(o):
    """dict faceset -> set of vertex indices"""
    me=o.data; fs=face_sets(o)
    lt=np.zeros(len(me.polygons),np.int32); me.polygons.foreach_get('loop_total',lt)
    ls=np.zeros(len(me.polygons),np.int32); me.polygons.foreach_get('loop_start',ls)
    lv=np.zeros(len(me.loops),np.int32); me.loops.foreach_get('vertex_index',lv)
    d={}
    for fi in range(len(fs)):
        d.setdefault(int(fs[fi]),set()).update(lv[ls[fi]:ls[fi]+lt[fi]].tolist())
    return d
