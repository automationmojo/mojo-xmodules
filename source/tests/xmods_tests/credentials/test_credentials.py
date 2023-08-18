
import os
import tempfile
import unittest

from mojo.xmods.xcollections.context import Context, ContextPaths

from mojo.xmods.credentials.credentialmanager import CredentialManager
from mojo.xmods.credentials.sshcredential import is_ssh_credential

CREDENTIAL_CONTENT = """
credentials:
    -   identifier: adminuser
        category:
            - basic
            - ssh
        username: adminuser
        password: "something"
    
    -   identifier: datauser
        category: basic
        username: datauser
        password: "datadata"

    -   identifier: pi-cluster
        category: ssh
        username: pi
        password: "pipass"
        primitive: True
"""

class TestCredentials(unittest.TestCase):

    def setUp(self) -> None:
        self._cred_file = tempfile.mktemp(suffix=".yaml")

        with open(self._cred_file, 'w') as cf:
            cf.write(CREDENTIAL_CONTENT)

        credential_files = [self._cred_file]
        context = Context()

        context.insert(ContextPaths.CONFIG_CREDENTIAL_FILES, credential_files)
        return
    
    def tearDown(self) -> None:
        os.remove(self._cred_file)
        return
    
    def test_initialize_credentials(self):

        cred_mgr = CredentialManager()

        credentials = cred_mgr.credentials

        assert "adminuser" in credentials, "There should have been a 'adminuser' credential."
        assert "datauser" in credentials, "There should have been a 'datauser' credential."
        assert "pi-cluster" in credentials, "There should have been a 'pi-cluster' credential."

        admincred = credentials["adminuser"]

        assert "basic" in admincred.categories, "The 'adminuser' credential should include the 'basic' category."
        assert "ssh" in admincred.categories, "The 'adminuser' credential should include the 'basic' category."

        assert is_ssh_credential(admincred), "The 'adminuser' should be considered an SSH credential."

        return

if __name__ == '__main__':
    unittest.main()
