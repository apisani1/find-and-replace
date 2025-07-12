#!/usr/bin/env python3
"""
Test suite for find-and-replace script with mocked file operations.
"""

from unittest.mock import (
    Mock,
    mock_open,
    patch,
)

import pytest

from find_and_replace.main import (
    Colors,
    find_files,
    main,
    print_colored,
    process_file,
)


class TestFindFiles:
    """Test cases for the find_files function."""

    @patch("find_and_replace.main.os.path.isfile", return_value=True)
    @patch("find_and_replace.main.Path")
    @patch("find_and_replace.main.glob.glob")
    def test_find_files_non_recursive(self, mock_glob, mock_path, mock_isfile):  # type: ignore[no-untyped-def]  # pylint: disable=unused-argument
        """Test finding files non-recursively."""
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = True
        mock_path.return_value = mock_path_instance

        mock_glob.return_value = ["/test/file1.py", "/test/file2.py"]

        result = find_files("*.py", "/test", recursive=False)

        assert result == ["/test/file1.py", "/test/file2.py"]
        mock_glob.assert_called_once_with("/test/*.py")

    @patch("find_and_replace.main.Path")
    def test_find_files_recursive(self, mock_path):  # type: ignore[no-untyped-def]
        """Test finding files recursively."""
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = True

        mock_file1 = Mock()
        mock_file1.is_file.return_value = True
        mock_file1.__str__ = lambda self: "/test/file1.py"

        mock_file2 = Mock()
        mock_file2.is_file.return_value = True
        mock_file2.__str__ = lambda self: "/test/subdir/file2.py"

        mock_path_instance.rglob.return_value = [mock_file1, mock_file2]
        mock_path.return_value = mock_path_instance

        result = find_files("*.py", "/test", recursive=True)

        assert result == ["/test/file1.py", "/test/subdir/file2.py"]
        mock_path_instance.rglob.assert_called_once_with("*.py")

    @patch("find_and_replace.main.Path")
    @patch("find_and_replace.main.print_colored")
    def test_find_files_directory_not_exists(self, mock_print, mock_path):  # type: ignore[no-untyped-def]
        """Test finding files when directory doesn't exist."""
        mock_path_instance = Mock()
        mock_path_instance.exists.return_value = False
        mock_path.return_value = mock_path_instance

        result = find_files("*.py", "/nonexistent", recursive=False)

        assert result == []
        mock_print.assert_called_once_with("Error: Directory '/nonexistent' does not exist.", Colors.RED)


class TestProcessFile:
    """Test cases for the process_file function."""

    @patch("builtins.open", new_callable=mock_open, read_data="def old_function():\n    pass\n")
    @patch("find_and_replace.main.print_colored")
    def test_process_file_with_matches_no_confirm(self, mock_print, mock_file):  # type: ignore[no-untyped-def]  # pylint: disable=unused-argument
        """Test processing file with matches and no confirmation."""
        result = process_file("/test/file.py", "old_function", "new_function", no_confirm=True)

        assert result is True
        mock_file.assert_called()

        write_calls = list(mock_file().write.call_args_list)
        assert len(write_calls) == 1
        written_content = write_calls[0][0][0]
        assert "new_function" in written_content
        assert "old_function" not in written_content

    @patch("builtins.open", new_callable=mock_open, read_data="def some_function():\n    pass\n")
    @patch("find_and_replace.main.print_colored")
    def test_process_file_no_matches(self, mock_print, mock_file):  # type: ignore[no-untyped-def]  # pylint: disable=unused-argument
        """Test processing file with no matches."""
        result = process_file("/test/file.py", "nonexistent_pattern", "replacement", no_confirm=True)

        assert result is False
        mock_print.assert_called_with("No matches found in: /test/file.py", Colors.YELLOW)

    @patch("builtins.open", new_callable=mock_open, read_data="def old_function():\n    pass\n")
    @patch("builtins.input", return_value="y")
    @patch("find_and_replace.main.print_colored")
    def test_process_file_with_confirmation_yes(  # type: ignore[no-untyped-def]
        self, mock_print, mock_input, mock_file  # pylint: disable=unused-argument
    ):
        """Test processing file with confirmation (user says yes)."""
        result = process_file("/test/file.py", "old_function", "new_function", no_confirm=False)

        assert result is True
        mock_input.assert_called()

    @patch("builtins.open", new_callable=mock_open, read_data="def old_function():\n    pass\n")
    @patch("builtins.input", return_value="n")
    @patch("find_and_replace.main.print_colored")
    def test_process_file_with_confirmation_no(  # type: ignore[no-untyped-def]
        self, mock_print, mock_input, mock_file
    ):  # pylint: disable=unused-argument
        """Test processing file with confirmation (user says no)."""
        result = process_file("/test/file.py", "old_function", "new_function", no_confirm=False)

        assert result is False
        mock_print.assert_called_with("Skipping file.", Colors.YELLOW)

    @patch("builtins.open", new_callable=mock_open, read_data="def old_function():\n    pass\n")
    @patch("builtins.input", return_value="q")
    @patch("find_and_replace.main.print_colored")
    def test_process_file_with_confirmation_quit(  # type: ignore[no-untyped-def]
        self, mock_print, mock_input, mock_file
    ):  # pylint: disable=unused-argument
        """Test processing file with confirmation (user quits)."""
        with pytest.raises(SystemExit):
            process_file("/test/file.py", "old_function", "new_function", no_confirm=False)

    @patch("find_and_replace.main.print_colored")
    def test_process_file_invalid_regex(self, mock_print):  # type: ignore[no-untyped-def]
        """Test processing file with invalid regex pattern."""
        result = process_file("/test/file.py", "[invalid", "replacement", no_confirm=True)

        assert result is False
        mock_print.assert_called()

    @patch("builtins.open", side_effect=PermissionError("Permission denied"))
    @patch("find_and_replace.main.print_colored")
    def test_process_file_permission_error(self, mock_print, mock_file):  # type: ignore[no-untyped-def]  # pylint: disable=unused-argument
        """Test processing file with permission error."""
        result = process_file("/test/file.py", "pattern", "replacement", no_confirm=True)

        assert result is False
        mock_print.assert_called_with("Error: Permission denied accessing file '/test/file.py'", Colors.RED)

    @patch("builtins.open", side_effect=UnicodeDecodeError("utf-8", b"", 0, 1, "invalid"))
    @patch("find_and_replace.main.print_colored")
    def test_process_file_unicode_error(self, mock_print, mock_file):  # type: ignore[no-untyped-def]  # pylint: disable=unused-argument
        """Test processing file with unicode decode error."""
        result = process_file("/test/file.py", "pattern", "replacement", no_confirm=True)

        assert result is False
        mock_print.assert_called_with(
            "Error: Cannot read file '/test/file.py' - not a text file or encoding issue", Colors.RED
        )


class TestMain:
    """Test cases for the main function."""

    @patch("sys.argv", ["find-and-replace", "*.py", "/test", "old", "new", "-n"])
    @patch("find_and_replace.main.find_files", return_value=["/test/file1.py", "/test/file2.py"])
    @patch("find_and_replace.main.process_file", return_value=True)
    @patch("find_and_replace.main.print_colored")
    def test_main_no_confirm(self, mock_print, mock_process, mock_find):  # type: ignore[no-untyped-def]  # pylint: disable=unused-argument
        """Test main function with no confirmation flag."""
        main()

        assert mock_find.call_count == 1
        assert mock_process.call_count == 2

    @patch("sys.argv", ["find-and-replace", "*.py", "/test", "old", "new", "--dry-run"])
    @patch("find_and_replace.main.find_files", return_value=["/test/file1.py"])
    @patch("builtins.open", new_callable=mock_open, read_data="def old_function():\n    pass\n")
    @patch("find_and_replace.main.print_colored")
    def test_main_dry_run(self, mock_print, mock_file, mock_find):  # type: ignore[no-untyped-def]  # pylint: disable=unused-argument
        """Test main function with dry run flag."""
        main()

        mock_find.assert_called_once()
        mock_print.assert_called()

    @patch("sys.argv", ["find-and-replace", "*.py", "/test", "[invalid", "new"])
    @patch("find_and_replace.main.print_colored")
    def test_main_invalid_regex(self, mock_print):  # type: ignore[no-untyped-def]  # pylint: disable=unused-argument
        """Test main function with invalid regex."""
        with pytest.raises(SystemExit):
            main()

    @patch("sys.argv", ["find-and-replace", "*.py", "/test", "old", "new"])
    @patch("find_and_replace.main.find_files", return_value=[])
    @patch("find_and_replace.main.print_colored")
    def test_main_no_files_found(self, mock_print, mock_find):  # type: ignore[no-untyped-def]  # pylint: disable=unused-argument
        """Test main function when no files are found."""
        with pytest.raises(SystemExit):
            main()

        mock_print.assert_called_with("No matching files found.", Colors.YELLOW)

    @patch("sys.argv", ["find-and-replace", "*.py", "/test", "old", "new"])
    @patch("find_and_replace.main.find_files", return_value=["/test/file1.py"])
    @patch("builtins.input", return_value="n")
    @patch("find_and_replace.main.print_colored")
    def test_main_user_cancellation(self, mock_print, mock_input, mock_find):  # type: ignore[no-untyped-def] # pylint: disable=unused-argument
        """Test main function when user cancels operation."""
        with pytest.raises(SystemExit):
            main()

        mock_print.assert_called_with("Operation cancelled.", Colors.YELLOW)


class TestPrintColored:
    """Test cases for the print_colored function."""

    @patch("builtins.print")
    def test_print_colored_with_color(self, mock_print):  # type: ignore[no-untyped-def]
        """Test printing with color."""
        print_colored("test message", Colors.GREEN)

        expected = f"{Colors.GREEN.value}test message{Colors.NC.value}"
        mock_print.assert_called_once_with(expected)

    @patch("builtins.print")
    def test_print_colored_no_color(self, mock_print):  # type: ignore[no-untyped-def]
        """Test printing without color."""
        print_colored("test message")

        expected = f"{Colors.NC.value}test message{Colors.NC.value}"
        mock_print.assert_called_once_with(expected)


if __name__ == "__main__":
    pytest.main([__file__])
