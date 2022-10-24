import pygame as pg
from OpenGL.GL import *
import numpy as np
from OpenGL.GL.shaders import compileShader, compileProgram


class App:

    def __init__(self):
        pg.init()
        pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        glClearColor(0, 0, 0, 1)
        self.shader = self.create_shader('vertex.txt','fragment.txt')
        glUseProgram(self.shader)
        self.triangle = Triangle()
        self.mainLoop()

    def create_shader(self, vertex_file_path, fragment_vertex_path):
        with open(vertex_file_path, 'r') as file:
            vertex_src = file.readlines()

        with open(fragment_vertex_path, 'r') as file:
            fragment_src = file.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER),
        )
        return shader

    def mainLoop(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
            glClear(GL_COLOR_BUFFER_BIT)

            glUseProgram(self.shader)
            glBindVertexArray(self.triangle.vao)
            glDrawArrays(GL_TRIANGLES,0,self.triangle.vertex_count)


            pg.display.flip()

            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.triangle.destroy()
        glDeleteProgram(self.shader)

        pg.quit()


class Triangle:
    def __init__(self):
        self.verticies = (
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
            0, 0.5, 0.0, 0.0, 0.0, 1.0,
        )

        self.verticies = np.array(self.verticies, dtype=np.float32)

        self.vertex_count = 3

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.verticies.nbytes, self.verticies, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))

    def destroy(self):
        glDeleteBuffers(1, (self.vbo,))
        glDeleteVertexArrays(1, (self.vao,))


if __name__ == '__main__':
    myApp = App()
