#!/usr/bin/python3
"""Defines the AirBnB console"""

from cmd import Cmd
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.place import Place
from models.amenity import Amenity
from models import storage
import shlex
import re


class HBNBCommand(Cmd):
    """Defines the AirBnB command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "

    def __parser(self, line: str) -> list:
        """Console Arguments parser"""
        if re.fullmatch(r'\s*', line):
            return None
        args = shlex.split(line, posix=False)

        for x in range((len(args))):
            if args[x].startswith("'"):
                args[x] = args[x].strip("\'")
            elif args[x].startswith('"'):
                args[x] = args[x].strip('\"')
        return (args)

    def __parserDotFn(self, line: str):
        """Console Arguments
            class method (dot command) parser
        """
        line = line.strip(" ")
        srch_cls = re.search(r'^[A-Z]\w+\.', line)
        ret = {}
        tokens = ""
        is_valid_arg = False
        if srch_cls:
            cls_ind = srch_cls.span()
            cls = line[cls_ind[0]: cls_ind[1] - 1]
            chks = self.__console_utility('dotn', [cls])
            for chk in chks:
                is_valid_arg = chk()
            if not is_valid_arg:
                return None
            tokens += cls
        srch_cmd = re.search(r'\.\w+\(', line)
        if srch_cmd:
            cmd_ind = srch_cmd.span()
            cmdcm = line[cmd_ind[0] + 1: cmd_ind[1] - 1]
            chks = self.__console_utility('dotm', [f"self.do_{cmdcm}"])
            is_valid_arg = False
            for chk in chks:
                is_valid_arg = chk(self)
            if not is_valid_arg:
                return None
            ret.update({"cmdcm": f"self.do_{cmdcm}"})
        srch_args = re.search(r'\(.*\)', line)
        if srch_args:
            cmd_ind = srch_args.span()
            args = line[cmd_ind[0] + 1: cmd_ind[1] - 1]
            is_id = r'(\w+)\-(\w+)\-(\w+)\-(\w+)\-(\w+)'
            mid = re.search(is_id, args)
            arg_id = ""
            if mid:
                index = mid.span()
                arg_id = args[index[0]:index[1]]
            elif args and not mid:
                print("** no instance found **")
                return None
            if arg_id:
                id_toks = ['plc_hold', arg_id.strip(" ")]
                chks = self.__console_utility('doto', id_toks)
                is_valid_arg = False
                for chk in chks:
                    is_valid_arg = chk()
                if not is_valid_arg:
                    return None
                tokens += f' {arg_id.strip(" ")}'
            is_dictArgs = re.search(r'\{.*\}',  args)
            if is_dictArgs:
                m = is_dictArgs.span()
                ret.update({"attributes": eval(args[m[0]: m[1]])})
            elif not is_dictArgs:
                p_toks = args.split(",")
                if len(p_toks) == 3:
                    ret.update({'attributes': {p_toks[1]: p_toks[2]}})

            ret.update({"tokens": tokens})
        return ret

    def __console_utility(self, cm: str, toks: list, objs: dict = {}) -> list:
        """Console  Utility
            for validation and  object fetch
        """

        is_id = r'(\w+)\-(\w+)\-(\w+)\-(\w+)\-(\w+)'
        cmds = {
                    'show': {'argc': 2, 'argv': ['class', 'id', 'instance']},
                    'create': {'argc': 1, 'argv': ['class']},
                    'destroy': {'argc': 2, 'argv': ['class', 'id',
                                                    'instance']},
                    'update': {'argc': 4, 'argv': ['class', 'id', 'instance',
                                                   'attribute']},
                    'dotn': {'argc': 1, 'argv': ['class']},
                    'dotm': {'argc': 1, 'argv': ['cmd']},
                    'doto': {'argc': 1, 'argv': ['id']},
                }

        checks = {}

        def __class_ck() -> bool:
            """class validation (1st Arg)"""

            if toks:
                test = re.fullmatch(is_id, toks[0])
            if not toks or cmds[cm]['argc'] >= 1 and test:
                print("** class name missing **")
                return False
            try:
                eval(toks[0])
            except NameError:
                print("** class doesn't exist **")
                return False
            return True

        def __instance_ck() -> bool:
            """instance validation
            And object fetch if object exists
            """

            if len(toks) >= 2:
                srch = f"{toks[0]}.{toks[1]}"
                for key, value in (storage.all()).items():
                    if key == srch:
                        objs.update({key: value})
                        return True
            print("** no instance found **")
            return False

        def __cmd_ck(self) -> bool:
            """cmd command validation"""

            try:
                eval(toks[0])
            except AttributeError:
                print("** command not found **")
                return False
            return True

        def __id_ck() -> bool:
            """obj ID validation (2nd Arg)"""

            if len(toks) < 2:
                print("** instance id missing **")
                return False
            return True

        def __attribute_ck() -> bool:
            """Object Attribute validation"""

            if len(toks) == 2:
                print("** attribute name missing **")
                return False
            if len(toks) == 3:
                print("** value missing **")
                return False
            """
            # attributes present in obj creation only
            if toks[2] not in dir(eval(toks[0])):
                msg = "< __class__ > has no attribute"
                print(f"** [{toks[0]}] {msg} {toks[2]} **")
                return False
            """
            if toks[2] in ("id", "created_at", "updated_at"):
                msg = "<__class__> not allowed"
                print(f"** update {toks[2]} on [{toks[0]}] {msg} !! **")
                return False

            return True

        checks.update({'class': __class_ck, 'id': __id_ck,
                       'instance': __instance_ck, 'attribute': __attribute_ck,
                       "cmd": __cmd_ck})
        return ([checks[chk] for chk in cmds[cm]['argv']])

    def emptyline(self):
        """Do nothing upon receiving an empty args."""

        pass

    def do_quit(self, args):
        """Quit command to exit the program."""

        return True

    def do_EOF(self, args):
        """EOF signal to exit the program."""

        print("")
        return True

    def do_create(self, args):
        """Usage: create <class>
        Create a new class instance and print its id.
        """

        class_nm = self.__parser(args)
        chks = self.__console_utility('create', class_nm)
        is_valid_arg = False
        for chk in chks:
            is_valid_arg = chk()
        if is_valid_arg:
            obj = eval(class_nm[0])()
            obj.save()
            print(obj.id)

    def do_show(self, args):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """

        obj = {}
        tokens = self.__parser(args)
        chks = self.__console_utility('show', tokens, obj)

        is_valid_arg = False
        for chk in chks:
            is_valid_arg = chk()
            if not is_valid_arg:
                break
        if is_valid_arg:
            print(obj[[*obj][0]])

    def do_destroy(self, args):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""

        obj = {}
        tokens = self.__parser(args)
        chks = self.__console_utility('destroy', tokens, obj)
        is_valid_arg = False
        for chk in chks:
            is_valid_arg = chk()
            if not is_valid_arg:
                break
        if is_valid_arg:
            del storage.all()[[*obj][0]]
            del obj[[*obj][0]]
            storage.save()

    def do_all(self, args):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""

        tokens = self.__parser(args)
        ret = []
        if tokens:
            chks = self.__console_utility('dotn', tokens)
            is_valid_arg = False
            for chk in chks:
                is_valid_arg = chk()
            if is_valid_arg:

                for value in (storage.all()).values():
                    if value.__class__.__name__ == tokens[0]:
                        ret.append(value.__str__())
                print(ret)
        else:
            for value in (storage.all()).values():
                ret.append(value.__str__())
            print(ret)

    def do_count(self, args):
        """Usage: count or count <class> or <class>.count()
            Retrieve the count of instances of a given class.
            Retrieve the count of instances of all store object.
        """

        tokens = self.__parser(args)
        count = 0
        if tokens:
            chks = self.__console_utility('dotn', tokens)
            is_valid_arg = False
            for chk in chks:
                is_valid_arg = chk()
            if is_valid_arg:

                for value in (storage.all()).values():
                    if value.__class__.__name__ == tokens[0]:
                        count += 1
                print(count)
        else:
            for value in (storage.all()).values():
                count += 1
            print(count)

    def default(self, args):
        """Default behavior for cmd module when input is invalid
            for reconstruction of dot command
        """

        dot_func = r'^[A-Z]\w+\.\w+\(.*\)'
        if re.fullmatch(dot_func, args):
            toks = self.__parserDotFn(args)
            if toks:
                if toks['cmdcm'] != 'self.do_update':
                    eval(toks['cmdcm'])(toks['tokens'])
                elif toks['cmdcm'] == 'self.do_update':
                    for key, value in toks['attributes'].items():
                        if type(value) is str:
                            for x in ("'", "\\", '"'):
                                value = value.replace(x, "").strip(" ")
                        arg = f"{toks['tokens']} {key} '{value}'"
                        eval(toks['cmdcm'])(arg)
        elif re.fullmatch(r'^\.\w+\(\)', args):
            cm = args.split("(")[0]
            cm = cm.strip(" ").strip(".")
            if cm in ['count', 'all']:
                eval(f'self.do_{cm}')("")
            else:
                print(f"*** Unknown syntax: {args}")
        else:
            print(f"*** Unknown syntax: {args}")

    def do_update(self, args):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
        <class>.update(<id>, <attribute_name>, <attribute_value>) or
        <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""

        obj = {}
        tokens = self.__parser(args)
        chks = self.__console_utility('update', tokens, obj)
        is_valid_arg = False
        for chk in chks:
            is_valid_arg = chk()
            if not is_valid_arg:
                break
        if is_valid_arg:
            attri_type = str
            try:
                x = getattr(obj[[*obj][0]], tokens[2])
                attri_type = type(x)
            except AttributeError:
                if tokens[3].isdigit():
                    attri_type = int
                else:
                    try:
                        float(tokens[3])
                        attri_type = float
                    except ValueError:
                        pass
            if attri_type in (int, float):
                tokens[3] = attri_type(float(tokens[3]))
            setattr(obj[[*obj][0]], tokens[2], tokens[3])
            obj[[*obj][0]].save()


if __name__ == '__main__':
    HBNBCommand().cmdloop()
