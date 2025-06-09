#!/usr/bin/env python3
"""
AWE Electronics Online Store - Main Application
==============================================

A modern e-commerce management system built with Python and Tkinter.
This enhanced version includes improved GUI design, better error handling,
and comprehensive functionality for both customers and administrators.

Features:
- Modern, responsive GUI design that maintains window sizing
- Customer shopping experience with cart management
- Admin dashboard with inventory and sales management
- Secure user authentication and registration
- Real-time inventory tracking
- Comprehensive sales reporting
- Enhanced error handling and validation

Author: AWE Electronics Development Team
"""-

import sys
import os
import tkinter as tk
from tkinter import messagebox
import json
from pathlib import Path
import logging
from datetime import datetime
import traceback

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure logging
log_dir = Path("logs")
log_dir.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f"awe_electronics_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class AWEElectronicsApp:
    """Main application class for AWE Electronics Online Store"""
    
    def __init__(self):
        self.app_name = "AWE Electronics Online Store"
        self.version = "3.1"
        self.data_dir = Path("data")
        self.required_files = [
            "users.json",
            "products.json", 
            "orders.json"
        ]
        
    def display_startup_info(self):
        """Display enhanced startup information"""
        print("=" * 70)
        print(f" {self.app_name.upper()}")
        print("=" * 70)
        print(f"Version: {self.version} - Enhanced Responsive GUI Edition")
        print(f"Python Version: {sys.version.split()[0]}")
        print(f"Platform: {sys.platform}")
        print()
        print(" Features in v3.1:")
        print("  • Fixed login authentication with correct credentials")
        print("  • Improved responsive GUI design")
        print("  • Enhanced window management and sizing")
        print("  • Better error handling and user feedback")
        print("  • Quick login buttons for demo accounts")
        print("  • Consistent navigation between interfaces")
        print("  • Complete shopping cart functionality")
        print("  • Comprehensive admin dashboard")
        print()
        print(" Login Credentials:")
        print("   Admin: username='admin', password='admin123'")
        print("   Customer 1: username='customer1', password='customer123'")
        print("   Customer 2: username='saqib', password='saqib1'")
        print()
        print(" Starting AWE Electronics Online Store...")
        print()
        
        logger.info(f"Starting {self.app_name} v{self.version}")
        
    def setup_data_files(self):
        """Initialize data files with enhanced default data"""
        try:
            self.data_dir.mkdir(exist_ok=True)
            logger.info(f"Data directory ready: {self.data_dir}")
            
            # Initialize using the file handler
            from utils.file_handler import initialize_default_data
            initialize_default_data()
            
            print("Data files initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to setup data files: {str(e)}")
            print(f" Error setting up data files: {str(e)}")
            
            # Try to show error dialog if tkinter is available
            try:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror(
                    "Data Setup Error",
                    f"Failed to initialize data files:\n{str(e)}\n\n"
                    "Please check file permissions and try again."
                )
                root.destroy()
            except:
                pass
            
            return False
    
    def verify_dependencies(self):
        """Verify all required modules and files are available"""
        try:
            # Check Python version
            if sys.version_info < (3, 7):
                raise Exception(f"Python 3.7+ required, found {sys.version}")
            
            # Check tkinter availability
            try:
                import tkinter
                # Test tkinter works
                test_root = tkinter.Tk()
                test_root.withdraw()
                test_root.destroy()
            except Exception as e:
                raise Exception(f"Tkinter not available: {e}")
            
            # Check required directories
            required_dirs = ['gui', 'models', 'utils']
            missing_dirs = []
            
            for dir_name in required_dirs:
                if not Path(dir_name).exists():
                    missing_dirs.append(dir_name)
            
            if missing_dirs:
                raise Exception(f"Missing required directories: {', '.join(missing_dirs)}")
            
            # Check critical files
            critical_files = [
                'gui/start_gui.py',
                'gui/login_gui.py', 
                'gui/admin_gui.py',
                'gui/customer_gui.py',
                'utils/file_handler.py'
            ]
            
            missing_files = []
            for file_path in critical_files:
                if not Path(file_path).exists():
                    missing_files.append(file_path)
            
            if missing_files:
                raise Exception(f"Missing critical files: {', '.join(missing_files)}")
            
            logger.info("All dependencies verified successfully")
            return True
            
        except Exception as e:
            logger.error(f"Dependency verification failed: {str(e)}")
            print(f" Dependency error: {str(e)}")
            
            # Try to show error dialog
            try:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror(
                    "Dependency Error",
                    f"System requirements not met:\n{str(e)}\n\n"
                    "Please ensure all required files are present."
                )
                root.destroy()
            except:
                pass
            
            return False
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Global exception handler"""
        if issubclass(exc_type, KeyboardInterrupt):
            logger.info("Application interrupted by user")
            return
        
        error_msg = f"Unexpected error: {exc_type.__name__}: {exc_value}"
        logger.error(error_msg, exc_info=(exc_type, exc_value, exc_traceback))
        
        # Try to show error dialog
        try:
            root = tk.Tk()
            root.withdraw()
            messagebox.showerror(
                "Unexpected Error",
                f"An unexpected error occurred:\n\n{error_msg}\n\n"
                "Please check the log file for more details.\n"
                "If the problem persists, contact support."
            )
            root.destroy()
        except:
            print(f" {error_msg}")
    
    def start_gui(self):
        """Start the main GUI application"""
        try:
            logger.info("Launching main GUI")
            
            # Import and start the GUI
            from gui.start_gui import start_gui
            start_gui()
            
            logger.info("GUI closed normally")
            return True
            
        except ImportError as e:
            error_msg = f"Failed to import GUI modules: {str(e)}"
            logger.error(error_msg)
            print(f" {error_msg}")
            
            # Show detailed error information
            print("\n Required GUI files:")
            required_gui_files = [
                "gui/start_gui.py - Welcome screen",
                "gui/login_gui.py - Login interface",
                "gui/register_gui.py - Registration interface", 
                "gui/customer_gui.py - Customer interface",
                "gui/admin_gui.py - Admin dashboard"
            ]
            
            for file_info in required_gui_files:
                print(f"   • {file_info}")
            
            try:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror(
                    "Import Error",
                    f"{error_msg}\n\n"
                    "Please ensure all GUI files are in the gui/ directory:\n"
                    "• gui/start_gui.py\n"
                    "• gui/login_gui.py\n"
                    "• gui/register_gui.py\n"
                    "• gui/customer_gui.py\n"
                    "• gui/admin_gui.py"
                )
                root.destroy()
            except:
                pass
            
            return False
            
        except Exception as e:
            error_msg = f"GUI startup failed: {str(e)}"
            logger.error(error_msg)
            print(f" {error_msg}")
            
            # Print traceback for debugging
            print("\n Error details:")
            traceback.print_exc()
            
            try:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror(
                    "GUI Error",
                    f"{error_msg}\n\n"
                    "The application encountered an error during startup.\n"
                    "Check the console output for more details."
                )
                root.destroy()
            except:
                pass
            
            return False
    
    def show_system_info(self):
        """Display system information dialog"""
        try:
            import platform
            
            # Gather system information
            system_info = {
                "Application": f"{self.app_name} v{self.version}",
                "Python Version": sys.version.split()[0],
                "Platform": f"{platform.system()} {platform.release()}",
                "Architecture": platform.machine(),
                "Working Directory": str(Path.cwd()),
                "Data Directory": str(self.data_dir),
                "Log Directory": str(log_dir)
            }
            
            # Check file status
            file_status = []
            for filename in self.required_files:
                file_path = self.data_dir / filename
                status = "Found" if file_path.exists() else " Missing"
                try:
                    if file_path.exists():
                        size = file_path.stat().st_size
                        status += f" ({size} bytes)"
                except:
                    pass
                file_status.append(f"{filename}: {status}")
            
            # Check GUI files
            gui_files = []
            gui_dir = Path("gui")
            if gui_dir.exists():
                for gui_file in ["start_gui.py", "login_gui.py", "admin_gui.py", "customer_gui.py", "register_gui.py"]:
                    file_path = gui_dir / gui_file
                    status = "Found" if file_path.exists() else " Missing"
                    gui_files.append(f"{gui_file}: {status}")
            
            info_text = "System Information:\n\n"
            for key, value in system_info.items():
                info_text += f"{key}: {value}\n"
            
            info_text += "\nData Files:\n"
            for status in file_status:
                info_text += f"{status}\n"
            
            info_text += "\nGUI Files:\n"
            for status in gui_files:
                info_text += f"{status}\n"
            
            info_text += "\nLogin Credentials:\n"
            info_text += "Admin: admin / admin123\n"
            info_text += "Customer: customer1 / customer123\n"
            info_text += "Customer: saqib / saqib1\n"
            
            print(info_text)
            
            # Also show in GUI if possible
            try:
                root = tk.Tk()
                root.withdraw()
                messagebox.showinfo("System Information", info_text)
                root.destroy()
            except:
                pass
            
        except Exception as e:
            logger.error(f"Failed to show system info: {str(e)}")
            print(f" Error showing system info: {str(e)}")
    
    def run_setup(self):
        """Run setup process"""
        try:
            print("Running setup process...")
            from setup import main as setup_main
            return setup_main()
        except ImportError:
            print("Setup script not found, continuing with basic initialization...")
            return self.setup_data_files()
        except Exception as e:
            print(f" Setup failed: {str(e)}")
            return False
    
    def run(self):
        """Main application entry point"""
        try:
            # Set up global exception handler
            sys.excepthook = self.handle_exception
            
            # Display startup information
            self.display_startup_info()
            
            # Verify system requirements
            print("Verifying system requirements...")
            if not self.verify_dependencies():
                print("\n Try running 'python setup.py' first to initialize the application.")
                return 1
            
            # Setup data files
            print(" Setting up data files...")
            if not self.setup_data_files():
                print("\n If this continues, check file permissions in the application directory.")
                return 1
            
            print(" System initialization completed successfully!")
            print("  Launching GUI interface...")
            print()
            
            # Launch GUI
            if not self.start_gui():
                print("\n If the GUI fails to start:")
                print("   • Ensure all GUI files are present in gui/ directory")
                print("   • Check that tkinter is properly installed")
                print("   • Run 'python main.py --info' for system information")
                return 1
            
            print(" Thank you for using AWE Electronics Online Store!")
            logger.info("Application shutdown normally")
            return 0
            
        except KeyboardInterrupt:
            print("\n Application interrupted by user")
            logger.info("Application interrupted by user")
            return 0
            
        except Exception as e:
            error_msg = f"Critical error during startup: {str(e)}"
            print(f" {error_msg}")
            logger.critical(error_msg)
            
            # Print full traceback for debugging
            print("\n Full error traceback:")
            traceback.print_exc()
            
            try:
                root = tk.Tk()
                root.withdraw()
                messagebox.showerror("Critical Error", error_msg)
                root.destroy()
            except:
                pass
            
            return 1

def main():
    """
    Application entry point
    
    Usage:
        python main.py              # Start the application normally
        python main.py --info       # Show system information
        python main.py --help       # Show help information
        python main.py --setup      # Run setup process
    """
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg in ['--help', '-h']:
            print(f"""
     AWE Electronics Online Store v3.1

Usage: python main.py [options]

Options:
  --help, -h     Show this help message
  --info, -i     Show system information
  --version, -v  Show version information
  --setup, -s    Run setup process

Features:
• Customer shopping interface with responsive design
• Admin dashboard for inventory and sales management  
• User registration and authentication with correct credentials
• Shopping cart with real-time updates
• Order processing and tracking
• Sales reporting and analytics
• Responsive GUI design that maintains window sizing

Login Credentials:
• Admin: admin / admin123
• Customer: customer1 / customer123  
• Customer: saqib / saqib1

Quick Start:
1. Run: python setup.py (first time only)
2. Run: python main.py
3. Use quick login buttons or enter credentials manually

For support or issues:
• Check logs in the 'logs/' directory
• Run 'python main.py --info' for system information
• Ensure all files are in correct directories

GitHub: https://github.com/awe-electronics/online-store
            """)
            return 0
            
        elif arg in ['--info', '-i']:
            app = AWEElectronicsApp()
            app.show_system_info()
            return 0
            
        elif arg in ['--version', '-v']:
            app = AWEElectronicsApp()
            print(f"{app.app_name} v{app.version}")
            print("Enhanced GUI Edition with Responsive Design")
            return 0
            
        elif arg in ['--setup', '-s']:
            app = AWEElectronicsApp()
            success = app.run_setup()
            return 0 if success else 1
            
        else:
            print(f"  Unknown argument: {arg}")
            print("Use --help for usage information")
            return 1
    
    # Run the main application
    app = AWEElectronicsApp()
    return app.run()

def test_imports():
    """Test if all required modules can be imported"""
    print(" Testing imports...")
    
    modules_to_test = [
        ("tkinter", "GUI framework"),
        ("utils.file_handler", "File operations"),
        ("gui.start_gui", "Welcome interface"),
        ("gui.login_gui", "Login interface"),
        ("gui.admin_gui", "Admin dashboard"),
        ("gui.customer_gui", "Customer interface"),
        ("models.catalogue", "Product catalog"),
        ("models.customer", "Customer model"),
        ("models.order", "Order processing")
    ]
    
    all_good = True
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f" {module_name} - {description}")
        except ImportError as e:
            print(f" {module_name} - {description} - Error: {e}")
            all_good = False
        except Exception as e:
            print(f" {module_name} - {description} - Warning: {e}")
    
    if all_good:
        print("\n All imports successful! Application should run properly.")
    else:
        print("\n Some imports failed. Please check file structure and dependencies.")
    
    return all_good

if __name__ == "__main__":
    """
    Direct execution entry point
    
    This allows the application to be run directly with:
        python main.py
    """
    try:
        # Special test mode
        if len(sys.argv) > 1 and sys.argv[1].lower() == '--test':
            test_imports()
            sys.exit(0)
        
        # Normal execution
        exit_code = main()
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\n Application interrupted")
        sys.exit(0)
        
    except Exception as e:
        print(f" Critical error: {e}")
        traceback.print_exc()
        sys.exit(1)
