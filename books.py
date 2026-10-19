
import psycopg2


conn = psycopg2.connect(
    dbname="dars8",
    user="postgres",
    password="1",
    host="localhost",
    port="5433"
)

cursor = conn.cursor()

print("PostgreSQL bazasiga muvaffaqiyatli ulandi!")


def son_kiritish(matn):
    while True:
        try:
            son = int(input(matn))

            if son < 0:
                print("Manfiy son kiritmang!")
                continue

            return son

        except ValueError:
            print("Xato! Butun son kiriting.")


def kitoblarni_korish():
    cursor.execute(
        "SELECT id, title, author, price, quantity "
        "FROM books ORDER BY id"
    )

    kitoblar = cursor.fetchall()

    if not kitoblar:
        print("Bazada kitoblar mavjud emas.")
        return

    print("\n---------------------------------------------------------------------------------------")
    print(
        f"{'ID':<5} {'Kitob nomi':<25} {'Muallif':<25} "
        f"{'Narxi':<15} {'Miqdori':<10}"
    )
    print("\n---------------------------------------------------------------------------------------")
    for kitob in kitoblar:
        print(
            f"{kitob[0]:<5} {kitob[1]:<25} {kitob[2]:<25} "
            f"{kitob[3]:<15} {kitob[4]:<10}"
        )

    print("\n---------------------------------------------------------------------------------------")


def KitobQoshish():
    title = input("Kitob nomini kiriting: ").strip()
    author = input("Muallifni kiriting: ").strip()

    if not title or not author:
        print("Kitob nomi va muallif bo'sh bo'lmasligi kerak!")
        return

    price = son_kiritish("Kitob narxini kiriting: ")
    quantity = son_kiritish("Kitob miqdorini kiriting: ")

    cursor.execute(
        "INSERT INTO books (title, author, price, quantity) "
        "VALUES (%s, %s, %s, %s)",
        (title, author, price, quantity)
    )

    conn.commit()
    print("Yangi kitob muvaffaqiyatli qo'shildi!")


def KitobniYangilash():
    kitob_id = son_kiritish("Kitob ID raqamini kiriting: ")

    cursor.execute(
        "SELECT id FROM books WHERE id = %s",
        (kitob_id,)
    )

    if cursor.fetchone() is None:
        print("Bunday ID raqamli kitob topilmadi!")
        return

    yangi_narx = son_kiritish("Yangi narxni kiriting: ")
    yangi_miqdor = son_kiritish("Yangi miqdorni kiriting: ")

    cursor.execute(
        "UPDATE books SET price = %s, quantity = %s WHERE id = %s",
        (yangi_narx, yangi_miqdor, kitob_id)
    )

    conn.commit()
    print("Kitob ma'lumotlari yangilandi!")


def KitobniOchirish():
    kitob_id = son_kiritish("O'chiriladigan kitob ID sini kiriting: ")

    cursor.execute(
        "SELECT title FROM books WHERE id = %s",
        (kitob_id,)
    )

    kitob = cursor.fetchone()

    if kitob is None:
        print("Bunday ID raqamli kitob topilmadi!")
        return

    tasdiq = input(
        f"{kitob[0]} kitobini o'chirasizmi? (ha/yo'q): "
    ).strip().lower()

    if tasdiq == "ha":
        cursor.execute(
            "DELETE FROM books WHERE id = %s",
            (kitob_id,)
        )

        conn.commit()
        print("Kitob o'chirildi!")
    else:
        print("O'chirish bekor qilindi.")


def KitobQidirish():
    kitob_id = son_kiritish("Qidirilayotgan kitob ID sini kiriting: ")

    cursor.execute(
        "SELECT id, title, author, price, quantity "
        "FROM books WHERE id = %s",
        (kitob_id,)
    )

    kitob = cursor.fetchone()

    if kitob is None:
        print("Bunday ID raqamli kitob topilmadi!")
        return

    print("\n--- TOPILGAN KITOB ---")
    print(f"ID: {kitob[0]}")
    print(f"Kitob nomi: {kitob[1]}")
    print(f"Muallif: {kitob[2]}")
    print(f"Narxi: {kitob[3]} so'm")
    print(f"Miqdori: {kitob[4]} ta")


def KitoblarSoni():
    cursor.execute(
        "SELECT COUNT(*), COALESCE(SUM(quantity), 0) FROM books"
    )

    ja = cursor.fetchone()

    print(f"Kitob turlari soni: {ja[0]}")
    print(f"Jami kitob nusxalari: {ja[1]}")


try:
    while True:
        print("\n===== KUTUBXONA BOSHQARUV TIZIMI =====")
        print("1. Barcha kitoblarni ko'rish")
        print("2. Yangi kitob qo'shish")
        print("3. Kitob ma'lumotlarini yangilash")
        print("4. Kitobni o'chirish")
        print("5. Kitobni ID bo'yicha qidirish")
        print("6. Kitoblar umumiy sonini ko'rish")
        print("0. Dasturdan chiqish")

        tek = input("Tanlovingizni kiriting: ").strip()

        try:
            if tek == "1":
                kitoblarni_korish()

            elif tek == "2":
                KitobQoshish()

            elif tek == "3":
                KitobniYangilash()

            elif tek == "4":
                KitobniOchirish()

            elif tek == "5":
                KitobQidirish()

            elif tek == "6":
                KitoblarSoni()

            elif tek == "0":
                print("Dastur tugatildi!")
                break

            else:
                print("Xato menyudan 0 dan 6 gacha son tanlang")

        except psycopg2.Error as xato:
            conn.rollback()
            print("Ma'lumotlar bazasida xatolik!", xato)

finally:
    cursor.close()
    conn.close()
    print("Baza bilan aloqa yopildi!")
