import time
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
#from random import randint
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self,ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x,velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(4,0)):
        self.ball.center = self.center
        # self.ball.velocity = Vector(4,0).rotate(randint(0,360))
        self.ball.velocity = vel

    def update(self,dt):
        self.ball.move()

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if (self.ball.y < self.y) or (self.ball.top > self.top):
            self.ball.velocity_y *= -1
        
        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4,0))
        
        if self.ball.right > self.width:
            self.player1.score += 1
            self.serve_ball(vel=(-4,0))
        
        # if (self.ball.y < 0) or (self.ball.top > self.height):
        #     self.ball.velocity_y *= -1
        
        # if (self.ball.x < 0) or (self.ball.right > self.width):
        #     self.ball.velocity_x *= -1
    
    def on_touch_move(self, touch):
        if touch.x < self.width /3:
            self.player1.center_y = touch.y
        
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y
    
    def reset_game(self):
        self.player1.score = 0
        self.player2.score = 0
        self.serve_ball()
    
    def exit_game(self):
        App.get_running_app().stop()

class PongApp(App):
    
    def build(self):
        layout = BoxLayout(orientation = "vertical")

        game = PongGame()
        layout.add_widget(game)

        button_layout = BoxLayout(size_hint_y=None, height="50dp")
        reset_button = Button(text="Reiniciar juego")
        exit_button = Button(text="Salir del juego")

        reset_button.bind(on_release=lambda x: game.reset_game())
        exit_button.bind(on_release=lambda x: game.exit_game())

        button_layout.add_widget(reset_button)
        button_layout.add_widget(exit_button)

        layout.add_widget(button_layout)

        game.serve_ball()
        Clock.schedule_interval(game.update,1.0/60.0)
        return layout
    

if __name__ == "__main__":
    PongApp().run()