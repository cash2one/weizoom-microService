# -*- coding: utf-8 -*-

"""@package eaglet.core.watchdog

Watchdog接口
需要settings里面配置SERVICE_NAME和设置logging格式
logging.basicConfig(
	format='[%(asctime)s] %(name)s %(levelname)s %(message)s',
	datefmt="%Y-%m-%d %H:%M:%S",
	level=logging.INFO
)
"""
__author__ = 'duhao, bert'
# import settings
import logging
import json
import decimal
from eaglet.core.wd import watchdog_client
from eaglet.core.wd.watchdog_client import WatchdogClient
import uuid

from datetime import datetime, date

# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s %(levelname)s : %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S'
#                     )

logging.basicConfig(level=logging.INFO,
                    format='%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                    )

# DEBUG = 1
# INFO = 2
# WARNING = 3
# ERROR = 4
# # TODO delete
# ALERT = 5
# CRITICAL = 6
DEBUG = "DEBUG"
INFO = "INFO"
WARNING = "WARNING"
ERROR = "ERROR"
ALERT = "ALERT"
CRITICAL = "CRITICAL"

DEFAULT_LOG_TYPE = 'CUSTOM'


def debug(message, log_type=DEFAULT_LOG_TYPE, *args, **kwargs):
	__watchdog(DEBUG, message, log_type)


def info(message, log_type=DEFAULT_LOG_TYPE, *args, **kwargs):
	__watchdog(INFO, message, log_type)


def warning(message, log_type=DEFAULT_LOG_TYPE, *args, **kwargs):
	__watchdog(WARNING, message, log_type)


def error(message, log_type=DEFAULT_LOG_TYPE, *args, **kwargs):
	__watchdog(ERROR, message, log_type)


def alert(message, log_type=DEFAULT_LOG_TYPE, *args, **kwargs):
	__watchdog(ALERT, message, log_type)


def critical(message, log_type=DEFAULT_LOG_TYPE, *args, **kwargs):
	__watchdog(CRITICAL, message, log_type)


def _default(obj):
	if isinstance(obj, datetime):
		return obj.strftime('%Y-%m-%d %H:%M:%S')
	elif isinstance(obj, date):
		return obj.strftime('%Y-%m-%d')
	elif isinstance(obj, decimal.Decimal):
		return str(obj)
	else:
		return '<object>'


service_name = None

def __watchdog(level, message, log_type):
	"""
	@param[in] level 日志级别
	@param[in] message 日志信息，通常是json格式
	@param[in] log_type 日志类型，如WEB, API, H5
	@param[in] user_id 系统账号的user id，用来追踪是哪个用户的系统中出的问题
	"""
	global service_name
	if not service_name:
		try:
			import settings
		except ImportError:

			try:
				from django.conf import settings
			except:
				settings = None

		if settings and hasattr(settings, 'SERVICE_NAME'):
			service_name = settings.SERVICE_NAME
		else:
			service_name = 'unknown'

	log_id = str(uuid.uuid1())
	if hasattr(watchdog_client, 'watchdogClient') and watchdog_client.watchdogClient:
		message = watchdog_client.watchdogClient.getMessge(level, message, log_type, log_id)
	else:
		watchdog_client.watchdogClient = watchdog_client.WatchdogClient(service_name)
		message = watchdog_client.watchdogClient.getMessge(level, message, log_type, log_id)

	if level == DEBUG:
		logging.debug(message)
	elif level == INFO:
		logging.info(message)
	elif level == WARNING:
		logging.warn(message)
	elif level == ERROR:
		logging.error(message)
	elif level == ALERT:  # TODO delele alter
		logging.critical(message)
	elif level == CRITICAL:
		logging.critical(message)
