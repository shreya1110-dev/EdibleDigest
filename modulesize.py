import os, sys
dir_size = lambda dirpath:sum([(sum([os.path.getsize(os.path.join(root, f)) for f in files]) + sum([dir_size(os.path.join(root, d)) for d in dirs])) for root, files, dirs in os.walk(dirpath)])
def module_size(module_name):
    for p in sys.path:
        if os.path.exists(os.path.join(p, module_name)+'.py'):
            return f"{os.path.getsize(os.path.join(p, module_name)+'.py')/1024.0} KB"
        if os.path.exists(os.path.join(p, module_name)):            
            return f'{dir_size(os.path.join(p, module_name))/1024.0} KB'
    return 'Module not installed.'

modules = ['numpy', 'io', 'starlette', 'uvicorn', 'fastapi', 'cv2']

for m in modules:
  print(f"{m} ===> {module_size(m)}")
