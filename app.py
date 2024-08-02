from flask import Flask, request, jsonify

from db_connection.base_mysql import BaseMySQL
from config import config_mysql, config_query, PAGE_SIZE, HOST, PORT
from common import common
from base_log import BaseLogger

# setup logging
logger = BaseLogger(name='log_action', log_file='log_action.log')

app = Flask(__name__)


@app.route('/get_accounts_all', methods=['GET'])
def get_accounts_all():
	page = common.get_para_header(request, 'page')
	if not page:
		query = config_query['get_all_accounts']
	else:
		if not common.check_valid_integer(page):
			logger.info("GET ALL: You provide \'page\' is not integer")
			return jsonify({
				"status": False,
				"msg": "You provide \'page\' is not integer"
			})
		if int(page) < 1:
			logger.info("GET ALL: You provide \'page\' must be greater than 0")
			return jsonify({
				"status": False,
				"msg": "You provide \'page\' must be greater than 0"
			})
		query = config_query['get_accounts_with_page'].format(PAGE_SIZE, ((int(page) - 1) * PAGE_SIZE))

	_data = BaseMySQL(config_mysql).query(query)

	if not _data:
		logger.info("GET ALL: Not found data in database")
		return jsonify({
			"status": False,
			"msg": "Not found data in database"
		})
	logger.info("GET ALL: Success")
	return jsonify({
		"status": True,
		"data": _data
	})


@app.route('/get_accounts/<register_id>', methods=['GET'])
def get_accounts(register_id):
	if not common.check_valid_integer(register_id):
		logger.info("GET: You provide register_id is not valid")
		return jsonify({
			"status": False,
			"msg": "You provide register_id is not valid"
		}), 400

	query = config_query['get_accounts'].format(register_id)
	_data = BaseMySQL(config_mysql).query(query)
	if not _data:
		logger.info("GET: You provide register_id is not found")
		return jsonify({
			"status": False,
			"msg": "You provide register_id is not found"
		}), 400
	logger.info("GET: Success")
	return jsonify({
		"status": True,
		'data': _data[0]
	}), 200


@app.route('/create_accounts', methods=['POST'])
def create_accounts():
	_data = request.get_json()
	is_valid = common.check_valid_obj_accounts(_data)
	if isinstance(is_valid, dict):
		logger.info("CREATE ACCOUNT: {}".format(is_valid['msg']))
		return jsonify(is_valid), 400

	login = _data.get("login", "")
	password = _data.get("password", "")
	phone = _data.get("phone", "")
	query = config_query['create_accounts'].format(login, password, phone)
	res = BaseMySQL(config_mysql).execute(query)
	if res is True:
		logger.info("CREATE ACCOUNT: Success")
		return jsonify({
			"status": True,
			"msg": "Create accounts({}) is success!".format(login)
		}), 200
	else:
		logger.info("CREATE ACCOUNT: Create accounts({}) failed. Please try again!".format(login))
		return jsonify({
			"status": False,
			"msg": "Create accounts({}) failed. Please try again!".format(login)
		}), 400


@app.route('/update_accounts/<register_id>', methods=['POST', 'PUT'])
def update_accounts(register_id):
	if not common.check_valid_integer(register_id):
		logger.info("UPDATE ACCOUNT: You provide register_id is not valid")
		return jsonify({
			"status": False,
			"msg": "You provide register_id is not valid"
		}), 400

	_data = request.get_json()
	is_valid = common.check_valid_obj_accounts(_data)
	if isinstance(is_valid, dict):
		logger.info("UPDATE ACCOUNT: {}".format(is_valid['msg']))
		return jsonify(is_valid), 400

	update_fields = []
	for field, value in _data.items():
		if field in ['login', 'password', 'phone']:
			update_fields.append("{}='{}'".format(field, value))
	query = config_query['update_accounts'].format(",".join(update_fields), register_id)
	res = BaseMySQL(config_mysql).execute(query)
	if res is True:
		logger.info("UPDATE ACCOUNT: Success")
		return jsonify({
			"status": True,
			"msg": "Update accounts is success!"
		}), 200
	else:
		logger.info("UPDATE ACCOUNT: Update accounts failed. Please try again!")
		return jsonify({
			"status": False,
			"msg": "Update accounts failed. Please try again!"
		}), 400


@app.route('/delete_accounts/<register_id>', methods=['DELETE'])
def delete_accounts(register_id):
	if not common.check_valid_integer(register_id):
		logger.info("DELETE ACCOUNT: You provide register_id is not valid")
		return jsonify({
			"status": False,
			"msg": "You provide register_id is not valid"
		}), 400

	query = config_query['delete_accounts'].format(register_id)
	res = BaseMySQL(config_mysql).execute(query)
	if res is True:
		logger.info("DELETE ACCOUNT: Success")
		return jsonify({
			"status": True,
			"msg": "Delete accounts is success!"
		}), 200
	else:
		logger.info("DELETE ACCOUNT: Delete accounts failed. Please try again!")
		return jsonify({
			"status": False,
			"msg": "Delete accounts failed. Please try again!"
		}), 400


@app.route('/api/showSerialpaso', methods=['POST'])
def show_serialpaso():
	_data = request.get_json()
	if common.check_valid_obj_show_serialpaso(_data) is False:
		logger.info("SHOW SERIALPASO: Seal Info response false")
		return jsonify({
			"sucess": False,
			"filename": "",
			"message": "Seal Info response false",
		}), 400

	content_file = common.get_content_html_files(_data['file'])
	if content_file is None:
		logger.info("SHOW SERIALPASO: Seal Info response false")
		return jsonify({
			"sucess": False,
			"filename": "",
			"message": "Seal Info response false",
		}), 400
	logger.info("SHOW SERIALPASO: Seal Info response successfully")
	return jsonify({
		"sucess": True,
		"filename": "{}.html".format(_data['file']),
		"content": content_file,
		"message": "Seal Info response successfully",
	}), 200


if __name__ == '__main__':
	app.run(host=HOST, port=PORT)
