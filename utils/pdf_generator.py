from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
import os

def generate_resume_pdf(data: dict, file_path: str):
    doc = SimpleDocTemplate(file_path, pagesize=A4)
    styles = getSampleStyleSheet()

    elements = []

    # 🔹 Sarlavha
    elements.append(Paragraph("REZYUME", styles["Title"]))
    elements.append(Spacer(1, 10))

    # 🔹 Asosiy ma'lumotlar
    elements.append(Paragraph(f"F.I.Sh: {data.get('fullname', '')}", styles["Normal"]))
    elements.append(Paragraph(f"Telefon: {data.get('phone', '')}", styles["Normal"]))
    elements.append(Paragraph(f"Filial: {data.get('branch_name', '')}", styles["Normal"]))
    elements.append(Paragraph(f"Vakansiya: {data.get('vacancy_name', '')}", styles["Normal"]))
    elements.append(Paragraph(f"Manzil: {data.get('address', '')}", styles["Normal"]))
    elements.append(Paragraph(f"Tug'ilgan sana: {data.get('birthdate', '')}", styles["Normal"]))
    elements.append(Paragraph(f"Jins: {data.get('gender', '')}", styles["Normal"]))
    elements.append(Paragraph(f"Oilaviy holat: {data.get('marital', '')}", styles["Normal"]))
    elements.append(Paragraph(f"Ta'lim: {data.get('education', '')}", styles["Normal"]))

    elements.append(Spacer(1, 10))

    # 🔹 Ish tajribasi
    elements.append(Paragraph("Ish tajribasi:", styles["Heading2"]))
    elements.append(Paragraph(f"{data.get('exp_org', '')}", styles["Normal"]))
    elements.append(Paragraph(f"{data.get('exp_pos', '')}", styles["Normal"]))
    elements.append(Paragraph(f"{data.get('exp_period', '')}", styles["Normal"]))

    elements.append(Spacer(1, 10))

    # 🔹 Til
    elements.append(Paragraph(f"O'zbek tili: {data.get('uzbek', '')}", styles["Normal"]))
    elements.append(Paragraph(f"Rus tili: {data.get('russian', '')}", styles["Normal"]))

    elements.append(Spacer(1, 10))

    # 🔹 Maosh
    elements.append(Paragraph(f"Kutilayotgan oylik: {data.get('salary', '')}", styles["Normal"]))

    elements.append(Spacer(1, 15))

    # 🔹 RASM (agar bo‘lsa)
    photo_path = data.get("photo_path")
    if photo_path and os.path.exists(photo_path):
        elements.append(Paragraph("Rasm:", styles["Heading2"]))
        elements.append(Spacer(1, 5))
        elements.append(Image(photo_path, width=120, height=150))

    doc.build(elements)