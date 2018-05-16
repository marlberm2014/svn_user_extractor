#!/usr/bin/python3
import os
import sys
import re
from configparser import ConfigParser
from subprocess import Popen
from Source.FileReader import FileReader
from lxml import etree as ET

DEFAULT_FOLDER = os.path.dirname(os.path.abspath(__file__))

FILEREADER = FileReader()


def init_properties():
    """
    initialize the properties from the ini file.
    """
    configfile = os.path.join(DEFAULT_FOLDER, "extractor.ini")
    parser = ConfigParser()
    parser.read(configfile)
    url = parser.get("batch", "url")
    ldap_url = parser.get("batch", "ldap_url")
    raw_name_list = parser.get("batch", "raw_list")
    svn_bat = parser.get("batch", "svn_bat")
    user_bat = parser.get("batch", "user_bat")
    output = parser.get("batch", "output")
    error = parser.get("batch", "error")
    silent_delete_file(raw_name_list)
    silent_delete_file(output)
    silent_delete_file(error)
    names = process_svn_usernames(svn_bat, url, raw_name_list, error)
    return names, os.path.join(DEFAULT_FOLDER, user_bat), ldap_url, output, error

def process_svn_usernames(svn_bat, url, raw_name_list, error):
    trigger_command("%s %s %s %s" % (os.path.join(DEFAULT_FOLDER, svn_bat),
                                     url, raw_name_list, error))
    svn_logs = FILEREADER.read_file(os.path.join(DEFAULT_FOLDER,
                                                 raw_name_list))
    names = [line for line in svn_logs if line.startswith('r')]
    pattern = re.compile(".*\| (\w*) \|.*")
    return list(set([pattern.match(name).group(1) for name in names]))


def silent_delete_file(raw_name_list):
    try:
        os.remove(os.path.join(DEFAULT_FOLDER, raw_name_list))
    except OSError:
        pass


def trigger_command(command):
    """
    Trigger a command.
        :param command: the command to be triggered
    """
    print(command)
    p = Popen(command, cwd=DEFAULT_FOLDER)
    stdout, stderr = p.communicate()
    print("CMD: %s\n\n%s" % (stdout, stderr))


def create_ldap_detail_file():
    """
    Create the file that contains the ldap list
    """
    names, user_bat, ldap_url, output, error = init_properties()
    names = [name.rstrip() for name in names]
    with open(os.path.join(DEFAULT_FOLDER, output), "w") as f:
        f.write("<names>\n")
    for name in names:
        command = ("%s %s %s %s %s" % (user_bat, ldap_url, name, output, error))
        trigger_command(command)
    with open(os.path.join(DEFAULT_FOLDER, output), "a+") as f:
        f.write("</names>")
    return output, names


def get_name_tuples(output):
    """
    Get the username, name and email in tuples from the xml
        :param output: the xml file that will be readed
    """
    with open(os.path.join(DEFAULT_FOLDER, output)) as f:
        tree = ET.fromstring(f.read())
        emails = tree.xpath(
            "//dsml/directory-entries/entry/attr[@name='mail']/value/text()")
        names = tree.xpath(
            "//dsml/directory-entries/entry/attr[@name='cn']/value/text()")
        username = tree.xpath(
            "//dsml/directory-entries/entry/attr[@name='uid']/value/text()")
        all_values = list(zip(username, names, emails))
    return all_values


def write_git_svn_user_map(all_values, names):
    with open(os.path.join(DEFAULT_FOLDER, "users.txt"), "w") as f:
        names_with_ldap = list()
        for value in all_values:
            names_with_ldap.append(value[0])
            f.write("%s = %s <%s>\n" % (value))
            print("%s = %s <%s>" % (value))
        missing_names = list(set(names) - set(names_with_ldap))
        for name in missing_names:
            f.write("%s = First Last Name <email@address.com>\n" %
                    (name.rstrip()))
            print("%s = First Last Name <email@address.com>" % (name.rstrip()))

def main():
    """
    Main function
    """
    output, names = create_ldap_detail_file()
    all_values = get_name_tuples(output)
    write_git_svn_user_map(all_values, names)


if __name__ == '__main__':
    main()
