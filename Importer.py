import bpy
import mathutils
import math
import csv

bl_info = \
    {
        "name" : "Object Importer",
        "author" : "Dylan Blakemore",
        "version" : (1, 0, 0),
        "blender" : (2),
        "location" : "View 3D > Object Mode > Tool Shelf > Create",
        "description" :
            "Import entities from .csv files in (x,y,z) format",
        "warning" : "",
        "wiki_url" : "",
        "tracker_url" : "",
        "category" : "Import Positions",
    }

class ImportRigidSpheresPanel(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_context = "objectmode"
    bl_category = "Create"
    bl_label = "Import"
    
    def draw(self, context):
        TheCol = self.layout.column(align=True)
        TheCol.operator("rigidbody.import_rigid_spheres", text = "Import Rigid Spheres")
        TheCol.prop(context.scene, "conf_path")
    #end draw

#end ImportRigidSpheresPanel

class ImportRigidSpheres(bpy.types.Operator):
    bl_idname = "rigidbody.import_rigid_spheres"
    bl_label = "Import Rigid Spheres"
    
    def invoke(self, context, event):
        input_file = csv.reader(open("/home/user/Work/Blender/Tumbling Mill/input/mayaPos_0001.dsv","r"))
        #input_file = csv.reader(open(context.scene.conf_path,"r"))
        size_ratio = 1
        i = 0
        
        bpy.ops.object.select_all(action="DESELECT")
        sphere = bpy.context.object
        
        for row in input_file:
            i_location = (float(row[0])/size_ratio, float(row[2])/size_ratio, float(row[1])/size_ratio)
            if i == 0:
                bpy.ops.mesh.primitive_uv_sphere_add(segments=16, 
                                                     ring_count=8, 
                                                     size=0.5/size_ratio, 
                                                     location=i_location)
                sphere = bpy.context.object
                bpy.ops.rigidbody.object_add(type='ACTIVE')
                bpy.ops.rigidbody.shape_change(type='SPHERE')
                sphere.rigid_body.use_margin = True
                sphere.rigid_body.collision_margin = 0.05
            else:
                ob = sphere.copy()
                bpy.context.scene.rigidbody_world.group.objects.link(ob)
                bpy.context.scene.objects.link(ob)
                ob.location = i_location
                
            #end if
            i = i + 1
        #end for
        bpy.context.scene.update()
        return {"FINISHED"}
    
    #end invoke
#end ImportRigidSpheres

def register():
    bpy.utils.register_class(ImportRigidSpheres)
    bpy.utils.register_class(ImportRigidSpheresPanel)
    bpy.types.Scene.conf_path = bpy.props.StringProperty \
      (
      name = "File",
      default = "",
      description = "Define the root path of the project",
      subtype = 'FILE_PATH'
      )
    
def unregister():
    bpy.utils.unregister_class(ImportRigidSpheres)
    bpy.utils.unregister_class(ImportRigidSpheresPanel)
    
if __name__ == "__main__":
    register()
