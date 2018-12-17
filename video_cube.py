import bpy

bpy.context.scene.render.engine = "CYCLES"

for i in range(1, 420):
    name = str(i).zfill(4) + ".jpg"
    filepath = bpy.path.abspath("//Frames\\") + name
    bpy.data.images.load(filepath, check_existing=True)
    #bpy.data.images[name].name = str(i)

layers = []
for i in range(1, 420):
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, i * 0.02))
    bpy.ops.transform.resize(value=(1, 1, 0.01))
    ob = bpy.context.active_object
    layers.append(ob)

    # Get material
    mat = bpy.data.materials.get(str(i))
    if mat is None:
        # create material
        mat = bpy.data.materials.new(name=str(i))
    
    mat.use_nodes = True;
    for node in mat.node_tree.nodes:
        mat.node_tree.nodes.remove(node)
        
    output = mat.node_tree.nodes.new("ShaderNodeOutputMaterial")
    diff = mat.node_tree.nodes.new("ShaderNodeBsdfDiffuse")
    texture = mat.node_tree.nodes.new("ShaderNodeTexImage")
    coord = mat.node_tree.nodes.new("ShaderNodeTexCoord")
    
    texture.image = bpy.data.images[str(i).zfill(4) + ".jpg"]
    
    mat.node_tree.links.new(texture.inputs["Vector"], coord.outputs["Generated"])
    mat.node_tree.links.new(diff.inputs["Color"], texture.outputs["Color"])
    mat.node_tree.links.new(output.inputs["Surface"], diff.outputs["BSDF"])

    # Assign it to object
    if ob.data.materials:
        # assign to 1st material slot
        ob.data.materials[0] = mat
    else:
        # no slots
        ob.data.materials.append(mat)
        
for layer in layers:
    layer.select = True
bpy.ops.object.join()
bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY")
bpy.ops.object.select_all(action="TOGGLE")