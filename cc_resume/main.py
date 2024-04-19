import os

from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT, TA_JUSTIFY

from cc_resume.config import CONF
from cc_resume import CURRENT_DIR, utils

PAGE_WIDTH, PAGE_HEIGHT = A4
FULL_COLUMN_WIDTH = (PAGE_WIDTH - 1 * inch)


class Fonts:
    def __init__(self):
        self.normal, path = 'normal', os.path.join(CURRENT_DIR, "fonts/SourceHanSansCN-Normal.ttf")
        pdfmetrics.registerFont(ttfonts.TTFont(self.normal, path))
        self.bold, path = 'bold', os.path.join(CURRENT_DIR, "fonts/SourceHanSansCN-Bold.ttf")
        pdfmetrics.registerFont(ttfonts.TTFont(self.bold, path))


class FontStyle:
    def __init__(self, default_font_size, paragraph_leading):
        self.default_font_size = default_font_size
        self.paragraph_leading = paragraph_leading
        self.fonts = Fonts()

    def get_normal_style(self, font_size=None, alignment=0, leading=None):
        font_size = font_size or self.default_font_size
        leading = leading or self.paragraph_leading
        return ParagraphStyle('normal', fontName=self.fonts.normal,
                              fontSize=font_size, alignment=alignment, leading=leading)

    def get_bold_style(self, font_size=None, alignment=0, text_color=colors.black, leading=None):
        font_size = font_size or self.default_font_size
        leading = leading or self.paragraph_leading
        return ParagraphStyle('bold', fontName=self.fonts.bold,
                              fontSize=font_size, alignment=alignment, textColor=text_color, leading=leading)


class CreatePdf:
    def __init__(self, font_size=None, title_padding=None, top_margin=None, bottom_margin=None, extra_leading=0):
        self.default_size = font_size or CONF.font_size
        self.default_title_padding = title_padding or CONF.title_padding
        self.paragraph_leading = self.default_size + extra_leading
        top_margin = top_margin or 0.2 * inch
        bottom_margin = bottom_margin or 0.1 * inch
        self.font_style = FontStyle(default_font_size=self.default_size, paragraph_leading=self.paragraph_leading)
        from cc_resume.config import Author
        from cc_resume import utils
        yaml_path = os.path.join(CONF.resume.config_dir, CONF.resume.name)
        file_name, file_extension = os.path.splitext(CONF.resume.name)
        self.output_path = os.path.join(CONF.resume.config_dir, f"{file_name}.pdf")
        self.doc = SimpleDocTemplate(self.output_path, pagesize=A4, showBoundary=0, leftMargin=0.4 * inch,
                                     rightMargin=0.4 * inch,
                                     topMargin=top_margin, bottomMargin=bottom_margin, title=f"Resume of {Author.name}",
                                     author=Author.name)
        self.data = utils.read_yaml(yaml_path)

        self.col_width = [FULL_COLUMN_WIDTH * 0.75, FULL_COLUMN_WIDTH * 0.25]
        self.build_elements = []

    def append_section_table_style(self, table_styles, running_row_index):
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), self.default_title_padding))
        table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), self.default_title_padding))
        table_styles.append(('LINEBELOW', (0, running_row_index), (-1, running_row_index), 1, colors.black))

    def config_education(self):
        education_list = self.data['education']
        table_data = []
        table_styles = []
        running_row_index = 0
        # Append education heading
        table_data.append(
            [Paragraph("教育经历", self.font_style.get_bold_style(
                font_size=self.default_size+1, text_color=CONF.resume.title_color))]
        )
        self.append_section_table_style(table_styles, running_row_index)
        running_row_index += 1

        # Append education
        for education in education_list:
            table_data.append([
                Paragraph(education['university'], self.font_style.get_bold_style()),
                Paragraph(education['year'], self.font_style.get_normal_style(alignment=TA_RIGHT)),
            ])
            table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), self.default_title_padding))
            running_row_index += 1

            table_data.append([
                Paragraph(education['degree'], self.font_style.get_normal_style()),
                Paragraph(education['location'], self.font_style.get_normal_style(alignment=TA_RIGHT)),
            ])
            table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
            # table_styles.append(('ALIGN', (0, running_row_index), (1, running_row_index+1), 'RIGHT'))
            running_row_index += 1

        table_style = TableStyle(table_styles)
        # Create the table and apply the style
        table = Table(table_data, colWidths=self.col_width, spaceBefore=0, spaceAfter=0)
        table.setStyle(table_style)
        self.build_elements.append(table)

    def config_experience(self):
        education_list = self.data['experience']
        table_data = []
        table_styles = []
        running_row_index = 0
        # Append education heading
        table_data.append(
            [Paragraph("工作经历", self.font_style.get_bold_style(font_size=self.default_size+1, text_color=CONF.resume.title_color))]
        )
        self.append_section_table_style(table_styles, running_row_index)
        running_row_index += 1

        # Append education
        for education in education_list:
            table_data.append([
                Paragraph(education['company'], self.font_style.get_bold_style()),
                Paragraph(education['duration'], self.font_style.get_normal_style(alignment=TA_RIGHT)),
            ])
            table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), self.default_title_padding))
            running_row_index += 1

            table_data.append([
                Paragraph(education['name'], self.font_style.get_normal_style()),
                Paragraph(education['location'], self.font_style.get_normal_style(alignment=TA_RIGHT)),
            ])
            table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
            # table_styles.append(('ALIGN', (0, running_row_index), (1, running_row_index+1), 'RIGHT'))
            running_row_index += 1

            for des in education['description']:
                table_data.append(
                    [Paragraph(des, self.font_style.get_normal_style(font_size=self.default_size, alignment=TA_JUSTIFY))]
                )
                table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
                table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
                running_row_index += 1

        table_style = TableStyle(table_styles)
        # Create the table and apply the style
        table = Table(table_data, colWidths=self.col_width, spaceBefore=0, spaceAfter=0)
        table.setStyle(table_style)
        self.build_elements.append(table)

    def config_projects(self):
        education_list = self.data['work_projects']
        table_data = []
        table_styles = []
        running_row_index = 0
        # Append education heading
        table_data.append(
            [Paragraph("工作主要项目经历", self.font_style.get_bold_style(font_size=self.default_size+1, text_color=CONF.resume.title_color))]
        )
        self.append_section_table_style(table_styles, running_row_index)
        running_row_index += 1

        # Append education
        for education in education_list:
            ptext = f"<font face=bold size={self.default_size}>{education['name']}</font>" \
                    f"   <font face=normal size={self.default_size}>{education['role']}</font>"
            styles = getSampleStyleSheet()
            # para = Paragraph(ptext, style=styles["Normal"])
            # flowables.append(para)
            table_data.append([
                Paragraph(ptext, style=styles["Normal"]),
                # Paragraph(education['name'], self.font_style.get_bold_style()),
                Paragraph(education['duration'], self.font_style.get_normal_style(alignment=TA_RIGHT)),
            ])
            table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index),self.default_title_padding ))
            running_row_index += 1

            for des in education['description']:
                table_data.append(
                    [Paragraph(des, self.font_style.get_normal_style(font_size=self.default_size, alignment=TA_JUSTIFY))]
                )
                table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
                table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
                running_row_index += 1

        table_style = TableStyle(table_styles)
        # Create the table and apply the style
        table = Table(table_data, colWidths=self.col_width, spaceBefore=0, spaceAfter=0)
        table.setStyle(table_style)
        self.build_elements.append(table)

    def config_author(self):
        education = self.data['author']
        table_data = []
        table_styles = []
        running_row_index = 0
        # Append education heading
        table_data.append(
            [Paragraph("个人信息", self.font_style.get_bold_style(
                font_size=self.default_size+1, text_color=CONF.resume.title_color))]
        )
        self.append_section_table_style(table_styles, running_row_index)
        running_row_index += 1

        ptext = f"<font face=normal size={self.default_size}>基本信息: </font>" \
                f"<font face=bold size={self.default_size}>{education['name']}</font>" \
                f"<font face=normal size={self.default_size}>，{education['msg']}</font>"
        styles = getSampleStyleSheet()
        table_data.append([
            Paragraph(ptext, style=styles["Normal"]),
            Paragraph("", self.font_style.get_normal_style(font_size=self.default_size, alignment=TA_JUSTIFY))
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index),self.default_title_padding ))
        running_row_index += 1
        table_data.append([
            [Paragraph(education['contact'], self.font_style.get_normal_style(font_size=self.default_size, alignment=TA_JUSTIFY))]
        ])
        table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index), 1))
        table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
        running_row_index += 1

        table_style = TableStyle(table_styles)
        # Create the table and apply the style
        table = Table(table_data, colWidths=self.col_width, spaceBefore=0, spaceAfter=0)
        table.setStyle(table_style)
        self.build_elements.append(table)

    def config_open_projects(self):
        data = self.data['open_projects']
        table_data = []
        table_styles = []
        running_row_index = 0
        table_data.append(
            [
                Paragraph("个人开源项目", self.font_style.get_bold_style(
                    font_size=self.default_size + 1, text_color=colors.orange)),
                Paragraph("")
            ]
        )
        self.append_section_table_style(table_styles, running_row_index)
        running_row_index += 1

        for project in data:
            ptext = f"<font face=bold size={self.default_size}>{project['name']}: </font>" \
                    f"<font face=normal size={self.default_size}>{project['description']}</font>" \
                    f"<font face=normal size={self.default_size}>{project['link']}</font>"
            table_data.append([Paragraph(ptext, style=self.font_style.get_bold_style(font_size=self.default_size))])
            table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index),self.default_title_padding ))
            table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
            table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
            running_row_index += 1

        table_style = TableStyle(table_styles)
        # Create the table and apply the style
        table = Table(table_data, colWidths=self.col_width, spaceBefore=0, spaceAfter=0)
        table.setStyle(table_style)
        self.build_elements.append(table)

    def config_summary(self):
        data = self.data['summary']
        table_data = []
        table_styles = []
        running_row_index = 0
        table_data.append(
            [
                Paragraph("个人总结", self.font_style.get_bold_style(
                    font_size=self.default_size + 1, text_color=CONF.resume.title_color)),
                Paragraph("")
            ]
        )
        self.append_section_table_style(table_styles, running_row_index)
        running_row_index += 1

        for line in data:
            table_data.append([Paragraph(line, style=self.font_style.get_normal_style(font_size=self.default_size))])
            table_styles.append(('TOPPADDING', (0, running_row_index), (1, running_row_index),self.default_title_padding ))
            table_styles.append(('BOTTOMPADDING', (0, running_row_index), (1, running_row_index), 0))
            table_styles.append(('SPAN', (0, running_row_index), (1, running_row_index)))
            running_row_index += 1

        table_style = TableStyle(table_styles)
        # Create the table and apply the style
        table = Table(table_data, colWidths=self.col_width, spaceBefore=0, spaceAfter=0)
        table.setStyle(table_style)
        self.build_elements.append(table)

    def add_data(self):
        self.config_author()
        self.config_education()
        self.config_experience()
        self.config_projects()
        self.config_open_projects()
        self.config_summary()

    def build(self):
        self.doc.build(self.build_elements)
        print(f'pdf page is {self.doc.page}, path is {self.output_path}')


def main():
    config_dir = utils.mkdir_config('resume')
    config_file_path = os.path.join(config_dir, '.resume.conf')
    CONF(default_config_files=[config_file_path])
    create_one_page_pdf()


def create_one_page_pdf():
    title_padding = CONF.title_padding
    extra_leading = 1
    times = 1

    for i in range(5):
        font_size = CONF.font_size - i
        for padding in list(range(1, title_padding+1))[::-1]:
            print(f'create pdf {times} times')
            pdf = CreatePdf(font_size, padding, extra_leading=extra_leading)
            pdf.add_data()
            pdf.build()
            print(f'page={pdf.doc.page}, font_size={font_size}, padding={padding}, height={pdf.doc.height}, frame_height={pdf.doc.frame._y}')
            if pdf.doc.page == 1:
                if pdf.doc.frame._y < pdf.doc.height*0.2:
                    return
            times += 1
            # time.sleep(0.5)
    else:
        print(f'generate failed')
        exit(1)


if __name__ == "__main__":
    main()
