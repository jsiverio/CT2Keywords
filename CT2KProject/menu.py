import argparse as argparse
import os
import DataScraper

sourcePath = os.getcwd()
outputPath = os.getcwd()
cybertipFiles=[]
fileCount = 0

parser = argparse.ArgumentParser(description="Extract identifiers from cybertips and generats keyword list")

parser.add_argument("-s", "--source", type=str, help="Directory where cybertips are located")
parser.add_argument("-o", "--output", type=str, help="Keyword file destination")
parser.add_argument("-a", "--all", action="store_true", help="Extracts all identifiers")
parser.add_argument("-c", "--combined", action="store_true", help= "Puts all identifiers in one file")
parser.add_argument("-e", "--separate", action="store_true", help="Separates identifiers per category in to individual files")
parser.add_argument("-u", "--usernames", action="store_true", help="Extracts usernames and/or ESP user ID only")
parser.add_argument("-f", "--files", action="store_true", help="Extracts file names only")
parser.add_argument("-ha", "--hashes", action="store_true", help="Extracts hash values only")
parser.add_argument("-i", "--ip", action="store_true", help="Extracts all IPs only")
args = parser.parse_args()

if args.source:
    sourcePath = args.source
if args.output:
    outputPath = args.output

try:
    if os.path.exists(sourcePath):
        for root, dirs, files in os.walk(sourcePath, topdown=False):
            for name in files:
                if name.endswith('pdf'):
                    cybertipFiles.append(os.path.join(root, name))
    fileCount = len(cybertipFiles)
except:
    print("An error occurred while trying to access the directory")

for file in cybertipFiles:
    DataScraper.scraper(file)


