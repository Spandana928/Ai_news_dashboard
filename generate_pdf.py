from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, self.title, 0, 1, "C")

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", 0, 0, "C")

def generate_pdf(news_data, topic):
    pdf = PDF()
    pdf.title = f"Top News on {topic.capitalize()}"
    pdf.add_page()

    pdf.set_font("Arial", "", 12)

    if not news_data:
        pdf.cell(0, 10, "No news available.", 0, 1)
    else:
        for i, article in enumerate(news_data, 1):
            title = article.get("title", "No Title")
            desc = article.get("description", "No Description")
            url = article.get("url", "")

            # ✅ SAFELY replace unsupported characters
            def safe_text(s):
                if not s:
                    return ""
                # Replace problematic Unicode quotes and dashes with ASCII
                replacements = {
                    "\u2018": "'",
                    "\u2019": "'",
                    "\u201c": '"',
                    "\u201d": '"',
                    "\u2013": "-",
                    "\u2014": "-",
                    "\u2026": "...",
                }
                for bad, good in replacements.items():
                    s = s.replace(bad, good)
                return s.encode("latin-1", "replace").decode("latin-1")

            pdf.multi_cell(0, 10, f"{i}. {safe_text(title)}", 0, 1)
            pdf.set_font("Arial", "I", 11)
            pdf.multi_cell(0, 8, safe_text(desc), 0, 1)
            pdf.set_font("Arial", "U", 11)
            pdf.set_text_color(0, 0, 255)
            pdf.cell(0, 10, safe_text(url), ln=1, link=url)
            pdf.set_text_color(0, 0, 0)
            pdf.ln(5)
            pdf.set_font("Arial", "", 12)

    # Save PDF
    os.makedirs("downloads", exist_ok=True)
    file_name = f"downloads/news_{topic}.pdf"
    pdf.output(file_name, "F")

    return file_name





