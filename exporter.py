"""
Copyright 2025 Barcelli Pte Ltd

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import os
import csv
import bpy


bl_info = {
        "name":  "B2UE Scene Exporter",
        "author":  "Rodolfo Barcelli Jo",
        "description":  "Export Scenes to Unreal Live",
        "version": (1,1,0),
        "location":  "View3D > Sidebar > B2UE",
        "category":  "B2UE",
        "support":  "COMMUNITY",
        "blender":  (4,3,2)
        }

class B2UE_UI(bpy.types.Panel):
    bl_label = "Blender to UE"
    bl_idname = "B2UEUI"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "B2UE"

    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Something")
        row.operator("b2ue.export_button")

def get_meshes():
    meshes = []
    for obj in bpy.context.selected_objects:
        if obj.type == 'MESH':
            meshes.append(obj)
    return meshes

def export_locations(meshes, save_dir):
    header = ['name', 'data', 'tx', 'ty', 'tz', 'sx', 'sy', 'sz', 'rx', 'ry', 'rz']
    locations = []
    locations.append(header)
    for obj in meshes:
        entry = []

        # Add object name and data to entry
        entry.append(obj.name)
        entry.append(obj.data.name)

        objLocation = obj.location
        # Fix units
        objLocation = [coord * 100 for coord in objLocation]
        for coord in objLocation:
            entry.append(coord)

        objScale = obj.scale
        for scale in objScale:
            entry.append(scale)

        # NOTE: This is in radian
        objRotation = obj.rotation_euler
        for rot in objRotation:
            entry.append(rot)

        locations.append(entry)

    with open(os.path.join(save_dir, "location_data.csv"), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(locations)

def get_instanced_mesh_data(meshes):
    data = []
    for obj in meshes:
        data.append(obj.data)

    data = list(set(data)) 
    return data

def export_data(data, save_dir):
    exportCollection = bpy.data.collections.new(name="forexport")
    bpy.context.scene.collection.children.link(exportCollection)

    for obj in data:
        exportObj = bpy.data.objects.new(name=obj.name, object_data=obj)
        exportCollection.objects.link(exportObj)
        exportObj.location = (0.0, 0.0, 0.0)
        exportObj.scale= (1.0, 1.0, 1.0)
        exportObj.rotation_euler= (0.0, 0.0, 0.0)
        print(obj.name)

    for obj in exportCollection.objects:
        # Deselect all objects
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        export_path = os.path.join(save_dir, f"{obj.data.name}.fbx")

        bpy.ops.export_scene.fbx(
                filepath=export_path,
                use_selection=True,
                path_mode='COPY',
                embed_textures=True,
                axis_up='Z',
                axis_forward='X'
                )
        bpy.ops.object.delete()
        
    bpy.data.collections.remove(exportCollection)

class B2UE_StartServerButton(bpy.types.Operator):
    bl_idname = "b2ue.start_server"
    bl_label = "Start Connection"

class B2UE_ExportButton(bpy.types.Operator):
    bl_idname = "b2ue.export_button"
    bl_label = "Export Meshes"

    def execute(self, context):
        basedir = os.path.dirname(bpy.data.filepath)
        if not basedir:
            raise Exception("Blend file not saved")

        meshes = get_meshes()
        data = get_instanced_mesh_data(meshes)
        export_data(data, basedir)
        export_locations(meshes, basedir)
        print("done")
        return {"FINISHED"}

def register():
    bpy.utils.register_class(B2UE_UI)
    bpy.utils.register_class(B2UE_ExportButton)
    bpy.utils.register_class(B2UE_StartServerButton)

def unregister():
    bpy.utils.unregister_class(B2UE_UI)
    bpy.utils.unregister_class(B2UE_ExportButton)
    bpy.utils.unregister_class(B2UE_StartServerButton)

if __name__ == "__main__":
    register()
