import argparse
import json
import os
import shutil
import tarfile
import time
import uuid
from zipfile import ZipFile

import gdown
import requests
from torchvision.datasets import MNIST


def stage_path(data_dir, name):
    full_path = os.path.join(data_dir, name)

    if not os.path.exists(full_path):
        os.makedirs(full_path)

    return full_path


def download_and_extract(url, dst, remove=True):
    if "drive.google" in url:
        gdown.download(url, dst, quiet=False)

        if dst.endswith(".tar.gz"):
            tar = tarfile.open(dst, "r:gz")
            tar.extractall(os.path.dirname(dst))
            tar.close()

        if dst.endswith(".tar"):
            tar = tarfile.open(dst, "r:")
            tar.extractall(os.path.dirname(dst))
            tar.close()

        if dst.endswith(".zip"):
            zf = ZipFile(dst, "r")
            zf.extractall(os.path.dirname(dst))
            zf.close()

    else:

        chunk_size = 1024 * 1024
        begin = time.time()

        session = requests.Session()
        req = session.get(url, stream=True)
        with open(dst, "w") as f:
            for chunk in req.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    f.flush()

        end = time.time()
        print(
            f" downloaded {dst} in {(end - begin)/60} minutes, with chunk size = {chunk_size}"
        )

        if dst.endswith(".tar.gz"):
            tar = tarfile.open(dst, "r:gz")
            tar.extractall(os.path.dirname(dst))
            tar.close()

        if dst.endswith(".tar"):
            tar = tarfile.open(dst, "r:")
            tar.extractall(os.path.dirname(dst))
            tar.close()

        if dst.endswith(".zip"):
            zf = ZipFile(dst, "r")
            zf.extractall(os.path.dirname(dst))
            zf.close()

    if remove:
        os.remove(dst)


# VLCS ########################################################################

# Slower, but builds dataset from the original sources
#
def download_vlcs_slow(data_dir):
    full_path = stage_path(data_dir, "VLCS")

    tmp_path = os.path.join(full_path, "tmp/")
    if not os.path.exists(tmp_path):
        os.makedirs(tmp_path)

    with open("domainbed/misc/vlcs_files.txt", "r") as f:
        lines = f.readlines()
        files = [line.strip().split() for line in lines]

    download_and_extract(
        "http://pjreddie.com/media/files/VOCtrainval_06-Nov-2007.tar",
        os.path.join(tmp_path, "voc2007_trainval.tar"),
    )

    download_and_extract(
        "https://drive.google.com/uc?id=1I8ydxaAQunz9R_qFFdBFtw6rFTUW9goz",
        os.path.join(tmp_path, "caltech101.tar.gz"),
    )

    download_and_extract(
        "http://groups.csail.mit.edu/vision/Hcontext/data/sun09_hcontext.tar",
        os.path.join(tmp_path, "sun09_hcontext.tar"),
    )

    tar = tarfile.open(os.path.join(tmp_path, "sun09.tar"), "r:")
    tar.extractall(tmp_path)
    tar.close()

    for src, dst in files:
        class_folder = os.path.join(data_dir, dst)

        if not os.path.exists(class_folder):
            os.makedirs(class_folder)

        dst = os.path.join(class_folder, uuid.uuid4().hex + ".jpg")

        if "labelme" in src:
            # download labelme from the web
            gdown.download(src, dst, quiet=False)
        else:
            src = os.path.join(tmp_path, src)
            shutil.copyfile(src, dst)

    shutil.rmtree(tmp_path)


def download_vlcs(data_dir):
    # Original URL: http://www.eecs.qmul.ac.uk/~dl307/project_iccv2017
    full_path = stage_path(data_dir, "VLCS")
    if os.path.exists(full_path):
        print("data folder exists already")
        if len(os.listdir(full_path)) == 0:
            print("data folder empty")
            download_and_extract(
                "https://drive.google.com/uc?id=1skwblH1_okBwxWxmRsp9_qi15hyPpxg8",
                os.path.join(data_dir, "VLCS.tar.gz"),
            )

    else:
        download_and_extract(
            "https://drive.google.com/uc?id=1skwblH1_okBwxWxmRsp9_qi15hyPpxg8",
            os.path.join(data_dir, "VLCS.tar.gz"),
        )


# Digits #######################################################################
def download_digits(data_dir):
    full_path = stage_path(data_dir, "Digits")
    if os.path.exists(full_path):
        print("data folder exists already")
        if len(os.listdir(full_path)) == 0:
            print("data folder empty")
            download_and_extract(
                "https://drive.google.com/uc?id=1RwY1X2MmR-AsvpGjxHZfQOUTnNn15Z_q",
                os.path.join(data_dir, "Digits.zip"),
            )

    else:
        download_and_extract(
            "https://drive.google.com/uc?id=1RwY1X2MmR-AsvpGjxHZfQOUTnNn15Z_q",
            os.path.join(data_dir, "Digits.zip"),
        )


# MNIST #######################################################################
def download_mnist(data_dir):
    # Original URL: http://yann.lecun.com/exdb/mnist/
    full_path = stage_path(data_dir, "MNIST")
    MNIST(full_path, download=True)


# PACS ########################################################################
def download_pacs(data_dir):
    # Original URL: http://www.eecs.qmul.ac.uk/~dl307/project_iccv2017
    full_path = stage_path(data_dir, "PACS")

    if os.path.exists(full_path):
        print("data folder exists already")
        if len(os.listdir(full_path)) == 0:
            print("data folder empty")
            download_and_extract(
                "https://drive.google.com/uc?id=1AP9FS_H0k581eRUbNU9Q3yBbk4sk-vmW",
                os.path.join(data_dir, "PACS.zip"),
            )

    else:
        download_and_extract(
            "https://drive.google.com/uc?id=1AP9FS_H0k581eRUbNU9Q3yBbk4sk-vmW",
            os.path.join(data_dir, "PACS.zip"),
        )


# Office-Home #################################################################


def download_office_home(data_dir):
    # Original URL: http://hemanthdv.org/OfficeHome-Dataset/
    full_path = stage_path(data_dir, "OfficeHome")

    if os.path.exists(full_path):
        print("data folder exists already")
        if len(os.listdir(full_path)) == 0:
            print("data folder empty")
            download_and_extract(
                "https://drive.google.com/uc?id=1Jza7tgNWfRecJ4ypf9d36ASnH9ckWt92",
                os.path.join(data_dir, "office_home.zip"),
            )

            os.rename(os.path.join(data_dir, "OfficeHomeDataset_10072016"), full_path)

    else:

        download_and_extract(
            "https://drive.google.com/uc?id=1Jza7tgNWfRecJ4ypf9d36ASnH9ckWt92",
            os.path.join(data_dir, "office_home.zip"),
        )

        os.rename(os.path.join(data_dir, "OfficeHomeDataset_10072016"), full_path)


# DomainNET ###################################################################


def download_domain_net(data_dir):
    # Original URL: http://ai.bu.edu/M3SDA/
    full_path = stage_path(data_dir, "domain_net")

    urls = [
        "http://csr.bu.edu/ftp/visda/2019/multi-source/groundtruth/clipart.zip",
        "http://csr.bu.edu/ftp/visda/2019/multi-source/infograph.zip",
        "http://csr.bu.edu/ftp/visda/2019/multi-source/groundtruth/painting.zip",
        "http://csr.bu.edu/ftp/visda/2019/multi-source/quickdraw.zip",
        "http://csr.bu.edu/ftp/visda/2019/multi-source/real.zip",
        "http://csr.bu.edu/ftp/visda/2019/multi-source/sketch.zip",
    ]

    for url in urls:
        download_and_extract(url, os.path.join(full_path, url.split("/")[-1]))

    with open("domainbed/misc/domain_net_duplicates.txt", "r") as f:
        for line in f.readlines():
            try:
                os.remove(os.path.join(full_path, line.strip()))
            except OSError:
                pass


# TerraIncognita ##############################################################


def download_terra_incognita(data_dir):
    # Original URL: https://beerys.github.io/CaltechCameraTraps/
    full_path = stage_path(data_dir, "terra_incognita")
    if os.path.exists(full_path):
        print("data folder exists already")
        if len(os.listdir(full_path)) == 0:
            print("data folder empty")
            download_and_extract(
                "http://www.vision.caltech.edu/~sbeery/datasets/caltechcameratraps18/eccv_18_all_images_sm.tar.gz",
                os.path.join(full_path, "terra_incognita_images.tar.gz"),
            )

            download_and_extract(
                "http://www.vision.caltech.edu/~sbeery/datasets/caltechcameratraps18/eccv_18_all_annotations.tar.gz",
                os.path.join(full_path, "terra_incognita_annotations.tar.gz"),
            )

            include_locations = [38, 46, 100, 43]

            include_categories = [
                "bird",
                "bobcat",
                "cat",
                "coyote",
                "dog",
                "empty",
                "opossum",
                "rabbit",
                "raccoon",
                "squirrel",
            ]

            images_folder = os.path.join(full_path, "eccv_18_all_images_sm/")
            annotations_file = os.path.join(full_path, "CaltechCameraTrapsECCV18.json")
            destination_folder = full_path

            stats = {}

            if not os.path.exists(destination_folder):
                os.mkdir(destination_folder)

            with open(annotations_file, "r") as f:
                data = json.load(f)

            category_dict = {}
            for item in data["categories"]:
                category_dict[item["id"]] = item["name"]

            for image in data["images"]:
                image_location = image["location"]

                if image_location not in include_locations:
                    continue

                loc_folder = os.path.join(
                    destination_folder, "location_" + str(image_location) + "/"
                )

                if not os.path.exists(loc_folder):
                    os.mkdir(loc_folder)

                image_id = image["id"]
                image_fname = image["file_name"]

                for annotation in data["annotations"]:
                    if annotation["image_id"] == image_id:
                        if image_location not in stats:
                            stats[image_location] = {}

                        category = category_dict[annotation["category_id"]]

                        if category not in include_categories:
                            continue

                        if category not in stats[image_location]:
                            stats[image_location][category] = 0
                        else:
                            stats[image_location][category] += 1

                        loc_cat_folder = os.path.join(loc_folder, category + "/")

                        if not os.path.exists(loc_cat_folder):
                            os.mkdir(loc_cat_folder)

                        dst_path = os.path.join(loc_cat_folder, image_fname)
                        src_path = os.path.join(images_folder, image_fname)

                        shutil.copyfile(src_path, dst_path)

            shutil.rmtree(images_folder)
            os.remove(annotations_file)

    else:
        download_and_extract(
            "http://www.vision.caltech.edu/~sbeery/datasets/caltechcameratraps18/eccv_18_all_images_sm.tar.gz",
            os.path.join(full_path, "terra_incognita_images.tar.gz"),
        )

        download_and_extract(
            "http://www.vision.caltech.edu/~sbeery/datasets/caltechcameratraps18/eccv_18_all_annotations.tar.gz",
            os.path.join(full_path, "terra_incognita_annotations.tar.gz"),
        )

        include_locations = [38, 46, 100, 43]

        include_categories = [
            "bird",
            "bobcat",
            "cat",
            "coyote",
            "dog",
            "empty",
            "opossum",
            "rabbit",
            "raccoon",
            "squirrel",
        ]

        images_folder = os.path.join(full_path, "eccv_18_all_images_sm/")
        annotations_file = os.path.join(full_path, "CaltechCameraTrapsECCV18.json")
        destination_folder = full_path

        stats = {}

        if not os.path.exists(destination_folder):
            os.mkdir(destination_folder)

        with open(annotations_file, "r") as f:
            data = json.load(f)

        category_dict = {}
        for item in data["categories"]:
            category_dict[item["id"]] = item["name"]

        for image in data["images"]:
            image_location = image["location"]

            if image_location not in include_locations:
                continue

            loc_folder = os.path.join(
                destination_folder, "location_" + str(image_location) + "/"
            )

            if not os.path.exists(loc_folder):
                os.mkdir(loc_folder)

            image_id = image["id"]
            image_fname = image["file_name"]

            for annotation in data["annotations"]:
                if annotation["image_id"] == image_id:
                    if image_location not in stats:
                        stats[image_location] = {}

                    category = category_dict[annotation["category_id"]]

                    if category not in include_categories:
                        continue

                    if category not in stats[image_location]:
                        stats[image_location][category] = 0
                    else:
                        stats[image_location][category] += 1

                    loc_cat_folder = os.path.join(loc_folder, category + "/")

                    if not os.path.exists(loc_cat_folder):
                        os.mkdir(loc_cat_folder)

                    dst_path = os.path.join(loc_cat_folder, image_fname)
                    src_path = os.path.join(images_folder, image_fname)

                    shutil.copyfile(src_path, dst_path)

        shutil.rmtree(images_folder)
        os.remove(annotations_file)


# miniDomainNet #################################################################
def download_mini_domain_net(data_dir):

    full_path = stage_path(data_dir, "miniDomainNet")
    if os.path.exists(full_path):
        print("data folder exists already")
        if len(os.listdir(full_path)) == 0:
            print("data folder empty")
            download_and_extract(
                "https://drive.google.com/uc?id=1-ZdxH-0SH6qcQgUuhPCgHWAUNmPpttqz",
                os.path.join(data_dir, "miniDomainNet.zip"),
            )
    else:
        download_and_extract(
            "https://drive.google.com/uc?id=1-ZdxH-0SH6qcQgUuhPCgHWAUNmPpttqz",
            os.path.join(data_dir, "miniDomainNet.zip"),
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download datasets")
    parser.add_argument("--data_dir", type=str, required=True)
    parser.add_argument("--dataset", type=str, required=True)

    args = parser.parse_args()

    if len(args.data_dir)>0 and not os.path.isdir(args.data_dir):
        os.system("mkdir -p {}".format(args.data_dir))

    if args.dataset == "MNIST":
        download_mnist(args.data_dir)
    elif args.dataset == "Digits":
        download_digits(args.data_dir)
    elif args.dataset == "PACS":
        download_pacs(args.data_dir)
    elif args.dataset == "OfficeHome":
        download_office_home(args.data_dir)
    elif args.dataset == "DomainNet":
        download_domain_net(args.data_dir)
    elif args.dataset == "miniDomainNet":
        download_mini_domain_net(args.data_dir)
    elif args.dataset == "VLCS":
        try:
            download_vlcs(args.data_dir)
        except:
            print("using slow download ##########")
            download_vlcs_slow(args.data_dir)
