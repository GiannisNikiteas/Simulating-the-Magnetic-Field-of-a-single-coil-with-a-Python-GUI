from traits.api import HasTraits, Range, Instance, \
                    on_trait_change
from traitsui.api import View, Item, HGroup
from tvtk.pyface.scene_editor import SceneEditor
from mayavi.tools.mlab_scene_model import \
                    MlabSceneModel
from mayavi.core.ui.mayavi_scene import MayaviScene


class Visualization(HasTraits):
    meridional = Range(1, 30,  6)
    transverse = Range(0, 30, 11)
    scene = Instance(MlabSceneModel, ())

    def __init__(self):
        # Do not forget to call the parent's __init__
        HasTraits.__init__(self)
        x, y, z, t = curve(self.meridional, self.transverse)
        self.plot = self.scene.mlab.plot3d(x, y, z, t, colormap='Spectral')

    @on_trait_change('meridional,transverse')
    def update_plot(self):
        x, y, z, t = curve(self.meridional, self.transverse)
        self.plot.mlab_source.set(x=x, y=y, z=z, scalars=t)


    # the layout of the dialog created
    view = View(Item('scene', editor=SceneEditor(scene_class=MayaviScene),
                    height=250, width=300, show_label=False),
                HGroup(
                        '_', 'meridional', 'transverse',
                    ),
                )

visualization = Visualization()
visualization.configure_traits()