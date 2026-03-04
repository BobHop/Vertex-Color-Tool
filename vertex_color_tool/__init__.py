bl_info = {
    "name": "Vertex Color Tool",
    "blender": (4, 5, 3),
    "category": "Mesh",
    "version": (1, 0, 0),
    "author": "BobHop",
    "description": "Apply an RGBA color to selected vertices"
}

import bpy
from bpy import context

class MESH_OT_assign_vertex_color(bpy.types.Operator):
    """Apply an RGBA color to selected vertices"""
    bl_idname = "mesh.assign_vertex_color"
    bl_label = "Apply Color"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        obj = context.active_object
        
        if obj is None or obj.type != 'MESH':
            self.report({'ERROR'}, "No active mesh object")
            return {'CANCELLED'}
        
        mesh = obj.data
        color_value = context.scene.vertex_color_value
        attribute_name = "Color"
        
        # Passer en mode objet si nécessaire
        was_in_edit = context.mode == 'EDIT_MESH'
        if was_in_edit:
            bpy.ops.object.mode_set(mode='OBJECT')
        
        # Créer l'attribut s'il n'existe pas
        if attribute_name not in mesh.color_attributes:
            mesh.color_attributes.new(name=attribute_name, type='FLOAT_COLOR', domain='POINT')
        
        color_attr = mesh.color_attributes[attribute_name]
        color_data = color_attr.data
        
        # Récupérer les indices des vertex sélectionnés
        selected_indices = [v.index for v in mesh.vertices if v.select]
        
        # Assigner la couleur (R, G, B, A)
        for idx in selected_indices:
            color_data[idx].color = color_value
        
        self.report({'INFO'}, f"Color applied to {len(selected_indices)} vertices")
        
        # Revenir en mode édition si on y était
        if was_in_edit:
            bpy.ops.object.mode_set(mode='EDIT')
        
        return {'FINISHED'}


class MESH_PT_vertex_color_panel(bpy.types.Panel):
    """This panel applies a color to vertices"""
    bl_label = "Vertex Color"
    bl_idname = "MESH_PT_vertex_color"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    
    def draw(self, context):
        layout = self.layout
        
        # Sélecteur de couleur RGBA
        row = layout.row()
        row.label(text="Color:")
        row.prop(context.scene, "vertex_color_value", text="")
        
        # Bouton pour assigner
        layout.operator("mesh.assign_vertex_color", text="Apply Color", icon='CHECKMARK')


# Enregistrer les classes
def register():
    bpy.utils.register_class(MESH_OT_assign_vertex_color)
    bpy.utils.register_class(MESH_PT_vertex_color_panel)
    
    # Ajouter la propriété de scène (couleur RGBA)
    bpy.types.Scene.vertex_color_value = bpy.props.FloatVectorProperty(
        name="Vertex Color",
        description="RGBA color to apply to vertices",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 1.0)  # Blanc opaque par défaut
    )


def unregister():
    bpy.utils.unregister_class(MESH_OT_assign_vertex_color)
    bpy.utils.unregister_class(MESH_PT_vertex_color_panel)
    
    del bpy.types.Scene.vertex_color_value


if __name__ == "__main__":
    register()
