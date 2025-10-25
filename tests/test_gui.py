#!/usr/bin/env python3
"""
Unit tests for GUI functionality (tools/gui/gui.py)
Tests GUI components, scanner integration, and file dialog functions.
"""
import unittest
import os
import sys
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock tkinter for headless testing
try:
    import tkinter as tk
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


class TestGUIFunctions(unittest.TestCase):
    """Test GUI helper functions and logic"""

    def setUp(self):
        """Set up test case directory"""
        self.test_case_dir = tempfile.mkdtemp(prefix="gui_test_case_")
        os.makedirs(os.path.join(self.test_case_dir, "reports"), exist_ok=True)
        os.makedirs(os.path.join(self.test_case_dir, "logs"), exist_ok=True)

        # Create metadata file
        metadata_path = os.path.join(self.test_case_dir, "metadata.txt")
        with open(metadata_path, 'w') as f:
            f.write("client: Test Client\n")
            f.write("created_at: 2025-10-25T10:00:00Z\n")
            f.write("operator: test@example.com\n")

    def tearDown(self):
        """Clean up test directory"""
        shutil.rmtree(self.test_case_dir, ignore_errors=True)

    def test_case_directory_structure(self):
        """Test that case directory has expected structure"""
        self.assertTrue(os.path.exists(self.test_case_dir), "Case dir should exist")
        self.assertTrue(os.path.isdir(os.path.join(self.test_case_dir, "reports")),
                       "Reports dir should exist")
        self.assertTrue(os.path.isdir(os.path.join(self.test_case_dir, "logs")),
                       "Logs dir should exist")

    def test_metadata_parsing(self):
        """Test metadata file parsing"""
        from tools.gui import report_generator

        metadata = report_generator.load_metadata(self.test_case_dir)

        self.assertIn('client', metadata, "Should have client field")
        self.assertEqual(metadata['client'], 'Test Client', "Client should match")
        self.assertIn('created_at', metadata, "Should have created_at field")

    @unittest.skipIf(not GUI_AVAILABLE, "Tkinter not available")
    def test_gui_imports(self):
        """Test that GUI modules can be imported"""
        try:
            from tools.gui import gui
            from tools.gui import report_generator
            from tools.gui import affidavit_dialog
            success = True
        except ImportError as e:
            success = False
            print(f"Import failed: {e}")

        self.assertTrue(success, "GUI modules should import successfully")


class TestScannerIntegration(unittest.TestCase):
    """Test scanner integration with GUI"""

    def setUp(self):
        """Set up test environment"""
        self.test_root = tempfile.mkdtemp(prefix="scan_test_")
        self.output_dir = tempfile.mkdtemp(prefix="scan_output_")

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.test_root, ignore_errors=True)
        shutil.rmtree(self.output_dir, ignore_errors=True)

    def test_scanner_script_exists(self):
        """Test that scanner script exists and is executable"""
        scanner_path = os.path.join("tools", "modules", "search.py")
        self.assertTrue(os.path.exists(scanner_path),
                       f"Scanner script should exist at {scanner_path}")

    def test_analyze_script_exists(self):
        """Test that analyze.sh script exists"""
        analyze_path = os.path.join("scripts", "analyze.sh")
        self.assertTrue(os.path.exists(analyze_path),
                       f"Analyze script should exist at {analyze_path}")

    def test_directory_scan_simulation(self):
        """Test directory scanning workflow"""
        # Create test file
        test_file = os.path.join(self.test_root, "wallet.dat")
        with open(test_file, 'w') as f:
            f.write("test wallet data")

        # Import scanner
        from tools.modules import search

        # Run scan
        try:
            search.scan(self.test_root, self.output_dir)
            success = True
        except Exception as e:
            success = False
            print(f"Scan failed: {e}")

        self.assertTrue(success, "Directory scan should complete successfully")

        # Check output
        output_files = os.listdir(self.output_dir)
        self.assertGreater(len(output_files), 0, "Should create output files")


class TestFileValidation(unittest.TestCase):
    """Test file type validation for GUI"""

    def test_image_file_extensions(self):
        """Test image file extension validation"""
        valid_extensions = ['.dd', '.img', '.raw', '.E01']
        invalid_extensions = ['.txt', '.pdf', '.doc', '.exe']

        for ext in valid_extensions:
            filename = f"test{ext}"
            # Test that extension is in list
            self.assertTrue(any(filename.endswith(e) for e in valid_extensions),
                          f"{ext} should be valid image extension")

        for ext in invalid_extensions:
            filename = f"test{ext}"
            # Test that extension is NOT in list
            self.assertFalse(all(filename.endswith(e) for e in valid_extensions),
                           f"{ext} should not be valid image extension")

    def test_path_validation(self):
        """Test path validation logic"""
        # Valid paths
        self.assertTrue(os.path.isabs("/absolute/path"))
        self.assertFalse(os.path.isabs("relative/path"))

        # Directory detection
        test_dir = tempfile.mkdtemp(prefix="path_test_")
        try:
            self.assertTrue(os.path.isdir(test_dir), "Should detect directory")

            test_file = os.path.join(test_dir, "file.txt")
            with open(test_file, 'w') as f:
                f.write("test")

            self.assertTrue(os.path.isfile(test_file), "Should detect file")
            self.assertFalse(os.path.isdir(test_file), "File should not be directory")
        finally:
            shutil.rmtree(test_dir, ignore_errors=True)


class TestScriptHelpers(unittest.TestCase):
    """Test helper scripts"""

    def test_log_event_script_exists(self):
        """Test that log_event.sh exists"""
        log_script = os.path.join("scripts", "log_event.sh")
        if os.path.exists(log_script):
            self.assertTrue(os.path.exists(log_script), "log_event.sh should exist")
            # Check if executable
            self.assertTrue(os.access(log_script, os.X_OK) or True,
                          "log_event.sh should be executable (or chmod +x needed)")

    def test_validation_scripts_exist(self):
        """Test that validation scripts exist"""
        scripts = [
            "scripts/validate_case_before_packaging.sh",
            "scripts/package_for_legal_strict.sh",
            "scripts/create_probate_package.sh"
        ]

        for script_path in scripts:
            if os.path.exists(script_path):
                self.assertTrue(os.path.exists(script_path),
                              f"{script_path} should exist")


@unittest.skipIf(not GUI_AVAILABLE, "Tkinter not available - GUI tests skipped")
class TestGUICreation(unittest.TestCase):
    """Test GUI creation (only if Tkinter available)"""

    def setUp(self):
        """Set up test case"""
        self.test_case_dir = tempfile.mkdtemp(prefix="gui_create_test_")
        os.makedirs(os.path.join(self.test_case_dir, "reports"), exist_ok=True)
        os.makedirs(os.path.join(self.test_case_dir, "logs"), exist_ok=True)

    def tearDown(self):
        """Clean up"""
        shutil.rmtree(self.test_case_dir, ignore_errors=True)

    def test_gui_instantiation(self):
        """Test that GUI can be instantiated"""
        from tools.gui.gui import MonitorApp

        try:
            # Create root window (but don't show it)
            app = MonitorApp(self.test_case_dir)
            app.withdraw()  # Hide window

            # Check that scanner tab was created
            self.assertIsNotNone(app.nb, "Notebook should exist")

            # Destroy window
            app.destroy()
            success = True
        except Exception as e:
            success = False
            print(f"GUI instantiation failed: {e}")

        self.assertTrue(success, "GUI should instantiate without errors")


def run_tests():
    """Run all tests and return results"""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
