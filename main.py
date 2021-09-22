import random
import arcade

SPRITE_SCALING_WRAITH = 0.5
SPRITE_SCALING_TALIBAN = 0.5
SPRITE_SCALING_armory = 0.8

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Wraith vs. Taliban"


spell_speed = 2
taliban_speed = 2

wraith_inventory = 3

TALIBAN_VERTICAL_MARGIN = 15
RIGHT_TALIBAN_BORDER = SCREEN_WIDTH - TALIBAN_VERTICAL_MARGIN
LEFT_TALIBAN_BORDER = TALIBAN_VERTICAL_MARGIN

TALIBAN_MOVE_DOWN_AMOUNT = 30

GAME_OVER = 1
PLAY_GAME = 0
SCALING = 2


class MyGame(arcade.Window):
    def __init__(self):


        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)


        self.wraith_list = None
        self.taliban_list = None
        self.wraith_spells = None
        self.taliban_missle_list = None
        self.kabul_shield_wall = None


        self.taliban_uniforms = None #textures


        self.game_state = PLAY_GAME


        self.wraith_sprite = None
        self.score = 0


        self.taliban_change_x = -taliban_speed

        #wont show mouse cursor
        self.set_mouse_visible(False)

        # Load sounds
        self.spell_sound = arcade.load_sound("knifeSlice.ogg")
        self.hit_sound = arcade.load_sound("arcade-a-primer_sounds_Collision.wav")

        arcade.set_background_color(arcade.color.AMAZON)



    def setup_level_one(self):

        self.taliban_uniforms = []
        texture = arcade.load_texture("cloud.png", mirrored=True)
        self.taliban_uniforms.append(texture)
        texture = arcade.load_texture("cloud.png")
        self.taliban_uniforms.append(texture)

        # Creates rows and columns of clouds
        x_count = 7
        x_start = 380
        x_spacing = 60
        y_count = 5
        y_start = 420
        y_spacing = 40
        for x in range(x_start, x_spacing * x_count + x_start, x_spacing):
            for y in range(y_start, y_spacing * y_count + y_start, y_spacing):


                enemy = arcade.Sprite()
                enemy.scale = SPRITE_SCALING_TALIBAN
                enemy.texture = self.taliban_uniforms[1]

                # Position the enemy
                enemy.center_x = x
                enemy.center_y = y

                # Add the enemy to the list
                self.taliban_list.append(enemy)

    def make_twall(self, x_start):

        wall_width = 5
        wall_height = 10
        wall_width_count = 20
        wall_height_count = 5
        y_start = 150
        for x in range(x_start, x_start + wall_width_count * wall_width, wall_width):
            for y in range(y_start, y_start + wall_height_count * wall_height, wall_height):
                wall_sprite = arcade.SpriteSolidColor(wall_width, wall_height, arcade.color.RED)
                wall_sprite.center_x = x
                wall_sprite.center_y = y
                self.kabul_shield_wall.append(wall_sprite)

    def setup(self):


        self.game_state = PLAY_GAME

        # Sprite list
        self.wraith_list = arcade.SpriteList()
        self.taliban_list = arcade.SpriteList()
        self.wraith_spells = arcade.SpriteList()
        self.taliban_missle_list = arcade.SpriteList()
        self.kabul_shield_wall = arcade.SpriteList(is_static=True)


        self.score = 0


        self.wraith_sprite = arcade.Sprite("Wraith1.png", SPRITE_SCALING_WRAITH)
        self.wraith_sprite.center_x = 50
        self.wraith_sprite.center_y = 40
        self.wraith_list.append(self.wraith_sprite)

        for x in range(75, 800, 190):
            self.make_twall(x)

        # Set the background color
        arcade.set_background_color(arcade.color.PURPLE)

        self.setup_level_one()
    def reinforcements(self, delta_time: float):
        enemy = MyGame("jet.png", SCALING )
        enemy.left = random.randint(self.width, self.width + 8)
        enemy.top = random.randint(8, self.height - 10)
        enemy.velocity = (random.randint(-200, -50), 0)

        self.taliban_list.append(enemy)
        self.wraith_list.append(enemy)

    def on_draw(self):

        arcade.start_render()

        # draw sprites
        self.taliban_list.draw()
        self.wraith_spells.draw()
        self.taliban_missle_list.draw()
        self.kabul_shield_wall.draw()
        self.wraith_list.draw()

        # Render the text
        arcade.draw_text(f"Score: {self.score}", 10, 20, arcade.color.WHITE, 14)

        # Draw game over if the game state is such
        if self.game_state == GAME_OVER:
            arcade.draw_text(f"GAME OVER", 250, 300, arcade.color.WHITE, 55)
            self.set_mouse_visible(True)

    def on_mouse_motion(self, x, y, dx, dy):

        if self.game_state == GAME_OVER:
            return

        self.wraith_sprite.center_x = x

    def on_mouse_press(self, x, y, button, modifiers):

        #prevents bullet spamming
        if len(self.wraith_spells) < wraith_inventory:


            arcade.play_sound(self.spell_sound)

            # Create a spell
            spell = arcade.Sprite("Spells Effect.png", SPRITE_SCALING_armory)

            spell.angle = 90

            spell.change_y = spell_speed

            spell.center_x = self.wraith_sprite.center_x
            spell.bottom = self.wraith_sprite.top

            self.wraith_spells.append(spell)

    def update_enemies(self):


        for enemy in self.taliban_list:
            enemy.center_x += self.taliban_change_x

        move_down = False
        for enemy in self.taliban_list:
            if enemy.right > RIGHT_TALIBAN_BORDER and self.taliban_change_x > 0:
                self.taliban_change_x *= -1
                move_down = True
            if enemy.left < LEFT_TALIBAN_BORDER and self.taliban_change_x < 0:
                self.taliban_change_x *= -1
                move_down = True

        if move_down:
            for enemy in self.taliban_list:
                enemy.center_y -= TALIBAN_MOVE_DOWN_AMOUNT
                if self.taliban_change_x > 0:
                    enemy.texture = self.taliban_uniforms[0]
                else:
                    enemy.texture = self.taliban_uniforms[1]

    def taliban_fires_back(self):

        x_spawn = []
        for enemy in self.taliban_list:
            chance = 4 + len(self.taliban_list) * 4

            if random.randrange(chance) == 0 and enemy.center_x not in x_spawn:

                bullet = arcade.Sprite("missile.png", SPRITE_SCALING_armory)

                bullet.angle = 180

                bullet.change_y = -spell_speed

                bullet.center_x = enemy.center_x
                bullet.top = enemy.bottom

                self.taliban_missle_list.append(bullet)

            x_spawn.append(enemy.center_x)

    def process_taliban_missles(self):

        self.taliban_missle_list.update()

        for bullet in self.taliban_missle_list:
            hit_list = arcade.check_for_collision_with_list(bullet, self.kabul_shield_wall)

            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()
                continue

            if arcade.check_for_collision_with_list(self.wraith_sprite, self.taliban_missle_list):
                self.game_state = GAME_OVER

            if bullet.top < 0:
                bullet.remove_from_sprite_lists()

    def process_wraith_spells(self):

        self.wraith_spells.update()

        for bullet in self.wraith_spells:

            hit_list = arcade.check_for_collision_with_list(bullet, self.kabul_shield_wall)
            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()
                for shield in hit_list:
                    shield.remove_from_sprite_lists()
                continue

            hit_list = arcade.check_for_collision_with_list(bullet, self.taliban_list)

            if len(hit_list) > 0:
                bullet.remove_from_sprite_lists()

            for enemy in hit_list:
                enemy.remove_from_sprite_lists()
                self.score += 1

                arcade.play_sound(self.hit_sound)

            #removes missle if it goes off screen
            if bullet.bottom > SCREEN_HEIGHT:
                bullet.remove_from_sprite_lists()

    def on_update(self, delta_time):


        if self.game_state == GAME_OVER:
            return

        self.update_enemies()
        self.taliban_fires_back()
        self.process_taliban_missles()
        self.process_wraith_spells()

        if len(self.taliban_list) == 0:
            self.setup_level_one()


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()