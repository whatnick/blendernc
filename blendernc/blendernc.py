# Imports
import bpy
from collections import defaultdict

import nodeitems_utils

from blendernc.blendernc.panels import BlenderNC_UI_PT_3dview, BlenderNC_LOAD_OT_On, \
                     BlenderNC_LOAD_OT_Off

from blendernc.blendernc.operators import BlenderNC_OT_ncload, BlenderNC_OT_ncload_Sui, BlenderNC_OT_var, \
                        BlenderNC_OT_netcdf2img, BlenderNC_OT_preloader,\
                        BlenderNC_OT_apply_material, ImportnetCDFCollection,\
                        Import_OT_mfnetCDF, BlenderNC_OT_compute_range, BlenderNC_OT_colorbar
                        

# from . nodes import BlenderNC_NT_netcdf, BlenderNC_NT_preloader,\
#                     BlenderNC_NT_resolution, BlenderNC_NT_output,\
#                     BlenderNC_NT_select_axis, BlenderNC_NT_path

from . nodes.node_categories import node_categories

from blendernc.blendernc.nodes.inputs.BlenderNC_NT_path import BlenderNC_NT_path
from blendernc.blendernc.nodes.inputs.BlenderNC_NT_netcdf import BlenderNC_NT_netcdf
from blendernc.blendernc.nodes.inputs.BlenderNC_NT_range import BlenderNC_NT_range
from blendernc.blendernc.nodes.grid.BlenderNC_NT_resolution import BlenderNC_NT_resolution
from blendernc.blendernc.nodes.grid.BlenderNC_NT_rotate_lon import BlenderNC_NT_rotatelon
from blendernc.blendernc.nodes.selecting.BlenderNC_NT_select_axis import BlenderNC_NT_select_axis
from blendernc.blendernc.nodes.selecting.BlenderNC_NT_select_time import BlenderNC_NT_select_time
from blendernc.blendernc.nodes.selecting.BlenderNC_NT_drop_dims import BlenderNC_NT_drop_dims

from blendernc.blendernc.nodes.math.BlenderNC_NT_transpose import BlenderNC_NT_transpose
from blendernc.blendernc.nodes.math.BlenderNC_NT_derivatives import BlenderNC_NT_derivatives
from blendernc.blendernc.nodes.math.BlenderNC_NT_math import BlenderNC_NT_math

from blendernc.blendernc.nodes.outputs.BlenderNC_NT_output import BlenderNC_NT_output
from blendernc.blendernc.nodes.outputs.BlenderNC_NT_preloader import BlenderNC_NT_preloader

from blendernc.blendernc.nodes.shortcuts.BlenderNC_NT_basic_nodes import BlenderNC_NT_basic_nodes
        
from blendernc.blendernc.nodes.node_tree import create_new_node_tree, BlenderNCNodeTree,\
                        node_tree_name

from blendernc.blendernc.sockets import bNCnetcdfSocket,bNCstringSocket

from blendernc.blendernc.nodes.cmaps.cmapsnode import BLENDERNC_CMAPS_NT_node

from . handlers import update_all_images

classes = [
    # Panels
    BlenderNC_UI_PT_3dview,
    BlenderNC_LOAD_OT_On,
    BlenderNC_LOAD_OT_Off,
    # Nodes
    BlenderNC_NT_path,
    BlenderNC_NT_netcdf,
    BlenderNC_NT_range,
    BlenderNC_NT_resolution,
    BlenderNC_NT_rotatelon,
    BlenderNC_NT_select_axis,
    BlenderNC_NT_select_time,
    BlenderNC_NT_drop_dims,
    BlenderNC_NT_math,
    BlenderNC_NT_transpose,
    BlenderNC_NT_derivatives,
    BlenderNC_NT_preloader,
    BlenderNC_NT_output,
    # Nodes shortcuts
    BlenderNC_NT_basic_nodes,
    # Shader Nodes 
    BLENDERNC_CMAPS_NT_node,
    # Operators: files
    ImportnetCDFCollection,
    Import_OT_mfnetCDF,
    # Operators
    BlenderNC_OT_ncload,
    BlenderNC_OT_ncload_Sui,
    BlenderNC_OT_var,
    BlenderNC_OT_netcdf2img,
    BlenderNC_OT_preloader,
    BlenderNC_OT_apply_material,
    BlenderNC_OT_compute_range,
    BlenderNC_OT_colorbar,
    # Sockets
    bNCnetcdfSocket,
    bNCstringSocket,
]

if create_new_node_tree:
    classes.append(BlenderNCNodeTree)

handlers = bpy.app.handlers


def registerBlenderNC():
    bpy.types.Scene.update_all_images = update_all_images

    #bpy.types.Scene.nc_dictionary = defaultdict(None)
    bpy.types.Scene.nc_cache = defaultdict(None)
    # Register handlers
    handlers.frame_change_pre.append(bpy.types.Scene.update_all_images)
    handlers.render_pre.append(bpy.types.Scene.update_all_images)

    # Register node categories
    nodeitems_utils.register_node_categories(node_tree_name, node_categories)

    for cls in classes:
        bpy.utils.register_class(cls)


def unregisterBlenderNC():
    #del bpy.types.Scene.nc_dictionary
    del bpy.types.Scene.update_all_images
    del bpy.types.Scene.nc_cache

    # Delete from handlers
    handlers.frame_change_pre.remove(update_all_images)
    handlers.render_pre.remove(update_all_images)
    # del bpy.types.Scene.nc_file_path

    nodeitems_utils.unregister_node_categories(node_tree_name)

    for cls in classes:
        bpy.utils.unregister_class(cls)
