import os
import subprocess

'''
Module for running a phantomJS instance and getting the location
'''
class PhantomJSDriver:
    '''
    Interacts with the PhantomJS binary file and returns the output using pipes.
    '''
    def __init__(self):
        # Get the path of the bin folder.
        self.bin_folder = os.path.dirname(os.path.realpath(__file__)) + "\\bin\\"
        self.exe_path = self.bin_folder + "phantomjs.exe"
        self.js_script_name = 'getFinalURL.js'
        self.script_file_path = self.bin_folder + self.js_script_name

    def get_final_url(self, url):
        '''
        Passes the URL to the js script that opens the page and waits for some time before exiting.
        Prints the final URL before printing.
        '''
        out = os.popen(self.exe_path + " " + self.script_file_path + " " + url).read()
        return out

if __name__ == '__main__':
    driver = PhantomJSDriver()
    print(driver.get_final_url("https://goo.gl/maps/7ECDXPFxo2S2"))
