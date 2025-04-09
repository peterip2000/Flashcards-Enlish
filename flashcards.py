import random

# 單字庫
vocabulary = {
    "蘋果": "apple",
    "香蕉": "banana",
    "貓": "cat",
    "狗": "dog",
    "書": "book",
    "電腦": "computer",
    "手機": "phone",
    "桌子": "table",
    "椅子": "chair",
    "水": "water"
}

def play_flashcards():
    print("歡迎使用英文單字卡！")
    print("請輸入對應的英文單字。輸入 'q' 可以退出遊戲。")
    
    # 將單字轉換為列表以便隨機選擇
    words = list(vocabulary.items())
    random.shuffle(words)
    
    correct = 0
    total = len(words)
    
    for chinese, english in words:
        print(f"\n中文: {chinese}")
        user_input = input("請輸入英文: ").strip().lower()
        
        if user_input == 'q':
            print("\n遊戲結束！")
            break
            
        if user_input == english:
            print("✓ 正確！")
            correct += 1
        else:
            print(f"✗ 錯誤！正確答案是: {english}")
    
    print(f"\n遊戲結束！你的得分是: {correct}/{total}")

if __name__ == "__main__":
    play_flashcards() 