import glob
import os
import mysql.connector

from tkinter import *
from tkinter.ttk import Frame, Button, Label, Style

from PIL import Image
from PIL.ImageTk import PhotoImage
import sys

class DBEngine:
    def __init__(self):
        db_config = {'user': 'rohan', 'database': 'products'}
        self.connection = mysql.connector.connect(**db_config)
        self.cursor = self.connection.cursor()                          

    def exec_stmt(self, stmt):
        self.cursor.execute(stmt)
        self.connection.commit()

    def exec_qry(self, qry):
        self.cursor.execute(qry)
        res = self.cursor.fetchall()
        return res


class Example(Frame):   
    def __init__(self, unlabeled_img_files):
        super().__init__()  

        self.dbm = DBEngine()
        self.stmt_tmpl = "insert into texture_type (image_file_id, tex_type) values ('{file_name}', '{section}')"

        self.index = 0
        self.unlabeled_img_files = unlabeled_img_files
        self.max_index = len(self.unlabeled_img_files)       

        self.init_gui()        
        
    def init_gui(self):      
        self.master.title('Threedy texture labeler')
        self.style = Style()
        self.style.theme_use("default")
                
        frame1 = Frame(self)
        frame1.grid(row=0, column=0)

        frame2 = Frame(self)
        frame2.grid(row=0, column=1)

        self.canvas = Canvas(frame1)
        self.canvas.pack()
        
        self.pack(fill=BOTH, expand=True)
        self.master.resizable(False, False)

        top_btn = Button(frame2, text='top', command=self._insert_top)
        top_btn.grid(row=0, column=0, padx=5, pady=2)

        stem_btn = Button(frame2, text='stem', command=self._insert_stem)
        stem_btn.grid(row=1, column=0, padx=5, pady=2)

        base_btn = Button(frame2, text='base', command=self._insert_base)
        base_btn.grid(row=2, column=0, padx=5, pady=2)

        close_btn = Button(frame2, text='close', command=self.master.quit)
        close_btn.grid(row=3, column=0, padx=5, pady=2)

        self.draw_next_image()

    def draw_next_image(self):                
        if self.index >= self.max_index:
            print('done')
            self.master.quit()
            sys.exit(0)         

        self.cur_img_fname = self.unlabeled_img_files[self.index]        
        self.photo_img = PhotoImage(Image.open(self.cur_img_fname))
        self.canvas.create_image(100, 100, image=self.photo_img)
        self.canvas.image = self.photo_img
        self.index += 1

    def _insert(self, file_name, section):
        stmt = self.stmt_tmpl.format(file_name=file_name, section=section)
        self.dbm.exec_stmt(stmt)

    def _insert_top(self):
        self._insert(self.cur_img_fname, 'top')
        self.draw_next_image()

    def _insert_stem(self):
        self._insert(self.cur_img_fname, 'stem')
        self.draw_next_image()

    def _insert_base(self):
        self._insert(self.cur_img_fname, 'base')
        self.draw_next_image()

def get_labeled_img_files():
    dbm = DBEngine()    
    qry = 'select image_file_id from texture_type where tex_type is not null;'
    res = dbm.exec_qry(qry)
    labeled_img_files = set(x[0] for x in res)
    return labeled_img_files


def get_unlabeled_img_files(images_dir):
    all_img_files = set()
    extensions = ['.jpg', '.png']
    for fn in os.listdir(images_dir):
        for ext in extensions:
            if fn.endswith(ext):
                all_img_files.add(fn)

    labeled_img_files = get_labeled_img_files()
    unlabeled_img_files = all_img_files.difference(labeled_img_files)
    unlabeled_img_files = list(unlabeled_img_files)
    return unlabeled_img_files


def main():
    images_dir = '.'
    unlabeled_img_files = get_unlabeled_img_files(images_dir)
    if len(unlabeled_img_files) == 0:
        print('No unlabeled files found. Clear `products.texture_type` table and relaunch.')
        return

    root = Tk()
    root.geometry("400x300+300+300")
    app = Example(unlabeled_img_files)
    root.mainloop()  
    

if __name__ == '__main__':
    main()  