# from server.config import project_id, stage
import dialogflow_v2 as dialogflow
from google.protobuf.json_format import MessageToDict
import os

dirpath = os.path.dirname(os.path.realpath(__file__))


key_files = {
    '2019123456001': dirpath + '/' + '/telle-ai-demo-do-not-change-ww-183694ce7fe8.json',
    '2019123456002': dirpath + '/' + 'telle-ai-dev-rdgebu-64f1c788f7c9.json',
    '2019123456003': dirpath + '/' + 'nissan-dev-lfyhff-ad49980c10f4.json',
    '2019123456004': dirpath + '/' + 'infiniti-dev-ndlngp-4d01d54c2b61.json',
    '2019123456005': dirpath + '/' + 'toyota-dev-yrimbi-8bfcc21f6fef.json',
    '2019123456006': dirpath + '/' + 'kia-dev-upyddx-8642b466f659.json',
    '2019123456007': dirpath + '/' + 'hyundai-dev-dgqwci-efce5d197fb9.json',
    '2019123456008': dirpath + '/' + 'cadillac-dev-bbbbrq-69749d2b44d4.json',
    '2019123456009': dirpath + '/' + 'chevrolet-dev-mcxoio-66d052fe29ea.json',

    '201978945125001': dirpath + '/' + 'nissan-dev-lfyhff-ad49980c10f4.json',
    '201978945125002': dirpath + '/' + 'infiniti-dev-ndlngp-4d01d54c2b61.json',
    '201978945124789': dirpath + '/' + 'honda-dev-hpdbal-77db5e37f8d6.json',
    '201979145126001': dirpath + '/' + 'toyota-dev-yrimbi-8bfcc21f6fef.json',
    '201979145126002': dirpath + '/' + 'kia-dev-upyddx-8642b466f659.json',
    '201979145126003': dirpath + '/' + 'hyundai-dev-dgqwci-efce5d197fb9.json',
    '201979145126004': dirpath + '/' + 'cadillac-dev-bbbbrq-69749d2b44d4.json',
    '201979145126005': dirpath + '/' + 'chevrolet-dev-mcxoio-66d052fe29ea.json',

    '101978945125001': dirpath + '/' + 'nissan-dev-lfyhff-ad49980c10f4.json',
    '101978945125002': dirpath + '/' + 'infiniti-dev-ndlngp-4d01d54c2b61.json',
    '101978945124789': dirpath + '/' + 'honda-dev-hpdbal-77db5e37f8d6.json',
    '101979145126001': dirpath + '/' + 'toyota-dev-yrimbi-8bfcc21f6fef.json',
    '101979145126002': dirpath + '/' + 'kia-dev-upyddx-8642b466f659.json',
    '101979145126003': dirpath + '/' + 'hyundai-dev-dgqwci-efce5d197fb9.json',
    '101979145126004': dirpath + '/' + 'cadillac-dev-bbbbrq-69749d2b44d4.json',
    '101979145126005': dirpath + '/' + 'chevrolet-dev-mcxoio-66d052fe29ea.json'
}

project_ids = {
    '2019123456001': 'telle-ai-demo-do-not-change-ww',
    '2019123456002': 'telle-ai-dev-rdgebu',
    '2019123456003': 'nissan-dev-lfyhff',
    '2019123456004': 'infiniti-dev-ndlngp',
    '2019123456005': 'toyota-dev-yrimbi',
    '2019123456006': 'kia-dev-upyddx',
    '2019123456007': 'hyundai-dev-dgqwci',
    '2019123456008': 'cadillac-dev-bbbbrq',
    '2019123456009': 'chevrolet-dev-mcxoio',

    '201978945125001': 'nissan-dev-lfyhff',
    '201978945125002': 'infiniti-dev-ndlngp',
    '201978945124789': 'honda-dev-hpdbal',
    '201979145126001': 'toyota-dev-yrimbi',
    '201979145126002': 'kia-dev-upyddx',
    '201979145126003': 'hyundai-dev-dgqwci',
    '201979145126004': 'cadillac-dev-bbbbrq',
    '201979145126005': 'chevrolet-dev-mcxoio',

    '101978945125001': 'nissan-dev-lfyhff',
    '101978945125002': 'infiniti-dev-ndlngp',
    '101978945124789': 'honda-dev-hpdbal',
    '101979145126001': 'toyota-dev-yrimbi',
    '101979145126002': 'kia-dev-upyddx',
    '101979145126003': 'hyundai-dev-dgqwci',
    '101979145126004': 'cadillac-dev-bbbbrq',
    '101979145126005': 'chevrolet-dev-mcxoio'
}


def detect_intent_texts(dealer_id, group_id, message):
    try:
        # print(message)
        message_dict = message
        # add dealer id to sid to separate the message origin
        sid = '{0}_{1}'.format(dealer_id, group_id)

        texts = [message_dict['data']['text']]
        language_code = message_dict.get('language_code', 'en-US')

        google_key_file = key_files.get(dealer_id)
        project_id = project_ids.get(dealer_id)

        session_client = dialogflow.SessionsClient.from_service_account_json(google_key_file)

        session = session_client.session_path(project_id, sid)

        for text in texts:
            text_input = dialogflow.types.TextInput(
                text=text, language_code=language_code)

            query_input = dialogflow.types.QueryInput(text=text_input)

            response = session_client.detect_intent(
                session=session, query_input=query_input)

            response_dict = MessageToDict(response)

            messages = response_dict['queryResult'].get('fulfillmentMessages')

            # print(messages)
            return messages
    except Exception as e:
        raise e
