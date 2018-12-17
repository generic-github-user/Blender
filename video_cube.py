import bpy

# Set rendering engine to Cycles
bpy.context.scene.render.engine = "CYCLES"

# Import images into scene to use as object textures
for i in range(1, 420):
	# Name of image file
    name = str(i).zfill(4) + ".jpg"
	# File path (relative to .blend file)
    filepath = bpy.path.abspath("//Frames\\") + name
	# Load image into scene
    bpy.data.images.load(filepath, check_existing=True)
    #bpy.data.images[name].name = str(i)

# List of objects representing video frames
layers = []
# Add objects and materials
for i in range(1, 420):
	# Add new cube to scene (one video frame)
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, i * 0.02))
	# Resize cube to be thinner
    bpy.ops.transform.resize(value=(1, 1, 0.01))
	# Selected object
    ob = bpy.context.active_object
	# Add slice to list of layers
    layers.append(ob)

    # Check if material exists
    mat = bpy.data.materials.get(str(i))
    if mat is None:
        # Create new material if none exists
        mat = bpy.data.materials.new(name=str(i))
    
	# Set material to use node editor
    mat.use_nodes = True;
	# List of nodes in material node tree
    nodes = mat.node_tree.nodes
	# Remove all nodes from material
    for node in nodes:
        nodes.remove(node)
        
	# Add nodes
    output = nodes.new("ShaderNodeOutputMaterial")
    diff = nodes.new("ShaderNodeBsdfDiffuse")
    texture = nodes.new("ShaderNodeTexImage")
    coord = nodes.new("ShaderNodeTexCoord")
    
	# Set source image for texture
    texture.image = bpy.data.images[str(i).zfill(4) + ".jpg"]
    
	# Create links between material nodes
    mat.node_tree.links.new(texture.inputs["Vector"], coord.outputs["Generated"])
    mat.node_tree.links.new(diff.inputs["Color"], texture.outputs["Color"])
    mat.node_tree.links.new(output.inputs["Surface"], diff.outputs["BSDF"])

    # Assign material to object
    if ob.data.materials:
        ob.data.materials[0] = mat
    else:
        ob.data.materials.append(mat)

# Select all slices
for layer in layers:
    layer.select = True
# Combine layers
bpy.ops.object.join()
# Set origin to center of geometry
bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY")
# Deselect
bpy.ops.object.select_all(action="TOGGLE")