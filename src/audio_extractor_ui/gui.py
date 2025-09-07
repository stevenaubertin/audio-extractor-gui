"""
GUI interface for the audio extractor.
"""

import sys
from pathlib import Path

try:
    import tkinter as tk
    from tkinter import ttk, filedialog, messagebox

    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

from .core import AudioExtractor
from .utils import (
    validate_file_path,
    validate_url,
    is_video_file,
    sanitize_filename,
)


class AudioExtractorGUI:
    """Main GUI application class."""

    def __init__(self):
        """Initialize the GUI application."""
        if not GUI_AVAILABLE:
            raise ImportError("GUI dependencies (tkinter) not available")

        self.root = tk.Tk()
        self.root.title("Audio Extractor UI")
        self.root.geometry("700x600")

        # Initialize core functionality
        self.extractor = AudioExtractor()

        # Setup GUI
        self.setup_gui()

    def setup_gui(self):
        """Set up the GUI components."""
        # Create notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # File extraction tab
        file_frame = ttk.Frame(notebook)
        notebook.add(file_frame, text="File Extraction")
        self.setup_file_tab(file_frame)

        # URL extraction tab
        url_frame = ttk.Frame(notebook)
        notebook.add(url_frame, text="URL Extraction")
        self.setup_url_tab(url_frame)

    def setup_file_tab(self, parent):
        """Set up the file extraction tab."""
        # File selection
        ttk.Label(parent, text="Select Video File:").pack(
            anchor="w", pady=(10, 5)
        )

        file_frame = ttk.Frame(parent)
        file_frame.pack(fill="x", pady=(0, 10))

        self.file_path_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.file_path_var).pack(
            side="left", fill="x", expand=True, padx=(0, 5)
        )
        ttk.Button(file_frame, text="Browse", command=self.browse_file).pack(
            side="right"
        )

        # Format selection
        ttk.Label(parent, text="Output Format:").pack(anchor="w", pady=(10, 5))
        self.format_var = tk.StringVar(value="mp3")
        format_combo = ttk.Combobox(
            parent,
            textvariable=self.format_var,
            values=self.extractor.get_supported_formats(),
        )
        format_combo.pack(fill="x", pady=(0, 10))

        # Quality selection
        ttk.Label(parent, text="Quality:").pack(anchor="w", pady=(10, 5))
        self.quality_var = tk.StringVar(value="high")
        quality_combo = ttk.Combobox(
            parent,
            textvariable=self.quality_var,
            values=self.extractor.get_quality_options(),
        )
        quality_combo.pack(fill="x", pady=(0, 10))

        # Output directory selection
        ttk.Label(parent, text="Output Directory:").pack(
            anchor="w", pady=(10, 5)
        )

        output_dir_frame = ttk.Frame(parent)
        output_dir_frame.pack(fill="x", pady=(0, 10))

        self.file_output_dir_var = tk.StringVar(value="output")
        ttk.Entry(
            output_dir_frame, textvariable=self.file_output_dir_var
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(
            output_dir_frame,
            text="Browse",
            command=self.browse_output_dir_file,
        ).pack(side="right")

        # Output filename
        ttk.Label(parent, text="Output Filename (optional):").pack(
            anchor="w", pady=(10, 5)
        )

        filename_frame = ttk.Frame(parent)
        filename_frame.pack(fill="x", pady=(0, 10))

        self.file_output_name_var = tk.StringVar()
        ttk.Entry(filename_frame, textvariable=self.file_output_name_var).pack(
            side="left", fill="x", expand=True, padx=(0, 5)
        )

        ttk.Label(filename_frame, text="(leave empty for auto)").pack(
            side="right", anchor="e"
        )

        # Extract button
        ttk.Button(
            parent, text="Extract Audio", command=self.extract_from_file
        ).pack(pady=20)

        # Progress and status
        self.file_progress = ttk.Progressbar(parent, mode="indeterminate")
        self.file_progress.pack(fill="x", pady=(10, 5))

        self.file_status = ttk.Label(parent, text="Ready")
        self.file_status.pack(anchor="w")

    def setup_url_tab(self, parent):
        """Set up the URL extraction tab."""
        # URL input
        ttk.Label(parent, text="Enter Video URL:").pack(
            anchor="w", pady=(10, 5)
        )

        self.url_var = tk.StringVar()
        ttk.Entry(parent, textvariable=self.url_var).pack(
            fill="x", pady=(0, 10)
        )

        # Format selection
        ttk.Label(parent, text="Output Format:").pack(anchor="w", pady=(10, 5))
        self.url_format_var = tk.StringVar(value="mp3")
        format_combo = ttk.Combobox(
            parent,
            textvariable=self.url_format_var,
            values=self.extractor.get_supported_formats(),
        )
        format_combo.pack(fill="x", pady=(0, 10))

        # Quality selection
        ttk.Label(parent, text="Quality:").pack(anchor="w", pady=(10, 5))
        self.url_quality_var = tk.StringVar(value="high")
        quality_combo = ttk.Combobox(
            parent,
            textvariable=self.url_quality_var,
            values=self.extractor.get_quality_options(),
        )
        quality_combo.pack(fill="x", pady=(0, 10))

        # Output directory selection
        ttk.Label(parent, text="Output Directory:").pack(
            anchor="w", pady=(10, 5)
        )

        url_output_dir_frame = ttk.Frame(parent)
        url_output_dir_frame.pack(fill="x", pady=(0, 10))

        self.url_output_dir_var = tk.StringVar(value="output")
        ttk.Entry(
            url_output_dir_frame, textvariable=self.url_output_dir_var
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(
            url_output_dir_frame,
            text="Browse",
            command=self.browse_output_dir_url,
        ).pack(side="right")

        # Output filename
        ttk.Label(parent, text="Output Filename (optional):").pack(
            anchor="w", pady=(10, 5)
        )

        url_filename_frame = ttk.Frame(parent)
        url_filename_frame.pack(fill="x", pady=(0, 10))

        self.url_output_name_var = tk.StringVar()
        ttk.Entry(
            url_filename_frame, textvariable=self.url_output_name_var
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))

        ttk.Label(url_filename_frame, text="(leave empty for auto)").pack(
            side="right", anchor="e"
        )

        # Extract button
        ttk.Button(
            parent, text="Extract Audio", command=self.extract_from_url
        ).pack(pady=20)

        # Progress and status
        self.url_progress = ttk.Progressbar(parent, mode="indeterminate")
        self.url_progress.pack(fill="x", pady=(10, 5))

        self.url_status = ttk.Label(parent, text="Ready")
        self.url_status.pack(anchor="w")

    def browse_file(self):
        """Open file browser dialog."""
        filetypes = [
            (
                "Video files",
                "*.mp4 *.avi *.mkv *.mov *.wmv *.flv *.webm *.m4v",
            ),
            ("All files", "*.*"),
        ]

        filename = filedialog.askopenfilename(
            title="Select Video File", filetypes=filetypes
        )

        if filename:
            self.file_path_var.set(filename)
            # Auto-populate output filename if empty
            if not self.file_output_name_var.get():
                input_path = Path(filename)
                self.file_output_name_var.set(input_path.stem)

    def browse_output_dir_file(self):
        """Open directory browser dialog for file tab output."""
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.file_output_dir_var.get(),
        )

        if directory:
            self.file_output_dir_var.set(directory)

    def browse_output_dir_url(self):
        """Open directory browser dialog for URL tab output."""
        directory = filedialog.askdirectory(
            title="Select Output Directory",
            initialdir=self.url_output_dir_var.get(),
        )

        if directory:
            self.url_output_dir_var.set(directory)

    def extract_from_file(self):
        """Extract audio from selected file."""
        file_path = self.file_path_var.get()

        if not file_path:
            messagebox.showerror("Error", "Please select a video file")
            return

        if not validate_file_path(file_path):
            messagebox.showerror(
                "Error", "Invalid file path or file does not exist"
            )
            return

        if not is_video_file(file_path):
            if not messagebox.askyesno(
                "Warning",
                "Selected file may not be a video file. Continue anyway?",
            ):
                return

        # Start extraction
        self.file_progress.start()
        self.file_status.config(text="Extracting audio...")

        try:
            # Get custom output settings
            output_dir = self.file_output_dir_var.get().strip() or "output"
            custom_filename = self.file_output_name_var.get().strip()
            format_ext = self.format_var.get()

            # Create output directory if it doesn't exist
            Path(output_dir).mkdir(parents=True, exist_ok=True)

            # Prepare filename
            if custom_filename:
                # Sanitize custom filename and ensure proper extension
                safe_filename = sanitize_filename(custom_filename)
                if not safe_filename.endswith(f".{format_ext}"):
                    safe_filename += f".{format_ext}"
                output_path = str(Path(output_dir) / safe_filename)
            else:
                output_path = None  # Let core module handle auto-naming

            # Create a temporary AudioExtractor with custom output directory
            temp_extractor = AudioExtractor()
            temp_extractor.output_dir = Path(output_dir)

            result = temp_extractor.extract_from_file(
                file_path, self.format_var.get(), self.quality_var.get()
            )

            if isinstance(result, dict) and result.get("success", False):
                success_msg = "Audio extraction completed successfully!"
                if output_dir != "output":
                    success_msg += f"\nSaved to: {output_dir}"
                messagebox.showinfo("Success", success_msg)
                self.file_status.config(text="Extraction completed")
            else:
                error_msg = "Audio extraction failed"
                if isinstance(result, dict) and result.get("error"):
                    error_msg += f": {result['error']}"
                messagebox.showerror("Error", error_msg)
                self.file_status.config(text="Extraction failed")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.file_status.config(text="Error occurred")

        finally:
            self.file_progress.stop()

    def extract_from_url(self):
        """Extract audio from URL."""
        url = self.url_var.get().strip()

        if not url:
            messagebox.showerror("Error", "Please enter a video URL")
            return

        if not validate_url(url):
            if not messagebox.askyesno(
                "Warning", "URL format may be invalid. Continue anyway?"
            ):
                return

        # Start extraction
        self.url_progress.start()
        self.url_status.config(text="Downloading and extracting audio...")

        try:
            # Get custom output settings
            output_dir = self.url_output_dir_var.get().strip() or "output"
            custom_filename = self.url_output_name_var.get().strip()
            format_ext = self.url_format_var.get()

            # Create output directory if it doesn't exist
            Path(output_dir).mkdir(parents=True, exist_ok=True)

            # Create a temporary AudioExtractor with custom output directory
            temp_extractor = AudioExtractor()
            temp_extractor.output_dir = Path(output_dir)

            result = temp_extractor.extract_from_url(
                url, self.url_format_var.get(), self.url_quality_var.get()
            )

            if isinstance(result, dict) and result.get("success", False):
                success_msg = "Audio extraction completed successfully!"
                if output_dir != "output":
                    success_msg += f"\nSaved to: {output_dir}"
                messagebox.showinfo("Success", success_msg)
                self.url_status.config(text="Extraction completed")
            else:
                error_msg = "Audio extraction failed"
                if isinstance(result, dict) and result.get("error"):
                    error_msg += f": {result['error']}"
                messagebox.showerror("Error", error_msg)
                self.url_status.config(text="Extraction failed")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.url_status.config(text="Error occurred")

        finally:
            self.url_progress.stop()

    def run(self):
        """Start the GUI application."""
        self.root.mainloop()


def run_gui():
    """Run the GUI application."""
    try:
        app = AudioExtractorGUI()
        app.run()
    except Exception as e:
        print(f"Failed to start GUI: {e}")
        sys.exit(1)
