from datetime import *
from tabulate import *
import csv


data = [["ID", "Дата", "Описание", "Сумма"]] #Замена БД


def main():
    user = input("Введите ваше имя: ")
    print(f"Здравствуйте {user}, я помогу вам следить за вашими расходами.")
    print('Если вам нужна помощь с командами используйте команду: "Помощь"')
    print('Если вы хотите закрыть приложение используйте команду: "Выход"')
    
    id = 1
    expenses = 0
    while 1:
        
        command = input("Введите команду: ").lower().strip() #Ввод команды 
        
        if command == "помощь": #Выводит все команды в виде таблицы
            help = [
                ["Команда", "Атрибуты", "Описание"],
                ["Добавить", "--Описание, --Сумма", "Добавляет расходы"],
                ["Удалить", "--id", "Удаляет расходы по ID"],
                ["Список", "", "Выводит список всех расходов"],
                ["Сумма расходов", "", "Выводит общую сумму расходов"],
                ["Экспорт", "", "Переносит данные в cvs файл"],
                ["Помощь", "", "Выводит все команды с объяснением"],
                ["Выйти", "", "Закрывает приложение"]
            ]
            print(tabulate(help))
        
        elif command[:8] == "добавить": #Добавляет расходы в БД
            
            description_ind = command.find("--описание")
            amount_ind = command.find("--сумма")
            if description_ind == -1:    
                description = ""
                amount = command[amount_ind+7+1:]
            elif description_ind < amount_ind:
                description = command[description_ind+11:amount_ind].strip()
                amount = command[amount_ind+8:]
            elif description_ind > amount_ind:
                description = command[description_ind+11:].strip()
                amount = command[amount_ind+8:description_ind] 
            
            try:
                amount = int(amount)
            except ValueError:
                print("Сумма должна быть числом.")
                continue
            
            if amount < 0:
                print("Расходы не могут быть меньше нуля, иначе это доходы)")
            elif len(description) > 10:
                print("Описание должно быть не больше 10 символов.")
            else:
                data.append([id, date.today(), description, amount])
                expenses += amount
                id += 1
                print("Расходы успешно добавлены.")
        
        elif command[:6] == "список": #Выводит все расходы в виде таблицы 
            print(tabulate(data))
        
        elif command[:14] == "сумма расходов": #Выводит сумму всех расходов
            print(f"Всего было потрачено: {expenses}.")
        
        elif command[:7] == "удалить": #Удаляет расход по id
            id_ind = command.find("--id")
            id = command[id_ind+5:]
            
            try:
                id = int(id)
            except ValueError:
                print("ID это число или цифра.")   
            
            f = True
            for expense in data:
                if expense[0] == id:
                    expenses -= expense[3]
                    data.remove(expense)
                    print("Расходы успешно удалены.")
                    f = False
                    break
            if f:
                print("Расходов с таким ID нет.")
        
        elif command == "выход": #Выходит из цикла 
            break
        
        elif command == "экспорт":
            with open('data.cvs', mode="w+", encoding='cp1251', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerows(data)
        
        else: #Если пользователь ввёл неправильную команду
            print("К сожалению такой команды нет.")
            print('Воспользуйтесь командой "Помощь" для ознакомления с командами.')

if __name__ == "__main__":
    main()