from calendar import c
import mysql.connector
from tkinter import *

root = Tk()
root.geometry("1200x700")
root.title("Car rental")

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='Wal!48102',
    database='car_rental')

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
    title_label = Label(client_window, text="NOWY KLIENT").grid(row=0, column=0, columnspan=2)
    f_name_label = Label(client_window, text='Imie').grid(row=1, column=0, sticky=W, padx=10, pady=5)
    l_name_label = Label(client_window, text='Nazwisko').grid(row=2, column=0, sticky=W, padx=10, pady=5)
    phone_label = Label(client_window, text='Numer telefonu').grid(row=3, column=0, sticky=W, padx=10, pady=5)
    f_name_box = Entry(client_window)
    f_name_box.grid(row=1, column=1, padx=10)
    l_name_box = Entry(client_window)
    l_name_box.grid(row=2, column=1, padx=10)
    phone_box = Entry(client_window)
    phone_box.grid(row=3, column=1, padx=10)
    add_client_button = Button(client_window, text="Dodaj nowego klienta",
                               command=lambda: add_client(f_name_box, l_name_box, phone_box)).grid(row=4, column=0,
                                                                                                   columnspan=2)
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
    id_box.grid(row=0, column=1, pady=20)
    label_client = Label(rent_window, text="Podaj id klienta").grid(row=1, column=0, padx=30)
    client_box = Entry(rent_window)
    client_box.grid(row=1, column=1)
    submit_button = Button(rent_window, text="Wypożycz", command=lambda: change_rent_status(id_box))
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
            car_label = Label(rent_window, text=y).grid(row=index + 6, column=i)
            i = i + 1


def reception(id_box):
    id = int(id_box.get())
    query = "UPDATE samochod set stan_wypożyczenia = 'niewypozyczony' WHERE id = %s"
    data = (id,)
    db_cursor.execute(query, data)
    mydb.commit()


def reception_car():
    db_cursor.execute(
        "SELECT id, marka, model, rok_produkcji, pojemnosc_silnika, moc_silnika,  color FROM samochod WHERE stan_wypożyczenia='wypozyczony'")
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
    label_engine = Label(reception_window, text="Silnik").grid(row=2, column=4)
    label_km = Label(reception_window, text="Km").grid(row=2, column=5)
    label_color = Label(reception_window, text="Kolor").grid(row=2, column=6)
    for index, x in enumerate(result):
        i = 0
        for y in x:
            car_label = Label(reception_window, text=y).grid(row=index + 3, column=i)
            i = i + 1


def show_available_cars():
    db_cursor.execute(
        "SELECT id, marka, model, rok_produkcji, pojemnosc_silnika, moc_silnika, ilosc_drzwi, typ_nadwozia, color FROM samochod WHERE stan_wypożyczenia='niewypozyczony'")
    result = db_cursor.fetchall()
    label = Label(root, text="Dostępne samochody: ").grid(row=0, column=1, padx=(100, 10))
    label_car_number = Label(root, text="ID").grid(row=1, column=1)
    label_marka = Label(root, text="Marka").grid(row=1, column=2)
    label_model = Label(root, text="Model").grid(row=1, column=3)
    label_year = Label(root, text="Rok produkcji").grid(row=1, column=4)
    label_engine = Label(root, text="Silnik").grid(row=1, column=5)
    label_km = Label(root, text="Km").grid(row=1, column=6)
    label_door_number = Label(root, text="Liczba drzwi").grid(row=1, column=7)
    label_typ = Label(root, text="Nadwozie").grid(row=1, column=8)
    label_color = Label(root, text="Kolor").grid(row=1, column=9)
    for index, x in enumerate(result):
        i = 1
        for y in x:
            car_label = Label(root, text=y).grid(row=index + 2, column=i)
            i = i + 1


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
            car_label = Label(client_window, text=y).grid(row=index + 2, column=i)
            i = i + 1


def add_car(make, model, year, displacement, power, door_num, chasis_type, reception_status, PT, OC, price, color):
        query = "INSERT INTO samochod (marka, model, rok_produkcji, pojemnosc_silnika, moc_silnika, ilosc_drzwi, typ_nadwozia, stan_wypożyczenia, data_waznosci_PT, data_waznosci_OC, cena_dobowa_wypozyczenia, color) VALUES (%s, %s, %s ,%s, %s, %s, %s, %s, %s, %s, %s,%s)"
        data = (make.get(), model.get(), year.get(), displacement.get(), power.get(), door_num.get(), chasis_type.get(), reception_status.get(), PT.get(), OC.get(), price.get(), color.get())
        db_cursor.execute(query, data)
        mydb.commit()
        make.delete(0, END)
        model.delete(0, END)
        year.delete(0, END)
        displacement.delete(0, END)
        power.delete(0, END)
        door_num.delete(0, END)
        chasis_type.delete(0, END)
        reception_status.delete(0, END)
        PT.delete(0, END)
        OC.delete(0, END)
        price.delete(0, END)
        color.delete(0, END)


def new_car():
    car_window = Tk()
    car_window.geometry("700x250")
    car_window.title("Samochod")
    title_label = Label(car_window, text="NOWY SAMOCHOD").grid(row=0, column=0, columnspan=4)
    make_label = Label(car_window, text='Marka').grid(row=1, column=0, sticky=W, padx=10, pady=5)
    model_label = Label(car_window, text='Model').grid(row=2, column=0, sticky=W, padx=10, pady=5)
    year_label = Label(car_window, text='Rok produkcji').grid(row=3, column=0, sticky=W, padx=10, pady=5)
    displacement_label = Label(car_window, text='Pojemnosc silnika').grid(row=4, column=0, sticky=W, padx=10, pady=5)
    power_label = Label(car_window, text='Moc silnika').grid(row=5, column=0, sticky=W, padx=10, pady=5)
    door_label = Label(car_window, text='Liczba drzwi').grid(row=6, column=0, sticky=W, padx=10, pady=5)
    chasis_label = Label(car_window, text='Typ nadwozia').grid(row=1, column=2, sticky=W, padx=10, pady=5)
    reception_label = Label(car_window, text='Stan wypozyczenia').grid(row=2, column=2, sticky=W, padx=10, pady=5)
    PT_label = Label(car_window, text='Data waznosci PT').grid(row=3, column=2, sticky=W, padx=10, pady=5)
    OC_label = Label(car_window, text='Data waznosci OC').grid(row=4, column=2, sticky=W, padx=10, pady=5)
    price_label = Label(car_window, text='Cena dobowa wypozyczenia').grid(row=5, column=2, sticky=W, padx=10, pady=5)
    color_label = Label(car_window, text='Kolor').grid(row=6, column=2, sticky=W, padx=10, pady=5)
    make_box = Entry(car_window)
    make_box.grid(row=1, column=1, padx=10)
    model_box = Entry(car_window)
    model_box.grid(row=2, column=1, padx=10)
    year_box = Entry(car_window)
    year_box.grid(row=3, column=1, padx=10)
    displacement_box = Entry(car_window)
    displacement_box.grid(row=4, column=1, padx=10)
    power_box = Entry(car_window)
    power_box.grid(row=5, column=1, padx=10)
    door_box = Entry(car_window)
    door_box.grid(row=6, column=1, padx=10)
    chasis_box = Entry(car_window)
    chasis_box.grid(row=1, column=3, padx=10)
    reception_box = Entry(car_window)
    reception_box.grid(row=2, column=3, padx=10)
    PT_box = Entry(car_window)
    PT_box.grid(row=3, column=3, padx=10)
    OC_box = Entry(car_window)
    OC_box.grid(row=4, column=3, padx=10)
    price_box = Entry(car_window)
    price_box.grid(row=5, column=3, padx=10)
    color_box = Entry(car_window)
    color_box.grid(row=6, column=3, padx=10)

    add_car_button = Button(car_window, text="Dodaj nowy samochod",
                               command=lambda: add_car(make_box, model_box, year_box, displacement_box, power_box, door_box, chasis_box, reception_box, PT_box, OC_box, price_box, color_box)).grid(row=7, column=0,
                                                                                                   columnspan=4)
    car_window.mainloop()


def add_worker(f_name_box, l_name_box, password, position, salary, phone):
    query = "INSERT INTO pracownik (imie, nazwisko, haslo, stanowisko, wynagrodzenie, numer_telefonu_sluzbowego) VALUES (%s, %s, %s, %s, %s, %s)"
    data = (f_name_box.get(), l_name_box.get(), password.get(), position.get(), salary.get(), phone.get())
    db_cursor.execute(query, data)
    mydb.commit()
    f_name_box.delete(0, END)
    l_name_box.delete(0, END)
    password.delete(0, END)
    position.delete(0, END)
    salary.delete(0, END)
    phone.delete(0, END)


def new_worker():
    worker_window = Tk()
    worker_window.geometry("280x250")
    worker_window.title("Pracownik")
    title_label = Label(worker_window, text="NOWY Pracownik").grid(row=0, column=0, columnspan=2)
    f_name_label = Label(worker_window, text='Imie').grid(row=1, column=0, sticky=W, padx=10, pady=5)
    l_name_label = Label(worker_window, text='Nazwisko').grid(row=2, column=0, sticky=W, padx=10, pady=5)
    password_label = Label(worker_window, text='Haslo').grid(row=3, column=0, sticky=W, padx=10, pady=5)
    position_label = Label(worker_window, text='Stanowisko').grid(row=4, column=0, sticky=W, padx=10, pady=5)
    salary_label = Label(worker_window, text='Wynagrodzenie').grid(row=5, column=0, sticky=W, padx=10, pady=5)
    phone_label = Label(worker_window, text='Telefon sluzbowy').grid(row=6, column=0, sticky=W, padx=10, pady=5)
    f_name_box = Entry(worker_window)
    f_name_box.grid(row=1, column=1, padx=10)
    l_name_box = Entry(worker_window)
    l_name_box.grid(row=2, column=1, padx=10)
    password_box = Entry(worker_window)
    password_box.grid(row=3, column=1, padx=10)
    position_box = Entry(worker_window)
    position_box.grid(row=4, column=1, padx=10)
    salary_box = Entry(worker_window)
    salary_box.grid(row=5, column=1, padx=10)
    phone_box = Entry(worker_window)
    phone_box.grid(row=6, column=1, padx=10)
    add_worker_button = Button(worker_window, text="Dodaj nowego pracownika",
                               command=lambda: add_worker(f_name_box, l_name_box, password_box,position_box, salary_box, phone_box)).grid(row=7, column=0,
                                                                                                   columnspan=2)
    worker_window.mainloop()


def remove_worker_query(id_box):
    id = int(id_box.get())
    query = "DELETE FROM pracownik WHERE id = %s"
    data = (id,)
    db_cursor.execute(query, data)
    mydb.commit()


def remove_worker():
    worker_window = Tk()
    worker_window.geometry('700x400')
    worker_window.title('Zwolnienie pracownika')
    db_cursor.execute("SELECT id, imie, nazwisko, haslo, stanowisko, wynagrodzenie, numer_telefonu_sluzbowego FROM pracownik")
    result = db_cursor.fetchall()
    id_label = Label(worker_window, text="Podaj id pracownika: ")
    id_label.grid(row=0, column=2, columnspan=2)
    id_box = Entry(worker_window)
    id_box.grid(row=0, column=4, columnspan=2, pady=20)
    remove_button = Button(worker_window, text="Usuń", command=lambda: remove_worker_query(id_box))
    remove_button.grid(row=0, column=5, columnspan=2)
    label = Label(worker_window, text="Lista pracownikow: ").grid(row=0, column=0, padx=(10, 10))
    id_label = Label(worker_window, text="ID").grid(row=1, column=0)
    f_name_label = Label(worker_window, text="Imie").grid(row=1, column=1)
    l_name_label = Label(worker_window, text="Nazwisko").grid(row=1, column=2)
    password_label = Label(worker_window, text="Haslo").grid(row=1, column=3)
    position_label = Label(worker_window, text="Stanowisko").grid(row=1, column=4)
    salary_label = Label(worker_window, text="Wynagrodzenie").grid(row=1, column=5)
    phone_label = Label(worker_window, text="Telefon").grid(row=1, column=6)
    for index, x in enumerate(result):
        i = 0
        for y in x:
            car_label = Label(worker_window, text=y).grid(row=index + 2, column=i)
            i = i + 1


def OC_PT_modify_query(id_car, OC_date, PT_date):
        query = "UPDATE samochod SET data_waznosci_PT= %s, data_waznosci_OC= %s WHERE id = %s"
        values = (PT_date.get(), OC_date.get(), id_car.get())
        db_cursor.execute(query, values)


def OC_PT_modify():
        modification_window = Tk()
        modification_window.title("OC, PT")
        modification_window.geometry('850x400')
        modification_label = Label(modification_window, text='Podaj id samochodu, którego OC lub PT chcesz zmodyfikować: ')
        modification_label.grid(row=0, column=0, padx = 10, pady=10)
        modification_box = Entry(modification_window)
        modification_box.grid(row=0, column=1)
        OC_label = Label(modification_window, text="Wprowadź nowy termin ważnosci OC: ")
        OC_label.grid(row=1, column=0)
        OC_box = Entry(modification_window)
        OC_box.grid(row=1, column=1)
        PT_label = Label(modification_window, text="Wprowadź nowy termin ważnosci PT: ")
        PT_label.grid(row=2, column=0, pady=10)
        PT_box = Entry(modification_window)
        PT_box.grid(row=2, column=1, pady=10)
        cars_label = Label(modification_window, text="Samochody: ")
        cars_label.grid(row=3, column=0, sticky=W)
        submit_button = Button(modification_window, text="Zatwierdź", command = lambda: OC_PT_modify_query(modification_box, OC_box, PT_box))
        submit_button.grid(row=1, column = 2, columnspan=2, ipadx=10)
        db_cursor.execute("SELECT id, marka, model, rok_produkcji, pojemnosc_silnika, data_waznosci_PT, data_waznosci_OC, color FROM samochod")
        result = db_cursor.fetchall()
        label_car_number = Label(modification_window, text="ID").grid(row=4, column=0)
        label_marka = Label(modification_window, text="Marka").grid(row=4, column=1)
        label_model = Label(modification_window, text="Model").grid(row=4, column=2)
        label_year = Label(modification_window, text="Rok produkcji").grid(row=4, column=3)
        label_engine = Label(modification_window, text="Silnik").grid(row=4,column=4)
        label_PT = Label(modification_window, text="PT").grid(row=4, column=5)
        label_OC = Label(modification_window, text="OC").grid(row=4, column=6)
        label_color = Label(modification_window, text="Kolor").grid(row=4, column=7)
        for index, x in enumerate(result):
                i = 0
                for y in x:
                        car_label = Label(modification_window, text=y).grid(row = index+5, column=i)
                        i = i+1


def salary_modufy_query(id_worker, new_salary):
    query = "UPDATE pracownik SET wynagrodzenie= %s WHERE id = %s"
    values = (new_salary.get(), id_worker.get())
    db_cursor.execute(query, values)

def salary_modify():
        modification_window = Tk()
        modification_window.title("Wynagrodzenia")
        modification_window.geometry('850x400')
        modification_label = Label(modification_window,
                                   text='Podaj id pracownika, którego wynagrodzenie chcesz zmodyfikować: ')
        modification_label.grid(row=0, column=0, padx=10, pady=10)
        modification_box = Entry(modification_window)
        modification_box.grid(row=0, column=1)
        salary_label = Label(modification_window, text="Wprowadz wyoskosc nowego wynagrodzenia: ")
        salary_label.grid(row=1, column=0)
        salary_box = Entry(modification_window)
        salary_box.grid(row=1, column=1)
        worker_label = Label(modification_window, text="Pracownicy: ")
        worker_label.grid(row=2, column=0, sticky=W)
        submit_button = Button(modification_window, text="Zatwierdź",
                               command=lambda: salary_modufy_query(modification_box,salary_box))
        submit_button.grid(row=1, column=2, columnspan=2, ipadx=10)
        db_cursor.execute(
            "SELECT id, imie, nazwisko, stanowisko, wynagrodzenie FROM pracownik")
        result = db_cursor.fetchall()
        label_car_number = Label(modification_window, text="ID").grid(row=4, column=0)
        label_marka = Label(modification_window, text="Imie").grid(row=4, column=1)
        label_model = Label(modification_window, text="Nazwisko").grid(row=4, column=2)
        label_year = Label(modification_window, text="Stanowisko").grid(row=4, column=3)
        label_engine = Label(modification_window, text="Wynagrodzenie").grid(row=4, column=4)

        for index, x in enumerate(result):
            i = 0
            for y in x:
                car_label = Label(modification_window, text=y).grid(row=index + 5, column=i)
                i = i + 1



rent_button = Button(root, text='Wypożyczenie samochodu', font=10, command=rent_car).grid(row=0, column=0, sticky=W,
                                                                                          padx=10, pady=5, ipady=5,
                                                                                          ipadx=5)
reception_button = Button(root, text='Odbiór samochodu', font=10, command=reception_car).grid(row=1, column=0, sticky=W,
                                                                                              padx=10, pady=5, ipady=5,
                                                                                              ipadx=37)
new_client_button = Button(root, text='Nowy klient', font=10, command=new_client).grid(row=2, column=0, sticky=W,
                                                                                       padx=10, pady=5, ipady=5,
                                                                                       ipadx=70)
client_removal_button = Button(root, text='Usunięcie klienta', font=10, command=remove_client).grid(row=3, column=0,
                                                                                                    sticky=W, padx=10,
                                                                                                    pady=5, ipady=5,
                                                                                                    ipadx=48)
modification_button = Button(root, text='Modyfikacja OC lub PT', font=10, command=OC_PT_modify).grid(row=4, column=0, sticky=W, padx=10,
                                                                               pady=5, ipady=5, ipadx=19)
new_car_button = Button(root, text='Dodanie samochodu', font=10, command=new_car).grid(row=5, column=0, sticky=W,
                                                                                      padx=10, pady=5, ipady=5,
                                                                                      ipadx=32)
car_removal_button = Button(root, text='Usunięcie samochodu', font=10, state=DISABLED).grid(row=6, column=0, sticky=W,
                                                                                            padx=10, pady=5, ipady=5,
                                                                                            ipadx=27)
new_worker_button = Button(root, text='Nowy pracownik', font=10, command=new_worker).grid(row=7, column=0,
                                                                                                     sticky=W, padx=10,
                                                                                                     pady=5, ipady=5,
                                                                                                     ipadx=21)
remove_worker_button = Button(root, text='Zwolnij pracownika', font=10, command=remove_worker).grid(row=8, column=0,
                                                                                                     sticky=W, padx=10,
                                                                                                     pady=5, ipady=5,
                                                                                                     ipadx=21)
salary_modification_button = Button(root, text='Zmiana wynagrodzenia', font=10, command=salary_modify).grid(row=9, column=0,
                                                                                                     sticky=W, padx=10,
                                                                                                     pady=5, ipady=5,
                                                                                                     ipadx=21)
refresh_button = Button(root, text='Odswiez', font=10, command=show_available_cars).grid(row=10, column=0, sticky=W, padx=10, pady=5, ipady=5, ipadx=32)
show_available_cars()

root.mainloop()