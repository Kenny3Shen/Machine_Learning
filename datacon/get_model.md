```python
import os
from bs4 import BeautifulSoup
import pandas as pd
from email import policy
from email.parser import BytesParser
import jieba
```

## 使用email库提取邮件内容
1. 读取eml文件
2. 提取邮件头
3. 提取邮件正文（不包括附件），注意到邮件正文可能是html格式或base64编码格式（图片），使用bs4库进行解析
4. 将邮件数据保存为DataFrame


```python
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

# dataset path
eml_dir = "D:\\notebook\datacon\dataset"

eml_files = [os.path.join(eml_dir, filename) for filename in os.listdir(eml_dir) if filename.endswith(".eml")]

data = [eml_to_dict(eml_file) for eml_file in eml_files]
df = pd.DataFrame(data)
```
    

## 查看数据集
- 4277条数据，包含630个字段
- 分析得知，邮件正文的内容在body字段中（若为空值通常表示正文为图片或其余非html格式）
- 邮件头中的Subject字段包含邮件主题
- 其余邮件头多数为空值或经过脱敏处理


```python
df
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Received</th>
      <th>X-Securemailgate-Identity</th>
      <th>Message-Id</th>
      <th>Subject</th>
      <th>Date</th>
      <th>X-Priority</th>
      <th>X-Mailer</th>
      <th>Mime-Version</th>
      <th>Content-Type</th>
      <th>X-Originating-Ip</th>
      <th>...</th>
      <th>X-Rm-Spam</th>
      <th>X-Hqip</th>
      <th>X-Sfdc-Lk</th>
      <th>X-Sfdc-User</th>
      <th>X-Mail_abuse_inquiries</th>
      <th>X-Sfdc-Tls-Norelay</th>
      <th>X-Sfdc-Binding</th>
      <th>X-Sfdc-Emailcategory</th>
      <th>X-Sfdc-Entityid</th>
      <th>X-Sfdc-Interface</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>from xsaypzzai (unknown [180.106.88.161])\t(us...</td>
      <td>dreyero_de;web277.dogado.net</td>
      <td>&lt;936e72d64105baa9a1dbe2640e6f5d81@dreyero.de&gt;</td>
      <td>2023年第一季度《财 政》补〉贴</td>
      <td>Mon, 13 Feb 2023 10:01:30 +0800</td>
      <td>3</td>
      <td>Cvzlvliqe Wydootqd 37.9</td>
      <td>1.0</td>
      <td>multipart/related; boundary="44b28501923df81c8...</td>
      <td>31.47.255.57</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>from mail.nfqwao.top (mail.nfqwao.top [94.131....</td>
      <td>NaN</td>
      <td>&lt;684317841.2471931.1676254079269@mail.nfqwao.top&gt;</td>
      <td>三八妇女节的礼品，准备好了吗？</td>
      <td>Mon, 13 Feb 2023 10:07:59 +0800</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>multipart/mixed; boundary="----=_Part_2471930_...</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>from zbyvlxgzm (unknown [49.85.250.111])\tby m...</td>
      <td>NaN</td>
      <td>&lt;91E13A01FF5D908B806E8253D52BCD1E@zbyvlxgzm&gt;</td>
      <td>邮箱系统在线升级</td>
      <td>Tue, 22 Aug 2023 01:33:46 +0800</td>
      <td>3</td>
      <td>Microsoft Outlook Express 6.00.2900.5512</td>
      <td>1.0</td>
      <td>multipart/alternative; boundary="----=_NextPar...</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>高薪工作提拔晋升户口出国轻松全搞定tianjinAD</td>
      <td>Mon, 13 Feb 2023 11:05:30 +0800</td>
      <td>2</td>
      <td>EhooPost 2004b</td>
      <td>NaN</td>
      <td>text/plain; charset="GB2312"</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>from josie (unknown [123.11.53.20])\t(Authenti...</td>
      <td>NaN</td>
      <td>&lt;63E9AA25.1B4E5E.14145@qn-cmmxproxy-4&gt;</td>
      <td>转发：  刘建华老师  收</td>
      <td>Mon, 13 Feb 2023 11:04:00 +0800</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>multipart/mixed; charset="UTF-8"; boundary="sa...</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4272</th>
      <td>from mail.cciy.top (mail.cciy.top [193.201.126...</td>
      <td>NaN</td>
      <td>&lt;1728955067.808585.1676254668606@mail.cciy.top&gt;</td>
      <td>三八妇女节！贵司完成礼品采购了吗？</td>
      <td>Mon, 13 Feb 2023 10:17:48 +0800</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>multipart/mixed; boundary="----=_Part_808584_3...</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4273</th>
      <td>from [115.219.6.56] (port=51513 helo=jutchefkw...</td>
      <td>NaN</td>
      <td>&lt;9d2eb98d929ff192aa4aa29a35fac9ef@sistemasimpl...</td>
      <td>个人劳动（补贴））已下发，请查看下图查收</td>
      <td>Mon, 13 Feb 2023 10:01:06 +0800</td>
      <td>3</td>
      <td>Ohbtef Bukgybuiiu 8.94</td>
      <td>1.0</td>
      <td>multipart/related; boundary="7cddf233ae28b4399...</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4274</th>
      <td>from tbq (unknown [180.108.236.38])\tby mail.i...</td>
      <td>NaN</td>
      <td>&lt;1FA8A33A5750EC0F102DAFC7825CDE4C@tbq&gt;</td>
      <td>邮箱系统在线升级</td>
      <td>Tue, 22 Aug 2023 13:05:50 +0800</td>
      <td>3</td>
      <td>Microsoft Outlook Express 6.00.2900.5512</td>
      <td>1.0</td>
      <td>multipart/alternative; boundary="----=_NextPar...</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4275</th>
      <td>from eeydxfmjnl (unknown [122.230.145.252])\tb...</td>
      <td>NaN</td>
      <td>&lt;5adc13a1db92fd10ed1eceb60dc7180c@luckymoonpac...</td>
      <td>2023年第一季度《财 政》补〉贴</td>
      <td>Mon, 13 Feb 2023 11:06:20 +0800</td>
      <td>3</td>
      <td>Jxczs Ohnhwu 12.78</td>
      <td>1.0</td>
      <td>multipart/related; boundary="3978b51d8dea23bcf...</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4276</th>
      <td>from DESKTOP-QRNFVRG (unknown [175.167.22.69])...</td>
      <td>NaN</td>
      <td>&lt;F8C0AA07-2CC4-4E97-A171-103C025C05B6@eos.ocn....</td>
      <td>DNA与RNA甲基化数据分析技术及应用</td>
      <td>Mon, 13 Feb 2023 10:52:06 +0800</td>
      <td>NaN</td>
      <td>MailMasterPC/4.18.1.1007 (Win10 21H2)</td>
      <td>1.0</td>
      <td>multipart/mixed; boundary="=_mailmaster-63e9a5...</td>
      <td>NaN</td>
      <td>...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>4277 rows × 630 columns</p>
</div>




```python
df.shape
```




    (4277, 630)



## 特征提取

- 提取邮件主题(Subject)和正文(body)内容
- 提取邮件名的前八位，方便具体分析
- Received 属性可能包含特征信息，但分析难度较大，故放弃  


```python
content = df[['email_id','Subject', 'body']]
```


```python
content
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>email_id</th>
      <th>Subject</th>
      <th>body</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>000249d6</td>
      <td>2023年第一季度《财 政》补〉贴</td>
      <td></td>
    </tr>
    <tr>
      <th>1</th>
      <td>0016a8f1</td>
      <td>三八妇女节的礼品，准备好了吗？</td>
      <td>Hello，你好1、我是为企业提供礼品采购的陈晓飞，如：商务伴手礼、节日礼品、活动礼品、员工...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>003804af</td>
      <td>邮箱系统在线升级</td>
      <td>亲爱的用户： \r\n为了加强网络安全管理，提高邮件系统的安全性和稳定性，保障收发畅通，为用...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0040c33b</td>
      <td>高薪工作提拔晋升户口出国轻松全搞定tianjinAD</td>
      <td>历经三年疫情洗礼，实业蓄能已久，人工智能AI技术WEB3.0, 区块链技术应用场景会越来越广...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>00493728</td>
      <td>转发：  刘建华老师  收</td>
      <td>您好！之前给您发过关于2月底将在线上开展 “表观遗传学-DNA甲基化 Rna甲基化 M6a甲...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4272</th>
      <td>ffc67ed7</td>
      <td>三八妇女节！贵司完成礼品采购了吗？</td>
      <td>Hello，你好﻿1、我是陈晓飞 Felix，为企业提供礼品采购的企业：商务馈赠、节日礼品、...</td>
    </tr>
    <tr>
      <th>4273</th>
      <td>ffcc00a4</td>
      <td>个人劳动（补贴））已下发，请查看下图查收</td>
      <td></td>
    </tr>
    <tr>
      <th>4274</th>
      <td>ffce9394</td>
      <td>邮箱系统在线升级</td>
      <td>亲爱的用户： \r\n为了加强网络安全管理，提高邮件系统的安全性和稳定性，保障收发畅通，为用...</td>
    </tr>
    <tr>
      <th>4275</th>
      <td>ffd7b406</td>
      <td>2023年第一季度《财 政》补〉贴</td>
      <td></td>
    </tr>
    <tr>
      <th>4276</th>
      <td>fffea489</td>
      <td>DNA与RNA甲基化数据分析技术及应用</td>
      <td>请老师查看附件\n        \n\n\n\n\n\n\n\n\ny-takabey-t...</td>
    </tr>
  </tbody>
</table>
<p>4277 rows × 3 columns</p>
</div>



## 特征分析
- 注意到邮件主题中包含了大量的空格、换行符、制表符等，需要进行清洗
- 注意到4277封邮件中只有878个独立主题，需要进行去重



```python
content.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>email_id</th>
      <th>Subject</th>
      <th>body</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>4277</td>
      <td>4277</td>
      <td>4277</td>
    </tr>
    <tr>
      <th>unique</th>
      <td>4277</td>
      <td>878</td>
      <td>1188</td>
    </tr>
    <tr>
      <th>top</th>
      <td>000249d6</td>
      <td>邮箱系统在线升级</td>
      <td></td>
    </tr>
    <tr>
      <th>freq</th>
      <td>1</td>
      <td>618</td>
      <td>856</td>
    </tr>
  </tbody>
</table>
</div>




```python
content.info()
```

    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 4277 entries, 0 to 4276
    Data columns (total 3 columns):
     #   Column    Non-Null Count  Dtype 
    ---  ------    --------------  ----- 
     0   email_id  4277 non-null   object
     1   Subject   4277 non-null   object
     2   body      4277 non-null   object
    dtypes: object(3)
    memory usage: 100.4+ KB
    

## 数据清洗
- 去除空格、换行符、制表符等
- 去除非UTF-8编码的字符
- 丢弃清洗后主题为空的邮件
- 去除重复邮件


```python
content['Subject'] = content['Subject'].str.replace(' ', '').str.replace('〉', '').str.replace('\n', '').str.replace('\r', '').str.replace('\t', '').str.replace('\xa0', ' ').str.replace('\ufeff', ' ').str.replace('◖','')
content['body'] = content['body'].str.replace('\n', '').str.replace('\r', '').str.replace('\t', '').str.replace('\xa0', ' ').str.replace('\ufeff', ' ')
content.drop(content.loc[content['Subject'] == ''].index, inplace=True)
content.drop_duplicates(subset=['Subject'], keep='first', inplace=True)
```

    C:\Users\Shen\AppData\Local\Temp\ipykernel_4452\3541818220.py:1: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      content['Subject'] = content['Subject'].str.replace(' ', '').str.replace('〉', '').str.replace('\n', '').str.replace('\r', '').str.replace('\t', '').str.replace('\xa0', ' ').str.replace('\ufeff', ' ').str.replace('◖','')
    C:\Users\Shen\AppData\Local\Temp\ipykernel_4452\3541818220.py:2: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      content['body'] = content['body'].str.replace('\n', '').str.replace('\r', '').str.replace('\t', '').str.replace('\xa0', ' ').str.replace('\ufeff', ' ')
    C:\Users\Shen\AppData\Local\Temp\ipykernel_4452\3541818220.py:3: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      content.drop(content.loc[content['Subject'] == ''].index, inplace=True)
    C:\Users\Shen\AppData\Local\Temp\ipykernel_4452\3541818220.py:4: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      content.drop_duplicates(subset=['Subject'], keep='first', inplace=True)
    

## 对清洗去除后的数据集分析
- 仅剩下863条数据
- 如第1条email（2023年第一季度《财政》补贴），正文内容为空，打开邮件观察得知，该邮件正文为图片，故正文为能正常解析，且为冒充政府机构的**钓鱼邮件**
- 如第3条email（邮箱系统在线升级），这一类邮件在之前分析中存在大量重复，打开邮件观察得知，该类邮件属于冒充邮箱管理员的**钓鱼邮件**


```python
content
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>email_id</th>
      <th>Subject</th>
      <th>body</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>000249d6</td>
      <td>2023年第一季度《财政》补贴</td>
      <td></td>
    </tr>
    <tr>
      <th>1</th>
      <td>0016a8f1</td>
      <td>三八妇女节的礼品，准备好了吗？</td>
      <td>Hello，你好1、我是为企业提供礼品采购的陈晓飞，如：商务伴手礼、节日礼品、活动礼品、员工...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>003804af</td>
      <td>邮箱系统在线升级</td>
      <td>亲爱的用户： 为了加强网络安全管理，提高邮件系统的安全性和稳定性，保障收发畅通，为用户提供优...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0040c33b</td>
      <td>高薪工作提拔晋升户口出国轻松全搞定tianjinAD</td>
      <td>历经三年疫情洗礼，实业蓄能已久，人工智能AI技术WEB3.0, 区块链技术应用场景会越来越广...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>00493728</td>
      <td>转发：刘建华老师收</td>
      <td>您好！之前给您发过关于2月底将在线上开展 “表观遗传学-DNA甲基化 Rna甲基化 M6a甲...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4243</th>
      <td>fe2242b6</td>
      <td>中国智造企业全球化人才吸引与发展新引擎—领英智能制造行业线上研讨会，期待您的免费上线观看！</td>
      <td>智能制造行业峰会 人才“智造”出海机遇赢在出海在线浏览请点击[1] 这里[2]智能制造行业峰...</td>
    </tr>
    <tr>
      <th>4253</th>
      <td>fee2719a</td>
      <td>DHLSHIPPINGDOCUMENT</td>
      <td>&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;Dear Customer, &gt;&gt;&gt;&gt; &gt;&gt;&gt;&gt;There is a...</td>
    </tr>
    <tr>
      <th>4254</th>
      <td>fef188cd</td>
      <td>RE:914790529、914704622帮忙通知厦门外代出具改单授权委托书[ref:_0...</td>
      <td>Dear 外代以下客户要求请协助帮忙，谢谢Regards,Derreck WuReprese...</td>
    </tr>
    <tr>
      <th>4266</th>
      <td>ff753c51</td>
      <td>報價請求：重慶INV212AS//114CN</td>
      <td>尊敬的先生/女士，請發送更新的價格列表，以進行新的新要求。 我們對購買非常感興趣。 如果您可...</td>
    </tr>
    <tr>
      <th>4268</th>
      <td>ff8e3cbe</td>
      <td>企业在做股权设计时必须注意哪些问题?</td>
      <td>老板是一家企业的核心灵魂人物，老板所具备的远见、前瞻性与决策往往牵连着企业的长远发展，所以老...</td>
    </tr>
  </tbody>
</table>
<p>863 rows × 3 columns</p>
</div>



## 自动化标注
- 通过观察，发现钓鱼邮件的特征为：邮件主题中包含“薪资、工资、财政、补助、补贴、津贴、邮箱、邮件、及时、系统、通告、警告、抵扣、增值、税务”等词汇，正文中包含“郵箱、系統、money”等词汇
- 通过正则表达式进行匹配，将钓鱼邮件标记为1，其余邮件标记为0
- 新增属性class，表示对此封邮件的分类标注



```python
a = content['Subject'].apply(lambda x: 1 if any(word in x for word in ['薪资','工资','财政','补助','补贴','津贴','邮箱','邮件','及时','系统','通告', '警告','抵扣','增值','税务']) else 0)
b =content['body'].apply(lambda x: 1 if any(word in x for word in ['郵箱','系統','money']) else 0)
content['class'] = a | b
```

    C:\Users\Shen\AppData\Local\Temp\ipykernel_4452\2815912577.py:3: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      content['class'] = a | b
    


```python
content['class'].value_counts()
```




    0    622
    1    241
    Name: class, dtype: int64



## 空值处理
- 由于部分正文内容为空，这里采用一种简单的空值处理办法
- 将主题与正文内容合并为Message
- 提取Message和class两列，作为需要学习的数据


```python
content['Message'] = content['Subject'] + ' ' + content['body']
```

    C:\Users\Shen\AppData\Local\Temp\ipykernel_4452\2827404937.py:1: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      content['Message'] = content['Subject'] + ' ' + content['body']
    


```python
data = content[['Message', 'class']]
```


```python
data.to_csv('D:\\notebook\datacon\data.csv', index=False)
data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Message</th>
      <th>class</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2023年第一季度《财政》补贴</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>三八妇女节的礼品，准备好了吗？ Hello，你好1、我是为企业提供礼品采购的陈晓飞，如：商务...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>邮箱系统在线升级 亲爱的用户： 为了加强网络安全管理，提高邮件系统的安全性和稳定性，保障收发...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>高薪工作提拔晋升户口出国轻松全搞定tianjinAD 历经三年疫情洗礼，实业蓄能已久，人工智...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>转发：刘建华老师收 您好！之前给您发过关于2月底将在线上开展 “表观遗传学-DNA甲基化 R...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4243</th>
      <td>中国智造企业全球化人才吸引与发展新引擎—领英智能制造行业线上研讨会，期待您的免费上线观看！ ...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4253</th>
      <td>DHLSHIPPINGDOCUMENT &gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;&gt;Dear Customer,...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4254</th>
      <td>RE:914790529、914704622帮忙通知厦门外代出具改单授权委托书[ref:_0...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4266</th>
      <td>報價請求：重慶INV212AS//114CN 尊敬的先生/女士，請發送更新的價格列表，以進行...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4268</th>
      <td>企业在做股权设计时必须注意哪些问题? 老板是一家企业的核心灵魂人物，老板所具备的远见、前瞻性...</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>863 rows × 2 columns</p>
</div>



## 分词
- 英文天然具有分词属性，中文则需要进行分词
- 由于邮件主题和正文内容绝大数为中文，这里采用jieba库进行分词
- 分词有助于特征提取，提高分类准确率


```python
data['Message'] = data['Message'].apply(lambda x: ' '.join(jieba.cut(x)))
```

    Building prefix dict from the default dictionary ...
    Loading model from cache C:\Users\Shen\AppData\Local\Temp\jieba.cache
    Loading model cost 0.769 seconds.
    Prefix dict has been built successfully.
    C:\Users\Shen\AppData\Local\Temp\ipykernel_4452\2702886797.py:1: SettingWithCopyWarning: 
    A value is trying to be set on a copy of a slice from a DataFrame.
    Try using .loc[row_indexer,col_indexer] = value instead
    
    See the caveats in the documentation: https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#returning-a-view-versus-a-copy
      data['Message'] = data['Message'].apply(lambda x: ' '.join(jieba.cut(x)))
    


```python
data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Message</th>
      <th>class</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2023 年 第一季度 《 财政 》 补贴</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1</th>
      <td>三八妇女节 的 礼品 ， 准备 好了吗 ？   Hello ， 你好 1 、 我 是 为 企...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>邮箱 系统 在线 升级   亲爱 的 用户 ：   为了 加强 网络安全 管理 ， 提高 邮...</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3</th>
      <td>高薪 工作 提拔 晋升 户口 出国 轻松 全 搞定 tianjinAD   历经 三年 疫情...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>转发 ： 刘建华 老师 收   您好 ！ 之前 给 您 发过 关于 2 月底 将 在线 上 ...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>4243</th>
      <td>中国 智造 企业 全球化 人才 吸引 与 发展 新 引擎 — 领英 智能 制造 行业 线上 ...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4253</th>
      <td>DHLSHIPPINGDOCUMENT   &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; &gt; ...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4254</th>
      <td>RE : 914790529 、 914704622 帮忙 通知 厦门 外代 出具 改单 授...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4266</th>
      <td>報價 請求 ： 重慶 INV212AS / / 114CN   尊敬 的 先生 / 女士 ，...</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4268</th>
      <td>企业 在 做 股权 设计 时 必须 注意 哪些 问题 ?   老板 是 一家 企业 的 核心...</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>863 rows × 2 columns</p>
</div>



## 模型设计
- 使用sklearn库进行模型设计以及数据集划分
- 采用Pipeline进行数据预处理
- 采用朴素贝叶斯分类器(Native Bayes)进行分类
- 采用CountVectorizer进行特征提取

### 基本思想
1. 学习不同分类的邮件的特征
2. 基于特征出现的概率，对邮件进行分类，如：某封邮件的Message若同时出现“邮箱”、“系统”、“升级”、“密码”等特征词时，该邮件属于钓鱼邮件的概率较大，故将其分类为钓鱼邮件
3. 朴素贝叶斯分类器的基本思想是：假设特征之间相互独立，即某封邮件的Message若同时出现“邮箱”、“系统”、“升级”、“密码”等特征词时，这些特征词之间相互独立，不会相互影响，但这也缺乏对整体邮件内容的相关性分析


```python
from sklearn.model_selection import train_test_split
X_train,X_test,y_train,y_test=train_test_split(data['Message'],data['class'],test_size=0.25)
```


```python
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
clf=Pipeline([
    ('vectorizer',CountVectorizer()),
    ('nb',MultinomialNB())
])
```


```python
clf.fit(X_train,y_train)
```




<style>#sk-container-id-1 {color: black;}#sk-container-id-1 pre{padding: 0;}#sk-container-id-1 div.sk-toggleable {background-color: white;}#sk-container-id-1 label.sk-toggleable__label {cursor: pointer;display: block;width: 100%;margin-bottom: 0;padding: 0.3em;box-sizing: border-box;text-align: center;}#sk-container-id-1 label.sk-toggleable__label-arrow:before {content: "▸";float: left;margin-right: 0.25em;color: #696969;}#sk-container-id-1 label.sk-toggleable__label-arrow:hover:before {color: black;}#sk-container-id-1 div.sk-estimator:hover label.sk-toggleable__label-arrow:before {color: black;}#sk-container-id-1 div.sk-toggleable__content {max-height: 0;max-width: 0;overflow: hidden;text-align: left;background-color: #f0f8ff;}#sk-container-id-1 div.sk-toggleable__content pre {margin: 0.2em;color: black;border-radius: 0.25em;background-color: #f0f8ff;}#sk-container-id-1 input.sk-toggleable__control:checked~div.sk-toggleable__content {max-height: 200px;max-width: 100%;overflow: auto;}#sk-container-id-1 input.sk-toggleable__control:checked~label.sk-toggleable__label-arrow:before {content: "▾";}#sk-container-id-1 div.sk-estimator input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 div.sk-label input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 input.sk-hidden--visually {border: 0;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);height: 1px;margin: -1px;overflow: hidden;padding: 0;position: absolute;width: 1px;}#sk-container-id-1 div.sk-estimator {font-family: monospace;background-color: #f0f8ff;border: 1px dotted black;border-radius: 0.25em;box-sizing: border-box;margin-bottom: 0.5em;}#sk-container-id-1 div.sk-estimator:hover {background-color: #d4ebff;}#sk-container-id-1 div.sk-parallel-item::after {content: "";width: 100%;border-bottom: 1px solid gray;flex-grow: 1;}#sk-container-id-1 div.sk-label:hover label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 div.sk-serial::before {content: "";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: 0;}#sk-container-id-1 div.sk-serial {display: flex;flex-direction: column;align-items: center;background-color: white;padding-right: 0.2em;padding-left: 0.2em;position: relative;}#sk-container-id-1 div.sk-item {position: relative;z-index: 1;}#sk-container-id-1 div.sk-parallel {display: flex;align-items: stretch;justify-content: center;background-color: white;position: relative;}#sk-container-id-1 div.sk-item::before, #sk-container-id-1 div.sk-parallel-item::before {content: "";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: -1;}#sk-container-id-1 div.sk-parallel-item {display: flex;flex-direction: column;z-index: 1;position: relative;background-color: white;}#sk-container-id-1 div.sk-parallel-item:first-child::after {align-self: flex-end;width: 50%;}#sk-container-id-1 div.sk-parallel-item:last-child::after {align-self: flex-start;width: 50%;}#sk-container-id-1 div.sk-parallel-item:only-child::after {width: 0;}#sk-container-id-1 div.sk-dashed-wrapped {border: 1px dashed gray;margin: 0 0.4em 0.5em 0.4em;box-sizing: border-box;padding-bottom: 0.4em;background-color: white;}#sk-container-id-1 div.sk-label label {font-family: monospace;font-weight: bold;display: inline-block;line-height: 1.2em;}#sk-container-id-1 div.sk-label-container {text-align: center;}#sk-container-id-1 div.sk-container {/* jupyter's `normalize.less` sets `[hidden] { display: none; }` but bootstrap.min.css set `[hidden] { display: none !important; }` so we also need the `!important` here to be able to override the default hidden behavior on the sphinx rendered scikit-learn.org. See: https://github.com/scikit-learn/scikit-learn/issues/21755 */display: inline-block !important;position: relative;}#sk-container-id-1 div.sk-text-repr-fallback {display: none;}</style><div id="sk-container-id-1" class="sk-top-container"><div class="sk-text-repr-fallback"><pre>Pipeline(steps=[(&#x27;vectorizer&#x27;, CountVectorizer()), (&#x27;nb&#x27;, MultinomialNB())])</pre><b>In a Jupyter environment, please rerun this cell to show the HTML representation or trust the notebook. <br />On GitHub, the HTML representation is unable to render, please try loading this page with nbviewer.org.</b></div><div class="sk-container" hidden><div class="sk-item sk-dashed-wrapped"><div class="sk-label-container"><div class="sk-label sk-toggleable"><input class="sk-toggleable__control sk-hidden--visually" id="sk-estimator-id-1" type="checkbox" ><label for="sk-estimator-id-1" class="sk-toggleable__label sk-toggleable__label-arrow">Pipeline</label><div class="sk-toggleable__content"><pre>Pipeline(steps=[(&#x27;vectorizer&#x27;, CountVectorizer()), (&#x27;nb&#x27;, MultinomialNB())])</pre></div></div></div><div class="sk-serial"><div class="sk-item"><div class="sk-estimator sk-toggleable"><input class="sk-toggleable__control sk-hidden--visually" id="sk-estimator-id-2" type="checkbox" ><label for="sk-estimator-id-2" class="sk-toggleable__label sk-toggleable__label-arrow">CountVectorizer</label><div class="sk-toggleable__content"><pre>CountVectorizer()</pre></div></div></div><div class="sk-item"><div class="sk-estimator sk-toggleable"><input class="sk-toggleable__control sk-hidden--visually" id="sk-estimator-id-3" type="checkbox" ><label for="sk-estimator-id-3" class="sk-toggleable__label sk-toggleable__label-arrow">MultinomialNB</label><div class="sk-toggleable__content"><pre>MultinomialNB()</pre></div></div></div></div></div></div></div>



## 模型验证
- 对单独数据的验证
- 对测试集的验证，准确率为98%


```python
emails=['''CraftBeerChina2023|亞洲國際精釀啤酒會議暨展覽會|2023.5.30~6.1|14.2億的人口市場等您來開發|疫後商機等您來開發!!!'''
    ,'''你好，本公司有增值税（票），代开全国各地类发票发票真实有效，网上可验证，点数优惠，绝对保真可线下取票/邮寄取票，联系徽信：131-2259-9416（电)  sh在仍处于阴影中的山谷草地上卵酣炮除朵锋摇寅炎厘眉支征低化箕sh@peony.cn'''
    ,'''邮箱OA更新各位公司同事，您好！正在OA系统更新,没有进行OA系统更新的用户三天后将无法使用。您当前的IMAP版本较低，建议立即升级点击进行OA更新小贴士：IMAP属于同步协议，您在移动端或MAC端需要正常使用，请在2023-2-20前完成OA系统更新！SESSIONID:MentAQAAAGaX6WMFLAAAIP:59.125.11.37ClientPort:25HASIPINFO:0...''',
    '''E-mail郵箱系統計劃於即日起開始進行遷移升級請如實填寫下列信息，回復此郵件！姓名：職位：郵箱賬號：登陸密碼：歷史密碼：註：請在收到郵件後立即進行回復，逾時將被回收賬號！d9rnfdh2   কমিশনের অফিস সহকারী/ডাটা এন্ট্রি অপারেটর জনাব মোঃ তহিদুল ইসলাম এর পাসপোর্ট অনাপত্তি সনদকমিশনের অফিস...
    ''',
    '''
    2023年第一季度《财政》补贴
    ''',
    '''高薪工作提拔晋升户口出国轻松全搞定tianjinAD 历经三年疫情洗礼，实业蓄能已久，人工智能AI技术WEB3.0, 区块链技术应用场景会越来越广泛，作为各类大企业需要新型人才的若你，将更加需要专业高端学历的加持，增强核心竞争力的砝码！如果你有能力缺平台 ，那么我们可以让你实现职场质的跨越！学信网全网独家的学历学位大数据融合平台（BDP  big  data platform  ,data...''',
    '''做账抵扣冲账'''
]
emails = [' '.join(jieba.cut(email)) for email in emails]
```


```python
clf.predict(emails)
```




    array([1, 1, 1, 1, 1, 0, 1], dtype=int64)




```python
clf.score(X_test,y_test)
```




    0.9814814814814815



## 查看测试集预测结果


```python
y_pred = clf.predict(X_test)

# Create a DataFrame with actual and predicted values
results = pd.DataFrame({
    'Message': X_test,
    'Actual': y_test,
    'Predicted': y_pred
})
results
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Message</th>
      <th>Actual</th>
      <th>Predicted</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>510</th>
      <td>回复 ： 流程 变革 （ 2 月 23 - 26 日 深圳 ）   您好 ！        ...</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>397</th>
      <td>测量 技术 的 趋势 与 创新   View   online   version     ...</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1505</th>
      <td>2023 - 02 - 13 日 通告 ： qwsun</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>3156</th>
      <td>2023 - 02 - 13 日 通告 ： huangqiongrui</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>672</th>
      <td>2023 - 02 - 13 日 通告 ： songxinjie</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>493</th>
      <td>RE ：   Untitled   document 您好 ， 抱歉 打扰 了 。 如果 您...</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2249</th>
      <td>2023 - 02 - 13 日 通告 ： huanghui5</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1895</th>
      <td>2023 - 02 - 13 日 通告 ： 13110240014</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>1518</th>
      <td>2023 - 02 - 13 日 通告 ： xfli</td>
      <td>1</td>
      <td>1</td>
    </tr>
    <tr>
      <th>4</th>
      <td>转发 ： 刘建华 老师 收   您好 ！ 之前 给 您 发过 关于 2 月底 将 在线 上 ...</td>
      <td>0</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
<p>216 rows × 3 columns</p>
</div>



## 模型保存


```python
from joblib import dump
dump(clf, 'email_predict.joblib') 
```




    ['email_predict.joblib']

## 预测流程
1. 查找 "\mail" 文件夹下所有 eml 文件路径
2. 逐条读取 eml 文件内容 
    - 提取Subject和body，进行数据预处理
    - 合并为Message，进行分词
    - 使用模型进行预测
    - 注意到存在一些与“开发票”相关的钓鱼邮件，使用正则表达式进行匹配，将其分类为1
3. 将预测结果写入 "\answer.txt"文件

```python
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
```