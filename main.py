from sqlite3 import Date
from tkinter import *
import datetime
from tkinter import messagebox
from turtle import width
import qrcode
from fpdf import FPDF
import os

# create window
list_operatores = [str(i) for i in range(1, 17)]


def check_fields():
    operator = operator_entry.get()
    data
    material = "AG100H"
    pdf_loc = r"https://drive.google.com/file/d/1GldZoQGR5j_g_MEETvSdtNKxuOJ6CQOs/view?usp=sharing"

    if operator == "":
        messagebox.showerror(
            title="Erro",
            message="operador não informado!",
        )
        return

    if operator not in list_operatores:
        messagebox.showerror(
            title="Erro",
            message="Código de operador está incorreto!",
        )
        return

    # string a ser indicada no qr code gerado -> caminho do pdf analisado

    qr_code_fp = criar_qr_code(pdf_loc)  # operator,data,pdf_loc

    pdf_fp = criar_pdf(qr_code_fp, operator, data, material)

    ## send to print

    os.remove(qr_code_fp)

    os.remove(pdf_fp)


def criar_qr_code(url):  # params = op,date,pdfpath
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    temp = "qrcodetemp.png"
    img.save(temp)
    return temp


def criar_pdf(qr, OP, date, material):
    pdf = FPDF(orientation="P", unit="mm", format=(200, 200))
    pdf.add_page()
    pdf.set_font("Arial", "B", 30)
    pdf.set_text_color(0, 0, 0)
    pdf.image(name=qr, w=180, h=155)
    pdf.text(x=85, y=165, txt="OP: {}".format(OP))
    pdf.text(x=75, y=180, txt=date)
    pdf.text(x=80, y=195, txt=material)
    temp = "etiqueta.pdf"
    pdf.output(temp)
    return temp


app = Tk()

# label creation
operator_text = StringVar()
operator_label = Label(app, text="operator: ", font=("bold", 14), pady=20)
# label location
operator_label.grid(row=0, column=0, sticky=W)

# entry creation
operator_entry = Entry(app, textvariable=operator_text)
operator_entry.grid(row=0, column=1, sticky=W)

# data
data = datetime.datetime.today().strftime("%d/%m/%Y")
data_label = Label(app, text="Data: ", font=("bold", 14), pady=20)
data_text = Label(app, text=data, font=("bold", 14), pady=20)
data_label.grid(row=0, column=3, sticky=E)
data_text.grid(row=0, column=4, sticky=E)


# Qrc button
qr_code_btn = Button(
    app, text="Imprimir QR Code", width=24, font=("bold", 16), command=check_fields
)
qr_code_btn.grid(row=2, column=3)

app.title("Bar Code Reader")
app.geometry("1000x550")

app.mainloop()
