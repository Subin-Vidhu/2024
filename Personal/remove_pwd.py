from PyPDF2 import PdfReader, PdfWriter

def remove_pdf_password(input_pdf, output_pdf, password):
    try:
        # Open the encrypted PDF
        reader = PdfReader(input_pdf)

        # Check if the PDF is encrypted
        if reader.is_encrypted:
            # Attempt to decrypt with the provided password
            if not reader.decrypt(password):
                raise ValueError("The provided password is incorrect.")

        # Create a PdfWriter object to write the unprotected PDF
        writer = PdfWriter()

        # Copy all pages from the reader to the writer
        for page in reader.pages:
            writer.add_page(page)

        # Write the output to a new PDF file without a password
        with open(output_pdf, 'wb') as output_file:
            writer.write(output_file)

        print(f"Password removed successfully. New file saved as: {output_pdf}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_pdf = r"c:\Users\Subin-PC\Downloads\TERM\PAN_CARD.pdf"  # Replace with your input PDF file path
output_pdf = r"c:\Users\Subin-PC\Downloads\TERM\PAN_CARD_.pdf"  # Replace with your desired output file path
password = "12011999"  # Current password

remove_pdf_password(input_pdf, output_pdf, password)
