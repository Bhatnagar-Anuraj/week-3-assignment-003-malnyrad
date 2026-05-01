"""
DIGM 131 - Assignment 3: Function Library (scene_functions.py)
===============================================================

OBJECTIVE:
    Create a library of reusable functions that each generate a specific
    type of scene element. This module will be imported by main_scene.py.

REQUIREMENTS:
    1. Implement at least 5 reusable functions.
    2. Every function must have a complete docstring with Args and Returns.
    3. Every function must accept parameters for position and/or size so
       they can be reused at different locations and scales.
    4. Every function must return the name(s) of the Maya object(s) it creates.
    5. Follow PEP 8 naming conventions (snake_case for functions/variables).

GRADING CRITERIA:
    - [30%] At least 5 functions, each creating a distinct scene element.
    - [25%] Functions accept parameters and use them (not hard-coded values).
    - [20%] Every function has a complete docstring (summary, Args, Returns).
    - [15%] Functions return the created object name(s).
    - [10%] Clean, readable code following PEP 8.
"""

import maya.cmds as cmds
import math

def create_building(width=4, height=8, depth=4, position=(0, 0, 0)):
    """Create a simple building from a cube, placed on the ground plane.

    The building is a single scaled cube whose base sits at ground level
    (y = 0) at the given position.

    Args:
        width (float): Width of the building along the X axis.
        height (float): Height of the building along the Y axis.
        depth (float): Depth of the building along the Z axis.
        position (tuple): (x, y, z) ground-level position. The building
            base will rest at this point; y is typically 0.

    Returns:
        str: The name of the created building transform node.
    """
    #   Create a cube with the given width, height, and depth.
    building = cmds.polyCube(width, height, depth)[0]
    #   Move it so its base sits on the ground at 'position', offsetting Y by height / 2.0.
    cmds.move(position[0], position[1] / 2.0, position[2], building)

    #   Return the object name.
    return building


def create_tree(trunk_radius=0.3, trunk_height=3, canopy_radius=2,
                position=(0, 0, 0)):
    """Create a simple tree using a cylinder trunk and a sphere canopy.

    Args:
        trunk_radius (float): Radius of the cylindrical trunk.
        trunk_height (float): Height of the trunk cylinder.
        canopy_radius (float): Radius of the sphere used for the canopy.
        position (tuple): (x, y, z) ground-level position for the tree base.

    Returns:
        str: The name of a group node containing the trunk and canopy.
    """
    #   Create a cylinder for the trunk and position it.
    trunk = cmds.polyCylinder(trunk_radius, trunk_height)[0]
    cmds.move(0, trunk_height / 2.0, 0, trunk)
    #   Create a sphere for the canopy, positioned on top of the trunk.
    canopy = cmds.polySphere(canopy_radius)[0]
    cmds.move(0, trunk_height, 0, canopy)

    #   Group the trunk and the canopy together.
    tree = cmds.group(trunk, canopy, name="tree")
    #   Move the group to 'position'.
    cmds.move(position[0], position[1], position[2], tree)
    
    #   Return the group name.
    return tree


def create_fence(length=10, height=1.5, post_count=6, position=(0, 0, 0)):
    """Create a simple fence made of posts and rails.

    The fence runs along the X axis starting at the given position.

    Args:
        length (float): Total length of the fence along the X axis.
        height (float): Height of the fence posts.
        post_count (int): Number of vertical posts (must be >= 2).
        position (tuple): (x, y, z) starting position of the fence.

    Returns:
        str: The name of a group node containing all fence parts.
    """
    #   Calculate spacing between posts.
    post_spacing = length / (post_count - 1)
    post_size = 0.1
    posts = []

    #   Loop to create 'post_count' thin, tall cubes as posts.
    for item in range(post_count):
        #   Calculate position.
        x_pos = item * post_spacing
        
        #   Create each post.
        post = cmds.polyCube(w=post_size, h=height, d=post_size)[0]
        cmds.move(x_pos, height / 2.0, 0, post)
        posts.append(post)
    
    #   Create a long, thin cube as a horizontal rail connecting them.
    rail = cmds.polyCube(w=length, h=post_size, d=post_size)[0]
    cmds.move(length / 2.0, height * 0.75, 0, rail)

    #   Group everything and move to 'position'.
    fence = cmds.group(posts, rail, name="fence")
    cmds.move(position[0], position[1], position[2], fence)

    #   Return the group name.
    return fence


def create_lamp_post(pole_height=5, light_radius=0.5, position=(0, 0, 0)):
    """Create a street lamp using a cylinder pole and a sphere light.

    Args:
        pole_height (float): Height of the lamp pole.
        light_radius (float): Radius of the sphere representing the light.
        position (tuple): (x, y, z) ground-level position.

    Returns:
        str: The name of a group node containing the pole and light.
    """
    #   Create a thin cylinder for the pole.
    pole_radius = 0.2
    pole = cmds.polyCylinder(pole_height, pole_radius)[0]
    cmds.move(0, pole_height / 2.0, 0, pole)
    #   Create a sphere for the light, placed at the top of the pole.
    light = cmds.polySphere(light_radius)[0]
    cmds.move(0, pole_height + light_radius, 0, light)

    #   Group them, move to 'position', and return the group name.
    lamp = cmds.group(pole, light, name="lamp")
    cmds.move(position[0], position[1], position[2], lamp)

    return lamp


def place_in_circle(create_func, count=8, radius=10, center=(0, 0, 0),
                     **kwargs):
    """Place objects created by 'create_func' in a circular arrangement.

    This is a higher-order function: it takes another function as an
    argument and calls it repeatedly to place objects around a circle.

    Args:
        create_func (callable): A function from this module (e.g.,
            create_tree) that accepts a 'position' keyword argument
            and returns an object name.
        count (int): Number of objects to place around the circle.
        radius (float): Radius of the circle.
        center (tuple): (x, y, z) center of the circle.
        **kwargs: Additional keyword arguments passed to create_func
            (e.g., trunk_height=4).

    Returns:
        list: A list of object/group names created by create_func.
    """
    results = []
    #   Loop 'count' times.
    for item in range(count):
        #   Calculate the angle.
        angle = 2 * math.pi * item / count

        #   Calculate x.
        x = center[0] + radius * math.cos(angle)
        #   Calculate z.
        z = center[2] + radius * math.sin(angle)

        #   Call create_func.
        created = create_func(position=(x, center[1], z), **kwargs)

        #   Append the returned name to a results list.
        results.append(created)
        circle = cmds.group(results, name="circle")

    #   Return the results list.
    return results, circle