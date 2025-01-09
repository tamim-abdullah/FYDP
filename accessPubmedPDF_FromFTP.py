import ftplib
import os

def download_pdfs_from_ftp(ftp_server, ftp_path, local_dir, file_limit=3):
    try:
        # Connect to the FTP server
        ftp = ftplib.FTP(ftp_server)
        ftp.login()  # Anonymous login
        
        # Navigate to the desired directory
        ftp.cwd(ftp_path)
        
        # List files in the directory
        files = ftp.nlst()
        print(f"Files in '{ftp_path}': {files}")
        
        # Create local directory if it doesn't exist
        os.makedirs(local_dir, exist_ok=True)
        
        # Download a limited number of PDF files
        pdf_count = 0
        for file in files:
            if file.endswith(".pdf"):
                local_file_path = os.path.join(local_dir, file)
                with open(local_file_path, "wb") as f:
                    print(f"Downloading {file}...")
                    ftp.retrbinary(f"RETR {file}", f.write)
                print(f"Downloaded: {local_file_path}")
                
                pdf_count += 1
                if pdf_count >= file_limit:
                    print(f"Downloaded {file_limit} PDF files. Stopping further downloads.")
                    break
        
        # Close the FTP connection
        ftp.quit()
        print("FTP connection closed.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example Usage
ftp_server = "ftp.ncbi.nlm.nih.gov"
ftp_path = "/pub/pmc/oa_pdf/01/01/"  # Update with the target directory
local_dir = "./downloaded_pdfs"

download_pdfs_from_ftp(ftp_server, ftp_path, local_dir, file_limit=3)
