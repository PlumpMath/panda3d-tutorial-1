from math import pi, sin, cos

from direct.actor.Actor import Actor
from direct.showbase.ShowBase import ShowBase
from direct.task import Task


class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self)

        self.environ = self.loader.loadModel('models/environment')
        self.environ.reparentTo(self.render)
        self.environ.setScale(.25, .25, .25)
        self.environ.setPos(-8, 42, 0)

        self.taskMgr.add(self.spin_camera_task, 'spin_camera_task')

        self.panda = Actor('models/panda-model', {'walk': 'models/panda-walk4'})
        self.panda.setScale(.005, .005, .005)
        self.panda.reparentTo(self.render)
        self.panda.loop('walk')


    def spin_camera_task(self, task):
        angle_deg = task.time * 6.0
        angle_rad = angle_deg * (pi / 180.0)
        self.camera.setPos(20 * sin(angle_rad), -20.0 * cos(angle_rad), 3)
        self.camera.setHpr(angle_deg, 0, 0)
        return Task.cont


if __name__ == '__main__':
    app = MyApp()
    app.run()

