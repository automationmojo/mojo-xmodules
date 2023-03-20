__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import logging
import os

import yaml


from mojo.xmods.exceptions import ConfigurationError
from mojo.xmods.xcollections.context import Context, ContextPaths

from mojo.xmods.credentials.basiccredential import BasicCredential
from mojo.xmods.credentials.sshcredential import SshCredential
from mojo.xmods.credentials.wifichoicecredential import WifiChoiceCredential

logger = logging.getLogger()

class CredentialManager:

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(CredentialManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self._credentials = {}

        self._initialize_credentials()
        return

    @property
    def credentials(self):
        return self._credentials

    def _initialize_credentials(self):
        """
        """

        ctx = Context()
        
        credential_files = ctx.lookup(ContextPaths.CONFIG_CREDENTIAL_FILES,
            [os.path.expanduser("~/credentials.yaml")])

        for cred_file in credential_files:
            if os.path.exists(cred_file):
                credential_info = None

                with open(cred_file, 'r') as lf:
                    lfcontent = lf.read()
                    credential_info = yaml.safe_load(lfcontent)

                try:
                    credentials_list = credential_info["credentials"]
                    errors, warnings = self._validate_credentials(credentials_list)

                    if len(errors) == 0:
                        for credential in credentials_list:
                            if "identifier" not in credential:
                                errmsg = "Credential items in 'environment/credentials' must have an 'identifier' member."
                                raise ConfigurationError(errmsg)
                            ident = credential["identifier"]

                            if "category" not in credential:
                                errmsg = "Credential items in 'environment/credentials' must have an 'category' member."
                                raise ConfigurationError(errmsg)
                            category = credential["category"]

                            if category == "basic":
                                BasicCredential.validate(credential)
                                credobj = BasicCredential(**credential)
                                self._credentials[ident] = credobj
                            elif category == "ssh":
                                SshCredential.validate(credential)
                                credobj = SshCredential(**credential)
                                self._credentials[ident] = credobj
                            elif category == "wifi-choice":
                                WifiChoiceCredential.validate(credential)
                                credobj = WifiChoiceCredential(**credential)
                                self._credentials[ident] = credobj
                            else:
                                warnmsg = f"Unknown category '{category}' found in credential '{ident}'"
                                logger.warn(warnmsg)
                    else:
                        errmsg_lines = [
                            f"Errors found in credential file={cred_file}",
                            "ERRORS:"
                        ]
                        for err in errors:
                            errmsg_lines.append(f"    {err}")

                        errmsg_lines.append("WARNINGS:")
                        for warn in warnings:
                            errmsg_lines.append(f"    {warn}")

                        errmsg = os.linesep.join(errmsg_lines)
                        raise ConfigurationError(errmsg)
                except KeyError:
                    errmsg = f"No 'credentials' field found in file={cred_file}"
                    raise ConfigurationError(errmsg)
            else:
                warnmsg = f"Credential file not found. expected={cred_file}"
                logger.warn(warnmsg)

        return

    def _validate_credentials(self, cred_list):
        errors = []
        warnings = []

        identifier_set = set()

        for cinfo in cred_list:
            if "identifier" in cinfo:
                identifier = cinfo["identifier"]
                if identifier in identifier_set:
                    errmsg = f"Duplicate identifer found. identifier={identifier}"
                    errors.append(errmsg)
                else:
                    identifier_set.add(identifier)
            else:
                errmsg = f"All credentials must have an identifier field. cinfo={cinfo}"
                errors.append(errmsg)

            if "category" in cinfo:
                category = cinfo["category"]
                if category == "basic":
                    child_errors, child_warnings =  self._validate_credential_basic(cinfo)
                    errors.extend(child_errors)
                    warnings.extend(child_warnings)
                elif category == "ssh":
                    child_errors, child_warnings =  self._validate_credential_ssh(cinfo)
                    errors.extend(child_errors)
                    warnings.extend(child_warnings)
                else:
                    warnmsg = f"Unknown credential category={category}. info={cinfo}"
                    warnings.append(warnmsg)
            else:
                errmsg = "Credential info has no category. info=%r" % cinfo
                errors.append(errmsg)

        return errors, warnings

    def _validate_credential_basic(self, cred):
        """
            Validates the non-common fields of a 'basic' credential.
        """
        errors = []
        warnings = []

        if "username" in cred:
            if len(cred["username"].strip()) == 0:
                errmsg = "The 'username' for a basic credential cannot be empty."
                errors.append(errmsg)
        else:
            errmsg = "Basic credentials must have a 'username' field."
            errors.append(errmsg)

        if "password" not in cred:
            errmsg = "Basic credentials must have a 'password' field."
            errors.append(errmsg)

        return errors, warnings

    def _validate_credential_ssh(self, cred):
        """
            Validates the non-common fields of an 'ssh' credential.
        """
        """
        -   "identifier": "some-node"
            "category": "ssh"
            "username": "ubuntu"
            "password": "blahblah"
            "keyfile": "~/.ssh/id_somenode_rsa"

        """
        errors = []
        warnings = []

        if "username" in cred:
            if len(cred["username"].strip()) == 0:
                errmsg = "The 'username' for an SSH credential cannot be empty."
                errors.append(errmsg)
        else:
            errmsg = "SSH credentials must have a 'username' field."
            errors.append(errmsg)

        if "password" not in cred and "keyfile" not in cred:
            errmsg = "SSH credentials must have a 'password' or 'keyfile' field."
            errors.append(errmsg)
        elif "keyfile" in cred:
            keyfile = os.path.abspath(os.path.expanduser(os.path.expandvars(cred["keyfile"])))
            if not os.path.exists(keyfile):
                errmsg = "The specified SSH keyfile does not exist. file=%s" % keyfile
                errors.append(errmsg)

        return errors, warnings
