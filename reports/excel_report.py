from odoo import http
from odoo.http import request, Response
import io
import xlsxwriter
from ast import literal_eval


class Student_Excel_Report(http.Controller):
    @http.route("/whatsapp_message/report/excel/<string:message_ids>", type="http", auth="user")
    def download_excel_student_report(self, message_ids):
        message_ids = request.env["whatsapp.message"].browse(literal_eval(message_ids))
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {"in_memory": True})
        worksheet = workbook.add_worksheet("Student")
        header_format = workbook.add_format({
            "bold": True,
            "align": "center",
            "valign": "vcenter",
            "text_wrap": True,
            "bg_color": "#800080",
            "border": 1,
            "font_color": "#FFFFFF",
            "font_size": 14,

        })
        worksheet.set_row(0, 30)  # Set row height for header
        worksheet.set_column("A:A", 20)  # Set column width for Sender Name
        worksheet.set_column("B:B", 50)  # Set column width for Message Body
        worksheet.set_column("C:C", 20)  # Set column width for Date Sent   

        string_format = workbook.add_format({"align": "center", "border": 1,"valign": "vcenter", "text_wrap": True, "font_size": 12})

        header_format.set_indent(1)
        headers = [
            "Sender Name",
            "Message Body",
            "Date Sent",
     
        ]
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)
        for row_num, msg in enumerate(message_ids, start=1):

            worksheet.write(row_num, 0, str(msg.sender_name), string_format)
            worksheet.write(row_num, 1, msg.message_body or "", string_format)
            date_str = msg.date_sent.strftime('%Y-%m-%d %I:%M %p') if msg.date_sent else ''
            worksheet.write(row_num, 2, date_str, string_format)
        workbook.close()
        output.seek(0)

        file_name = "WhatsApp Message Report.xlsx"

        return Response(
            output.getvalue(),
            headers=[
                (
                    "Content-Type",
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                ),
                ("Content-Disposition", f"attachment;filename={file_name}"),
            ],
        )
