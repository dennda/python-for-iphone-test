print 'SETUP KIVY >>'
from kivy.logger import Logger
import logging
Logger.setLevel(logging.DEBUG)

from kivy.config import Config
Config.remove_option('input', 'default')
Config.remove_option('input', 'mactouch')
Config.set('graphics', 'fullscreen', 'auto')
print 'SETUP KIVY << done'



from kivy.graphics.opengl import *


def buildShader(source, shaderType):
    shaderHandle = glCreateShader(shaderType)
    glShaderSource(shaderHandle, source)
    glCompileShader(shaderHandle)

    compileSuccess = glGetShaderiv(shaderHandle, GL_COMPILE_STATUS)

    if compileSuccess == GL_FALSE:
        messages = None
        glGetShaderInfoLog(shaderHandle, sizeof(messages), 0, messages);
        print 'error compiling shader', messages

    return shaderHandle


#struct Vertex {
#    float Position[2];
#    float Color[4];
#};

def render():
    coords = [
        -0.5, -0.866,
        0.5, -0.866,
        0, 1,
        -0.5, -0.866,
        0.5, -0.866,
        0, -0.4
    ]

    colors = [
         1, 1, 0.5, 1,
         1, 1, 0.5, 1,
         1, 1, 0.5, 1,
         0.5, 0.5, 0.5,
         0.5, 0.5, 0.5,
         0.5, 0.5, 0.5
    ]

    glViewport(0, 0, 768, 1024)

    vertexShader = buildShader("attribute vec4 Position; attribute vec4 SourceColor; varying vec4 DestinationColor; uniform mat4 Projection; uniform mat4 Modelview; void main(void) { DestinationColor = SourceColor; gl_Position = Projection * Modelview * Position; }", GL_VERTEX_SHADER)
    fragmentShader = buildShader("varying lowp vec4 DestinationColor; void main(void) { gl_FragColor = DestinationColor; }", GL_FRAGMENT_SHADER)

    m_simpleProgram = glCreateProgram()
    glAttachShader(m_simpleProgram, vertexShader);
    glAttachShader(m_simpleProgram, fragmentShader);
    glLinkProgram(m_simpleProgram);

    linkSuccess = glGetProgramiv(m_simpleProgram, GL_LINK_STATUS)
    if linkSuccess == GL_FALSE:
        infolog = glGetProgramInfoLog(m_simpleProgram)
        print "error linking shader", infolog

    glUseProgram(m_simpleProgram)

    a = 1.0 / 2
    b = 1.0 / 3
    ortho = [
        a, 0, 0, 0,
        0, b, 0, 0,
        0, 0, -1, 0,
        0, 0, 0, 1
    ]


    projectionUniform = glGetUniformLocation(m_simpleProgram, "Projection")
#    glUniformMatrix4fv(projectionUniform, 1, 0, ortho)
    glUniformFoo(projectionUniform, 1., 1.)

    zRotation = [
        1, 0, 0, 0,
        0, 1, 0, 0,
        0, 0, 1, 0,
        0, 0, 0, 1
    ]

    modelviewUniform = glGetUniformLocation(m_simpleProgram, "Modelview")
#    glUniformMatrix4fv(modelviewUniform, 1, 0, zRotation)
    glUniformFoo(modelviewUniform, 2., 3.)

    glClearColor(0.3, 0.4, 0.5, 1)
    glClear(GL_COLOR_BUFFER_BIT)


    positionSlot = glGetAttribLocation(m_simpleProgram, "Position")
    colorSlot = glGetAttribLocation(m_simpleProgram, "SourceColor")

    glEnableVertexAttribArray(positionSlot);
    glEnableVertexAttribArray(colorSlot);

    stride = 6

    glVertexAttribPointer(positionSlot, 2, GL_FLOAT, GL_FALSE, 0, coords);
    glVertexAttribPointer(colorSlot, 4, GL_FLOAT, GL_FALSE, 0, colors);

    vertexCount = 6
    glDrawArrays(GL_TRIANGLES, 0, vertexCount);

    glDisableVertexAttribArray(positionSlot);
    glDisableVertexAttribArray(colorSlot);


while True:
    from kivy.core.sdl import setup_window, poll, flip
    from time import sleep

    setup_window(768, 1024, False, True)

    while True:
        poll()
        render()
        flip()
        sleep(1/60.)
