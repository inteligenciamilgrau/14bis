# render helpers
import bpy, math, mathutils
def setup(engine='BLENDER_WORKBENCH', res=(640,640)):
    sc=bpy.context.scene
    sc.render.engine=engine
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage=100
    sc.render.film_transparent=False
    if engine=='BLENDER_WORKBENCH':
        sh=sc.display.shading
        sh.light='STUDIO'; sh.color_type='MATERIAL'; sh.show_cavity=True; sh.cavity_type='BOTH'
        sh.show_shadows=False; sh.show_specular_highlight=True
    else:
        w=bpy.data.worlds.new('W') if not sc.world else sc.world
        sc.world=w; w.use_nodes=True
        bg=w.node_tree.nodes.get('Background'); bg.inputs[0].default_value=(0.55,0.6,0.68,1); bg.inputs[1].default_value=0.8
        # key + rim lights
        for n,loc,en,col in [('Key',(-1.5,-2.2,2.6),450,(1,0.96,0.9)),('Fill',(2.2,-1.5,1.4),150,(0.8,0.85,1)),('Rim',(0.5,2.5,2.4),300,(1,1,1))]:
            if n in bpy.data.objects: continue
            ld=bpy.data.lights.new(n,'AREA'); ld.energy=en; ld.size=1.5; ld.color=col
            lo=bpy.data.objects.new(n,ld); bpy.context.collection.objects.link(lo); lo.location=loc
            d=mathutils.Vector((0,0,1.1))-lo.location; lo.rotation_euler=d.to_track_quat('-Z','Y').to_euler()
    return sc
def cam_shot(path, target, dist, az_deg=0, el_deg=5, lens=85):
    sc=bpy.context.scene
    cam=bpy.data.objects.get('ShotCam')
    if not cam:
        cd=bpy.data.cameras.new('ShotCam'); cam=bpy.data.objects.new('ShotCam',cd); bpy.context.collection.objects.link(cam)
    cam.data.lens=lens; cam.data.clip_start=0.01
    t=mathutils.Vector(target); az=math.radians(az_deg); el=math.radians(el_deg)
    # az=0 -> camera in front (-Y side) looking +Y
    cam.location=t+mathutils.Vector((math.sin(az)*math.cos(el)*dist, -math.cos(az)*math.cos(el)*dist, math.sin(el)*dist))
    cam.rotation_euler=(t-cam.location).to_track_quat('-Z','Y').to_euler()
    sc.camera=cam; sc.render.filepath=path
    bpy.ops.render.render(write_still=True)
