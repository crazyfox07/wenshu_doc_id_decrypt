import execjs
import re

from aes_decrypt import aes_decode

def py_execjs(js='',file_='aes.js'):
    node = execjs.get()
    content=open(file_,encoding='utf-8',errors='ignore').read()
    ctx = node.compile(content)
    result = ctx.eval(js)
    return result


def get_b64_data_unzip(str_):
    js_func = 'unzip("{}")'.format(str_)
    b64_data = py_execjs(js=js_func, file_='b64_unzip.js')
    return b64_data

# 获取aes的key
def get_aes_key(str_):
    b64_data_unzip = get_b64_data_unzip(str_)
    str1, str2 = re.findall('\$hidescript=(.*?);.*?\((.*?)\)\(\)',b64_data_unzip)[0]
    js_func = str2.replace('$hidescript',str1)
    aes_key = py_execjs(js=js_func, file_='aes.js')
    aes_key = re.findall('com.str._KEY=\"(.*?)\";',aes_key)[0]
    return aes_key

# aes解密
def aes_decrypt(str_, aes_key):
    js_func = 'DecryptInner("{}")'.format(str_)
    # 获取加密过的文本
    text_encrypted = py_execjs(js=js_func, file_='aes.js')
    # aes解密
    text_decode = aes_decode(text_encrypted, aes_key)
    return text_decode

# 程序运行入口，解密"文书ID"
def doc_id_decyrpt(run_eval, doc_id_src):
    # 通过"RunEval" 解密aes的key, iv为常量'abcd134556abcedf'
    aes_key = get_aes_key(run_eval)
    # 文书id预处理
    doc_id__b64_unzip = get_b64_data_unzip(doc_id_src)
    # 连续两次aes解密
    result1 = aes_decrypt(doc_id__b64_unzip, aes_key)
    result2 = aes_decrypt(result1, aes_key)
    return result2

if __name__ == '__main__':
    # "RunEval"
    run_eval = 'w61ZS27CgzAQPQtRFsK2wqh6AcKUVcKOw5DDpcOIQhFJGhYNwpVDV1HDrl4gCcOlY37DgRA3fhIawoQ9wr/Dt8OGY8KwWB7DgsOtw64Uw4jDsDtefcOEMjx+wr7Dr2XDtMK1PmzDpDrDmsOuwpjDq8K4JCDCjBZvIAHDgsKOFcOyCkAsaVfDrErCqC0EeAfCsxDCqB4YQ3FBB0gAagAGE2AHw7hBDHgCOEBCBSDCsBBMEcOcw7PDvMOVIsKIwo7Cp1jDvgRxJBfCnk/Cvkguw4bDnMOzJVXDi8Kvw7PChcOTw5XCkhIhwoTDi8KcbMKCU8OZZzrDkT3Ckz0uw79+RxNLwocTDXLDkhkSwpTDnCoBw4vDqsOOw43CoDlYJW/CpW5rTkVvw6rDsTxUwpZ1wp3ColoKSgwtwr7DsyTDuzFaeMOsTMK7wqfDhhDCtcOBwrrCjxnCjMKwGmvCqsOFXsKfE8ONwp7CpnBXw67DhntjwqvDu8O0w4FRw6PDocOfwrMfw5jCnMKvwrHCqGzDgcO5woTCmk/CncK8PsKSwpvDm1/Di1bDmsO4AsKuwrA/fQfDjlrCocK5QkwbwqfDrSPDjsK8wq1jLsK6wrvCg8ONwprDicK/X2o2w7s0N8OsLXZ9wp/DrnEoM8KIG8OFw4nCqwbCiUpvQMO1aMORIcKNODs+wp0yW8KzEMKcccOvFw=='
    doc_id_src = 'DcKNwrcNw4BADMOEVlLClsK+VMOcfyTDuwrDogAWwpQKXxtEw7LChhYWwoAGw5DCggzCrcKFwpnCl8KjwrB3woDCg2cyRMKUw5xZSnXClA7CnmQGL8KeRXDCmcO+L3bCmmFJQ3cWwofDnXPDolLDkWIUGcOewqbDvcOiJcOCFmEywpTCs8O3EsKUwqBHRcOfwrEww7rDgcODw77Ct8OPw7p+wqvDjEJPw7LDtMOvGsKYw7Qwwp7DqHUzWcOVw43DuxFvBcOkbx3DjQc='
    result = doc_id_decyrpt(run_eval, doc_id_src)
    print(result)