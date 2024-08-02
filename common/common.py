import os


def find_name_html_files(directory='C:\\', name_file=""):
	for root, dirs, files in os.walk(directory):
		html_files = [
			os.path.join(root, file) for file in files
			if file.endswith('.html') and file.startswith(name_file)
		]
		if html_files:
			return html_files[0]
	return None


def get_content_html_files(name_file, directory='C:\\'):
	path_file = find_name_html_files(directory, name_file)
	if not path_file:
		return None
	try:
		with open(path_file, 'r', encoding='utf-8') as f:
			return f.read()
	except (OSError, IOError) as e:
		print(f"Error reading file {path_file}: {e}")
		return None


def get_para_header(request, name, default_value=''):
	try:
		return request.headers.get(name)
	except ValueError:
		try:
			return request.headers[name]
		except ValueError:
			return default_value


def check_valid_obj_accounts(obj):
	if not obj:
		return {
			"status": False,
			"msg": "No JSON data provided"
		}
	if ('login' not in obj) and ('password' not in obj) and ('phone' not in obj):
		return {
			"status": False,
			"msg": "Please provide must to have three fields: login, password, phone"
		}
	if (len(obj.get("login", "")) > 20) or (len(obj.get("password", "")) > 40) or (len(obj.get("phone", "")) > 20):
		return {
			"status": False,
			"msg": "You provide field is invalid",
			"note": {
				"login": "less than 20 characters",
				"password": "less than 40 characters",
				"phone": "less than 20 characters",
			}
		}
	return True


def check_valid_integer(register_id):
	try:
		int(register_id)
		return True
	except:
		return False


def check_valid_obj_show_serialpaso(obj):
	if not obj:
		return False
	# return {
	# 	"status": False,
	# 	"msg": "No JSON data provided"
	# }
	if ('file' not in obj) or ('contract_app' not in obj) or ('contract_server' not in obj):
		return False
	# return {
	# 	"status": False,
	# 	"msg": "Please provide must to have four fields: file, app_env, contract_app, contract_server"
	# }
	# 0: AWS, 1: K5, 2:T2
	if obj.get('app_env', 0) not in [0, 1, 2]:
		return False
	# return {
	# 	"status": False,
	# 	"msg": "field \'app_env\' must be 0, 1, 2"
	# }
	# 0: app1, 1: app2
	if (obj['contract_app'] not in [0, 1]) or (obj['contract_server'] not in [0, 1]):
		return False
	# return {
	# 	"status": False,
	# 	"msg": "field \'contract_app\' and \'contract_server\' must be 0 or 1"
	# }
	if not isinstance(obj['file'], str) and len(obj['file']) > 128:
		return False
	return True
