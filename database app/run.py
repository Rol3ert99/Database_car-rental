from calendar import c
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

def change_rent_status(id_box):
        id = int(id_box.get())
        query = "UPDATE samochod set stan_wypożyczenia = 'wypozyczony' WHERE id = %s"
        data = (id,)
        db_cursor.execute(query, data)
        mydb.commit()


def rent_car():
        rent_window = Tk()
        rent_window.geometry('520x200')
        rent_window.title("Wypożyczenie")
        label_id = Label(rent_window, text="Podaj id wypożyczanego samochodu:").grid(row=0, column=0, padx=30)
        id_box = Entry(rent_window)
        id_box.grid(row=0, column=1, pady = 20)
        label_client = Label(rent_window, text="Podaj id klienta").grid(row=1, column=0, padx=30)
        client_box = Entry(rent_window)
        client_box.grid(row=1, column=1)
        submit_button = Button(rent_window, text="Wypożycz", command=lambda:change_rent_status(id_box))
        submit_button.grid(row=3, column=1)
        db_cursor.execute("SELECT id, imie, nazwisko, numer_telefonu FROM klient")
        result = db_cursor.fetchall()
        label = Label(rent_window, text="Zarejestrowani klienci: ").grid(row=4, column=0, padx=(10, 10))     
        id_label = Label(rent_window, text="ID").grid(row=5, column=0)   
        f_name_label = Label(rent_window, text="Imie").grid(row=5, column=1)
        l_name_label = Label(rent_window, text="Nazwisko").grid(row=5, column=2)
        phone_label = Label(rent_window, text="Telefon").grid(row=5, column=3)
        for index, x in enumerate(result):
                i = 0
                for y in x:
                        car_label = Label(rent_window, text=y).grid(row = index+6, column=i)
                        i = i+1


def reception(id_box):
        id = int(id_box.get())
        query = "UPDATE samochod set stan_wypożyczenia = 'niewypozyczony' WHERE id = %s"
        data = (id,)
        db_cursor.execute(query, data)
        mydb.commit()


def reception_car():
        db_cursor.execute("SELECT id, marka, model, rok_produkcji, pojemnosc_silnika, moc_silnika,  color FROM samochod WHERE stan_wypożyczenia='wypozyczony'")
        result = db_cursor.fetchall()
        reception_window = Tk()
        reception_window.title("Odbiór")
        reception_window.geometry('700x300')
        id_label = Label(reception_window, text="Podaj id odbieranego samochodu: ")
        id_label.grid(row=0, column=0, columnspan=2)
        id_box = Entry(reception_window)
        id_box.grid(row=0, column=2, columnspan=2, pady=20)
        reception_button = Button(reception_window, text="Odbierz", command=lambda: reception(id_box))
        reception_button.grid(row=0, column=4, columnspan=2)
        label = Label(reception_window, text="Wypożyczone samochody: ").grid(row=1, column=0, padx=(10, 10))
        label_car_number = Label(reception_window, text="ID").grid(row=2, column=0)
        label_marka = Label(reception_window, text="Marka").grid(row=2, column=1)
        label_model = Label(reception_window, text="Model").grid(row=2, column=2)
        label_year = Label(reception_window, text="Rok produkcji").grid(row=2, column=3)
        label_engine = Label(reception_window, text="Silnik").grid(row=2,column=4)
        label_km = Label(reception_window, text="Km").grid(row=2,column=5)
        label_color = Label(reception_window, text="Kolor").grid(row=2, column=6)
        for index, x in enumerate(result):
                i = 0
                for y in x:
                        car_label = Label(reception_window, text=y).grid(row = index+3, column=i)
                        i = i+1


def show_available_cars():
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


def remove_client_query(id_box):
        id = int(id_box.get())
        query = "DELETE FROM klient WHERE id = %s"
        data = (id,)
        db_cursor.execute(query, data)
        mydb.commit()        


def remove_client():
        client_window = Tk()
        client_window.geometry('400x400')
        client_window.title('Usunięcie klienta')
        db_cursor.execute("SELECT id, imie, nazwisko, numer_telefonu, data_ostatniego_wypozyczenia FROM klient")
        result = db_cursor.fetchall()
        id_label = Label(client_window, text="Podaj id klienta: ")
        id_label.grid(row=0, column=0, columnspan=2)
        id_box = Entry(client_window)
        id_box.grid(row=0, column=2, columnspan=2, pady=20)
        remove_button = Button(client_window, text="Usuń", command=lambda: remove_client_query(id_box))
        remove_button.grid(row=0, column=4, columnspan=2)
        label = Label(client_window, text="Zarejestrowani klienci: ").grid(row=1, column=0, padx=(10, 10))     
        id_label = Label(client_window, text="ID").grid(row=1, column=0)   
        f_name_label = Label(client_window, text="Imie").grid(row=1, column=1)
        l_name_label = Label(client_window, text="Nazwisko").grid(row=1, column=2)
        phone_label = Label(client_window, text="Telefon").grid(row=1, column=3)
        for index, x in enumerate(result):
                i = 0
                for y in x:
                        car_label = Label(client_window, text=y).grid(row = index+2, column=i)
                        i = i+1
        

rent_button = Button(root, text='Wypożyczenie samochodu', font = 10, command=rent_car).grid(row=0, column=0, sticky = W, padx = 10, pady = 5, ipady=5, ipadx =5)
reception_button = Button(root, text='Odbiór samochodu', font = 10, command=reception_car).grid(row=1, column=0, sticky = W, padx = 10, pady = 5, ipady=5, ipadx =37)
new_client_button = Button(root, text='Nowy klient', font=10, command=new_client).grid(row=2, column=0, sticky = W, padx = 10, pady = 5, ipady=5, ipadx =70)
client_removal_button = Button(root, text='Usunięcie klienta', font=10, command=remove_client).grid(row=3, column=0, sticky = W, padx = 10, pady = 5, ipady=5, ipadx =48)
modification_button = Button(root, text='Modyfikacja OC lub PT', font=10).grid(row=4, column=0, sticky = W, padx = 10, pady = 5, ipady=5, ipadx =19)
new_car_button = Button(root, text='Dodanie samochodu', font=10, state = DISABLED).grid(row=5, column=0, sticky = W, padx = 10, pady = 5, ipady=5, ipadx =32)
car_removal_button = Button(root, text='Usunięcie samochodu', font=10, state = DISABLED).grid(row=6, column=0, sticky = W, padx = 10, pady = 5, ipady=5, ipadx =27)
salary_modification_button = Button(root, text='Zmaian wynagrodzenia', font=10, state = DISABLED).grid(row=7, column=0, sticky = W, padx = 10, pady = 5, ipady=5, ipadx =21)



show_available_cars()


root.mainloop()