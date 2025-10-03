import os
import importlib.util

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def check_app_urls(app_name):
    urls_path = os.path.join(BASE_DIR, app_name, "urls.py")
    if not os.path.exists(urls_path):
        print(f"[ERROR] No se encontró urls.py en la app '{app_name}'")
        return False

    spec = importlib.util.spec_from_file_location(f"{app_name}.urls", urls_path)
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as e:
        print(f"[ERROR] No se pudo importar urls.py de '{app_name}': {e}")
        return False

    if not hasattr(module, "app_name"):
        print(f"[ERROR] Falta 'app_name' en urls.py de '{app_name}'")
    else:
        print(f"[OK] app_name de '{app_name}' = '{module.app_name}'")

    if not hasattr(module, "urlpatterns"):
        print(f"[ERROR] Falta 'urlpatterns' en urls.py de '{app_name}'")
    elif not isinstance(module.urlpatterns, (list, tuple)):
        print(f"[ERROR] urlpatterns de '{app_name}' no es lista/tupla")
    else:
        print(f"[OK] urlpatterns de '{app_name}' tiene {len(module.urlpatterns)} rutas")

    return True

if __name__ == "__main__":
    apps = ["landing", "auth_app", "dashboard", "resources", "forum"]
    print("=== Validando urls.py de todas las apps ===")
    for app in apps:
        check_app_urls(app)
