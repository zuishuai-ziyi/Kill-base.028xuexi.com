from concurrent.futures import ThreadPoolExecutor
import time, typing

class Default(type):
    '''默认值'''
    def __new__(cls):
        raise TypeError("Default cannot be instantiated")


def add_many_thread(task_list:list[object], thread_quantity:int=1, full_task:int|object=-1, max_workers:typing.Type[Default]|int = Default, thread_name_format:Default = Default): # type: ignore
    '''
    创建线程

    Parameters:
        task_list(list[function]): 任务列表，包含每个线程需执行的任务
        thread_quantity(int): 线程总数
        full_task(function | int): 填充任务，若有线程无对应任务，则使用该任务
                                   若为 int，则在 task_list 中选择对应下标的任务，默认为 -1
        max_workers(Default | int):最大线程并发数，默认为Default，即不限制并发数
        thread_name_format(Default | int): 线程名函数，用于获取线程名
                                           该函数应接受一个参数（当前线程编号），返回一个唯一字符串作为线程名
                                           若未提供，则使用 "task-i" 格式字符串作为线程名（i为线程编号）

    Returns:
        out(dict):
            get result(function -> Any): 用于获取特定名称任务的返回值，留空以获取所有任务的返回值\n
            spend time(float): 该函数的总耗时（包括线程执行任务耗时）
    '''
    # 设置参数默认值
    if isinstance(full_task, int):
        full_task = task_list[full_task]
    if thread_name_format is Default:
        thread_name_format = lambda i: f'task-{i}'
    # 补足任务
    task_list += [full_task for i in range(0, thread_quantity) if len(task_list)<i+1]
    # 补齐最大线程并行数量
    if max_workers is Default:
        max_workers: int = thread_quantity
    start_time = time.time()
    # 创建线程池
    with ThreadPoolExecutor(max_workers=max_workers) as executor: # type: ignore
        # 提交线程任务
        result_dict = {thread_name_format(i): executor.submit(task_list[i], thread_name_format(i)) for i in range(0, thread_quantity)} # type: ignore
    def get_result(name:typing.Type[Default]|str = Default) -> typing.Any:
        '''获取特定名称任务的返回值'''
        if name is Default:
            return [n.result() for n in result_dict.values()]
        else:
            return None if (res := result_dict.get(name, None)) is None else res.result()

    return {'get result':get_result, 'spend time':time.time()-start_time}

if __name__ == '__main__':
    # 定义线程任务
    def thread_task(name):
        print(f"{name} 开始运行")
        for i in range(1, 51):
            time.sleep(0.1)
            print(f'{name}：正在进行步骤{i}')
        return f"{name} return value"
    def return_(name):
        print(f"{name} 开始运行")
        return f"{name} return value"
    def return_None(name):
        return
    r = add_many_thread([thread_task, return_], 100)
    print(r)
    print(r['get result']())
