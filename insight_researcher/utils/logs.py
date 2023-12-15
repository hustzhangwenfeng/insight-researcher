import sys
from pathlib import Path
from loguru import logger as _logger
from datetime import datetime


def get_project_root():
    """Search upwards to find the project root directory."""
    current_path = Path.cwd()
    while True:
        if (
            (current_path / ".git").exists()
            or (current_path / ".project_root").exists()
            or (current_path / ".gitignore").exists()
        ):
            # use metagpt with git clone will land here
            _logger.info(f"PROJECT_ROOT set to {str(current_path)}")
            return current_path
        parent_path = current_path.parent
        if parent_path == current_path:
            # use metagpt with pip install will land here
            cwd = Path.cwd()
            _logger.info(f"PROJECT_ROOT set to current working directory: {str(cwd)}")
            return cwd
        current_path = parent_path


def get_cur_timestamp():
    # 获取当前日期和时间
    current_time = datetime.now()

    # 格式化日期和时间为指定格式
    formatted_time = current_time.strftime("%Y_%m%d_%H%M")
    return formatted_time


PROJECT_ROOT = get_project_root()
cur_timestamp = get_cur_timestamp()


def define_logger(print_level="INFO", logfile_level="DEBUG"):
    """调整日志级别到level之上
       Adjust the log level to above level
    """
    _logger.remove()
    _logger.add(sys.stderr, level=print_level)
    _logger.add(PROJECT_ROOT / f'logs/log-{cur_timestamp}.txt', level=logfile_level)
    return _logger


log = define_logger()
