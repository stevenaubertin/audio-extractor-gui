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
        self.root.geometry("750x700")

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

        # Time range controls
        ttk.Label(parent, text="Time Range (optional):").pack(
            anchor="w", pady=(10, 5)
        )
        
        time_frame = ttk.Frame(parent)
        time_frame.pack(fill="x", pady=(0, 5))
        
        # Start time
        ttk.Label(time_frame, text="Start:").pack(side="left")
        self.file_start_time_var = tk.StringVar()
        start_entry = ttk.Entry(time_frame, textvariable=self.file_start_time_var, width=12)
        start_entry.pack(side="left", padx=(5, 10))
        
        # End time
        ttk.Label(time_frame, text="End:").pack(side="left")
        self.file_end_time_var = tk.StringVar()
        end_entry = ttk.Entry(time_frame, textvariable=self.file_end_time_var, width=12)
        end_entry.pack(side="left", padx=(5, 10))
        
        # Duration
        ttk.Label(time_frame, text="Duration:").pack(side="left")
        self.file_duration_var = tk.StringVar()
        duration_entry = ttk.Entry(time_frame, textvariable=self.file_duration_var, width=12)
        duration_entry.pack(side="left", padx=(5, 0))
        
        # Help text for time formats
        ttk.Label(
            parent, 
            text="Format: HH:MM:SS, MM:SS, or seconds (e.g., 1:30, 90.5). Use End OR Duration, not both."
        ).pack(anchor="w", pady=(0, 10))

        # Output path selection
        ttk.Label(parent, text="Output Path (optional):").pack(
            anchor="w", pady=(10, 5)
        )

        output_path_frame = ttk.Frame(parent)
        output_path_frame.pack(fill="x", pady=(0, 10))

        self.file_output_path_var = tk.StringVar()
        ttk.Entry(
            output_path_frame, textvariable=self.file_output_path_var
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(
            output_path_frame,
            text="Browse",
            command=self.browse_output_path_file,
        ).pack(side="right")

        ttk.Label(
            parent, text="(leave empty for auto: output/filename.ext)"
        ).pack(anchor="w", pady=(0, 10))

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

        # Time range controls
        ttk.Label(parent, text="Time Range (optional):").pack(
            anchor="w", pady=(10, 5)
        )
        
        url_time_frame = ttk.Frame(parent)
        url_time_frame.pack(fill="x", pady=(0, 5))
        
        # Start time
        ttk.Label(url_time_frame, text="Start:").pack(side="left")
        self.url_start_time_var = tk.StringVar()
        url_start_entry = ttk.Entry(url_time_frame, textvariable=self.url_start_time_var, width=12)
        url_start_entry.pack(side="left", padx=(5, 10))
        
        # End time
        ttk.Label(url_time_frame, text="End:").pack(side="left")
        self.url_end_time_var = tk.StringVar()
        url_end_entry = ttk.Entry(url_time_frame, textvariable=self.url_end_time_var, width=12)
        url_end_entry.pack(side="left", padx=(5, 10))
        
        # Duration
        ttk.Label(url_time_frame, text="Duration:").pack(side="left")
        self.url_duration_var = tk.StringVar()
        url_duration_entry = ttk.Entry(url_time_frame, textvariable=self.url_duration_var, width=12)
        url_duration_entry.pack(side="left", padx=(5, 0))
        
        # Help text for time formats
        ttk.Label(
            parent, 
            text="Format: HH:MM:SS, MM:SS, or seconds (e.g., 1:30, 90.5). Use End OR Duration, not both."
        ).pack(anchor="w", pady=(0, 10))

        # Output path selection
        ttk.Label(parent, text="Output Path (optional):").pack(
            anchor="w", pady=(10, 5)
        )

        url_output_path_frame = ttk.Frame(parent)
        url_output_path_frame.pack(fill="x", pady=(0, 10))

        self.url_output_path_var = tk.StringVar()
        ttk.Entry(
            url_output_path_frame, textvariable=self.url_output_path_var
        ).pack(side="left", fill="x", expand=True, padx=(0, 5))
        ttk.Button(
            url_output_path_frame,
            text="Browse",
            command=self.browse_output_path_url,
        ).pack(side="right")

        ttk.Label(
            parent, text="(leave empty for auto: output/filename.ext)"
        ).pack(anchor="w", pady=(0, 10))

        # Extract button
        ttk.Button(
            parent, text="Extract Audio", command=self.extract_from_url
        ).pack(pady=20)

        # Progress and status
        self.url_progress = ttk.Progressbar(parent, mode="indeterminate")
        self.url_progress.pack(fill="x", pady=(10, 5))

        self.url_status = ttk.Label(parent, text="Ready")
        self.url_status.pack(anchor="w")

    def validate_time_inputs(self, start_time, end_time, duration):
        """Validate time range inputs.
        
        Returns:
            tuple: (is_valid, error_message, cleaned_start, cleaned_end, cleaned_duration)
        """
        # Clean up empty strings
        start_time = start_time.strip() if start_time else None
        end_time = end_time.strip() if end_time else None
        duration = duration.strip() if duration else None
        
        # Check for conflicting end time and duration
        if end_time and duration:
            return (False, "Please specify either End time OR Duration, not both.", None, None, None)
        
        # If end time or duration is specified, start time is required
        if (end_time or duration) and not start_time:
            return (False, "Start time is required when specifying End time or Duration.", None, None, None)
        
        # Basic format validation (more detailed validation happens in the core)
        import re
        time_pattern = r'^(?:\d{1,2}:)?\d{1,2}:\d{1,2}$|^\d+(?:\.\d+)?$'
        
        for time_val, name in [(start_time, "Start time"), (end_time, "End time"), (duration, "Duration")]:
            if time_val and not re.match(time_pattern, time_val):
                return (False, f"{name} format invalid. Use HH:MM:SS, MM:SS, or seconds.", None, None, None)
        
        return (True, None, start_time, end_time, duration)
    
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
            # Auto-populate output path if empty
            if not self.file_output_path_var.get():
                input_path = Path(filename)
                format_ext = self.format_var.get()
                suggested_path = (
                    Path("output") / f"{input_path.stem}.{format_ext}"
                )
                self.file_output_path_var.set(str(suggested_path))

    def browse_output_path_file(self):
        """Open save file dialog for file tab output path."""
        # Get current path or suggest one
        current_path = self.file_output_path_var.get()
        if current_path:
            initial_dir = str(Path(current_path).parent)
            initial_file = Path(current_path).name
        else:
            initial_dir = "output"
            initial_file = "audio.mp3"

        # File types based on supported formats
        filetypes = [
            ("MP3 files", "*.mp3"),
            ("WAV files", "*.wav"),
            ("FLAC files", "*.flac"),
            ("AAC files", "*.aac"),
            ("All files", "*.*"),
        ]

        filepath = filedialog.asksaveasfilename(
            title="Save Audio As",
            initialdir=initial_dir,
            initialfile=initial_file,
            filetypes=filetypes,
        )

        if filepath:
            self.file_output_path_var.set(filepath)

    def browse_output_path_url(self):
        """Open save file dialog for URL tab output path."""
        # Get current path or suggest one
        current_path = self.url_output_path_var.get()
        if current_path:
            initial_dir = str(Path(current_path).parent)
            initial_file = Path(current_path).name
        else:
            initial_dir = "output"
            initial_file = "audio.mp3"

        # File types based on supported formats
        filetypes = [
            ("MP3 files", "*.mp3"),
            ("WAV files", "*.wav"),
            ("FLAC files", "*.flac"),
            ("AAC files", "*.aac"),
            ("All files", "*.*"),
        ]

        filepath = filedialog.asksaveasfilename(
            title="Save Audio As",
            initialdir=initial_dir,
            initialfile=initial_file,
            filetypes=filetypes,
        )

        if filepath:
            self.url_output_path_var.set(filepath)

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

        # Validate time inputs
        is_valid, error_msg, start_time, end_time, duration = self.validate_time_inputs(
            self.file_start_time_var.get(),
            self.file_end_time_var.get(),
            self.file_duration_var.get()
        )
        
        if not is_valid:
            messagebox.showerror("Time Range Error", error_msg)
            return

        # Start extraction
        self.file_progress.start()
        status_text = "Extracting audio"
        if start_time:
            if end_time:
                status_text += f" from {start_time} to {end_time}"
            elif duration:
                status_text += f" from {start_time} for {duration}"
            else:
                status_text += f" starting from {start_time}"
        status_text += "..."
        self.file_status.config(text=status_text)

        try:
            # Get custom output path
            custom_output_path = self.file_output_path_var.get().strip()
            format_ext = self.format_var.get()

            if custom_output_path:
                # Use the specified output path
                output_path = Path(custom_output_path)

                # Ensure proper extension
                if (
                    not output_path.suffix
                    or output_path.suffix[1:] != format_ext
                ):
                    output_path = output_path.with_suffix(f".{format_ext}")

                # Create directory if it doesn't exist
                output_path.parent.mkdir(parents=True, exist_ok=True)

                # Use custom output directory and filename
                temp_extractor = AudioExtractor()
                temp_extractor.output_dir = output_path.parent

                # For custom paths, we'll handle the naming manually
                result = temp_extractor.extract_from_file(
                    file_path, 
                    self.format_var.get(), 
                    self.quality_var.get(),
                    start_time=start_time,
                    end_time=end_time,
                    duration=duration
                )

                final_output_path = str(output_path)
            else:
                # Use default behavior - let core module handle everything
                temp_extractor = AudioExtractor()
                result = temp_extractor.extract_from_file(
                    file_path, 
                    self.format_var.get(), 
                    self.quality_var.get(),
                    start_time=start_time,
                    end_time=end_time,
                    duration=duration
                )
                final_output_path = "output directory"

            if isinstance(result, dict) and result.get("success", False):
                success_msg = "Audio extraction completed successfully!"
                if custom_output_path:
                    success_msg += f"\nSaved to: {final_output_path}"
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

        # Validate time inputs
        is_valid, error_msg, start_time, end_time, duration = self.validate_time_inputs(
            self.url_start_time_var.get(),
            self.url_end_time_var.get(),
            self.url_duration_var.get()
        )
        
        if not is_valid:
            messagebox.showerror("Time Range Error", error_msg)
            return

        # Start extraction
        self.url_progress.start()
        status_text = "Downloading and extracting audio"
        if start_time:
            if end_time:
                status_text += f" from {start_time} to {end_time}"
            elif duration:
                status_text += f" from {start_time} for {duration}"
            else:
                status_text += f" starting from {start_time}"
        status_text += "..."
        self.url_status.config(text=status_text)

        try:
            # Get custom output path
            custom_output_path = self.url_output_path_var.get().strip()
            format_ext = self.url_format_var.get()

            if custom_output_path:
                # Use the specified output path
                output_path = Path(custom_output_path)

                # Ensure proper extension
                if (
                    not output_path.suffix
                    or output_path.suffix[1:] != format_ext
                ):
                    output_path = output_path.with_suffix(f".{format_ext}")

                # Create directory if it doesn't exist
                output_path.parent.mkdir(parents=True, exist_ok=True)

                # Use custom output directory
                temp_extractor = AudioExtractor()
                temp_extractor.output_dir = output_path.parent

                result = temp_extractor.extract_from_url(
                    url, 
                    self.url_format_var.get(), 
                    self.url_quality_var.get(),
                    start_time=start_time,
                    end_time=end_time,
                    duration=duration
                )

                final_output_path = str(output_path)
            else:
                # Use default behavior - let core module handle everything
                temp_extractor = AudioExtractor()
                result = temp_extractor.extract_from_url(
                    url, 
                    self.url_format_var.get(), 
                    self.url_quality_var.get(),
                    start_time=start_time,
                    end_time=end_time,
                    duration=duration
                )
                final_output_path = "output directory"

            if isinstance(result, dict) and result.get("success", False):
                success_msg = "Audio extraction completed successfully!"
                if custom_output_path:
                    success_msg += f"\nSaved to: {final_output_path}"
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
