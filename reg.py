from pprint import pprint
import csv
import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
    last_name, first_name, surname, organisation, position, phone_num, email = [], [], [], [], [], [], []
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


    def names_sorted():
        """Функция достает и редактирует неверно записанные имена, фамилии и отчества из записной книги"""
        for row in contacts_list[1:]:
            line = row[0] + row[1] + row[2]
            pattern = r'([А-Я][а-я]+)?'
            repl = r'\1 '
            result = re.sub(pattern, repl, line)
            last_name.append(result.split()[0])
            first_name.append(result.split()[1])
            try:
                surname.append(result.split()[2])
            except IndexError:
                surname.append('')


    def get_phones():
        """Функция на оснвове регулярки достает все телефоны и приводит в шаблонный вид"""
        phone = []
        line = ''
        for row in contacts_list[1:]:
            phone.append(row[5])
        for i in phone:
            if i:
                line += f'{i},'
            else:
                line += '\'\','
        pattern = r'\+?(7?|8)?\s?\s?\(?(\d{3})\)? ?-?(\d{3})-?(\d{2})-?(\d{2}) ?\(? ?(\w?\w?\w?\.)? ?(\d{4})?\)?'
        repl = r'+\1(\2)\3-\4-\5 \6\7'
        result = re.sub(pattern, repl, line)
        phone = result.split(',')
        for i in phone:
            if i == '\'\'':
                phone_num.append('')
            elif i == '':
                continue
            else:
                phone_num.append(i.strip())


    def fill_others():
        """Функция заполняет остальные данные новой записной книги, которая не требует изменений"""
        for row in contacts_list[1:]:
            organisation.append(row[3])
            position.append(row[4])
            email.append(row[6])


    def make_new_list():
        """Функция создает новый список всех записей с дублями, но отредактированный по шаблону"""
        d = [last_name, first_name, surname, organisation, position, phone_num, email]
        new_list = list(map(list, zip(*d)))
        return new_list


    def get_out_repeats():
        """Функция делит данные на 2 словаря. Повторные отправляет в словарь repeat, затем объединяет их, обновляя данные если
        их нет по соответствующим индексам"""
        try_list = make_new_list()
        unique_dict = {}
        repeat_dict = {}
        for i in try_list:
            key = i[0]
            if i[0] not in unique_dict:
                unique_dict[key] = i[1:]
            else:
                repeat_dict[key] = i[1:]

        for person, info in repeat_dict.items():
            if person in unique_dict:
                for i in range(6):
                    if not unique_dict[person][i]:
                        unique_dict[person][i] = repeat_dict[person][i]
        finally_list = [[key, *value] for key, value in unique_dict.items()]
        return finally_list


    def main():
        names_sorted()
        fill_others()
        get_phones()
        finally_list = get_out_repeats()
        with open("phonebook.csv", "w", encoding='utf-8') as f:

            datawriter = csv.writer(f, delimiter=',')
            datawriter.writerow(contacts_list[0])
            datawriter.writerows(finally_list)

if __name__ == "__main__":
    main()
