# https://github.com/Korchy/1d_camswitch

# Versions:
#   1.0.2 - Добавлена смена изображения на заднике 3D Viewport если имя изображения
#       входит в имя камеры

import bpy
import os

bl_info = {
    "name": "Camswitch",
    "author": "nikitron.cc.ua, Nikita Akimov",
    "version": (0, 0, 2),
    "blender": (2, 7, 9),
    "location": "View3D > Tool Shelf > 1D > camswitch",
    "description": "switch cameras",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Camera"}


class D1_camswitch(bpy.types.Operator):
    ''' \
    Следующая и предыдущая камера в сцене. \
    next & previous camera in the scene. \
    '''
    bl_idname = "camera.camswitch"
    bl_label = "Camswitch"

    next = bpy.props.BoolProperty(name='next', default=True)

    def execute(self, context):
        cams = [k for k in bpy.data.objects if k.type == 'CAMERA']
        print(cams)
        active = bpy.data.scenes[bpy.context.scene.name].camera
        for i, k in enumerate(cams):
            if self.next:
                if k == active and i < (len(cams)-1):
                    bpy.data.scenes[bpy.context.scene.name].camera = \
                        bpy.data.objects[cams[i+1].name]
                    break
                elif k == active:
                    bpy.data.scenes[bpy.context.scene.name].camera = \
                        bpy.data.objects[cams[0].name]
                    break
            else:
                if k == active and i > 0:
                    bpy.data.scenes[bpy.context.scene.name].camera = \
                        bpy.data.objects[cams[i-1].name]
                    break
                elif k == active:
                    bpy.data.scenes[bpy.context.scene.name].camera = \
                        bpy.data.objects[cams[-1].name]
                    break
        # switch background image according current camera name
        for image in context.space_data.background_images:
            image_name = os.path.splitext(os.path.basename(image.image.name))[0]    # name without ext
            if image_name in context.scene.camera.name:
                image.show_background_image = True
            else:
                image.show_background_image = False

        return {'FINISHED'}


class D1_camswitch_panel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Camswitch"
    bl_options = {'DEFAULT_CLOSED'}
    bl_category = '1D'

    def draw(self, context):
        ''' \
        Следукющая активная камера \
        Next active camera \
        '''
        layout = self.layout
        row = layout.row(align=True)
        row.operator('camera.camswitch', text='Prev', icon='TRIA_LEFT').next = False
        row.operator('camera.camswitch', text='Next', icon='TRIA_RIGHT').next = True


def register():
    bpy.utils.register_class(D1_camswitch)
    bpy.utils.register_class(D1_camswitch_panel)


def unregister():
    bpy.utils.unregister_class(D1_camswitch_panel)
    bpy.utils.unregister_class(D1_camswitch)
    

if __name__ == "__main__":
    register()
