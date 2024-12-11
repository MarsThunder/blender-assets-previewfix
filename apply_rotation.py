
bl_info = {
    "name": "Correct Asset Display",
    "author": "Marshall Flynn",
    "version": (1, 0, 0),
    "blender": (4, 2, 0),
    "category": "Assets",
}


import bpy
from math import radians
import os

anum = 0

class AROperator(bpy.types.Operator):
    """Creates a Button in the Asset Menu"""
    bl_label = "Asset Thumbnail Adjust"
    bl_idname = "asset.adjust"
    bl_options = {'REGISTER', 'UNDO'}
    #  Any Variables here
    
    def execute(self, context):
        onum = 0
        # Iterate through all objects in the current scene
        # #  Comment out here --------------------------------------------------------------------------------------------------------------------------------------------------
       
        bpy.ops.object.select_all(action='DESELECT')
        print("Current Scene: ", str(bpy.context.scene))
        print("Starting Context Attributes: ", str(dir(bpy.context)))
        for obj in bpy.context.scene.objects:
            # Ensure the object is rotatable (skip lights, cameras, etc., if needed)
            # For testing, lets stop at 4:
            onum = onum + 1
            print("Object: ", str(obj.name))
            if obj.type in {'MESH', 'CURVE', 'SURFACE', 'META', 'FONT'}:
                # Apply rotation transformation like Ctrl-A
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                bpy.ops.object.make_single_user(object=True, obdata=True)
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=False)
                #print("Object Set!")
                obj.select_set(False)
        print("Set Rotation on this many objects: ", str(onum))
                


        print("Setting Assets Thumbnails.......")
        # print("Current Context Space Data Type: ", str(bpy.context.space_data.type))
        for screen in bpy.data.screens:
            # print("Screen: ", str(screen.name))
            if screen.name == "Layout":
                print("We have Layout Screen Type................................")
                for area in bpy.context.screen.areas:     # was screen.areas:
                    print("=====================================================")
                    print("Current Context Space Data Type: ", str(bpy.context.space_data.type))                   
                    print("Area Type: ", str(area.ui_type))
                    if area.ui_type == "ASSETS":
                        for thespace in area.spaces:
                            
                            if thespace.type == "FILE_BROWSER":
                                area_type = "FILE_BROWSER"
                                override = {'area': area}
                                # print("----------------------------------------------------")
                                print("Space Context Mode: ", str(thespace.type))
                                print("We are in ASSETS BROWSER Area...............................")
                                active_space = area.spaces.active
                                bpy.context.area.type = "FILE_BROWSER"
                                bpy.context.area.ui_type = "ASSETS"
                                # bpy.ops.wm.context_set_id(override, id='space_data', type='area_type')
                                print("Active Space: ", str(active_space))
                               
                                active_space.params.asset_library_reference = "LOCAL"
                                active_space.browse_mode = "ASSETS"
                                bpy.context.space_data.browse_mode = "ASSETS"
                                print("Space Data Browse Mode: ", str(bpy.context.space_data.browse_mode))
                                print("Space Data Operator: ", str(bpy.context.space_data.operator))
                                print("New Context Space Data Type: ", str(bpy.context.space_data.type))
                                # bpy.context.space_data.params.asset_library_reference = "LOCAL"
                                

                    
                        
                        

        if isinstance(active_space, bpy.types.SpaceFileBrowser) and active_space.browse_mode == 'ASSETS':
            global anum
            params = active_space.params
            # print("Params Attributes: ", str(dir(params)))
            print(" ")
            if isinstance(params, bpy.types.FileAssetSelectParams):
                # Access the linked asset library
                asset_library_ref = params.asset_library_reference
                print("Asset Library: ", str(asset_library_ref))
            # print("Context Attributes: ", str(dir(bpy.context)))
            print(" ")
            # print("Params Filename: ", str(params.filename))
            for assobj in bpy.data.objects:
                if assobj.asset_data:
                    anum = anum + 1
                    print("Asset Found: ", str(assobj.name))
                    print("Asset Type: ", str(assobj.id_type))
                    # print("Asset Data: ", str(assobj.asset_data))
                    # print("Asset Original: ", str(assobj.original))
                    # print("Asset Library: ", str(assobj.library))
                    # print("Asset Full Name: ", str(assobj.name_full))
                    bpy.context.view_layer.objects.active = assobj
                    assobj.select_set(True)
                    # print("Context Asset Mode: ", str(bpy.context.mode))
                    # print("Blend Data: ", str(bpy.context.blend_data))
                    print(f"Selected Object: {bpy.context.selected_objects}")
                    # print(f"Selected Asset: {bpy.context.selected_assets}")
                    # print(f"Active File: {bpy.context.active_file}")
                    # print(f"Asset Library Path: {bpy.context.asset}")
                    # bpy.ops.ed.lib_id_generate_preview()
                    assobj.asset_generate_preview()
                    assobj.select_set(False)
            print("Assets adjusted for rotation: ", str(anum))
        #bpy.context.area.ui_type = "TEXT_EDITOR"
        return {'FINISHED'}

# End Temporary Comment -------------------------------------------------------------------------------------------------


def put_menu(self, context):
    self.layout.operator(AROperator.bl_idname)

def register():
    bpy.utils.register_class(AROperator)
    bpy.types.ASSETBROWSER_MT_asset.append(put_menu)

def unregister():
    bpy.utils.unregister_class(AROperator)
    bpy.types.VIEW3D_MT_object.remove(put_menu)

if __name__ == "__main__":
    register()
