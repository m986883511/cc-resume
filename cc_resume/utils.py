import yaml
import os
import subprocess
import logging

LOG = logging.getLogger(__name__)

from cc_resume import Author

def read_yaml(filepath, encoding='utf-8') -> dict:
    with open(filepath, 'r', encoding=encoding) as f:
        # data = yaml.load(f, Loader=yaml.FullLoader)
        data = yaml.safe_load(f)
    return data


def execute_command(cmd: str, shell=True, encoding="utf-8", timeout=None, return_code_dict=None) -> (bool, str):
    try:
        logging.info("execute command: %s", cmd)
        tmp_cmd = cmd if shell else cmd.split()
        output = subprocess.check_output(tmp_cmd, stderr=subprocess.STDOUT, shell=shell, timeout=timeout)
        default_return = output.decode(encoding, errors='ignore').strip()
        if return_code_dict:
            default_return = return_code_dict.get('0') or default_return
        return 0, default_return
    except subprocess.TimeoutExpired as te:
        err_msg = f"timeout={timeout}, cmd='{cmd}'"
        logging.error(f"execute command timed out, {err_msg}")
        return -1, err_msg
    except subprocess.CalledProcessError as e:
        err_msg = f"cmd='{cmd}', err={e.output.decode(encoding, errors='ignore').strip()}"
        LOG.error(f"execute command failed, {err_msg}")
        return_code = e.returncode
        if return_code_dict:
            err_msg = return_code_dict.get(str(return_code)) or err_msg
        return return_code, err_msg
    except Exception as e:
        err_msg = f"cmd='{cmd}', err={e.output.decode(encoding, errors='ignore').strip()}"
        LOG.error(f"execute command failed, e_class={e.__class__}, {err_msg}")
        return_code = e.returncode
        if return_code_dict:
            err_msg = return_code_dict.get(str(return_code)) or err_msg
        return return_code, err_msg


def execute_command_in_popen(cmd: str, shell=True, output_func=None) -> int:
    def func():
        for _line in iter(proc.stdout.readline, ""):
            yield _line

    def default_print(x):
        if os.environ.get('IN_CLICK'):
            import click
            click.secho(x.strip())
        else:
            print(x, end='')

    output_func = output_func or default_print
    logging.info(f"execute_command_in_popen cmd={cmd}")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=shell, universal_newlines=True)
    for line in func():
        output_func(line)
    proc.stdout.close()
    return_code = proc.wait()
    LOG.info(f'execute_command_in_popen end, return_code={return_code}')
    return return_code


def execute_command_on_host(cmd: str, shell=True, encoding="utf-8", timeout=None, return_code_dict=None) -> (bool, str):
    assert shell, f'execute_command_on_host shell param must be true'
    cmd = f"nsenter --mount=/host/proc/1/ns/mnt sh -c '{cmd}'"
    logging.info("execute command on host")
    return execute_command(cmd, shell=shell, encoding=encoding, timeout=timeout, return_code_dict=return_code_dict)


def crudini_set_config(ini_path: str, section: str, key: str, value: str, check_file_exist=True) -> (int, str):
    if check_file_exist:
        assert os.path.exists(ini_path), f"{ini_path} is not exist"
    cmd = f'crudini --set {ini_path} "{section}" "{key}" {value}'
    flag, content = execute_command(cmd, shell=True)
    return flag, content


def crudini_get_config(ini_path: str, section: str, key: str, check_file_exist=True) -> (int, str):
    if check_file_exist:
        assert os.path.exists(ini_path), f"{ini_path} is not exist"
    cmd = f'crudini --get {ini_path} "{section}" "{key}"'
    flag, content = execute_command(cmd, shell=True)
    return flag, content


def completed(flag, dec, err=None, raise_flag=True, just_echo=False):
    if flag == 0:
        msg = f'{dec}'
        if not just_echo:
            msg += f' success'
        LOG.info(msg)
        if os.environ.get('IN_CLICK'):
            import click  # 不要在cc_utils模块中公开引入任何第三方包
            if just_echo:
                click.secho(msg)
            else:
                click.secho(msg, fg='green')
        elif os.environ.get('IN_TUI'):
            LOG.info(msg)
        else:
            print(msg)
    else:
        msg = f'{dec}'
        if not just_echo:
            msg += f' failed'
        if err:
            msg = f'{msg}, err: {err}'
        LOG.error(msg)
        if os.environ.get('IN_CLICK'):
            import click  # 不要在cc_utils模块中公开引入任何第三方包
            if just_echo:
                click.secho(msg)
            else:
                click.secho(msg, fg='red')
            if raise_flag:
                raise click.ClickException("")
        elif os.environ.get('IN_TUI'):
            LOG.error(msg)
        else:
            print(msg)
        if raise_flag:
            raise Exception(msg)


def set_simple_log(log_path):
    dir_name = os.path.dirname(log_path)
    os.makedirs(dir_name, exist_ok=True)
    logging.basicConfig(
        filename=log_path,  # 日志文件名
        level=logging.INFO,  # 日志级别
        format='%(asctime)s - %(levelname)s - %(message)s'  # 日志格式
    )
    LOG = logging.getLogger(__name__)
    LOG.info(f'set_simple_log={log_path} ok')


def mkdir_config(dir_name):
    local_app_data_path = os.environ.get('LocalAppData')
    config_dir = os.path.join(local_app_data_path, Author.name, dir_name)
    os.makedirs(config_dir, exist_ok=True)
    return config_dir
