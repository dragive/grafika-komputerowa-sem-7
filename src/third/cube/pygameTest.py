import numpy as np
import pygame
import pygame as pg
import pyrr
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from pygame.constants import *


class App:

    def __init__(self):
        pg.init()
        pg.display.set_mode((640, 480), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()

        glClearColor(0, 0, 0, 1)
        glEnable(GL_DEPTH_TEST)
        self.shader = self.create_shader('vertex.txt', 'fragment.txt')
        glUseProgram(self.shader)
        self.cube_mesh = CubeMesh()
        self.cube = Cube(
            position=[0, 0, -3],
            eulers=[10, 10, 10]
        )

        projection_transform = pyrr.matrix44.create_perspective_projection(
            fovy=45, aspect=640 / 480,
            near=0.1, far=10, dtype=np.float32
        )
        glUniformMatrix4fv(glGetUniformLocation(self.shader, "projection"),
                           1, GL_FALSE, projection_transform)

        self.modelMatrixLocation = glGetUniformLocation(self.shader, "model")
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

            if pygame.key.get_pressed()[K_w]:
                self.cube.eulers[0] += 1
                if self.cube.eulers[0] > 360:
                    self.cube.eulers[0] -= 360
            elif pygame.key.get_pressed()[K_s]:
                self.cube.eulers[0] -= 1
                if self.cube.eulers[0] < 0:
                    self.cube.eulers[0] += 360

            if pygame.key.get_pressed()[K_a]:
                self.cube.eulers[1] += 1
                if self.cube.eulers[1] > 360:
                    self.cube.eulers[1] -= 360
            elif pygame.key.get_pressed()[K_d]:
                self.cube.eulers[1] -= 1
                if self.cube.eulers[1] < 0:
                    self.cube.eulers[1] += 360

            if pygame.key.get_pressed()[K_q]:
                self.cube.eulers[2] += 1
                if self.cube.eulers[2] > 360:
                    self.cube.eulers[2] -= 360
            elif pygame.key.get_pressed()[K_e]:
                self.cube.eulers[2] -= 1
                if self.cube.eulers[2] < 0:
                    self.cube.eulers[2] += 360

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            glUseProgram(self.shader)

            model_transform = pyrr.matrix44.create_identity(dtype=np.float32)

            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_eulers(
                    eulers=np.radians(self.cube.eulers), dtype=np.float32
                )
            )
            model_transform = pyrr.matrix44.multiply(
                m1=model_transform,
                m2=pyrr.matrix44.create_from_translation(
                    vec=np.array(self.cube.position), dtype=np.float32
                )
            )
            glUniformMatrix4fv(self.modelMatrixLocation, 1, GL_FALSE, model_transform)

            glBindVertexArray(self.cube_mesh.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.cube_mesh.vertex_count)

            pg.display.flip()

            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.cube_mesh.destroy()
        glDeleteProgram(self.shader)

        pg.quit()


class CubeMesh:
    def __init__(self):
        self.verticies = (
            -0.5, -0.5, -0.5, 0, 1, 0,  # green
            0.5, -0.5, -0.5, 0, 1, 1,  # green blue
            0.5, 0.5, -0.5, 1, 1, 1,  # white

            0.5, 0.5, -0.5, 1, 1, 1,  # white
            -0.5, 0.5, -0.5, 1, 1, 0,  # green red
            -0.5, -0.5, -0.5, 0, 1, 0,  # green

            -0.5, -0.5, 0.5, 0, 0, 0,  # black
            0.5, -0.5, 0.5, 0, 0, 1,  # blue
            0.5, 0.5, 0.5, 1, 0, 1,  # red Blue

            0.5, 0.5, 0.5, 1, 0, 1,  # red Blue
            -0.5, 0.5, 0.5, 1, 0, 0,  # red
            -0.5, -0.5, 0.5, 0, 0, 0,  # black

            -0.5, 0.5, 0.5, 1, 0, 0,  # red
            -0.5, 0.5, -0.5, 1, 1, 0,  # green red
            -0.5, -0.5, -0.5, 0, 1, 0,  # green

            -0.5, -0.5, -0.5, 0, 1, 0,  # green
            -0.5, -0.5, 0.5, 0, 0, 0,  # white
            -0.5, 0.5, 0.5, 1, 0, 0,  # red

            0.5, 0.5, 0.5, 1, 0, 1,  # red blue
            0.5, 0.5, -0.5, 1, 1, 1,  # white
            0.5, -0.5, -0.5, 0, 1, 1,  # green blue

            0.5, -0.5, -0.5, 0, 1, 1,  # green blue
            0.5, -0.5, 0.5, 0, 0, 1,  # blue
            0.5, 0.5, 0.5, 1, 0, 1,  # red blue

            -0.5, -0.5, -0.5, 0, 1, 0,  # green
            0.5, -0.5, -0.5, 0, 1, 1,  # green blue
            0.5, -0.5, 0.5, 0, 0, 1,  # blue

            0.5, -0.5, 0.5, 0, 0, 1,  # blue
            -0.5, -0.5, 0.5, 0, 0, 0,  # black
            -0.5, -0.5, -0.5, 0, 1, 0,  # green

            -0.5, 0.5, -0.5, 1, 1, 0,  # green red
            0.5, 0.5, -0.5, 1, 1, 1,  # white
            0.5, 0.5, 0.5, 1, 0, 1,  # red blue

            0.5, 0.5, 0.5, 1, 0, 1,  # red blue
            -0.5, 0.5, 0.5, 1, 0, 0,  # red
            -0.5, 0.5, -0.5, 1, 1, 0,  # green red
        )

        self.verticies = np.array(self.verticies, dtype=np.float32)

        self.vertex_count = len(self.verticies) // 6

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


class Cube:

    def __init__(self, position, eulers):
        self.position = np.array(position, dtype=np.float32)
        self.eulers = np.array(eulers, dtype=np.float32)


if __name__ == '__main__':
    myApp = App()
