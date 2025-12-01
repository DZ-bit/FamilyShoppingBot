import os
from dotenv import load_dotenv
load_dotenv()

from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
)

# Хранилище списка продуктов (в памяти)
shopping_list = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Я бот-список покупок.\n"
        "Напишите продукт и я добавлю его в свой список.\n\n"
        "/list — команда, чтобы показать список\n"
        "/clear — команда, чтобы полностью очистить список\n"
        "/remove <название> — команда, чтобы удалить продукт из списка"
    )

async def add_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    item = update.message.text.strip()

    # Обычное добавление
    if not item:
        return
    shopping_list.append(item)
    await update.message.reply_text(f"Добавил: {item}")

async def remove_item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # context.args содержит список аргументов после команды
    if not context.args:
        await update.message.reply_text("Напишите: /remove продукт")
        return

    # Собираем весь аргумент (включая пробелы), например: /remove сливочное масло
    name = " ".join(context.args).strip().lower()

    # ищем совпадение без учета регистра
    for i, x in enumerate(shopping_list):
        if x.lower() == name:
            removed = shopping_list.pop(i)
            await update.message.reply_text(f"Удалено: {removed}")
            return

    await update.message.reply_text("Упс... Такого продукта нет в списке :(")

async def show_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not shopping_list:
        return await update.message.reply_text("Ой, а список то пустой :(")

    text = "🛒 Что надо купить:\n" + "\n".join(f"– {i}" for i in shopping_list)
    await update.message.reply_text(text)

async def clear_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    shopping_list.clear()
    await update.message.reply_text("Список очищен!")

def main():
    TOKEN = os.getenv("BOT_TOKEN")
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", show_list))
    app.add_handler(CommandHandler("clear", clear_list))
    app.add_handler(CommandHandler("remove", remove_item))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_item))

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
