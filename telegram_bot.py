# telegram_bot.py
import logging
import traceback
import os
import aiohttp
from telegram.constants import ParseMode
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)
from app.utils.oracledb_utils import (
    buscar_producto_por_nombre,
    obtener_productos_destacados,
    obtener_productos_por_categoria,
    limpiar_descripcion,
    obtener_categorias_disponibles,
    obtener_id_categoria_por_nombre,
    obtener_todos_los_productos,
    obtener_precio_predicho 
)
from app.utils.blip_online import describir_imagen_ruta
from app.utils.nlp_utils import extraer_nombre_producto
from app.utils.clip_utils import buscar_productos_similares

TELEGRAM_TOKEN = "7900344173:AAHhduYOZobjvZ_2xNm7MVTt2rw3ZseDaVE"
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    categorias = obtener_categorias_disponibles()
    categorias_texto = "\n".join([f"⭐ {cat.capitalize()}" for cat in categorias]) if categorias else "❌ No disponibles."

    mensaje = (
        "ℹ️ *Ayuda del Bot de E-commerce*\n\n"
        "📸 Envíame una *foto de un producto* para reconocerlo.\n"
        "🛒 Pregunta por el precio: ¿cuánto cuesta el iPhone 13?\n"
        "🔍 Si deseas conocer los productos más vendidos escribe: /destacados \n"
        "🔍 Usa las siguientes categorías para visualizar sugerencias especiales para ti:\n"
        f"{categorias_texto}"
    )
    await update.message.reply_text(mensaje, parse_mode="Markdown")

async def destacados(update: Update, context: ContextTypes.DEFAULT_TYPE):
    productos = obtener_productos_destacados()
    if productos:
        texto = "⭐ *Productos destacados para ti:*\n\n"
        for nombre, descripcion, precio, imagen_url in productos:
            texto += (
                f"📦 *{nombre}*\n"
                f"📝 {descripcion}\n"
                f"💰 ${precio}\n"
                f"🖼️ [Imagen]({imagen_url})\n\n"
            )
        await update.message.reply_text(texto, parse_mode="Markdown", disable_web_page_preview=False)
    else:
        await update.message.reply_text("⚠️ No se pudieron obtener productos destacados.")
    await update.message.reply_text("💬 Puedes seguir consultando por otro producto o enviarme una imagen.\n\n" "Si necesitas apoyo escribe: /ayuda 👋")

async def es_imagen_valida(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url, timeout=5) as resp:
                return resp.status == 200 and resp.headers.get("Content-Type", "").startswith("image/")
    except:
        return False

async def handle_photo(update, context):
    photo_file = await update.message.photo[-1].get_file()
    user_id = update.message.from_user.id
    local_path = f"temp_{user_id}.jpg"
    await photo_file.download_to_drive(local_path)

    await update.message.reply_text("📷 Imagen recibida. Analizando con IA...")

    try:
        descripcion = describir_imagen_ruta(local_path)
        os.remove(local_path)
        await update.message.reply_text(f"🧠 Descripción automática: *{descripcion}*", parse_mode="Markdown")

        productos = obtener_todos_los_productos()
        similares = buscar_productos_similares(descripcion, productos)

        if similares:
            await update.message.reply_text("🔍 *Coincidencias encontradas:*", parse_mode="Markdown")

            nombre, descripcion_p, precio, imagen_url = similares[0]

            resultado_principal = buscar_producto_por_nombre(nombre, limite=1)
            if not resultado_principal:
                await update.message.reply_text("⚠️ No se pudo obtener la categoría del producto.")
                return
            _, _, _, _, id_categoria = resultado_principal[0]

            # Precio predicho para producto principal
            precio_predicho = obtener_precio_predicho(id_categoria)
            if precio_predicho:
                mensaje = f"🛒 *{nombre}*\n📝 {descripcion_p}\n💰 Precio sugerido: ${precio_predicho:.2f}"
            else:
                mensaje = f"🛒 *{nombre}*\n📝 {descripcion_p}\n💰 ${precio:.2f}"

            boton = [[InlineKeyboardButton("🛍️ Ver producto", url=imagen_url)]]
            await update.message.reply_photo(
                photo=imagen_url,
                caption=mensaje,
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(boton)
            )


            # Sugerencias de la misma categoría
            sugerencias = obtener_productos_por_categoria(id_categoria)
            sugerencias = [s for s in sugerencias if s[0] != nombre][:4]

            if sugerencias:
                await update.message.reply_text("🔎 *También te puede interesar:*", parse_mode="Markdown")
                for nombre_s, desc_s, precio_s, url_s in sugerencias:
                    predicho = obtener_precio_predicho(id_categoria)
                    if predicho:
                        texto_s = f"📦 *{nombre_s}*\n📝 {desc_s}\n💰 Precio sugerido: ${predicho:.2f}"
                    else:
                        texto_s = f"📦 *{nombre_s}*\n📝 {desc_s}\n💰 ${precio_s:.2f}"

                    boton_s = [[InlineKeyboardButton("🛒 Ver producto", url=url_s)]]
                    await update.message.reply_photo(
                        photo=url_s,
                        caption=texto_s,
                        parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup(boton_s)
                    )
            await update.message.reply_text("💬 Puedes seguir consultando por otro producto o enviarme una imagen.\n\n" "Si necesitas apoyo escribe: /ayuda 👋")
        else:
            await update.message.reply_text("❓ No encontré productos similares.")
    except Exception as e:
        logging.error("❌ Error al analizar imagen: " + traceback.format_exc())
        await update.message.reply_text("⚠️ Hubo un problema procesando la imagen.")


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("precio:"):
        producto = query.data.replace("precio:", "")
        try:
            resultado = buscar_producto_por_nombre(producto, limite=1)
            if resultado:
                nombre, descripcion, precio, imagen_url, *_ = resultado[0]
                mensaje = (
                    f"🛒 *{nombre}*\n"
                    f"📄 {descripcion}\n"
                    f"💰 *Precio:* ${precio:.2f}"
                )
                await context.bot.send_photo(
                    chat_id=query.message.chat_id,
                    photo=imagen_url,
                    caption=mensaje,
                    parse_mode="Markdown"
                )
            else:
                await query.edit_message_text("⚠️ No encontré información del producto.")
        except Exception as e:
            logging.error(e, exc_info=True)
            await query.edit_message_text("❌ Error al consultar el producto.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower().strip()
    saludos = ["hola", "buenas", "buenos días", "hello", "qué tal", "hey"]
    if user_message in saludos:
        await update.message.reply_text("👋 ¡Hola soy tu amigo Boot! Puedes preguntarme por un producto o enviarme una imagen.\n\n" \
        "Si necesitas apoyo escribe: /ayuda 👋")
        return

    tiene_intencion_precio = any(k in user_message for k in ["precio", "cuánto cuesta", "vale", "valor"])
    producto_extraido = extraer_nombre_producto(user_message)

    if not tiene_intencion_precio and not producto_extraido:
        await update.message.reply_text("📸 Puedes preguntarme por un producto o enviarme una imagen.")
        return

    if producto_extraido:
        try:
            resultados = buscar_producto_por_nombre(producto_extraido, limite=1)
            if resultados:
                nombre, descripcion, precio, imagen_url, id_categoria = resultados[0]

                precio_predicho = obtener_precio_predicho(id_categoria)
                if precio_predicho:
                    mensaje = f"🛒 *{nombre}*\n📝 {descripcion}\n💰 Precio sugerido: ${precio_predicho:.2f}"
                else:
                    mensaje = f"🛒 *{nombre}*\n📝 {descripcion}\n💰 Precio: ${precio:.2f}"

                boton = [[InlineKeyboardButton("🛍️ Ver producto", url=imagen_url)]]
                await update.message.reply_photo(
                    photo=imagen_url,
                    caption=mensaje,
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup(boton)
                )

                sugerencias = obtener_productos_por_categoria(id_categoria)
                sugerencias = [s for s in sugerencias if s[0] != nombre][:4]
                if sugerencias:
                    await update.message.reply_text("🔎 *También te puede interesar:*", parse_mode="Markdown")
                    for nombre_s, desc_s, precio_s, url_s in sugerencias:
                        predicho = obtener_precio_predicho(id_categoria)
                        if predicho:
                            texto_s = f"📦 *{nombre_s}*\n📝 {desc_s}\n💰 Precio sugerido: ${predicho:.2f}"
                        else:
                            texto_s = f"📦 *{nombre_s}*\n📝 {desc_s}\n💰 ${precio_s:.2f}"
                        boton_s = [[InlineKeyboardButton("🛒 Ver producto", url=url_s)]]
                        await update.message.reply_photo(
                            photo=url_s,
                            caption=texto_s,
                            parse_mode="Markdown",
                            reply_markup=InlineKeyboardMarkup(boton_s)
                        )
                await update.message.reply_text("💬 Puedes seguir consultando por otro producto o enviarme una imagen.\n\n" "Si necesitas apoyo escribe: /ayuda 👋")

                return


            # Si no se encontró como producto, probar como categoría
            productos_categoria = obtener_productos_por_categoria(producto_extraido)
            if productos_categoria:
                await update.message.reply_text(f"📂 *Sugerencias en la categoría:* {producto_extraido}", parse_mode="Markdown")
                id_cat = obtener_id_categoria_por_nombre(producto_extraido)
                for nombre, desc, precio, url in productos_categoria[:5]:
                    predicho = obtener_precio_predicho(id_cat) if id_cat else None
                    if predicho:
                        texto = f"📦 *{nombre}*\n📝 {desc}\n💰 Precio sugerido: ${predicho:.2f}"
                    else:
                        texto = f"📦 *{nombre}*\n📝 {desc}\n💰 ${precio:.2f}"
                    boton = [[InlineKeyboardButton("🛒 Ver producto", url=url)]]
                    await update.message.reply_photo(
                        photo=url,
                        caption=texto,
                        parse_mode="Markdown",
                        reply_markup=InlineKeyboardMarkup(boton)
                    )
            await update.message.reply_text("💬 Puedes seguir consultando por otro producto o enviarme una imagen.\n\n" "Si necesitas apoyo escribe: /ayuda 👋")
            return


            await update.message.reply_text("❌ No encontré productos relacionados con ese término.")
        except Exception as e:
            logging.error(e, exc_info=True)
            await update.message.reply_text("⚠️ Error al consultar producto.")
    else:
        await update.message.reply_text("❓ No entendí el producto. Intenta ser más específico.")


app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("ayuda", ayuda))
app.add_handler(CommandHandler("destacados", destacados))
app.add_handler(CallbackQueryHandler(callback_handler))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    print("🤖 Bot en ejecución...")
    app.run_polling()