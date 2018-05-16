# svn_user_extractor
This python project is used to automatically get all the SVN username from a given SVN repository, and map it to a LDAP server to get the first name and last name of the users and generate a git user mapping that can be used for git svn call.

This project is run using python 3.6 on windows. Modifications are needed for unix support.

Remember to modify the extractor.ini for your SVN url and LDAP server url.
