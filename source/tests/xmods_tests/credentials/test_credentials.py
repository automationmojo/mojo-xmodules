
import os
import tempfile
import unittest

from mojo.xmods.xcollections.context import Context, ContextPaths
from mojo.xmods.credentials.credentialmanager import CredentialManager

CREDENTIAL_CONTENT = """
credentials:
    -   identifier: adminuser
        category:
            - basic
            - ssh
        username: adminuser
        password: "AdminData!!"
    
    -   identifier: datauser
        category: basic
        username: datauser
        password: "Acess2Data!!"

    -   identifier: pi-cluster
        category: ssh
        username: pi
        password: "Skate4Fun@@"
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

        return

if __name__ == '__main__':
    unittest.main()
