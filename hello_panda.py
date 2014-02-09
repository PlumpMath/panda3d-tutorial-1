import sys

from math import pi, sin, cos

from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
from direct.interval.IntervalGlobal import Sequence
from panda3d.core import Point3


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.disableMouse()

        self.environ = self.loader.loadModel('models/environment')
        self.environ.reparentTo(self.render)
        self.environ.setScale(.25, .25, .25)
        self.environ.setPos(-8, 42, 0)

        self.taskMgr.add(self.move_camera_task, 'move_camera_task')

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

        self.messenger.toggleVerbose()

    def set_key(self, key, value):
        self.key_map[key] = value

    def spin_camera_task(self, task):
        angle_deg = task.time * 6.0
        angle_rad = angle_deg * (pi / 180.0)
        self.camera.setPos(30 * sin(angle_rad), -40.0 * cos(angle_rad), 3)
        self.camera.setHpr(angle_deg, 0, 0)
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
        if base.mouseWatcherNode.hasMouse():
            x = base.mouseWatcherNode.getMouseX()
            y = base.mouseWatcherNode.getMouseY()

            prev_mouse = getattr(self, 'prev_mouse', None)
            if prev_mouse:
                delta_x = x - prev_mouse[0]
                delta_y = y - prev_mouse[1]

                self.camera.setHpr(self.camera,
                                   delta_x * -100,
                                   delta_y * 100,
                                   0)
                self.camera.setR(0)

            self.prev_mouse = x, y

        return Task.cont


if __name__ == '__main__':
    app = MyApp()
    app.run()
