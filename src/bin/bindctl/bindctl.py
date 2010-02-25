# Copyright (C) 2009  Internet Systems Consortium.
#
# Permission to use, copy, modify, and distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND INTERNET SYSTEMS CONSORTIUM
# DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL
# INTERNET SYSTEMS CONSORTIUM BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING
# FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT,
# NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
# WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.


from moduleinfo  import *
from bindcmd import *
import isc
import pprint
from optparse import OptionParser, OptionValueError

__version__ = 'Bindctl'

def prepare_config_commands(tool):
    module = ModuleInfo(name = "config", desc = "Configuration commands")
    cmd = CommandInfo(name = "show", desc = "Show configuration")
    param = ParamInfo(name = "identifier", type = "string", optional=True)
    cmd.add_param(param)
    module.add_command(cmd)

    cmd = CommandInfo(name = "add", desc = "Add entry to configuration list")
    param = ParamInfo(name = "identifier", type = "string", optional=True)
    cmd.add_param(param)
    param = ParamInfo(name = "value", type = "string", optional=False)
    cmd.add_param(param)
    module.add_command(cmd)

    cmd = CommandInfo(name = "remove", desc = "Remove entry from configuration list")
    param = ParamInfo(name = "identifier", type = "string", optional=True)
    cmd.add_param(param)
    param = ParamInfo(name = "value", type = "string", optional=False)
    cmd.add_param(param)
    module.add_command(cmd)

    cmd = CommandInfo(name = "set", desc = "Set a configuration value")
    param = ParamInfo(name = "identifier", type = "string", optional=True)
    cmd.add_param(param)
    param = ParamInfo(name = "value", type = "string", optional=False)
    cmd.add_param(param)
    module.add_command(cmd)

    cmd = CommandInfo(name = "unset", desc = "Unset a configuration value")
    param = ParamInfo(name = "identifier", type = "string", optional=False)
    cmd.add_param(param)
    module.add_command(cmd)

    cmd = CommandInfo(name = "diff", desc = "Show all local changes")
    module.add_command(cmd)

    cmd = CommandInfo(name = "revert", desc = "Revert all local changes")
    module.add_command(cmd)

    cmd = CommandInfo(name = "commit", desc = "Commit all local changes")
    module.add_command(cmd)

    cmd = CommandInfo(name = "go", desc = "Go to a specific configuration part")
    param = ParamInfo(name = "identifier", type="string", optional=False)
    cmd.add_param(param)
    module.add_command(cmd)

    tool.add_module_info(module)

def check_port(option, opt_str, value, parser):
    if (value < 0) or (value > 65535):
        raise OptionValueError('%s requires a port number (0-65535)' % opt_str)
    parser.values.port = value

def check_addr(option, opt_str, value, parser):
    ipstr = value
    ip_family = socket.AF_INET
    if (ipstr.find(':') != -1):
        ip_family = socket.AF_INET6

    try:
        socket.inet_pton(ip_family, ipstr)
    except:
        raise OptionValueError("%s invalid ip address" % ipstr)

    parser.values.addr = value

def set_bindctl_options(parser):
    parser.add_option('-p', '--port', dest = 'port', type = 'int',
            action = 'callback', callback=check_port,
            default = '8080', help = 'port for cmdctl of bind10')

    parser.add_option('-a', '--address', dest = 'addr', type = 'string',
            action = 'callback', callback=check_addr,
            default = '127.0.0.1', help = 'IP address for cmdctl of bind10')


if __name__ == '__main__':
    try:
        parser = OptionParser(version = __version__)
        set_bindctl_options(parser)
        (options, args) = parser.parse_args()
        server_addr = options.addr + ':' + str(options.port)
        tool = BindCmdInterpreter(server_addr)
        prepare_config_commands(tool)
        tool.run()
    except Exception as e:
        print(e, "\nFailed to connect with b10-cmdctl module, is it running?")


