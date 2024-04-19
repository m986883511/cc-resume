import os
import socket
import logging

from oslo_config import cfg
from reportlab.lib import colors

from cc_resume import Author

CONF = cfg.CONF
AIO_CONF_PATH = f'/etc/{Author.name}/resume.conf'

default_opts = [
    cfg.IntOpt('font_size', default=15, help="默认字体大小"),
    cfg.IntOpt('title_padding', default=10, help="title_padding"),
    cfg.StrOpt('author_des', default=f'本工具完全免费, 由{Author.zh_name}开发', help="tui title"),
]

resume_opts = [
    cfg.StrOpt('name', help="name"),
    cfg.StrOpt('config_dir', help="config_dir"),
    cfg.StrOpt('title_color', default=colors.orange, help="title_color"),
]

CONF.register_cli_opts(default_opts)
# todo: 在这之后 set_simple_log 无效
CONF.register_cli_opts(resume_opts, group='resume')
