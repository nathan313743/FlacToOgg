import os
import os.path
import subprocess

from mutagen.flac import FLAC

class OggFile:
    def __init__(self, flac_file, write_path, file_name, last_modified):
        self.flac_file = flac_file
        self.write_path = write_path
        self.file_name = file_name
        self.last_modified = last_modified
        self.full_path = self.write_path + "/" + self.file_name


def get_files(start_path):
    file_list = [];
    count = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            if os.path.splitext(f)[1] == ".flac":
                fp = os.path.join(dirpath, f)
                file_list.append(fp)
                count = count + 1
    return (file_list, count)


def sanitise_string(s):
    s = s.replace("?","_")
    s = s.replace("/","-")
    s = s.replace("\"","_")
    s = s.replace(":","_")
    s = s.replace("\\","_")
    s = s.replace(">","_")
    s = s.replace("<","_")
    s = s.replace("*","_")
    s = s.replace("|","_")
    return s

def prepare_ogg_files(file_list, dest):    
    ogg_files = []
    for file in file_list:
        try:
            f = FLAC(file)
            artist = sanitise_string(f["artist"][0])
            album = sanitise_string(f["album"][0])
            genre = sanitise_string(f["genre"][0])
            title = sanitise_string(f["title"][0])
            year = f["date"][0]
            tracknumber = f["tracknumber"][0]
            trackTotal = f["tracktotal"][0]
            output_dir = dest + "/" + genre + "/" + artist + "/" + "(" + year + ")" + " - " + album 
            file_name = artist + " -- " + album + " -- " + tracknumber + "-" + trackTotal + ".ogg"
            last_modified = os.path.getmtime(file)
            ogg_files.append(OggFile(file,output_dir, file_name, last_modified))
        except Exception as e:
            print(e)
            print(file)
            raise
    return ogg_files




def should_overwrite_file(flac_file, ogg_file):
    if not os.path.isfile(ogg_file):
        return True

    ogg_last_modified = os.path.getmtime(ogg_file)
    flac_last_modified = os.path.getmtime(flac_file)
    
    if flac_last_modified != ogg_last_modified:
        return True

    return False


def convert_to_ogg(ogg_file_list):
    count = 0
    totalCount = len(ogg_file_list)

    for f in ogg_file_list:

        if not should_overwrite_file(f.flac_file, f.full_path):
            continue
        
        cmd = ["oggenc","-q5", f.flac_file, "-o", f.full_path]

        if not os.path.exists(f.write_path):
            os.makedirs(f.write_path)

        count = count + 1
        print("# " + str(count ) + " of " + str(totalCount))
        process = subprocess.call(cmd)
        os.utime(f.full_path, (os.path.getmtime(f.flac_file) ,os.path.getmtime(f.flac_file)))


def convert_to_ogg_dummy(ogg_file_list):
    for f in ogg_file_list: 
        cmd = ["oggenc","-q5", f.flac_file, f.write_path + "/" + f.file_name]
        print(cmd)

                
def main(origin, dest):
    file_list, count  = get_files(origin)
    ogg_file_list = prepare_ogg_files(file_list, dest)
    convert_to_ogg(ogg_file_list)
        
        
if __name__ == "__main__":
    #main("source", "destination")
