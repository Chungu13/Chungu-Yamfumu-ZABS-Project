# your_app/template/pdf_generator.py
from io import BytesIO
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os
from django.core.files.base import ContentFile
from django.conf import settings


def generate_certificate_pdf(certification):
    """
    Generate a PDF for the given certificate similar to the HTML layout.
    """
    # Create a buffer to hold the PDF data
    buffer = BytesIO()
    pdf_canvas = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # === Certificate Title - Right Aligned ===
    pdf_canvas.setFont("Helvetica-Bold", 30)
    pdf_canvas.drawRightString(width - 50, 750, "CERTIFICATE OF CONFORMITY")

    # === Top Left Logo and Information ===
    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(50, 680, certification.manufacturer.company_name)
    pdf_canvas.drawString(50, 660, "(The Standard Act No. 4)")
    pdf_canvas.drawString(50, 640, "Lechwe House, Freedom Way - South End")
    pdf_canvas.drawString(50, 620, "P.O. Box 50259 ZA 15101, Ridgeway")
    pdf_canvas.drawString(50, 600, "Lusaka-Zambia")
    pdf_canvas.drawString(50, 580, "E-mail: info@zabs.org.zm | Tel: +260 211 231385 / 0777 764421")

    # === Certificate ID - Positioned at top right ===
    pdf_canvas.setFont("Helvetica-Bold", 16)
    pdf_canvas.drawRightString(width - 50, 680, certification.custom_certification_id)

    # === Middle Section: Logo, Award Info, Company Details ===
    pdf_canvas.setFont("Helvetica", 18)
    pdf_canvas.drawCentredString(width / 2, 580, "Awarded To")
    pdf_canvas.setFont("Helvetica-Bold", 24)
    pdf_canvas.drawCentredString(width / 2, 550, certification.manufacturer.company_name)
    pdf_canvas.setFont("Helvetica", 18)
    pdf_canvas.drawCentredString(width / 2, 520, certification.manufacturer.physical_address)

    # === Product Information Section ===
    pdf_canvas.setFont("Helvetica", 14)
    pdf_canvas.drawString(50, 480, f"Manufactures and Supplies: {certification.product}")
    pdf_canvas.drawString(50, 460, "In compliance with: ------------------------")
    pdf_canvas.drawString(50, 440, "Site(s): This is a single site certificate")
    pdf_canvas.drawString(50, 420, "Certification Scheme: ---------------------------")
    pdf_canvas.drawString(50, 400, f"First Issued on: {certification.first_issued}")
    pdf_canvas.drawString(50, 380, f"Last Issued on: {certification.last_issued}")
    pdf_canvas.drawString(50, 360, f"Modified on: {certification.modified_on}")
    pdf_canvas.drawString(50, 340, f"Expiry: {certification.expiry_date}")

    # === Footer Section: Signature and Contact Info ===
    pdf_canvas.setFont("Helvetica", 14)
    pdf_canvas.drawString(50, 250, "Authorized Signature")
    pdf_canvas.line(50, 240, 300, 240)

    pdf_canvas.setFont("Helvetica", 12)
    pdf_canvas.drawString(50, 220, "Lechwe House, Freedom Way - South End")
    pdf_canvas.drawString(50, 200, "P.O. Box 50259 ZA 15101, Ridgeway, Lusaka-Zambia")
    pdf_canvas.drawString(50, 180, "E-mail: info@zabs.org.zm | Tel: +260 211 231385 / 0777 764421")

    # Finish and save the PDF
    pdf_canvas.showPage()
    pdf_canvas.save()

    # Rewind the buffer
    buffer.seek(0)

    # Save the PDF to the model's `pdf_file` field
    pdf_file_name = f'certificate_{certification.id}.pdf'
    certification.pdf_file.save(pdf_file_name, ContentFile(buffer.getvalue()), save=True)

    # Return the PDF as an HTTP response (optional)
    response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{pdf_file_name}"'
    return response
