import logging
import requests
import utils


class HttpHandler:
    def __init__(self, config_data):
        self.config_data = config_data

    def make_api_call(self, data):
        response = None
        try:
            http = self.config_data[utils.PROPS_ENDPOINT]
        except KeyError:
            logging.error('configuration yaml is missing the\"' + utils.PROPS_ENDPOINT + '\"key')
            return
        if http is None or http['url'] is None:
            logging.error('End Point URL information not available to the configuration yml file')
            return
        url = http[utils.PROPS_URL]
        mime_type_json = 'application/json'
        content_type = 'Content-type'
        headers = {content_type: mime_type_json}
        try:
            response = requests.post(url, json=data, headers=headers)
        except (requests.exceptions.RequestException, Exception) as e:
            logging.error('Connection to endpoint failed %s\n' % e)
            return response

        if response.status_code != requests.codes.ok:
            logging.error('sending data to endpoint failed with status code %s due to %s ', response.status_code,
                          response.text)
        logging.debug('Success in sending the event to Endpoint')
        return response
