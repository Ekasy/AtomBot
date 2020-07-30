# most of the code is taken from the example by reference
# https://github.com/abbyy/ocrsdk.com/tree/master/Python
# but slightly modified to work with url images and text output


import os
import requests
import xml.dom.minidom
import time
from urllib.request import urlopen
from PIL import Image
from io import BytesIO
import config


class ProcessingSettings:
    Language = 'English'
    OutputFormat = 'txt'


class Task:
    Status = 'Unknown'
    Id = None
    DownloadUrl = None

    def is_active(self):
        if self.Status == "InProgress" or self.Status == "Queued":
            return True
        else:
            return False


class AbbyOnlineSdk:
    ServerUrl = 'http://cloud-eu.ocrsdk.com/'
    ApplicationId = config.ABBY_APP_ID
    Password = config.ABBY_PASSWORD
    Proxies = {}

    def process_image(self, file_path, settings):
        url_params = {
            "language": settings.Language,
            "exportFormat": settings.OutputFormat
        }
        request_url = self.get_request_url("processImage")

        response = requests.get(file_path)
        image_data = Image.open(BytesIO(response.content))
        imgByteArr = BytesIO()
        image_data.save(imgByteArr, format=image_data.format)
        imgByteArr = imgByteArr.getvalue()

        response = requests.post(request_url, data=imgByteArr, params=url_params,
                                 auth=(self.ApplicationId, self.Password), proxies=self.Proxies)

        # Any response other than HTTP 200 means error - in this case exception will be thrown
        response.raise_for_status()

        # parse response xml and extract task ID
        task = self.decode_response(response.text)
        return task

    def decode_response(self, xml_response):
        """ Decode xml response of the server. Return Task object """
        dom = xml.dom.minidom.parseString(xml_response)
        task_node = dom.getElementsByTagName("task")[0]
        task = Task()
        task.Id = task_node.getAttribute("id")
        task.Status = task_node.getAttribute("status")
        if task.Status == "Completed":
            task.DownloadUrl = task_node.getAttribute("resultUrl")
        return task

    def get_task_status(self, task):
        if task.Id.find('00000000-0') != -1:
            # GUID_NULL is being passed. This may be caused by a logical error in the calling code
            # print("Null task id passed")
            return None

        url_params = {"taskId": task.Id}
        status_url = self.get_request_url("getTaskStatus")

        response = requests.get(status_url, params=url_params,
                                auth=(self.ApplicationId, self.Password), proxies=self.Proxies)
        task = self.decode_response(response.text)
        return task

    def download_result(self, task):
        get_result_url = task.DownloadUrl
        if get_result_url is None:
            # print("No download URL found")
            return 'Не найден URL файла'

        res = urlopen(get_result_url)
        answer = ''
        for line in res:
            answer += line.decode('utf-8')
        return answer

    def get_request_url(self, url):
        return self.ServerUrl.strip('/') + '/' + url.strip('/')


processor = None


def setup_processor():
    if "ABBYY_APPID" in os.environ:
        processor.ApplicationId = os.environ["ABBYY_APPID"]

    if "ABBYY_PWD" in os.environ:
        processor.Password = os.environ["ABBYY_PWD"]

    if "http_proxy" in os.environ:
        proxy_string = os.environ["http_proxy"]
        processor.Proxies["http"] = proxy_string

    if "https_proxy" in os.environ:
        proxy_string = os.environ["https_proxy"]
        processor.Proxies["https"] = proxy_string


def recognize_file(file_path, language, output_format):
    settings = ProcessingSettings()
    settings.Language = language
    settings.OutputFormat = output_format
    task = processor.process_image(file_path, settings)
    if task is None:
        # print("Error")
        return 'Ошибка'
    if task.Status == "NotEnoughCredits":
        return 'Недостаточно свободных койнов для распознания текста'

    while task.is_active():
        time.sleep(5)
        task = processor.get_task_status(task)

    if task.Status == "Completed":
        if task.DownloadUrl is not None:
            return processor.download_result(task)


def text_recognising(source_file, language):
    global processor
    processor = AbbyOnlineSdk()
    setup_processor()

    language = 'Russian,English' if language is None else language
    output_format = 'txt'

    text = recognize_file(source_file, language, output_format)
    if len(text) < 2:
        return 'Прости, я не смог ничего прочитать'
    return recognize_file(source_file, language, output_format)
