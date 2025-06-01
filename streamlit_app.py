import streamlit as st
from menu_data import menu_items
from datetime import datetime
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# --- Konfigurasi Halaman ---
st.set_page_config(page_title="Warteg Paradise", layout="wide")

# CSS UNTUK BACKGROUND GAMBAR MAKANAN ANIMASI
st.markdown("""
    <style>
        .stApp {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background-image: url("https://cdn0-production-images-kly.akamaized.net/yytSuiXj1fs2gZHkK9s4vA6FWnM=/1280x720/smart/filters:quality(75):strip_icc():format(webp)/kly-media-production/medias/2852592/original/049149000_1563073547-1.jpg");
            background-size: cover;
            background-repeat: no-repeat;
            background-position: center center;
            background-attachment: fixed;
            z-index: -1;
        }

        .block-container {
            background-color: rgba(255, 255, 255, 0.3);
            backdrop-filter: blur(0px);
            -webkit-backdrop-filter: blur(0px);
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 0 10px rgba(0,0,0,0);
        }

        h1, h2, h3 {
            color: #5D4037;
        }

        .stButton>button {
            background-color: #FF7043;
            color: white;
            border-radius: 10px;
        }

        .stDownloadButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div style="text-align:center; padding: 20px 0;">
        <h1 style="color: #D2691E; font-weight: 1000;">🍛 <b>Warteg Paradise</b> 🍽️</h1>
        <h4 style="color: #333; font-weight: 1000;">Selamat datang di <span style='color:#D2691E;'>surga rasa</span> dan <span style='color:#D2691E;'>harga hemat</span></h4>
        <hr style="border: 1px solid #eee;">
    </div>
""", unsafe_allow_html=True)

st.markdown("<p style='font-size:18px; font-weight: 800; color:#222;'>Silakan pilih makanan favorit Anda di bawah ini:</p>", unsafe_allow_html=True)

# --- Fungsi PDF ---
def generate_pdf(order_list, total_price):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(200, y, "WARTEG PARADISE")
    y -= 30

    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Waktu Pesanan: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    y -= 20

    c.drawString(40, y, "-" * 80)
    y -= 15
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, "Qty")
    c.drawString(70, y, "Item")
    c.drawString(300, y, "Harga")
    c.drawString(380, y, "Subtotal")
    y -= 15
    c.setFont("Helvetica", 10)

    for o in order_list:
        c.drawString(40, y, str(o["qty"]))
        c.drawString(70, y, o["name"])
        c.drawRightString(360, y, f"Rp {o['price']:,}")
        c.drawRightString(460, y, f"Rp {o['subtotal']:,}")
        y -= 15
        if y < 50:
            c.showPage()
            y = height - 40

    y -= 10
    c.drawString(40, y, "-" * 80)
    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(460, y, f"TOTAL: Rp {total_price:,}")
    y -= 30
    c.setFont("Helvetica", 10)
    c.drawString(40, y, "Terima kasih telah memesan di Warteg Paradise!")
    y -= 15
    c.drawString(40, y, "Semoga hari Anda kenyang dan bahagia 😋")

    c.save()
    buffer.seek(0)
    return buffer

# --- Tampilan Menu & Pemesanan ---
order = []
total_price = 0

# Divider dekoratif
st.markdown("<hr style='border-top: 3px dashed #ff9900;'>", unsafe_allow_html=True)

for i, item in enumerate(menu_items):
    st.subheader(f"{item['name']} - Rp {item['price']:,}")
    if st.checkbox(f"Pesan {item['name']}", key=f"check_{i}"):
        qty = st.number_input(f"Jumlah porsi {item['name']}", min_value=1, max_value=10, value=1, key=f"qty_{i}")
        subtotal = item["price"] * qty
        total_price += subtotal
        order.append({
            "name": item["name"],
            "qty": qty,
            "price": item["price"],
            "subtotal": subtotal
        })

# --- Ringkasan & Struk ---
if order:
    st.markdown("<hr style='border-top: 2px solid #ccc;'>", unsafe_allow_html=True)
    st.header("🧾 Ringkasan Pesanan")
    for o in order:
        st.write(f"{o['qty']} x {o['name']} = Rp {o['subtotal']:,}")
    st.markdown(f"## 💰 Total Harga: Rp {total_price:,}")

    pdf_buffer = generate_pdf(order, total_price)
    st.download_button(
        label="📥 Download Struk (PDF)",
        data=pdf_buffer,
        file_name="struk_warteg_paradise.pdf",
        mime="application/pdf"
    )

    if st.button("✅ Konfirmasi Pesanan"):
        st.success("Pesanan Anda telah dikonfirmasi. Terima kasih!")
else:
    st.info("Silakan pilih makanan untuk mulai memesan.")
