import random
import arcade



class Apple(arcade.Sprite):
    def __init__(self ,game):
        super().__init__("class/snake/apple.png", scale=1.0)  # مسیر نسبی تصویر
        self.width = 20
        self.height = 20
        self.center_x = random.randint(5 , game.width - 5)  # جلوگیری از خروج از صفحه و موقعیت فعلی براساس اندازه صفحه عوض شود
        self.center_y = random.randint(5 , game.height - 5)  # جلوگیری از خروج از صفحه و موقعیت فعلی براساس اندازه صفحه عوض شود
        self.change_x = 0  # چون سیب قرار نیست تکون بخوره
        self.change_y = 0  # چون سیب قرار نیست تکون بخوره
    
    
    
class Snake(arcade.Sprite):
    def __init__(self ,game):
        super().__init__()
        self.width = 20
        self.height = 20
        self.center_x = game.width // 2  # برای این از // استفاده کردیم چون جواب عدد صحیح در بیاد و اعشاری نشه چون اگه ابعاد صفحه فرد باشه عدد اعشاری میشه
        self.center_y = game.height // 2
        self.color = (0, 255, 0)
        
    def draw(self):
        #  برای تعیین موقعیت مستطیل rect ایحاد شی 
        rect = arcade.Rect(
            left=self.center_x - self.width / 2,   # مختصات سمت چپ
            right=self.center_x + self.width / 2,  # مختصات سمت راست
            bottom=self.center_y - self.height / 2, # مختصات پایین
            top=self.center_y + self.height / 2,    # مختصات بالا
            width=self.width,                      # عرض مستطیل
            height=self.height,                    # ارتفاع مستطیل
            x=self.center_x - self.width / 2,      # مختصات  گوشه پایین-چپ x 
            y=self.center_y - self.height / 2      #  مختصات  گوشه پایین-چپ y   
        )
        arcade.draw_rect_filled(rect= rect ,color= self.color)   #  رسم مستطیل تو پر سبز
            
    
    
    
class Game(arcade.Window):
    def __init__(self):
        super().__init__(width=500, height=500, title="Super Snake 🐍 v1")
        arcade.set_background_color(arcade.color.KHAKI)
        self.snake = Snake(self)  #   self.snake و اختصاص دادن ان به Snake  ایجاد کلاس 
        self.food = Apple(self)   #   self.food و اختصاص دادن ان به Apple  ایجاد کلاس 
        
        self.food_list = arcade.SpriteList()
        self.food_list.append(self.food)  # SpriteList افزودن سیب به 
        
        self.snake_list = arcade.SpriteList() # SpriteList افزودن مار به 
        self.snake_list.append(self.snake)
        
        
        
    def on_draw(self):
        self.clear()          # پاک کردن صفحه
        self.snake.draw()     # show snake
        self.food_list.draw() # show apple
        
        
        
        
    
    
if __name__ == "__main__":
    game = Game()
    arcade.run()