from pickle import NONE
import time
from typing import Dict, Union
import requests
import os
from rich.progress import Progress
from rich import print as rprint
import re
from .basic import speedMapper, toascii

MAX_FILENAME = 15


class downloader:
    def __init__(
        self,
        url: str,
        save_as: Union[str, None] = None,
        downloadingFileName: Union[str, None] = None,
        maxSpeed: int = 126976,
        disable_progress_bar: bool = False,
        fn_callback=None,
        fn_callback_argc: Dict = {},
    ) -> None:

        self.url: str
        self.downloadingFileName: str
        self.fileName: str
        self.callback = fn_callback
        self.maxSpeed: int = maxSpeed
        self.fn_callback_argc: Dict = fn_callback_argc
        self.disable_progress_bar: bool = disable_progress_bar

        # check url
        if self.isUrl(url):
            self.url = url
        else:
            raise Exception("Invaild URL")

        # set the downloading file name
        self.downloadingFileName = (
            self.getDownloadingFileName(url)
            if downloadingFileName is None
            else os.path.realpath(downloadingFileName)
        )

        # set the file name
        self.fileName = (
            self.downloadingFileName[0:-12]
            if save_as is None
            else os.path.realpath(save_as)
        )

        # create session
        self.session: requests.Session = requests.Session()

        # intial size of partially downloaded file
        self.intial_size: int = self.getFileSize(self.downloadingFileName)

        # total size of downloading file
        self.total_size: int = self.getTotalsize(session=self.session, url=self.url)

        # remaing download size
        self.downloadableSize: int = self.total_size - self.intial_size

        # is fileName exists
        self.isexist_fileName = os.path.exists(self.fileName)

        # is downloadingFileName exists
        self.isexist_downloadingFileName = os.path.exists(self.downloadingFileName)

    def __child_download(self):

        endbyte: int = self.maxSpeed - 1 + self.intial_size
        startbyte: int = self.intial_size
        downloaded_size: int = self.intial_size
        headers: dict
        counter: int

        with Progress(disable=self.disable_progress_bar) as progress:
            with open(self.downloadingFileName, "ab") as file:
                task = progress.add_task(
                    "[red]Downloading...",
                    total=self.total_size,
                    completed=self.intial_size,
                )

                while startbyte <= self.total_size:
                    counter = time.perf_counter_ns()

                    headers = {"Range": f"bytes={startbyte}-{endbyte}"}

                    r = self.session.get(
                        self.url, stream=True, allow_redirects=True, headers=headers
                    )

                    downloaded_size += self.maxSpeed

                    file.write(r.content)

                    startbyte = endbyte + 1
                    endbyte += self.maxSpeed

                    cur_speed = self.maxSpeed * (time.perf_counter_ns() - counter) / 1e9

                    progress.update(
                        task,
                        advance=self.maxSpeed,
                        description=f"[blue]Speed [green bold]{speedMapper(cur_speed)} [red]Downloading[green] [{downloaded_size}]....",
                    )
                    if not self.callback==None:
                      self.callback(cur_speed, **self.fn_callback_argc)

    def downlaod(self):

        self.create_dir()

        if self.total_size == -1:
            if not self.isexist_fileName:
                with open(self.fileName, "wb") as file:
                    file.write(self.session.get(self.url).content)
            else:
                rprint("another file exists")

        try:

            # file already exist
            if self.intial_size > self.total_size:
                rprint(
                    f"{self.downloadingFileName} is edited corecpted file (delete the file and run)"
                )

            else:

                if not self.isexist_fileName:

                    self.__child_download()
                    os.rename(self.downloadingFileName, self.fileName)

                else:

                    if self.getFileSize(self.fileName) == self.total_size:
                        rprint(
                            "File already exist (you can delete the file *.downloading)"
                        )
                    else:
                        rprint("another file exists")

        except KeyboardInterrupt:
            pass
        except Exception as e:
            raise (e)

    def create_dir(self):

        if not self.isexist_fileName:
            file_dir = os.path.dirname(self.fileName)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)

        if not self.isexist_downloadingFileName:
            file_dir = os.path.dirname(self.downloadingFileName)
            if not os.path.exists(file_dir):
                os.makedirs(file_dir)

    @staticmethod
    def getDownloadingFileName(url):

        # get last text as filename
        filename: str = url.split("/")[-1]

        # filter non ascii char and select only the max filename lenght
        filename = toascii(filename)[0:MAX_FILENAME]

        return filename + ".downloading"

    @staticmethod
    def getFileSize(file: str) -> int:
        if os.path.exists(file):
            return os.path.getsize(file)
        else:
            return 0

    @staticmethod
    def getTotalsize(session: requests.Session, url: str) -> int:

        try:
            data = session.get(
                url,
                stream=True,
                allow_redirects=True,
                headers={"Range": "bytes=0-0"},
            ).headers.get("Content-Range")

        except AttributeError:
            return -1

        if data is None:
            return -1
        else:
            return int(data.split("/")[-1])

    @staticmethod
    def isUrl(url: str) -> bool:
        regex = re.compile(
            r"^(?:http|ftp)s?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|"
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        if re.match(regex, url) is not None:
            return True
        return False


