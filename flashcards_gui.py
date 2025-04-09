import tkinter as tk
from tkinter import ttk, filedialog
from PIL import Image, ImageTk
import random
import os

class RoundedFrame(tk.Canvas):
    def __init__(self, parent, width, height, corner_radius, bg="white", **kwargs):
        super().__init__(parent, width=width, height=height, bg=bg, highlightthickness=0, **kwargs)
        self.corner_radius = corner_radius
        self.bg = bg
        
        # Create rounded rectangle
        self.round_rectangle(0, 0, width, height, radius=corner_radius, fill=bg)
    
    def round_rectangle(self, x1, y1, x2, y2, radius=25, **kwargs):
        points = [
            x1+radius, y1,
            x2-radius, y1,
            x2, y1,
            x2, y1+radius,
            x2, y2-radius,
            x2, y2,
            x2-radius, y2,
            x1+radius, y2,
            x1, y2,
            x1, y2-radius,
            x1, y1+radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)

class FlashcardsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("English Flashcards")
        
        # 設置窗口大小
        self.root.geometry("800x600")
        
        # 單字庫
        self.vocabulary = {
            "書本": "book",
            "蘋果": "apple",
            "香蕉": "banana",
            "貓": "cat",
            "狗": "dog",
            "電腦": "computer",
            "手機": "phone",
            "桌子": "table",
            "椅子": "chair",
            "水": "water"
        }
        
        # 文件路徑
        self.current_file = None
        
        # 當前單字
        self.current_word = None
        
        # 創建主框架
        self.main_frame = tk.Frame(root, bg="white")  # 設置主框架背景為白色
        self.main_frame.pack(fill="both", expand=True)
        
        # 載入背景圖片
        try:
            bg_image = Image.open("night_sky.jpg")
            bg_image = bg_image.resize((800, 600))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            
            # 創建背景標籤
            bg_label = tk.Label(self.main_frame, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except:
            # 如果找不到圖片，使用白色背景
            self.main_frame.configure(bg="white")
        
        # 創建中文顯示區域（圓角白色背景）
        self.chinese_frame = RoundedFrame(self.main_frame, width=250, height=120, corner_radius=15, bg="white")
        self.chinese_frame.place(relx=0.5, rely=0.3, anchor="center")
        
        self.chinese_label = tk.Label(self.chinese_frame, text="", font=("Arial", 24), bg="white")
        self.chinese_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # 創建輸入框（使用圓角樣式）
        self.entry_style = ttk.Style()
        self.entry_style.configure("Custom.TEntry", padding=10)
        
        self.entry = ttk.Entry(self.main_frame, style="Custom.TEntry", font=("Arial", 14))
        self.entry.place(relx=0.5, rely=0.5, anchor="center", width=200)
        
        # 綁定 Enter 鍵
        self.entry.bind("<Return>", self.check_answer)
        
        # 創建結果顯示區域（圓角白色背景）- 放在輸入框下方
        self.result_frame = RoundedFrame(self.main_frame, width=250, height=120, corner_radius=15, bg="white")
        self.result_frame.place(relx=0.5, rely=0.65, anchor="center")
        
        self.result_label = tk.Label(self.result_frame, text="", font=("Arial", 16), bg="white")
        self.result_label.place(relx=0.5, rely=0.5, anchor="center")
        
        # 添加載入單字庫按鈕
        self.load_button = tk.Button(
            self.main_frame, 
            text="載入單字庫", 
            command=self.load_vocabulary,
            font=("Arial", 12),
            bg="#4CAF50",
            fg="white",
            relief=tk.RAISED,
            bd=0
        )
        self.load_button.place(relx=0.5, rely=0.8, anchor="center")
        
        
        # 版權信息（黑色字體）
        copyright_label = tk.Label(self.main_frame, 
                                 text="©English flashcards 2024",
                                 fg="black",
                                 bg="white")  # 設置背景色與主框架相同
        copyright_label.place(relx=0.5, rely=0.95, anchor="center")
        
        # 開始遊戲
        self.next_word()
    
    def load_vocabulary(self):
        file_path = filedialog.askopenfilename(
            title="選擇單字庫文件",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                self.vocabulary = {}
                with open(file_path, 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip()
                        if line and ':' in line:
                            chinese, english = line.split(':', 1)
                            self.vocabulary[chinese.strip()] = english.strip()
                
                self.current_file = os.path.basename(file_path)
                self.root.title(f"English Flashcards - {self.current_file}")
                
                # 如果成功載入，更新當前單字
                if self.vocabulary:
                    self.next_word()
                else:
                    self.result_label.config(text="單字庫為空！", fg="red")
            except Exception as e:
                self.result_label.config(text=f"載入失敗：{str(e)}", fg="red")
    
    def next_word(self):
        if not self.vocabulary:
            self.chinese_label.config(text="請載入單字庫")
            return
            
        # 隨機選擇一個單字
        self.current_word = random.choice(list(self.vocabulary.items()))
        self.chinese_label.config(text=self.current_word[0])
        self.entry.delete(0, tk.END)
        self.result_label.config(text="")
    
    def check_answer(self, event=None):
        user_answer = self.entry.get().strip().lower()
        correct_answer = self.current_word[1].lower()
        
        if user_answer == correct_answer:
            self.result_label.config(text="✓ 正確！", fg="green")
        else:
            self.result_label.config(text=f"✗ 錯誤！\n正確答案: {correct_answer}", fg="red")
        
        # 延遲1.5秒後顯示下一個單字
        self.root.after(1500, self.next_word)

if __name__ == "__main__":
    root = tk.Tk()
    app = FlashcardsApp(root)
    root.mainloop()