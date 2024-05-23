
from fpdf import FPDF
from fastapi.responses import Response
from io import BytesIO

class Reportx:
    
    def reportcompany(self,company,start_date,end_date,result,headers,column_widths,title):
         # Create a PDF document
        pdf = FPDF()
        pdf.add_page()
        pdf_buffer = BytesIO()
        

        # Add an image at the top of the page
        image_path="C:\\Users\\vpepen.PUJ\\Desktop\\reportingCCSBack\\assets\\ccs.png"
        pdf.image(image_path, x=10, y=10, w=50)  # Adjust x, y, and w as needed
    
        # Set title
        pdf.set_font("Arial", 'B', 14) # Set title fonts
        pdf.cell(200, 10, txt=f"{title}:{company}", ln=True, align='C')

        # Set title for date
        pdf.set_font("Arial", 'B', 12) # Set title fonts date
        # Set title for start date and end date
        pdf.cell(320, 10, txt="Fecha:", ln=True, align='C')
        pdf.set_font("Arial", size=10)  # Set title fonts start date and end date
        pdf.cell(320, 8, txt=f"{start_date} - {end_date} ", ln=True, align='C')
        # Add space below the title
        pdf.ln(10)
        # Add table headers
        pdf.set_font("Arial", size=10)
        

        for header, width in zip(headers,column_widths):
            pdf.cell(width, 10, header, 1)
        pdf.ln()

        # Add table rows
        for row in result:
            for item, width in zip(row, column_widths):
                pdf.cell(width, 10, str(item), 1)
            pdf.ln()

        pdf_data = pdf.output(dest='S').encode('latin1')  # Encode to match the expected output format
        pdf_buffer.write(pdf_data)
        pdf_buffer.seek(0)  # Reset the buffer position to the beginning

        # Return the PDF as a response
        return Response(content=pdf_buffer.getvalue(), media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=report_{company}_{start_date}_to_{end_date}.pdf"})
            
    
        
        # pdf_file_path = f"C:/Users/vpepen.PUJ/Desktop/report_{company}_{start_date}_to_{end_date}.pdf"
        # pdf.output(pdf_file_path)
    
        # return FileResponse(pdf_file_path, media_type='application/pdf', filename=f'report_{company}_{start_date}_to_{end_date}.pdf')

