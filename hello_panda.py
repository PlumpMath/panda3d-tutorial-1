import sys

from math import pi, sin, cos

from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3, loadPrcFileData
from pandac.PandaModules import WindowProperties


loadPrcFileData('', 'fullscreen 1')
loadPrcFileData('', 'win-size 1600 900')


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        props = WindowProperties()
        props.setCursorHidden(True)
        props.setMouseMode(WindowProperties.MRelative)
        self.win.requestProperties(props)
        self.disableMouse()

        self.environ = self.loader.loadModel('models/environment')
        self.environ.reparentTo(self.render)
        self.environ.setScale(.25, .25, .25)
        self.environ.setPos(-8, 42, 0)

        self.taskMgr.add(self.move_camera_task, 'move_camera_task')
        self.taskMgr.add(self.move_projectiles_task, 'move_projectiles_task')

        self.key_map = {
            'cam-forward': False,
            'cam-backward': False,
            'cam-left': False,
            'cam-right': False,
        }

        self.accept('w', self.set_key, ['cam-forward', True])
        self.accept('w-up', self.set_key, ['cam-forward', False])

        self.accept('s', self.set_key, ['cam-backward', True])
        self.accept('s-up', self.set_key, ['cam-backward', False])

        self.accept('a', self.set_key, ['cam-left', True])
        self.accept('a-up', self.set_key, ['cam-left', False])

        self.accept('d', self.set_key, ['cam-right', True])
        self.accept('d-up', self.set_key, ['cam-right', False])

        self.accept('escape', sys.exit)

        self.accept('mouse1', self.set_teapot)

        self.panda = Actor('models/panda-model', {'walk': 'models/panda-walk4'})
        self.panda.setScale(.01, .01, .01)
        self.panda.reparentTo(self.render)
        self.panda.loop('walk')

        point_a = Point3(0, -10, 0)
        point_b = Point3(0, 10, 0)
        point_c = Point3(180, 0, 0)
        point_d = Point3(0, 0, 0)

        self.panda_pace = Sequence(
            self.panda.posInterval(3,
                                   point_a,
                                   startPos=point_b),
            self.panda.hprInterval(1, point_c, startHpr=point_d),
            self.panda.posInterval(3,
                                   point_b,
                                   startPos=point_a),
            self.panda.hprInterval(1, point_d, startHpr=point_c),
            name='panda_pace'
        )
        self.panda_pace.loop()

        self.teapot = self.loader.loadModel('teapot')
        self.projectiles = []

    def set_key(self, key, value):
        self.key_map[key] = value

    def set_teapot(self):
        coords = self.camera.get_pos()
        quat = self.camera.get_quat()
        placeholder = self.render.attach_new_node('teapot_placeholder')
        placeholder.set_pos(self.camera, 0, 20, 0)
        placeholder.set_quat(quat)
        self.teapot.instance_to(placeholder)
        self.projectiles.append(placeholder)

    def move_projectiles_task(self, task):
        for proj in self.projectiles:
            proj.set_pos(proj, 0, 1, 0)
            if proj.get_distance(self.render) > 100:
                self.projectiles.remove(proj)
                proj.removeNode()
        return Task.cont

    def move_camera_task(self, task):
        coords = [0] * 3
        if self.key_map['cam-right']:
            coords[0] = 1
        if self.key_map['cam-left']:
            coords[0] = -1
        if self.key_map['cam-forward']:
            coords[1] = 1
        if self.key_map['cam-backward']:
            coords[1] = -1
        self.camera.setPos(self.camera, *coords)
        if self.mouseWatcherNode.hasMouse():
            x = self.mouseWatcherNode.getMouseX()
            y = self.mouseWatcherNode.getMouseY()

            prev_mouse = getattr(self, 'prev_mouse', None)
            if prev_mouse:
                delta_x = x - prev_mouse[0]
                delta_y = y - prev_mouse[1]

                self.camera.setHpr(self.camera,
                                   delta_x * -50,
                                   delta_y * 50,
                                   0)
                self.camera.setR(0)

            self.prev_mouse = x, y

        return Task.cont


if __name__ == '__main__':
    app = MyApp()
    app.run()
