import bpy, bmesh  
from mathutils import Vector

from bpy.app.handlers import persistent
bl_info = {
    'name': 'Extrude Vertices in all directions',
    'author': 'Lorenzo Bruni Pirani',
    'version': '1.',
    'blender': (2, 7, 5),
    'location': '3D View',
    'description': 'Toggle Render and Visibility',
    'url': 'http://www.parameciostudio.com',
    'category': 'Mesh'}

class PMS_AllDirectionsPanel(bpy.types.Panel):
    """Exturde seleceted vertices in all directions"""
    bl_label = "Extrude in all directions Panel"
    bl_idname = "PMS_AllDirectionsPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
 
    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="EXTRUDE IN ALL DIRECTIONS", icon='MESH_DATA')

        row = layout.row()
        row.prop(context.scene, "PMS_dist")
        
        row = layout.row()
        row.prop(context.scene, "PMS_toggle")

        row = layout.row()
        row.operator("mesh.extrude_all")
 

class PMS_ExtrudeAll(bpy.types.Operator) :
    bl_idname = "mesh.extrude_all"
    bl_label = "Extrude"
    bl_options = {"UNDO"}

    def invoke(self, context, event) :
        vertex = [(1,0,0),(0,1,0),(0,0,1),(-1,0,0),(0,-1,0),(0,0,-1)]
        obj = bpy.context.object 
        S = bpy.context.scene
        me =  obj.data
        if me.is_editmode:
            bm = bmesh.from_edit_mesh(me)  
            selected=[v for v in bm.verts if v.select]

            bm.verts.ensure_lookup_table();
            i = 0
            print('-----VERTICES-----')
            #loop selected vertices
            for sel in selected:
                for v in vertex:    
                    bm.verts.index_update()
                    tmp = bm.verts.new(Vector(sel.co) + Vector(v)*S.PMS_dist)
                    print(tmp.index)
                bm.verts.ensure_lookup_table();
                print('-----')
                #add edges
                for i in range(0, 6):
                    if not bm.edges.get((bm.verts[-6+i],sel)):
                        bm.verts.index_update()
                        bm.edges.new((bm.verts[-6+i],sel))
                        print(bm.verts[-6+i].index)
                if S.PMS_toggle:
                    for i in range(0, 6):
                        sel.select_set(0)
                        bm.verts[-6+i].select_set(1)
                    
                        
                  
            bmesh.update_edit_mesh(me)  
            

        return {"FINISHED"}
        #end invoke


def register():
    bpy.utils.register_class(PMS_AllDirectionsPanel)
    bpy.utils.register_class(PMS_ExtrudeAll)
    bpy.types.Scene.PMS_dist = bpy.props.FloatProperty \
      (
      name = "Distance",
      description = "Set extrusion value",
      min=0.0,
      default = 1.0
      )
    bpy.types.Scene.PMS_toggle = bpy.props.BoolProperty \
      (
      name = "Select created vertices",
      description = "Select the vertices just created",
      default = True
      )


def unregister():
    bpy.utils.unregister_class(PMS_AllDirectionsPanel)
    bpy.utils.unregister_class(PMS_ExtrudeAll)
    del bpy.types.Scene.PMS_dist
    del bpy.types.Scene.PMS_toggle


if __name__ == "__main__":
    register()
