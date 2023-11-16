import datetime
import os
import subprocess
from pathlib import PurePath

import pyexiv2

PHOTOS_DIR = "/photos"
TEMP_DIR = "/tmp"


def check_env():
    if not os.path.exists(PHOTOS_DIR):
        raise Exception("Photos directory does not exist.")


def get_tmp_file_dir(photos_file_path):
    tmp_file_dir = os.path.join(TEMP_DIR, os.path.relpath(
        os.path.dirname(photos_file_path), PHOTOS_DIR))
    os.makedirs(tmp_file_dir, exist_ok=True)
    return tmp_file_dir


def get_photos_file_dir(tmp_file_path):
    photos_file_dir = os.path.join(PHOTOS_DIR, os.path.relpath(
        os.path.dirname(tmp_file_path), TEMP_DIR))
    return photos_file_dir


def iterate_live_photos(input_dir):
    for root, _, files in os.walk(input_dir, topdown=False):
        for video_file in files:
            if video_file.endswith("_HEVC.MOV"):
                photo_file = video_file.removesuffix("_HEVC.MOV") + ".HEIC"
                motion_file = video_file.removesuffix("_HEVC.MOV") + "_mp4.jpg"
                if photo_file in files and not motion_file in files:
                    yield (os.path.join(root, photo_file), os.path.join(root, video_file))


def merge_jpg_and_mp4(photo_path, video_path):
    out_path = os.path.join(get_photos_file_dir(
        photo_path), PurePath(photo_path).stem + "_mp4.jpg")
    print("merge_jpg_and_mp4", out_path)
    with open(out_path, "wb") as out_file, open(photo_path, "rb") as photo_file, open(video_path, "rb") as video_file:
        out_file.write(photo_file.read())
        out_file.write(video_file.read())
    return out_path


def add_xmp_metadata(merged_path, offset):
    with pyexiv2.Image(merged_path) as img:
        try:
            pyexiv2.registerNs(
                "http://ns.google.com/photos/1.0/camera/", "GCamera")
        except Exception as e:
            print(e)
        xmp = {
            "Xmp.GCamera.MicroVideo": 1,
            "Xmp.GCamera.MicroVideoVersion": 1,
            "Xmp.GCamera.MicroVideoOffset": offset,
            "Xmp.GCamera.MicroVideoPresentationTimestampUs": 1500000
        }
        img.modify_xmp(xmp)


def convert_heic_to_jpg(heic_file_path):
    stem = PurePath(heic_file_path).stem
    out_path = os.path.join(get_tmp_file_dir(heic_file_path), stem + ".jpg")
    print("heic_file_path, out_path", heic_file_path, out_path)
    subprocess.call(["convert", heic_file_path, out_path])
    return out_path


def convert_hevc_to_mp4(hevc_file_path):
    stem = PurePath(hevc_file_path).stem.removesuffix("_HEVC")
    out_path = os.path.join(get_tmp_file_dir(hevc_file_path), stem + ".mp4")
    print("hevc_file_path, out_path", hevc_file_path, out_path)
    subprocess.call(["ffmpeg", "-i", hevc_file_path,
                    "-c:v", "libx264", "-y", out_path])
    return out_path


def convert_live_photo_to_motion_photo(photo_path, video_path):
    jpg_path = convert_heic_to_jpg(photo_path)
    mp4_path = convert_hevc_to_mp4(video_path)
    merged_path = merge_jpg_and_mp4(jpg_path, mp4_path)

    # The 'offset' field in the XMP metadata should be the offset (in bytes) from the end of the file to the part
    # where the video portion of the merged file begins.
    # In other words, merged size - photo_only_size = video_only_size = offset.
    offset = os.path.getsize(mp4_path)
    add_xmp_metadata(merged_path, offset)


def main():
    check_env()

    print("start at", datetime.datetime.now())

    for photo_path, video_path in iterate_live_photos(PHOTOS_DIR):
        convert_live_photo_to_motion_photo(photo_path, video_path)


if __name__ == '__main__':
    main()
