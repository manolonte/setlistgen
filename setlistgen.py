# imports pikepdf and pyexcel-ods library
from fpdf import FPDF
import pyexcel_ods
import sys

def add_page(pdf):
    pdf.add_page()
    pdf.image(x = 166, y = 2, w = 32, type = 'png', name = 'resources/logo_bluestop.png')
# main function
def main():
    # read arguments from command line input and output files
    # input file is the setlist
    # sheet_number is the sheet in the setlist file
    # output file is the pdf file
    # setlistgen.py <input file> <sheet> <output file>
    input_file = sys.argv[1]
    sheet_number = int(sys.argv[2])
    output_file = sys.argv[3]
    print("Input file: " + input_file)
    print("Sheet number: " + str(sheet_number))
    print("Output file: " + output_file)

    # read the setlist file
    # setlist is a list of lists
    setlist = list(pyexcel_ods.get_data(input_file).items())[sheet_number]
    lines = 0
    for song in setlist[1]:
        if song:
            if song[0] == "Descanso":
                break
        lines = lines + 1
    lines = max(lines, 17)
    print("Lines: " + str(lines))
    # generate a pdf file from the setlist
    pdf = FPDF()
    add_page(pdf)
    text_size = int(560/lines)
    cell_height = text_size/2
    pdf.set_font("Arial", style="B", size=16)
    title_printed = False
    for song in setlist[1]:
        if song:
            song_title = song[0].encode('latin-1', 'replace').decode('latin-1')
            song_title = song_title.replace("?", "'")
            if song_title == "Descanso":
                add_page(pdf)
                continue
            if song_title == "Tema":
                continue
            pdf.cell(156, cell_height, txt=song_title, ln=0, align="L")
            if not title_printed:
                pdf.set_font("Arial", style="B", size=text_size)
                title_printed = True
            if 1 < len(song):
                song_key = song[1].encode('latin-1', 'replace').decode('latin-1')
                pdf.cell(24, cell_height, txt=song_key, ln=0, align="L")
            else:
                pdf.cell(24, cell_height, txt="", ln=1, align="L")
                continue
            if 2 < len(song):
                song_harp_key = song[2].encode('latin-1', 'replace').decode('latin-1')
                pdf.cell(24, cell_height, txt=song_harp_key, ln=1, align="L")
            else:
                pdf.cell(24, cell_height, txt="", ln=1, align="L")

    pdf.output(output_file)

if __name__ == "__main__":
    main()
