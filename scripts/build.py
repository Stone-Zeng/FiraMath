#!/usr/bin/python

from __future__ import print_function

import argparse
import datetime
import os
import platform
import sys

import fontforge

# Even on Windows, we should use `/`, otherwise `include()` in AFDKO feature files will break.
PATH_SEP         = "/"
PWD              = os.getcwd()
SFD_PATH         = PATH_SEP.join([PWD, "src"])
FEATURE_PATH     = PATH_SEP.join([PWD, "src", "features"])
OTF_PATH         = PATH_SEP.join([PWD, "release", "fonts"])
TEST_PATH        = PATH_SEP.join([PWD, "test"])
TEX_PATH         = PATH_SEP.join([PWD, "tex"])
FAMILY_NAME      = "FiraMath"
FAMILY_NAME_FULL = "fira-math"
TEST_FILE_NAME   = "font-test"
DOCS_FILE_NAMES  = ["firamath-demo", "firamath-specimen", "unimath-symbols"]
# weights          = ["thin", "light", "regular", "medium", "bold"]
weights          = ["regular"]

def generate_fonts():
    print("FontForge version: " + fontforge.version())
    print("Python version: "+ platform.python_version())
    print("Platform: " + platform.platform() + "\n")
    for i in weights:
        font_name      = FAMILY_NAME + "-" + i.capitalize()
        font_name_full = FAMILY_NAME_FULL + "-" + i
        sfdir          = PATH_SEP.join([SFD_PATH, font_name_full + ".sfdir"])
        feature_file   = PATH_SEP.join([FEATURE_PATH, font_name_full + ".fea"])
        otf_file       = PATH_SEP.join([OTF_PATH, font_name + ".otf"])
        
        print(font_name)
        print(font_name_full)
        print(sfdir)
        print(feature_file)
        print(otf_file)

        font = fontforge.open(sfdir)
        print("Open:", font)
        print("Merge:", font.mergeFeature(feature_file))
        font.generate(otf_file, flags=("opentype"))
        print(datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S.%f]')
            + " '" + font_name + "' " + "generated successfully.")

def xelatex_test():
    os.chdir(TEST_PATH)
    run_xelatex(TEST_FILE_NAME)

def run_xelatex(file_name):
    os.system("xelatex " + file_name + ".tex")

def make_docs():
    os.chdir(TEX_PATH)
    for i in DOCS_FILE_NAMES:
        run_latexmk(i)

def run_latexmk(file_name):
    os.system("latexmk -g -xelatex " + file_name + ".tex")

def clean():
    os.chdir(TEST_PATH)
    clean_aux_files()
    os.chdir(TEX_PATH)
    clean_aux_files()

def clean_aux_files():
    aux_file_suffixes = ["aux", "fdb_latexmk", "fls", "log", "nav", "out", "snm", "toc", "xdv"]
    for i in aux_file_suffixes:
        rm("*." + i)

def rm(file_name):
    if platform.system() == "Linux":
        os.system("rm -f " + file_name)
    elif platform.system() == "Windows":
        os.system("DEL /Q " + file_name)

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-f", "--fonts", action="store_true", help="generate fonts")
group.add_argument("-t", "--test",  action="store_true", help="run xelatex test")
group.add_argument("-d", "--docs",  action="store_true", help="generate documentations")
group.add_argument("-r", "--run",   action="store_true", help="generate fonts and run test")
group.add_argument("-a", "--all",   action="store_true", help="generate fonts and documentations")
group.add_argument("-c", "--clean", action="store_true", help="clean working directory")
args = parser.parse_args()

if args.fonts:
    generate_fonts()
if args.test:
    xelatex_test()
if args.docs:
    make_docs()
if args.run:
    generate_fonts()
    xelatex_test()
if args.all:
    generate_fonts()
    make_docs()
if args.clean:
    clean()
