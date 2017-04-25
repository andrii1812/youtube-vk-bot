import requests
import vk


def auth(config):
    session = vk.AuthSession(config['app_id'], config['user_login'], config['user_password'], scope='video')
    api = vk.API(session)
    return api


def get_upload_data(api, video_name):
    return api.video.save(name=video_name, privacy_view=3, privacy_comment=3)


def compose_url(upload_data):
    return 'https://vk.com/video{0}_{1}'.format(upload_data['owner_id'], upload_data['vid'])


def upload_video(api, path, video_name):
    upload_data = get_upload_data(api, video_name)
    upload_url = upload_data['upload_url']

    stream = open(path, 'rb')
    payload = {
        'video_file': stream
    }
    requests.post(upload_url, files=payload)

    return compose_url(upload_data)