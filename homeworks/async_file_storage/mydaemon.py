import argparse
import asyncio
from aiohttp import web, ClientSession
from os.path import join
from os import stat
from sys import argv
import yaml


class AsyncFileStorage:
    def __init__(self, port=8000, save_files=True ,data_dir="/tmp/async_file_storage", nodes=()):
        self.port = port
        self.data_dir = data_dir
        self.nodes = nodes
        self.save_files = save_files

    async def fetch(self, url):
        async with ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    return await resp.text()
                else:
                    raise FileNotFoundError
                    
    
    def write_file(self, file_name, data):
        with open(file_name, "w") as file:
            file.write(data)
            return True
                
    async def is_in_nodes(self, file_name):
        futures = [self.api_call(node_id, file_name) for node_id in range(len(self.nodes))]
        done, _ = await asyncio.wait(futures)
        success_nodes = []
        for future in done:
            if not future.exception():
                success_nodes.append(future.result())
        return success_nodes

        
    async def api_call(self, node_id, file_name):
        get = "/".join([self.nodes[node_id]['url'], "api", file_name])
        if await self.fetch(get):
            return node_id        
        
    async def download_file(self, node_id, file_name):
        get = "/".join([self.nodes[node_id]['url'], file_name])
        data = await self.fetch(get)
        if self.save_files and self.nodes[node_id]['save_files']:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, self.write_file, join(self.data_dir, file_name), data)
        return data
        
    async def api_handle(self, request):
        file_name = request.match_info.get('file_name')
        try:
            file_size = stat(join(self.data_dir, file_name)).st_size
        except FileNotFoundError:
            return web.Response(status=404)
        else:
            return web.Response(text=str(file_size))

    async def file_handle(self, request):
        file_name = request.match_info.get('file_name')
        file_path = join(self.data_dir, file_name)

        try:
            file = open(file_path, 'r')
            loop = asyncio.get_running_loop()
            data = await loop.run_in_executor(None, file.read)

        except FileNotFoundError:
            success_nodes = await self.is_in_nodes(file_name)
            if success_nodes:
                data = await self.download_file(success_nodes[0], file_name)
                return web.Response(text=data)
            return web.Response(status=404)
        else:
            file.close()
            return web.Response(text=data)
            
    def run(self):
        app = web.Application()
        app.add_routes([web.get('/{file_name}', self.file_handle),
                        web.get('/api/{file_name}', self.api_handle)])
        web.run_app(app, host='127.0.0.1', port=self.port)
        
    
def load_config(config_path: str):
    with open(config_path, 'r') as config_file:
        config = yaml.load(config_file)
        print(f"Config loaded from: '{config_path}'")
        return config


def parse_args(args):
    parser = argparse.ArgumentParser(description='Async File Storage')
    parser.add_argument('-c',
                        '--config',
                        action="store",
                        type=str,
                        default="config.yaml",
                        help='Config file')
    return parser.parse_args(args)


if __name__ == "__main__":
    args = parse_args(argv[1:])
    config = load_config(args.config)
    a = AsyncFileStorage(**config)
    a.run()