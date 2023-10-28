import unittest
import test_accounts_routes
import test_auth_routes
import test_github_api_wrapper_script
import test_db_crud_script
import test_projects_routes

if __name__ == '__main__':
    # create a test suite
    suite = unittest.TestSuite()

    # add the tests from each module in the order they were imported
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(test_accounts_routes))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(test_auth_routes))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(test_github_api_wrapper_script))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(test_db_crud_script))
    suite.addTests(unittest.defaultTestLoader.loadTestsFromModule(test_projects_routes))

    # run the test suite
    unittest.TextTestRunner().run(suite)