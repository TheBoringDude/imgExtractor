from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image
from PIL.ExifTags import TAGS
import os, threading

# defined vars
bgColor = '#eee'

class ScrollableFrame(ttk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        canvas = Canvas(self, height=380)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
root = Tk()

#APP Info
label1 = Label(root, text="IMG Extractor", font=['Century Gothic', 18])
label1.pack(pady=5)
label2 = Label(root, text='Extract metadata information from images', font=['Century Gothic', 10])
label2.pack()

# TOP Frame
HeadFrame = Frame(root)
HeadFrame.pack(pady=10, padx=20)
btnChooseImg = Button(HeadFrame, text='Select Image', padx=10, fg='black', bg='gray', font=['Century Gothic', 10], command=lambda:getImage_source())
btnChooseImg.grid(row=0)
lblImgSrc = Label(HeadFrame, text='...')
lblImgSrc.grid(row=0, column=1)

btnExtract = Button(root, text="Extract", fg='white', bg='blue', padx=20, pady=5, font=['Century Gothic', 10], command=lambda:initExtract())
btnExtract.pack(pady=5)

lblFilename = Label(root, text="...", font=['Century Gothic', 9])
lblFilename.pack()

# ================== GET IMAGE SOURCE
def getImage_source():
    global imgName
    imgName = filedialog.askopenfilename(title="Select Image", 
                                            filetypes=[("Image Files", ".jpg .jpeg")])
    lblImgSrc.config(text=imgName)
    btnChooseImg.config(text="Change Image")

# ================== GET DATA FROM IMAGE
def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_labeled_exif(exif):
    labeled = {}
    for (key, val) in exif.items():
        labeled[TAGS.get(key)] = val
    return labeled

def initExtract():
    t = threading.Thread(target=extractData)
    t.daemon = True
    t.start()

def extractData():
    lblFilename.config(text=os.path.split(imgName)[1])
    try:
        exif = get_exif(imgName)
        imgData = get_labeled_exif(exif)
        imgData.pop('UserComment', None)
        plotData(imgData)
    except Exception:
        messagebox.showerror("No DATA!", "There are no exif data to be extracted from the chosen Image.")

# ================== GET DATA FROM IMAGE

# DATA Frame
DataFrame = ScrollableFrame(root)
def plotData(data):
    n = 0
    for x in data:
        try:
            if isinstance(data[x], (bytes, bytearray)):
                data[x] = data[x].decode()
            Label(DataFrame.scrollable_frame, text=x, anchor='w', font=['Century Gothic', 10]).grid(sticky=W, row=n, column=0)
            Label(DataFrame.scrollable_frame, text=str(data[x]), fg='green', anchor='w', font=['Century Gothic', 10]).grid(sticky=E, row=n, column=1)
            n+=1
        except (UnicodeDecodeError):
            pass

DataFrame.pack(padx=10)

root.title("IMG Exif Extractor")
root.configure(bg=bgColor)
root.geometry('450x600')
root.mainloop()