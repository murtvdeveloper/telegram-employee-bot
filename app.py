from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from database import (
    init_db,
    get_employee_by_telegram_id,
    link_employee_to_telegram,
    get_tasks_warnings_by_employee_id,
    update_task_status,
    add_employee,
    add_task
)
from auth import is_authorized
import os

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if is_authorized(user_id):
        await update.message.reply_text(
            "Вы — учредитель или генеральный директор. Доступ разрешен."
        )
    else:
        emp = get_employee_by_telegram_id(user_id)
        if emp:
            await update.message.reply_text(
                f"Добро пожаловать, {emp[1]}! Вы можете просматривать и обновлять свои задачи."
            )
        else:
            await update.message.reply_text(
                "Вас нет в базе. Введите /link, чтобы привязать себя."
            )

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    args = context.args
    if not args:
        await update.message.reply_text("Введите ФИО: /link Иванов Иван Иванович")
        return
    full_name = " ".join(args)
    result = link_employee_to_telegram(full_name, user_id)
    if result:
        await update.message.reply_text(f"Вы успешно привязаны к сотруднику: {full_name}")
    else:
        await update.message.reply_text("Сотрудник с таким именем не найден.")

async def view_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    emp = get_employee_by_telegram_id(user_id)
    if not emp:
        await update.message.reply_text("Сначала привяжите себя с помощью /link")
        return
    tasks = get_tasks_warnings_by_employee_id(emp[0])
    if not tasks:
        await update.message.reply_text("У вас пока нет задач/выговоров.")
        return
    response = "Ваши задачи/выговоры:\n"
    for task in tasks:
        response += f"- {task[1]} (Статус: {task[2]}, ID: {task[0]})\n"
    await update.message.reply_text(response)

async def update_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    emp = get_employee_by_telegram_id(user_id)
    if not emp:
        await update.message.reply_text("Сначала привяжите себя с помощью /link")
        return
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Используйте: /update_status <ID> <новый_статус>")
        return
    try:
        task_id = int(args[0])
        new_status = " ".join(args[1:])
        success = update_task_status(task_id, new_status)
        if success:
            await update.message.reply_text(f"Статус задачи {task_id} обновлен на '{new_status}'")
        else:
            await update.message.reply_text("Задача не найдена или ошибка обновления.")
    except ValueError:
        await update.message.reply_text("ID должен быть числом.")

async def add_task_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if not is_authorized(user_id):
        await update.message.reply_text("У вас нет доступа.")
        return
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("Используйте: /add_task <ID_сотрудника> <описание>")
        return
    try:
        emp_id = int(args[0])
        description = " ".join(args[1:])
        add_task(emp_id, description)
        await update.message.reply_text(f"Задача '{description}' добавлена сотруднику ID {emp_id}.")
    except ValueError:
        await update.message.reply_text("ID должен быть числом.")

def main():
    token = os.getenv("BOT_TOKEN")
    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("link", link))
    application.add_handler(CommandHandler("view_tasks", view_tasks))
    application.add_handler(CommandHandler("update_status", update_status))
    application.add_handler(CommandHandler("add_task", add_task_cmd))

    init_db()

    application.run_polling()

if __name__ == "__main__":
    main()
