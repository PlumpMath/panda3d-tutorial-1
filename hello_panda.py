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

        self.taskMgr.add(self.spin_camera_task, 'spin_camera_task')

        self.panda = Actor('models/panda-model', {'walk': 'models/panda-walk4'})
        self.panda.setScale(.005, .005, .005)
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

    def spin_camera_task(self, task):
        angle_deg = task.time * 6.0
        angle_rad = angle_deg * (pi / 180.0)
        self.camera.setPos(30 * sin(angle_rad), -40.0 * cos(angle_rad), 3)
        self.camera.setHpr(angle_deg, 0, 0)
        return Task.cont


if __name__ == '__main__':
    app = MyApp()
    app.run()

