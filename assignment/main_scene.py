"""
DIGM 131 - Assignment 3: Function Library (main_scene.py)
==========================================================

OBJECTIVE:
    Use the functions you wrote in scene_functions.py to build a complete
    scene. This file demonstrates how importing and reusing functions makes
    scene creation clean and readable.

REQUIREMENTS:
    1. Import scene_functions (the module you completed).
    2. Call each of your 5+ functions at least once.
    3. Use place_in_circle with at least one of your create functions.
    4. The final scene should contain at least 15 objects total.
    5. Comment your code explaining what you are building.

GRADING CRITERIA:
    - [30%] All 5+ functions from scene_functions.py are called.
    - [25%] place_in_circle is used at least once.
    - [20%] Scene contains 15+ objects and looks intentional.
    - [15%] Code is well-commented.
    - [10%] Script runs without errors from top to bottom.
"""

import maya.cmds as cmds
import scene_functions as sf

# ---------------------------------------------------------------------------
# Scene Setup
# ---------------------------------------------------------------------------
cmds.file(new=True, force=True)

# Create a ground plane.
ground = cmds.polyPlane(name="ground", width=60, height=60,
                        subdivisionsX=1, subdivisionsY=1)[0]

# Create objects.
sf.create_building(width=5, height=10, depth=5, position=(-10, 0, 8))
sf.create_building(width=5, height=10, depth=5, position=(-10, 0, -1))
sf.create_tree(position=(3, 0, -5))
sf.create_tree(position=(6, 0, 2))
sf.create_tree(position=(-2, 0, 4))
sf.create_fence(length=12, post_count=7, position=(-6, 0, -3))
sf.create_lamp_post(position=(8, 0, 2))

# Place 8 trees in a circle of radius 15:
sf.place_in_circle(sf.create_tree, count=8, radius=15)

# Remember: call each function at least once, and aim for 15+ objects.

# ---------------------------------------------------------------------------
# Final viewport framing (do not remove).
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    cmds.viewFit(allObjects=True)
    print("Main scene built successfully!")
