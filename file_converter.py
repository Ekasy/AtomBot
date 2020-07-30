import convertapi
import config


def get_extension(file_name):
    extension = ''
    for i in reversed(file_name):
        if i == '.':
            return extension
        else:
            extension = i + extension


def folder_exist(users_list, user_id):
    for user in users_list:
        if user['name'] == user_id:
            return True
    return False


def convert_to_pdf(file_name, extension, file_path, user_id):   # передали сообщение типа /djvu_to_pdf
    file_name = file_name.split('.' + extension)[0]
    convertapi.api_secret = config.CONVERT_API
    result = convertapi.convert('pdf', params={'File': config.PATH.format(token=config.TOKEN_BOT) + file_path,
                                               'FileName': file_name
                                               })
    # print(result.file.info)
    return result.file.url
