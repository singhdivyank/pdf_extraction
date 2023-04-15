"""
main file for program execution
"""

# required imports
import os
import sys
import time

# import from libraries
from tkinter import Tk, Text, END

# import from files
from aws_connect import dynamodb_func
from invoice import ImageExtraction
from resume import ResumeExtraction
from config import FILE_EXTENSIONS, TKINTER_CONSTS

# ui constants
UI_TITLE = TKINTER_CONSTS.get('title')
UI_GEOMETRY = TKINTER_CONSTS.get('ui_geometry')
# text dimensions
TEXT_HEIGHT = TKINTER_CONSTS.get('text_height')
TEXT_WIDTH = TKINTER_CONSTS.get('text_width')


class MainClass:

    def __init__(self, file_name, file_type, file_extension):
        self.file_name = file_name
        self.file_type = file_type
        self.file_extension = file_extension

    def extraction_results(self):

        """
        perform extraction based on file type
        """

        results = {}

        try:
            if not self.file_extension == 'pdf':
                if self.file_type == 'invoice' or self.file_type == 'kyc':
                    # perform extraction
                    invoice_ob = ImageExtraction(self.file_name)
                    results = invoice_ob.process_file()
                else:
                    print(f"{self.file_type} must be of jpg, png or jpeg formats")
            elif self.file_extension == 'pdf':
                if self.file_type == 'resume':
                    # perform extraction
                    resume_ob = ResumeExtraction(self.file_name)
                    results = resume_ob.process_resume()
                else:
                    print(f"Currently only resume supported for pdf file type")
            else:
                print(f"Invalid file type {self.file_type} provided for {self.file_extension} extension")
        except Exception as error:
            print(f"extraction_results :: Exception :: {str(error)}")
        
        return results

    def render_results(self, result_ls):

        """
        display list of results on UI using Tkinter
        :param list results: obtained results
        """
        
        # create GUI
        window = Tk()
        window.title(UI_TITLE)
        window.geometry(UI_GEOMETRY)

        try:
            # text layout
            text = Text(window, height=TEXT_HEIGHT, width=TEXT_WIDTH)
            text.pack(pady=30)
            # text to display
            text.insert(END, f"Obtained results for {self.file_name} \n") # line1
            text.insert(END, "------------ xxxxxxxxx -----------------\n") # line2
            # extraction results
            for ls_item in result_ls[:-1]:
                text.insert(END, ls_item + "\n")
            text.insert(END, "------------ xxxxxxxxx -----------------\n") # penultimate line
            end_time = time.time()
            text.insert(END, f"Finished Rendering\nTotal Time taken: {str(end_time - start_time)} seconds") # final line
            window.mainloop()
        except Exception as error:
            print(f"render_results :: Exception :: {str(error)}")


if __name__ == '__main__':

    start_time = time.time()
    file_type = str(sys.argv[1]).lower()
    file_name = str(sys.argv[-1])
    file_extension = os.path.basename(file_name).split(".")[-1]

    try:
        # check file extension
        if not file_extension in FILE_EXTENSIONS:
            print(f"Invalid file type. Only {FILE_EXTENSIONS} supported. Execution time: {time.time() - start_time} seconds")
            # exit and do not execute
            sys.exit(0)
        
        main_ob = MainClass(file_name, file_type, file_extension)
        extraction_results = main_ob.extraction_results()
        if extraction_results:
            # save them to dynamoDB
            dynamodb_func(extraction_results, file_type)
            # convert dict to string
            result_str = ""
            for key, value in extraction_results.items():
                result_str += key + ': ' + value + '\ ' # render in the form- Name: XXXX
            # convert the string to list
            result_ls = result_str.split("\ ")
            # render on UI
            main_ob.render_results(result_ls)
        else:
            print(f"No results extracted for {file_name}")
            sys.exit(0)
    except Exception as error:
        print(f"Exception:: {str(error)}")
