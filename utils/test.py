# from fpdf import FPDF
# import os

# class CustomPDF(FPDF):
#     def header(self):
#         self.set_font("DejaVu", "B", 14)
#         self.cell(0, 10, "Sample Header", ln=True, align="C")

#     def footer(self):
#         self.set_y(-15)
#         self.set_font("DejaVu", "I", 10)
#         self.cell(0, 10, f"Page {self.page_no()}", align="C")

# pdf = CustomPDF()

# font_dir = os.path.join("assets", "fonts", "ttf")
# pdf.add_font("DejaVu", "", os.path.join(font_dir, "DejaVuSans.ttf"), uni=True)
# pdf.add_font("DejaVu", "B", os.path.join(font_dir, "DejaVuSans-Bold.ttf"), uni=True)
# pdf.add_font("DejaVu", "I", os.path.join(font_dir, "DejaVuSans-Oblique.ttf"), uni=True)

# pdf.add_page()
# pdf.set_font("DejaVu", "", 14)
# pdf.cell(0, 10, "Hello, this is a test with DejaVu fonts and full Unicode support!", ln=True)

# pdf.output("test_output1.pdf")


from fpdf import FPDF
import os

pdf = FPDF()
pdf.add_page()

font_path = os.path.abspath("utils/assets/fonts/DejaVuSans.ttf")
print("Font Path:", font_path)

pdf.add_font("DejaVu", "", font_path, uni=True)
pdf.set_font("DejaVu", size=12)

pdf.cell(0, 10, "Hello from FPDF with DejaVuSans!", ln=True)

output_path = "sample_output.pdf"
pdf.output(output_path)
