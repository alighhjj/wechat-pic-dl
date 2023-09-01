import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import re  

folder_path = "none"

# 判断公众号链接是否正确
def match_url(text):  
    pattern = r'https://mp.weixin.qq.com/'  
    match = re.search(pattern, text)  
    if match: 
        return True  
    else:  
        return False 

def download_images(article_url):
    # 判断保存地址是否选定
    if folder_path == "none":
        messagebox.showinfo("错误", "请先选择保存地址！")
    else:
        # 获取文章页面内容
        response = requests.get(article_url)
        soup = BeautifulSoup(response.text, "html.parser")

        # 获取所有图片链接
        image_links = []
        for img in soup.find_all("img"):
            img_url = img.get("data-src") 
            if img_url is not None:
            # 执行处理图片链接的操作
                image_links.append(img.get("data-src"))
        progress['value'] = 0
        cons = len(image_links) 
        print(cons) 
        for i, url in enumerate(image_links):
            # print(url)
            response = requests.get(url)
            with open(f"{folder_path}/image_{i}.jpg", "wb") as f:
                f.write(response.content)
            item = (i+1)/cons*100
            print(f"{folder_path}/image_{i}.jpg")
            progress['value'] = item  
            window.update()  
        messagebox.showinfo("提示", "图片下载完成！")

# 创建GUI窗口
window = tk.Tk()
window.geometry("400x200")
window.title("微信公众号图片爬取程序")

# 文章链接输入框
url_label = tk.Label(window, text="公众号文章链接：")
url_label.pack()
url_entry = tk.Entry(window, width=300)
url_entry.pack(fill="x")

frame1 = tk.Frame(window)
frame2 = tk.Frame(window)
frame3 = tk.Frame(window)
frame3.pack(side="bottom")
frame1.pack(side='left',fill='both', pady=30, expand=True)
frame2.pack(side='left',fill='both', pady=30, expand=True)


# 下载目录选择按钮
def chose_folder():
    global folder_path
    folder_path = filedialog.askdirectory(title="选择保存文件夹")
    if not folder_path:
        return
file_button = tk.Button(frame1, text="选择地址", command=chose_folder, bg="#FDF5E6")
file_button.pack()

# 开始下载按钮
def start_download():
    article_url = url_entry.get()
    if match_url(article_url):
        download_images(article_url)
    else:
        messagebox.showinfo("错误", "请填写正确的公众号地址！")
download_button = tk.Button(frame2, text="开始下载", command=start_download, bg="#87CEFA")
download_button.pack()

# 创建进度条
progress = ttk.Progressbar(frame3, length=500, mode='determinate')  
progress.pack()

window.mainloop()