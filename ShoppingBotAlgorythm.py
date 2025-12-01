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

    # Команда /remove
    if item.startswith("/remove"):
        parts = item.split(maxsplit=1)
        if len(parts) < 2:
            return await update.message.reply_text("Напишите: /remove продукт")
        name = parts[1].lower()

        removed = False
        for x in shopping_list:
            if x.lower() == name:
                shopping_list.remove(x)
                removed = True
                break

        if removed:
            return await update.message.reply_text(f"Удалено: {name} :)")
        else:
            return await update.message.reply_text("Упс... Такого продукта нет в списке :(")

    # Обычное добавление
    shopping_list.append(item)
    await update.message.reply_text(f"Добавил: {item}")

async def show_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not shopping_list:
        return await update.message.reply_text("Ой, а список то пустой :(")

    text = "🛒 Что надо купить:\n" + "\n".join(f"– {i}" for i in shopping_list)
    await update.message.reply_text(text)

async def clear_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    shopping_list.clear()
    await update.message.reply_text("Список очищен!")

def main():
    TOKEN = "ТОКЕН"

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", show_list))
    app.add_handler(CommandHandler("clear", clear_list))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, add_item))

    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
