import requests
import threading
from queue import Queue


# 下载单个URL的函数
def download_url(url, filename):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # 如果请求失败，会抛出HTTPError异常
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        print(f"Downloaded {filename}")
    except Exception as e:
        print(f"Error downloading {url}: {e}")

    # 从队列中获取URL并下载的线程函数


def worker(queue, output_dir):
    while not queue.empty():
        url = queue.get()
        filename = f"{output_dir}/{url.split('/')[-1]}"  # 假设URL的最后一个部分是文件名
        download_url(url, filename+'.tar.gz')
        queue.task_done()  # 表示任务已完成


# 主函数
def main(url_file, output_dir, num_threads):
    if not output_dir.endswith('/'):
        output_dir += '/'

        # 读取URL文件并创建队列
    with open(url_file, 'r') as f:
        urls = f.readlines()
    url_queue = Queue()
    for url in urls:
        url_queue.put(url.strip())  # 去除URL字符串两端的空白字符

    # 创建并启动线程
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(url_queue, output_dir))
        thread.start()
        threads.append(thread)

        # 等待所有任务完成
    url_queue.join()

    # 等待所有线程结束
    for thread in threads:
        thread.join()

    print("All downloads completed.")


# 示例使用
url_file = '.txt'
output_dir = 'src'  # 确保此目录存在或代码中有创建目录的逻辑
num_threads = 10  # 根据你的机器和需要设置线程数
main(url_file, output_dir, num_threads)
