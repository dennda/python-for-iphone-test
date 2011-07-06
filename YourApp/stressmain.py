def server():
    import code, socket, sys

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    for port in range(5000, 5010):
        try:
            server_socket.bind(('', port))
            print "bound to port", port
            break
        except socket.error:
            pass
    server_socket.listen(1)
    client_socket, address = server_socket.accept()
    print 'I got a connection from ', address

    _stdout, _stderr = sys.stdout, sys.stderr

    socketFile = client_socket.makefile('rw')
    sys.stdout = sys.stderr = socketFile

    def socket_input(prompt):
        socketFile.write(prompt)
        socketFile.flush()
        return socketFile.readline().rstrip()

    try:
        code.interact(readfunc=socket_input, local=globals())
    finally:
        client_socket.close()


print 'SETUP KIVY >>'
from kivy.logger import Logger
import logging
Logger.setLevel(logging.DEBUG)

from kivy.config import Config
Config.remove_option('input', 'default')
Config.remove_option('input', 'mactouch')
Config.set('graphics', 'fullscreen', 'auto')
print 'SETUP KIVY << done'


try:
    from kivy.uix.button import Button
    from kivy.uix.widget import Widget
    from kivy.uix.label import Label
    from kivy.uix.boxlayout import BoxLayout
    from kivy.app import App
    from kivy.graphics import Color, Rectangle
    from random import random as r
    from functools import partial
    from kivy.clock import Clock
    from kivy.core.window import Window
    from kivy.graphics.transformation import Matrix
#    Window.clearcolor = (0, 0, 1, 1)



    class MatrixWidget(Widget):
#        deg = 0
        def on_touch_up(self, touch):
#            mwm = Window.render_context['modelview_mat']
#            mwm.rotate(self.deg * 180. / 3.14, r(), r(), r())
#            
#            self.deg += 10

            projection_mat = Matrix()
#            projection_mat.view_clip(0.0, Window.width, 0.0, Window.height, -100.0, 100.0, 0)
            Window.render_context['projection_mat'] = projection_mat
            print touch.pos
            
    class StressCanvasApp(App):

        def add_rects(self, *largs):
            print 'adding_rects', '=' * 80
            wid = self.wid
            count = 1000
            print 'adding', count, 'rects'
            with wid.canvas:
                for x in xrange(count):
                    Color(r(), 1, 1, mode='hsv')
                    Rectangle(pos=(r() * 100. - 50.,
                                   r() * 100. - 50.), size=(100 * r(), 200 * r()))
        def build(self):
            print "building"
            wid = MatrixWidget()
            self.wid = wid
            wid.pos = (-9999, -9999)
            wid.size = (9999, 9999)
            Clock.schedule_interval(self.add_rects, 0.5)

            
            
            with Window.canvas:
                Color(1, 0, 1, mode='hsv')
                Rectangle(pos=(-10000, -10000), size=(20000, 20000))
                
            return wid




    if __name__ in ('__main__', '__android__'):
        #TouchtracerApp().run()
        StressCanvasApp().run()
except Exception, inst:
    import traceback
    print 'caught exception', inst
    traceback.print_exc()
    
    server()


'''
'''