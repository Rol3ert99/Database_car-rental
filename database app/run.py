import mysql.connector
from tkinter import *

root = Tk()
root.geometry("1200x700")
root.title("Car rental")

mydb = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'Wal!48102',
        database = 'car_rental')

db_cursor = mydb.cursor()



def add_client(f_name_box, l_name_box, phone):
        query = "INSERT INTO klient (imie, nazwisko, numer_telefonu) VALUES (%s, %s, %s)"
        data = (f_name_box.get(), l_name_box.get(), phone.get())
        db_cursor.execute(query, data)
        mydb.commit()
        f_name_box.delete(0, END)
        l_name_box.delete(0, END)
        phone.delete(0, END)



def new_client():
        client_window = Tk()
        client_window.geometry("280x250")
        client_window.title("Klient")
        title_label = Label(client_window, text = "NOWY KLIENT").grid(row=0, column=0, columnspan=2)
        f_name_label = Label(client_window, text='Imie').grid(row=1, column=0, sticky=W, padx = 10, pady = 5)
        l_name_label = Label(client_window, text='Nazwisko').grid(row=2, column=0, sticky=W, padx = 10, pady = 5)
        phone_label = Label(client_window, text='Numer telefonu').grid(row=3, column=0, sticky=W, padx = 10, pady = 5)
        f_name_box = Entry(client_window)
        f_name_box.grid(row=1, column=1, padx = 10)
        l_name_box = Entry(client_window)
        l_name_box.grid(row=2, column=1, padx = 10)
        phone_box = Entry(client_window)
        phone_box.grid(row=3, column=1, padx = 10)
        add_client_button = Button(client_window, text="Dodaj nowego klienta", command=lambda: add_client(f_name_box, l_name_box, phone_box)).grid(row=4, column=0, columnspan=2)
        client_window.mainloop()





rent_button = Button(root, text='Wypożyczenie samochodu', font = 10).grid(row=0, column=0, sticky = W, padx = 10, pady = 5, ipady=5, ipadx =5)
reception_button = Button(root, text='Odbiór samochodu', font = 10).grid(row=1, column=0, sticky = W, padx = 10, pady = 5, ipady=5, ipadx =37)
new_client_button = Button(root, text='Nowy klient', font=10, command=new_client).grid(row=2, column=0, sticky = W, padx = 10, pady = 5, ipady=5, ipadx =70)
client_removal_button = Button(root, text='Usunięcie klienta', font=10).grid(row=3, column=0, sticky = W, padx = 10, pady = 5, ipady=5, ipadx =48)
modification_button = Button(root, text='Modyfikacja OC lub PT', font=10).grid(row=4, column=0, sticky = W, padx = 10, pady = 5, ipady=5, ipadx =19)
new_car_button = Button(root, text='Dodanie samochodu', font=10, state = DISABLED).grid(row=5, column=0, sticky = W, padx = 10, pady = 5, ipady=5, ipadx =32)
car_removal_button = Button(root, text='Usunięcie samochodu', font=10, state = DISABLED).grid(row=6, column=0, sticky = W, padx = 10, pady = 5, ipady=5, ipadx =27)
salary_modification_button = Button(root, text='Zmaian wynagrodzenia', font=10, state = DISABLED).grid(row=7, column=0, sticky = W, padx = 10, pady = 5, ipady=5, ipadx =21)

db_cursor.execute("SELECT id, marka, model, rok_produkcji, pojemnosc_silnika, moc_silnika, ilosc_drzwi, typ_nadwozia, color FROM samochod WHERE stan_wypożyczenia='niewypozyczony'")
result = db_cursor.fetchall()
label = Label(root, text="Dostępne samochody: ").grid(row=0, column=1, padx=(100, 10))
label_car_number = Label(root, text="ID").grid(row=1, column=1)
label_marka = Label(root, text="Marka").grid(row=1, column=2)
label_model = Label(root, text="Model").grid(row=1, column=3)
label_year = Label(root, text="Rok produkcji").grid(row=1, column=4)
label_engine = Label(root, text="Silnik").grid(row=1,column=5)
label_km = Label(root, text="Km").grid(row=1,column=6)
label_door_number = Label(root, text="Liczba drzwi").grid(row=1,column=7)
label_typ = Label(root, text="Nadwozie").grid(row=1, column=8)
label_color = Label(root, text="Kolor").grid(row=1, column=9)
for index, x in enumerate(result):
        i = 1
        for y in x:
                car_label = Label(root, text=y).grid(row = index+2, column=i)
                i = i+1


root.mainloop()