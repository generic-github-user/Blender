import bpy

bpy.context.scene.render.engine = "CYCLES"

for i in range(1, 420):
    name = str(i).zfill(4) + ".jpg"
    filepath = "C:/Users/diamo/Downloads/Frames/" + name
    bpy.data.images.load(filepath, check_existing=True)
    #bpy.data.images[name].name = 0

for i in range(1, 420):
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, i * 0.02))
    bpy.ops.transform.resize(value=(1,1,0.01))
    ob = bpy.context.active_object

    # Get material
    mat = bpy.data.materials.get(str(i))
    if mat is None:
        # create material
        mat = bpy.data.materials.new(name=str(i))
    
    mat.use_nodes = True;
    texture = mat.node_tree.nodes.new("ShaderNodeTexImage")
    texture.image = bpy.data.images[str(i).zfill(4) + ".jpg"]
    diff = mat.node_tree.nodes['Diffuse BSDF'].inputs["Color"]
    mat.node_tree.links.new(diff, texture.outputs['Color'])
    coord = mat.node_tree.nodes.new("ShaderNodeTexCoord")
    vector = texture.inputs["Vector"]
    mat.node_tree.links.new(vector, coord.outputs['Generated'])

    # Assign it to object
    if ob.data.materials:
        # assign to 1st material slot
        ob.data.materials[0] = mat
    else:
        # no slots
        ob.data.materials.append(mat)