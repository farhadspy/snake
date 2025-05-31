import random
import arcade



class Apple(arcade.Sprite):
    def __init__(self ,game):
        super().__init__("class/snake/apple.png", scale=1.0)  # مسیر نسبی تصویر
        self.width = 20
        self.height = 20
        self.game = game
        self.respawn()  # تنظیم اولیه موقعیت
        
    def respawn(self):
        # تنظیم مختصات برای جلوگیری از خروج سیب از کادر
        base_x = random.randint(10, self.game.width - 30)  # حداقل 10 پیکسل از لبه چپ، حداکثر 30 پیکسل از لبه راست
        self.center_x = base_x + 5  # جابه‌جایی 5 پیکسل به سمت راست
        self.center_y = random.randint(10, self.game.height - 30)  # حداقل 10 پیکسل از لبه پایین، حداکثر 30 پیکسل از لبه بالا
    
    
    
class Snake(arcade.Sprite):
    def __init__(self ,game):
        super().__init__()
        self.width = 20
        self.height = 20
        self.center_x = (game.width // self.width) * self.width // 2  # شروع روی شبکه
        self.center_y = (game.height // self.height) * self.height // 2
        self.color1 = arcade.color.JUNGLE_GREEN
        self.color2 = arcade.color.RED_DEVIL
        self.length = 1  # طول اولیه مار
        self.change_x = 0
        self.change_y = 0
        self.body = []  # لیستی برای ذخیره قطعات بدنه مار
        self.speed = self.width  # سرعت برابر با اندازه یک خانه
        self.score = 0
        self.stripe_length = 1  # تعداد بخش‌ها برای هر راه (برای فاصله بیشتر)
        self.just_ate = False  # پرچم برای تأخیر بعد از خوردن
        
    def draw(self):
       # رسم بدنه مار
        # رسم بدنه مار با راه‌راه‌های بزرگ‌تر
        for i, segment in enumerate(self.body):
            rect = arcade.Rect(
                left=segment["x"] - self.width // 2,
                right=segment["x"] + self.width // 2,
                bottom=segment["y"] - self.height // 2,
                top=segment["y"] + self.height // 2,
                width=self.width,
                height=self.height,
                x=segment["x"] - self.width // 2,
                y=segment["y"] - self.height // 2
            )
            # محاسبه شاخص راه‌راه بر اساس تعداد بخش‌ها
            stripe_index = i // self.stripe_length  # هر self.stripe_length بخش، رنگ عوض می‌شه
            if stripe_index % 2 == 0 and self.score:  # رنگ اول برای زوج‌ها
                arcade.draw_rect_filled(rect=rect, color=self.color1)
            elif stripe_index % 2 == 1 and self.score:  # رنگ دوم برای فردها
                arcade.draw_rect_filled(rect=rect, color=self.color2)
        
        # رسم سر مار (گرد)
        arcade.draw_circle_filled(
            center_x=self.center_x-10,
            center_y=self.center_y-10,
            radius=self.width / 2,
            color=arcade.color.DARK_GREEN
        )
           
    def update(self):
        self.body.append({"x": self.center_x, "y": self.center_y})  # اضافه کردن موقعیت فعلی سر به بدنه
        # حذف آخرین قطعه اگر طول از حد مجاز بیشتر باشد
        if len(self.body) > self.length:
            self.body.pop(0)
        # به‌روزرسانی موقعیت سر
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.just_ate = False  # ریست پرچم بعد از حرکت

        
    def move(self ,direction):
        if direction == "L":
            self.change_x = -self.speed
            self.change_y = 0
        elif direction == "R":
            self.change_x = self.speed
            self.change_y = 0
        elif direction == "U":
            self.change_x = 0
            self.change_y = self.speed
        elif direction == "D":
            self.change_x = 0
            self.change_y = -self.speed
    
    def eat(self):
        self.score += 1
        self.just_ate = True  # تنظیم پرچم بعد از خوردن
    
    def t_score(self ,height):
        arcade.draw_text(f"Score: {self.score}", 10, height - 30, arcade.color.BLACK, 16)      
        
        
class PauseMenu:
    def __init__(self):
        self.paused = False
        self.show_pause_menu = False

    def draw(self):
        if self.paused and self.show_pause_menu:
            # تنظیم مختصات مستطیل برای صفحه 500x500
            # وسط صفحه: (250, 250)
            # عرض مستطیل: 300، ارتفاع: 150
            arcade.draw_lrbt_rectangle_filled(
                left=100,    # 250 - 150
                right=400,   # 250 + 150
                top=325,     # 250 + 75
                bottom=175,  # 250 - 75
                color=arcade.color.DARK_SLATE_BLUE
            )
            # تنظیم مختصات و اندازه متن‌ها
            arcade.draw_text("Game Paused", 150, 280, arcade.color.WHITE, 24)
            arcade.draw_text("R: Resume", 185, 240, arcade.color.WHITE, 18)
            arcade.draw_text("Q: Quit", 200, 200, arcade.color.WHITE, 18)

    def handle_key_press(self, key: int):
        if key == arcade.key.ESCAPE:
            self.paused = not self.paused
            self.show_pause_menu = self.paused
            return True
        elif self.paused:
            if key == arcade.key.R:
                self.paused = False
                self.show_pause_menu = False
                return True
            elif key == arcade.key.Q:
                arcade.exit()
                return True
        return False       


class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=500, height=500, title="Super Snake 🐍 v1")
        arcade.set_background_color(arcade.color.KHAKI)
        self.snake = Snake(self)  #   self.snake و اختصاص دادن ان به Snake  ایجاد کلاس 
        self.food = Apple(self)   #   self.food و اختصاص دادن ان به Apple  ایجاد کلاس 
        
        self.food_list = arcade.SpriteList()
        self.food_list.append(self.food)  # SpriteList افزودن سیب به 
        
        self.snake_list = arcade.SpriteList() 
        self.snake_list.append(self.snake)   # SpriteList افزودن مار به 
        
        # اضافه کردن منوی توقف
        self.pause_menu = PauseMenu()
        
        self.game_over = False
        
        self.move_timer = 0  # تایمر برای کنترل زمان حرکت
        self.move_interval = 0.1  # بازه زمانی بین حرکت‌ها (۰٫۱ ثانیه)
             
    def on_draw(self):
        self.clear()          # پاک کردن صفحه
        self.snake.draw()     # show snake
        self.food_list.draw() # show apple
        if self.game_over:
            arcade.draw_text("Game Over!", self.width // 2 - 50, self.height // 2, arcade.color.RED, 20)
        #  مختصات نمایش امتیاز
        self.snake.t_score(self.height)
        # رسم منوی توقف
        self.pause_menu.draw()
        
    def on_key_press(self, key: int, modifiers: int):
        if self.pause_menu.handle_key_press(key):
            return  # اگه منو ورودی رو پردازش کرد، ادامه نمی‌دیم
        if key == arcade.key.UP and self.snake.change_y == 0:
            self.snake.move("U")
        elif key == arcade.key.DOWN and self.snake.change_y == 0:
            self.snake.move("D")
        elif key == arcade.key.LEFT and self.snake.change_x == 0:
            self.snake.move("L")
        elif key == arcade.key.RIGHT and self.snake.change_x == 0:
            self.snake.move("R")
            
    def on_update(self, delta_time):
        if not self.pause_menu.paused and not self.game_over: 
            self.move_timer += delta_time  # افزایش تایمر با زمان فریم
            if self.move_timer >= self.move_interval:  # اگه تایمر به بازه رسید
                self.snake.update()  # به‌روزرسانی موقعیت مار
                self.move_timer = 0  # ریست تایمر      
                
                # بررسی برخورد با دیوار
                if (self.snake.center_x < 15 or self.snake.center_x > self.width or
                    self.snake.center_y < 15 or self.snake.center_y > self.height):
                    self.game_over = True
                    print("Game Over: Hit the wall!")
                # بررسی برخورد با سیب
                if not self.snake.just_ate and arcade.check_for_collision(self.snake, self.food):
                    self.snake.length += 0.5
                    print(f"Snake ate apple! Length: {self.snake.length}, Snake pos: ({self.snake.center_x}, {self.snake.center_y}), Apple pos: ({self.food.center_x}, {self.food.center_y})")
                    # مکان جدید سیب
                    self.food.respawn()
                    self.snake.eat()
                    print("score: " ,self.snake.score)
                
    
                print("snake.just_ate: " ,self.snake.just_ate)   
                # بررسی برخورد با خود
                if not self.snake.just_ate:
                    for segment in self.snake.body[:-1]:
                        if abs(self.snake.center_x - segment["x"]) < self.snake.width * 0.8 and \
                           abs(self.snake.center_y - segment["y"]) < self.snake.height * 0.8:
                            self.game_over = True
                            print(f"Game Over: Snake hit itself! Head: ({self.snake.center_x}, {self.snake.center_y}), "
                                  f"Segment: ({segment['x']}, {segment['y']})")
                            print("Body segments:", self.snake.body)
                            break
            
                
            
                
  
if __name__ == "__main__":
    game = Game()
    arcade.run()