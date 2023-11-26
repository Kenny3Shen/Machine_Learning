import glob
from joblib import load
import os
from bs4 import BeautifulSoup
from email import policy
from email.parser import BytesParser
import pandas as pd
import jieba


def get_body(message):
    if message.is_multipart():
        return get_body(message.get_payload(0))
    else:
        return message.get_payload(None, True)


def eml_to_dict(eml_path):
    with open(eml_path, 'rb') as f:
        msg = BytesParser(policy=policy.default).parse(f)

    # get headers
    data = dict(msg.items())

    # get body
    body = get_body(msg)
    if body is not None:
        try:
            data['body'] = body.get_content()
        except AttributeError:
            data['body'] = body
        # get text from html
        data['body'] = BeautifulSoup(data['body'], "html.parser").text.strip()
    data['email_id'] = os.path.basename(eml_path).split('.')[0]
    return data


if __name__ == '__main__':
    # load model
    clf = load('/source/email_predict.joblib')
    eml_files = glob.glob('/mail/*.eml')
    print(f"Found {len(eml_files)} files:")
    with open('/answer.txt', 'w') as ans:
        for eml_file in eml_files:
            try:
                data = eml_to_dict(eml_file)
                data['Subject'] = data['Subject'].replace(' ', '').replace('〉', '').replace('\n', '').replace('\r', '').replace('\t', '').replace('\xa0', ' ').replace('\ufeff', ' ').replace('◖','')
                data['body'] = data['body'].replace('\n', '').replace('\r', '').replace('\t', '').replace('\xa0', ' ').replace('\ufeff', ' ')
                message = ' '.join(jieba.cut(data['Subject'] + ' ' + data['body']))
                predict = clf.predict([message])
                if any(s in data['Subject'] for s in ['嘌','瞟','缥','飘','漂']):
                    predict = [1]
                ans.write(str(data['email_id']) + ',' + str(predict[0]) + '\n')
            except Exception as e:
                print(e)
                print("Error:", eml_file)
                ans.write(str(os.path.basename(eml_file).split('.')[0]) + ',' + '0' + '\n')
                continue