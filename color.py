class Color():
    @staticmethod
    def rgb_to_hex(color):
        """Convert an RGB tuple (or vector) with values in [0, 1] to a hex string."""
        # Convert each color component from 0-1 to 0-255 and format as a 2-digit hex.
        r, g, b = [int(c * 255) for c in color]
        return "#{:02X}{:02X}{:02X}".format(r, g, b)
    
    @staticmethod
    def linear_to_srgb(c):
        if c <= 0.0031308:
            return 12.92 * c
        else:
            return 1.055 * (c ** (1/2.4)) - 0.055
    
    @staticmethod
    def get_world_color(bpy):
        world = bpy.context.scene.world

        if world.use_nodes:
            bg_node = world.node_tree.nodes.get("Background")
            if bg_node:
                # Retrieve the linear RGBA from the Background node
                linear_color = bg_node.inputs[0].default_value  # [R, G, B, A]
                # Convert each RGB channel to sRGB
                srgb_color = [Color.linear_to_srgb(linear_color[i]) for i in range(3)]
            else:
                srgb_color = [0, 0, 0]
        else:
            # If nodes are not used, get the linear world color (RGB)
            linear_color = world.color
            srgb_color = [Color.linear_to_srgb(c) for c in linear_color]
        
        hex_color = Color.rgb_to_hex(srgb_color)
        
        return hex_color
