import os
import re
import maya.cmds as cmds
import mtoa.core as core

def PBRNet_create_aiStandardSurface_from_PBR(file_path):
    # Extract material name from the file path
    base_name = os.path.basename(file_path)
    material_name = base_name.split('_')[0]
    dir_path = os.path.dirname(file_path)

    # Define the mapping of texture types to PBR channels
    pbr_mapping = {
        "albedo": "baseColor",
        "basecolor": "baseColor",
        "color": "baseColor",
        "nrm": "normalCamera",
        "normal": "normalCamera",
        "roughness": "specularRoughness",
        "metallic": "metalness",
        "metalness": "metalness",
        "ao": "ambientOcclusion",
        "opacity": "opacity",
        "emissive": "emissionColor",
        "height": "displacement",
        "displacement": "displacement",
        "vectordisplacement": "vectorDisplacement",
        "vdisp": "vectorDisplacement",
        "thinness": "subsurfaceScale"
    }

    # Color Space settings
    value_channels = ['roughness', 'metallic', 'metalness', 'ao', 'opacity', 'emissive', 'thinness']
    color_channels = ['albedo', 'basecolor', 'color']
    special_channels = ['nrm', 'normal', 'height', 'displacement', 'vectordisplacement', 'vdisp']

    # Find all relevant texture files in the directory
    texture_files = {key: None for key in pbr_mapping.keys()}
    for file in os.listdir(dir_path):
        if file.startswith(material_name):
            for key in texture_files.keys():
                if f"_{key}" in file.lower():
                    texture_files[key] = os.path.join(dir_path, file)

    # Create an aiStandardSurface material
    ai_shader = cmds.shadingNode('aiStandardSurface', asShader=True, name=material_name)
    shading_group = cmds.sets(renderable=True, noSurfaceShader=True, empty=True, name=material_name + 'SG')
    cmds.connectAttr(f'{ai_shader}.outColor', f'{shading_group}.surfaceShader')

    # Initialize displacementShader variable
    displacement_shader = None

    # Create file nodes and connect to the aiStandardSurface material
    for key, file_path in texture_files.items():
        if file_path:
            file_node = cmds.shadingNode('file', asTexture=True, isColorManaged=True)
            placement_node = cmds.shadingNode('place2dTexture', asUtility=True)
            # Standard connections for textures
            cmds.connectAttr(placement_node + '.coverage', file_node + '.coverage', force=True)
            cmds.connectAttr(placement_node + '.translateFrame', file_node + '.translateFrame', force=True)
            cmds.connectAttr(placement_node + '.rotateFrame', file_node + '.rotateFrame', force=True)
            cmds.connectAttr(placement_node + '.mirrorU', file_node + '.mirrorU', force=True)
            cmds.connectAttr(placement_node + '.mirrorV', file_node + '.mirrorV', force=True)
            cmds.connectAttr(placement_node + '.stagger', file_node + '.stagger', force=True)
            cmds.connectAttr(placement_node + '.wrapU', file_node + '.wrapU', force=True)
            cmds.connectAttr(placement_node + '.wrapV', file_node + '.wrapV', force=True)
            cmds.connectAttr(placement_node + '.repeatUV', file_node + '.repeatUV', force=True)
            cmds.connectAttr(placement_node + '.offset', file_node + '.offset', force=True)
            cmds.connectAttr(placement_node + '.rotateUV', file_node + '.rotateUV', force=True)
            cmds.connectAttr(placement_node + '.noiseUV', file_node + '.noiseUV', force=True)
            cmds.connectAttr(placement_node + '.vertexUvOne', file_node + '.vertexUvOne', force=True)
            cmds.connectAttr(placement_node + '.vertexUvTwo', file_node + '.vertexUvTwo', force=True)
            cmds.connectAttr(placement_node + '.vertexUvThree', file_node + '.vertexUvThree', force=True)
            cmds.connectAttr(placement_node + '.vertexCameraOne', file_node + '.vertexCameraOne', force=True)
            cmds.connectAttr(placement_node + '.outUV', file_node + '.uv', force=True)
            cmds.setAttr(file_node + '.fileTextureName', file_path, type='string')

            # Set color space and ignore file rules if necessary
            if key in special_channels or key in value_channels:
                cmds.setAttr(file_node + '.colorSpace', 'Raw', type='string')
                cmds.setAttr(file_node + '.ignoreColorSpaceFileRules', 1)  # Ignore color space file rules

            elif key in color_channels:
                cmds.setAttr(file_node + '.colorSpace', 'sRGB', type='string')

            # Check if the texture uses UDIM
            if re.search(r'\.\d{4}\.', file_path):
                cmds.setAttr(file_node + '.uvTilingMode', 3)  # UDIM (Mari) setting

            # Connect normal maps
            if key in ["nrm", "normal"]:
                # For normal maps, create a normal map node
                normal_map_node = cmds.shadingNode('aiNormalMap', asUtility=True)
                cmds.connectAttr(file_node + '.outColor', normal_map_node + '.input', force=True)
                cmds.connectAttr(normal_map_node + '.outValue', ai_shader + '.' + pbr_mapping[key], force=True)
            
            # Connect displacement textures
            elif key in ['height', 'displacement', 'vectordisplacement', 'vdisp']:
                # Create displacementShader if not already created
                if not displacement_shader:
                    displacement_shader = cmds.shadingNode('displacementShader', asShader=True, name=material_name + '_displacementShader')
                    cmds.connectAttr(f'{displacement_shader}.displacement', f'{shading_group}.displacementShader')
                if key in ['height', 'displacement']:
                    cmds.connectAttr(file_node + '.outAlpha', displacement_shader + '.displacement', force=True)
                else:  # vector displacement
                    cmds.connectAttr(file_node + '.outColor', displacement_shader + '.vectorDisplacement', force=True)
                    cmds.setAttr (displacement_shader + '.vectorSpace', 2);

            # Connect other value channels
            elif key in value_channels:
                # Connect using the red channel of the texture
                cmds.connectAttr(file_node + '.outColorR', ai_shader + '.' + pbr_mapping[key], force=True)
                if key == "roughness":
                    cmds.connectAttr(file_node + '.outColorR', ai_shader + '.diffuseRoughness', force=True)
            else:
                cmds.connectAttr(file_node + '.outColor', ai_shader + '.' + pbr_mapping[key], force=True)

def PBRNet_select_file():
    """打开文件选择对话框，允许用户选择一个贴图文件。"""
    project_path = cmds.workspace(q=True, rd=True)
    source_images_path = os.path.join(project_path, "sourceimages")
    file_path = cmds.fileDialog2(fileMode=1, caption="Select PBR Texture", dir=source_images_path)
    if file_path:
        cmds.textField('pbrFilenameTextField', edit=True, text=file_path[0])

def PBRNet_create_pbr_shader_network():
    """从UI中读取文件路径并创建PBR材质网络。"""
    file_path = cmds.textField('pbrFilenameTextField', query=True, text=True)
    PBRNet_create_aiStandardSurface_from_PBR(file_path)

def PBRNet_create_ui():
    """创建用户界面。"""
    window_id = 'createPBRShaderNetworkUI'
    if cmds.window(window_id, exists=True):
        cmds.deleteUI(window_id)

    window = cmds.window(window_id, title="Create PBR Shader Network", widthHeight=(400, 100), sizeable=True)
    form = cmds.formLayout(numberOfDivisions=100)
    text = cmds.text(label="PBR filename")
    textField = cmds.textField('pbrFilenameTextField')
    button = cmds.iconTextButton(style='iconOnly', image1='fileOpen.xpm', command=lambda: PBRNet_select_file())
    createButton = cmds.button(label="Create PBR Shader Network", command=lambda x: PBRNet_create_pbr_shader_network())

    cmds.formLayout(form, edit=True, attachForm=[
        (text, 'top', 10), (text, 'left', 10),
        (textField, 'top', 5), 
        (button, 'top', 5), (button, 'right', 10),
        (createButton, 'left', 10), (createButton, 'right', 10), (createButton, 'bottom', 10)
    ], attachControl=[
        (textField, 'left', 5, text), (textField, 'right', 5, button),
    ], attachPosition=[
        #(text, 'right', 5, 30),  # Text is at 30% of the form width
        #(textField, 'left', 5, 30), (textField, 'right', 5, 70),  # TextField starts at 30% and ends at 70%
        #(button, 'right', 5, 70)  # Button is at 70% of the form width
    ], attachNone=[
        (text, 'bottom'), (text, 'right'),
        (button, 'left'), (button, 'bottom'),
        (textField, 'bottom'),
        (createButton, 'top')
    ])

    cmds.showWindow(window)

PBRNet_create_ui();