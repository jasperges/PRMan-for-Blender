# ##### BEGIN MIT LICENSE BLOCK #####
#
# Copyright (c) 2011 Matt Ebb
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
#
# ##### END MIT LICENSE BLOCK #####
import bpy
import sys

bl_info = {
    "name": "RenderMan For Blender",
    "author": "Brian Savery",
    "version": (0, 9, 0),
    "blender": (2, 77, 0),
    "location": "Info Header, render engine menu",
    "description": "RenderMan 20.0 integration",
    "warning": "",
    "category": "Render"}


class PRManRender(bpy.types.RenderEngine):
    bl_idname = 'PRMAN_RENDER'
    bl_label = "RenderMan Render"
    bl_use_preview = True
    bl_use_save_buffers = True

    def __init__(self):
        self.render_pass = None

    def __del__(self):
        if hasattr(self, "render_pass"):
            if self.render_pass is not None:
                engine.free(self)

    # main scene render
    def update(self, data, scene):
        if(engine.ipr):
            return
        if self.is_preview:
            if not self.render_pass:
                engine.create(self, data, scene)
        else:
            if not self.render_pass:
                engine.create(self, data, scene)
            else:
                engine.reset(self, data, scene)

        engine.update(self, data, scene)

    def render(self, scene):
        if self.render_pass is not None:
            engine.render(self)


def add_handlers(scene):
    if engine.update_timestamp not in bpy.app.handlers.scene_update_pre:
        bpy.app.handlers.scene_update_pre.append(engine.update_timestamp)
    if properties.initial_groups not in bpy.app.handlers.scene_update_post:
        bpy.app.handlers.load_post.append(properties.initial_groups)


def remove_handlers():
    if properties.initial_groups in bpy.app.handlers.scene_update_pre:
        bpy.app.handlers.scene_update_pre.remove(properties.initial_groups)
    if engine.update_timestamp in bpy.app.handlers.scene_update_post:
        bpy.app.handlers.scene_update_post.remove(engine.update_timestamp)


def register():
    from . import preferences
    preferences.register()
    from . import ui
    from . import properties
    from . import operators
    from . import nodes
    # need this now rather than at beginning to make
    # sure preferences are loaded
    from . import engine
    properties.register()
    operators.register()
    ui.register()
    nodes.register()
    bpy.utils.register_module(__name__)
    add_handlers(None)
    # if add_handlers not in bpy.app.handlers.load_post:
    #    bpy.app.handlers.load_post.append(add_handlers)


def unregister():
    remove_handlers()

    from . import ui
    from . import properties
    from . import operators
    from . import nodes
    from . import icons
    preferences.unregister()
    properties.unregister()
    operators.unregister()
    ui.unregister()
    nodes.unregister()
    bpy.utils.unregister_module(__name__)
