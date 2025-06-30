# URL配置文件
# 包含用于API压力测试的图片URL列表

URL_LIST = [
    "https://cdn.deepseek.com/logo.png?x-image-process=image%2Fresize%2Cw_828",
    "https://ebui-cdn.cdn.bcebos.com/i18n/zh/layout/yiyan-logo.png",
    "https://gips2.baidu.com/it/u=3128910097,202208282&fm=3030&app=3030&size=re3,2&q=75&n=0&g=4n&f=JPEG&fmt=auto&maxorilen2heic=2000000?s=39843C7AED256A1359D5F4D60000D0B1",
    "https://t9.baidu.com/it/u=583269603,2071876283&fm=217&app=126&size=re3,2&q=75&n=0&g=4n&f=JPEG&fmt=auto&maxorilen2heic=2000000?s=082B5D30151A45CA14D8ECC80100A0B3",
    "https://senseflow-test.sensetime.com/app/create.png",
    "https://senseflow-test.sensetime.com/files/92255965-3e73-483e-8b86-7b893e021c6f/image-compress?timestamp=1749707296&nonce=63ea42b3609e550aecdcd0ec2f1f07a9&sign=MxRu76gsPQNgzYF_eGD3_d_DNUtj4sJocbLfDMz5I_U=",
    "https://senseflow-test.sensetime.com/files/30a7736c-34d0-43d8-be7b-5b1b082391db/image-compress?timestamp=1749707296&nonce=df4623eeb04af1c1cc9343148a56e972&sign=joWHGgfsJt1VRMiMaceO-E5rh61P81vpBm5_tcTrj8s=",
    "https://senseflow-test.sensetime.com/_next/static/media/cover.eacfe46b.png",
    "https://senseflow-test.sensetime.com/files/65a9e41c-2535-4fa3-ac7d-dc3cdde10e64/image-compress?timestamp=1749707388&nonce=f42a2f2b4d859770d2bbc22c441c70e3&sign=HSy2qRHRKKCBwOytsMjx7CRBQ97ZH0CFhmwq1DYg8ks=",
    "https://senseflow-test.sensetime.com/files/51f7482d-9799-44c2-b6a8-7dbf4ce7c738/image-compress?timestamp=1749707388&nonce=e1174bdd5e9ffe21d65048b71c61bd8b&sign=rjMaccxIgJ9LS_wcxIz6FxLRjueZOqQAdD3-sD_Fm8A=",
    "https://senseflow-test.sensetime.com/files/895d2e37-1300-4e7f-a50f-131c0feb2573/image-compress?timestamp=1749707388&nonce=561ec6eaf28026b47c4fe7e4c1f79459&sign=b3ci8FWahEb4snXjXAW9WnZIVyzNKANO4cEWDkZ8V5g=",
    "https://senseflow-test.sensetime.com/files/c3b58b1e-09c9-4899-9432-5a295170bb52/image-compress?timestamp=1749707388&nonce=1d723e6e45dd04a77255ba08c917f380&sign=alWbJuRHOUrtZ1jDs__X_kPtmSS8eYFUtXZd44_2Zdg=",
    "https://himg.bdimg.com/sys/portraitn/item/public.1.608673a6.WTT27DaQtwuPUvUeUHaFKQ?_d=29161787"
]

def get_url_list():
    """获取URL列表"""
    return URL_LIST

def add_url(url):
    """添加新的URL到列表中"""
    if url not in URL_LIST:
        URL_LIST.append(url)
        return True
    return False

def remove_url(url):
    """从列表中移除URL"""
    if url in URL_LIST:
        URL_LIST.remove(url)
        return True
    return False

def get_url_count():
    """获取URL列表的长度"""
    return len(URL_LIST) 