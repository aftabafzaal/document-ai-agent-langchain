"""
Utility for managing uploaded file lifecycle
"""

import os
import time
from pathlib import Path
from typing import List
from loguru import logger
from config.settings import settings


class FileCleanupManager:
    """Manages uploaded file lifecycle with configurable retention"""
    
    def __init__(self, retention_days: int = 30):
        """
        Args:
            retention_days: Number of days to keep files after processing
        """
        self.retention_days = retention_days
        self.upload_dir = Path(settings.UPLOAD_DIRECTORY)
    
    def delete_file_immediately(self, file_path: str) -> bool:
        """
        Delete file immediately after processing
        
        Args:
            file_path: Path to file to delete
        
        Returns:
            True if deleted successfully
        """
        try:
            path = Path(file_path)
            if path.exists():
                path.unlink()
                logger.info(f"Deleted file: {file_path}")
                return True
        except Exception as e:
            logger.error(f"Error deleting {file_path}: {e}")
        return False
    
    def cleanup_old_files(self) -> List[str]:
        """
        Delete files older than retention_days
        
        Returns:
            List of deleted file paths
        """
        deleted_files = []
        current_time = time.time()
        cutoff_time = current_time - (self.retention_days * 86400)  # 86400 sec/day
        
        try:
            for file_path in self.upload_dir.glob("*"):
                if file_path.is_file():
                    file_age = file_path.stat().st_mtime
                    
                    if file_age < cutoff_time:
                        try:
                            file_path.unlink()
                            deleted_files.append(str(file_path))
                            logger.info(f"Cleaned up old file: {file_path.name}")
                        except Exception as e:
                            logger.error(f"Error deleting {file_path}: {e}")
        
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")
        
        return deleted_files
    
    def get_file_info(self) -> dict:
        """
        Get information about stored files
        
        Returns:
            Dict with file statistics
        """
        files = list(self.upload_dir.glob("*"))
        total_size = sum(f.stat().st_size for f in files if f.is_file())
        
        current_time = time.time()
        files_by_age = {
            "0-7_days": 0,
            "8-30_days": 0,
            "30+_days": 0
        }
        
        for f in files:
            if f.is_file():
                age_days = (current_time - f.stat().st_mtime) / 86400
                if age_days <= 7:
                    files_by_age["0-7_days"] += 1
                elif age_days <= 30:
                    files_by_age["8-30_days"] += 1
                else:
                    files_by_age["30+_days"] += 1
        
        return {
            "total_files": len(files),
            "total_size_mb": round(total_size / 1024 / 1024, 2),
            "files_by_age": files_by_age,
            "retention_days": self.retention_days
        }


# Usage examples:

# Option 1: Delete immediately after processing
# cleanup_manager = FileCleanupManager()
# cleanup_manager.delete_file_immediately("data/uploads/file.pdf")

# Option 2: Cleanup old files (run daily)
# cleanup_manager = FileCleanupManager(retention_days=30)
# deleted = cleanup_manager.cleanup_old_files()

# Option 3: Get stats
# cleanup_manager = FileCleanupManager()
# stats = cleanup_manager.get_file_info()

