# Imports
import bpy

from blendernc.blendernc.python_functions import (get_new_identifier, get_possible_files, get_possible_variables,
                                dict_update)

from blendernc.blendernc.decorators import NodesDecorators

from collections import defaultdict

class BlenderNC_NT_netcdf(bpy.types.Node):
    # === Basics ===
    # Description string
    '''Node to initiate netCDF dataset using xarray'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'netCDFNode'
    # Label for nice name display
    bl_label = "netCDF input"
    # Icon identifier
    bl_icon = 'UGLYPACKAGE'
    bl_type = "NETCDF"

    blendernc_file: bpy.props.StringProperty()
    
    blendernc_netcdf_vars: bpy.props.EnumProperty(
        items=get_possible_variables,
        name="Select Variable",
        update=dict_update,
    )

    # Note that this dictionary is in shared memory.
    blendernc_dict = defaultdict()
    blendernc_dataset_identifier: bpy.props.StringProperty()

    # === Optional Functions ===
    # Initialization function, called when a new node is created.
    # This is the most common place to create the sockets for a node, as shown below.
    # NOTE: this is not the same as the standard __init__ function in Python, which is
    #       a purely internal Python method and unknown to the node system!
    def init(self, context):
        self.inputs.new('bNCstringSocket',"Path")
        self.outputs.new('bNCnetcdfSocket',"Dataset")
        self.blendernc_dataset_identifier = get_new_identifier(self)
        self.color = (0.4,0.8,0.4)
        self.use_custom_color = True
        

    # Copy function to initialize a copied node from an existing one.
    def copy(self, node):
        #self.blendernc_dataset_identifier = get_new_identifier(self)
        print("Copying from node ", node)

    # Free function to clean up on removal.
    def free(self):
        if self.blendernc_dataset_identifier in self.blendernc_dict.keys():
            self.blendernc_dict.pop(self.blendernc_dataset_identifier)
        print("Removing node ", self, ", Goodbye!")

    # Additional buttons displayed on the node.
    def draw_buttons(self, context, layout):
        layout.label(text = "Select Variable:")
        layout.prop(self, "blendernc_netcdf_vars",text='')
            
    # Detail buttons in the sidebar.
    # If this function is not defined, the draw_buttons function is used instead
    def draw_buttons_ext(self, context, layout):
        pass

    # Optional: custom label
    # Explicit user label overrides this, but here we can define a label dynamically
    def draw_label(self):
        if self.blendernc_dataset_identifier not in self.blendernc_dict.keys():
            return "netCDF input"
        else:
            return self.blendernc_file.split("/")[-1]

    @NodesDecorators.node_connections
    def update(self):                    
        identifier = self.blendernc_dataset_identifier
        blendernc_dict = self.blendernc_dict[identifier]
        updated_dataset = blendernc_dict['Dataset'][self.blendernc_netcdf_vars].to_dataset()

        # Note, only this node will have access to the socket. 
        # All the following nodes will pass directly to the next node.
        self.outputs[0].dataset[identifier] = blendernc_dict.copy()
        self.outputs[0].dataset[identifier]['Dataset'] = updated_dataset.copy()
        self.outputs[0].unique_identifier=identifier
        # Check decorators before modifying anything here.