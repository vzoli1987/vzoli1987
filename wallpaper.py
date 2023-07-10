import requests
import os
import subprocess

# Letöltendő posztok száma
num_posts = 1

# Letöltési mappa elérési útvonala
download_folder = "/media/hdd/scripts/wallpaper/"

# Fájlnév előtagja
filename_prefix = "wallpaper"

# Reddit API endpoint URL
api_url = "https://www.reddit.com/r/wallpapers/new.json?limit={}".format(num_posts)

# Letölti a legújabb Reddit posztokat a JSON formátumban
response = requests.get(api_url, headers={"User-Agent": "Mozilla/5.0"})
json_data = response.json()

# JSON feldolgozása és képek letöltése
for i, post in enumerate(json_data["data"]["children"]):
    image_url = post["data"]["url_overridden_by_dest"]

    # Letölti a képet a megadott mappába csendes módban
    image_filename = "{}_{}.jpg".format(filename_prefix, i)
    image_path = os.path.join(download_folder, image_filename)
    subprocess.run(["wget", "-q", "-O", image_path, image_url])

    if os.path.isfile(image_path):
        # Konvertálja a képet m1v fájlba ffmpeg segítségével
        output_filename = "{}_{}.m1v".format(filename_prefix, i)
        output_path = os.path.join(download_folder, output_filename)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "panic", "-loop", "1", "-i", image_path, "-t", "1", "-r", "25", "-b", "20000", output_path])

        # Törli a letöltött képet
        os.remove(image_path)
        # Mozgatja az átkonvertált videót a cél helyre
        final_path = "/usr/share/bootlogo.mvi"
        subprocess.run(["mv", output_path, final_path])

        print("A(z) {}. Reddit háttérkép sikeresen letöltve és konvertálva.".format(i))
    else:
        print("A kép letöltése sikertelen.")
