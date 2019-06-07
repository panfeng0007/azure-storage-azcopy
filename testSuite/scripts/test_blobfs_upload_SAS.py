import unittest
import os
import utility as util

class BlobFs_Upload_SAS_User_Scenarios(unittest.TestCase):
    def setUp(self):
        self.cachedAzCopyOAuthTokenInfo = os.environ['AZCOPY_OAUTH_TOKEN_INFO']
        os.environ['AZCOPY_OAUTH_TOKEN_INFO'] = ''
        self.cachedAccountName = os.environ['ACCOUNT_NAME']
        os.environ['ACCOUNT_NAME'] = ''
        self.cachedAccountKey = os.environ['ACCOUNT_KEY']
        os.environ['ACCOUNT_KEY'] = ''

    def tearDown(self):
        os.environ['AZCOPY_OAUTH_TOKEN_INFO'] = self.cachedAzCopyOAuthTokenInfo
        os.environ['ACCOUNT_NAME'] = self.cachedAccountName
        os.environ['ACCOUNT_KEY'] = self.cachedAccountKey

    def test_blobfs_sas_upload_1Kb_file(self):
        # Create file of size 1KB
        filename = "test_blobfs_sas_d_1kb_file.txt"
        file_path = util.create_test_file(filename, 1024)
        # Upload the file using azCopy
        result = util.Command("copy").add_arguments(file_path).add_arguments(util.test_bfs_sas_account_url). \
            add_flags("log-level", "Info").execute_azcopy_copy_command()
        self.assertTrue(result)

        # Validate the uploaded file
        file_url = util.get_resource_sas(filename)
        result = util.Command("testFile").add_arguments(file_path).add_arguments(file_url).execute_azcopy_verify()
        self.assertTrue(result)

    def test_blobfs_sas_upload_64MB_file(self):
        # Create file of size 1KB
        filename = "test_blobfs_sas_d_64MB_file.txt"
        file_path = util.create_test_file(filename, 64 * 1024 * 1024)
        # Upload the file using azCopy
        result = util.Command("copy").add_arguments(file_path).add_arguments(util.test_bfs_sas_account_url). \
            add_flags("log-level", "Info").execute_azcopy_copy_command()
        self.assertTrue(result)

        # Validate the uploaded file
        file_url = util.get_resource_sas(filename)
        result = util.Command("testFile").add_arguments(file_path).add_arguments(file_url).execute_azcopy_verify()
        self.assertTrue(result)

    def test_blobfs_sas_upload_100_1kb_file(self):
        # Create dir with 100 1kb files inside it
        dir_name = "dir_blobfs_sas_d_100_1K"
        dir_n_file_path = util.create_test_n_files(1024, 100, dir_name)

        # Upload the directory with 100 files inside it
        result = util.Command("copy").add_arguments(dir_n_file_path).add_arguments(util.test_bfs_sas_account_url). \
            add_flags("log-level", "Info").add_flags("recursive", "true").execute_azcopy_copy_command()
        self.assertTrue(result)

        # Validate the uploaded directory
        dirUrl = util.get_resource_sas(util.test_bfs_sas_account_url)
        result = util.Command("testBlobFS").add_arguments(dir_n_file_path).add_arguments(dirUrl). \
            add_flags("is-object-dir", "true").add_flags("recursive", "true").execute_azcopy_copy_command()
        self.assertTrue(result)