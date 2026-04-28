"""
Progress Tracker Module

Checkpoint management for resuming OCR pipeline after interruptions.
Tracks processed files, confidence scores, and flagged outputs.

Author: Jason Cruz
Institution: Universidad del Pacífico - CIUP
Date: January 2026
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)


class ProgressTracker:
    """
    Manages OCR pipeline progress checkpoints.

    Tracks:
    - Which PDFs have been processed
    - Confidence scores for each file
    - Files needing manual review
    - Processing statistics
    """

    def __init__(self, checkpoint_file: str = "OCR/checkpoints/ocr_progress.json"):
        """
        Initialize progress tracker.

        Args:
            checkpoint_file: Path to checkpoint JSON file
        """
        self.checkpoint_file = Path(checkpoint_file)
        self.checkpoint_file.parent.mkdir(parents=True, exist_ok=True)

        # Initialize or load checkpoint data
        self.data = self.load_checkpoint()

        logger.info(f"ProgressTracker initialized: {self.checkpoint_file}")

    def load_checkpoint(self) -> Dict:
        """
        Load existing checkpoint or create new one.

        Returns:
            Checkpoint data dictionary
        """
        if self.checkpoint_file.exists():
            try:
                with open(self.checkpoint_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                logger.info(f"Loaded checkpoint: {len(data.get('files', {}))} files tracked")
                return data
            except json.JSONDecodeError as e:
                logger.warning(f"Checkpoint file corrupted: {e}, creating new")

        # Create new checkpoint
        data = {
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "total_pdfs": 0,
            "processed": 0,
            "successful": 0,
            "needs_review": 0,
            "failed": 0,
            "files": {},
        }

        logger.info("Created new checkpoint")
        return data

    def save_checkpoint(self) -> None:
        """
        Save checkpoint to disk.
        """
        self.data["last_updated"] = datetime.now().isoformat()

        with open(self.checkpoint_file, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

        logger.debug(f"Checkpoint saved: {self.checkpoint_file}")

    def mark_completed(
        self, pdf_path: str, confidence: float, table_type: Optional[str] = None
    ) -> None:
        """
        Mark PDF as successfully processed.

        Args:
            pdf_path: Path to PDF file
            confidence: Confidence score (0-1)
            table_type: "table_1" or "table_2" or None
        """
        pdf_name = Path(pdf_path).name

        self.data["files"][pdf_name] = {
            "status": "completed",
            "confidence": confidence,
            "table_type": table_type,
            "timestamp": datetime.now().isoformat(),
        }

        self.data["processed"] += 1
        self.data["successful"] += 1

        self.save_checkpoint()

        logger.info(f"Marked completed: {pdf_name} ({confidence:.1%})")

    def mark_needs_review(self, pdf_path: str, confidence: float, issues: List[str]) -> None:
        """
        Mark PDF as needing manual review.

        Args:
            pdf_path: Path to PDF file
            confidence: Confidence score (0-1)
            issues: List of detected issues
        """
        pdf_name = Path(pdf_path).name

        self.data["files"][pdf_name] = {
            "status": "needs_review",
            "confidence": confidence,
            "issues": issues,
            "timestamp": datetime.now().isoformat(),
        }

        self.data["processed"] += 1
        self.data["needs_review"] += 1

        self.save_checkpoint()

        logger.warning(f"Marked needs review: {pdf_name} ({confidence:.1%}, {len(issues)} issues)")

    def mark_failed(self, pdf_path: str, error: str) -> None:
        """
        Mark PDF as failed.

        Args:
            pdf_path: Path to PDF file
            error: Error message
        """
        pdf_name = Path(pdf_path).name

        self.data["files"][pdf_name] = {
            "status": "failed",
            "error": error,
            "timestamp": datetime.now().isoformat(),
        }

        self.data["processed"] += 1
        self.data["failed"] += 1

        self.save_checkpoint()

        logger.error(f"Marked failed: {pdf_name} - {error}")

    def is_processed(self, pdf_path: str) -> bool:
        """
        Check if PDF has already been processed.

        Args:
            pdf_path: Path to PDF file

        Returns:
            True if processed, False otherwise
        """
        pdf_name = Path(pdf_path).name
        return pdf_name in self.data["files"]

    def get_status(self, pdf_path: str) -> Optional[str]:
        """
        Get processing status for PDF.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Status string or None if not processed
        """
        pdf_name = Path(pdf_path).name
        file_data = self.data["files"].get(pdf_name)

        if file_data:
            return file_data.get("status")

        return None

    def get_pending_pdfs(self, all_pdfs: List[str]) -> List[str]:
        """
        Get list of PDFs not yet processed.

        Args:
            all_pdfs: List of all PDF paths

        Returns:
            List of pending PDF paths
        """
        pending = [pdf for pdf in all_pdfs if not self.is_processed(pdf)]

        logger.info(f"Pending PDFs: {len(pending)} / {len(all_pdfs)}")
        return pending

    def get_needs_review_files(self) -> List[Dict]:
        """
        Get list of files needing manual review.

        Returns:
            List of file info dictionaries
        """
        needs_review = []

        for filename, file_data in self.data["files"].items():
            if file_data.get("status") == "needs_review":
                needs_review.append(
                    {
                        "filename": filename,
                        "confidence": file_data.get("confidence", 0.0),
                        "issues": file_data.get("issues", []),
                    }
                )

        return needs_review

    def get_statistics(self) -> Dict:
        """
        Get processing statistics.

        Returns:
            Dictionary with statistics
        """
        total = self.data["processed"]
        successful = self.data["successful"]
        needs_review = self.data["needs_review"]
        failed = self.data["failed"]

        # Calculate success rate
        success_rate = (successful / total * 100) if total > 0 else 0.0

        # Calculate average confidence
        confidences = [
            file_data.get("confidence", 0.0)
            for file_data in self.data["files"].values()
            if file_data.get("confidence") is not None
        ]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0

        stats = {
            "total_pdfs": self.data["total_pdfs"],
            "processed": total,
            "successful": successful,
            "needs_review": needs_review,
            "failed": failed,
            "pending": self.data["total_pdfs"] - total,
            "success_rate": success_rate,
            "avg_confidence": avg_confidence,
        }

        return stats

    def set_total_pdfs(self, total: int) -> None:
        """
        Set total number of PDFs to process.

        Args:
            total: Total PDF count
        """
        self.data["total_pdfs"] = total
        self.save_checkpoint()

    def reset(self) -> None:
        """
        Reset all progress (use with caution).
        """
        logger.warning("Resetting all progress!")

        self.data = {
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "total_pdfs": 0,
            "processed": 0,
            "successful": 0,
            "needs_review": 0,
            "failed": 0,
            "files": {},
        }

        self.save_checkpoint()

    def print_summary(self) -> None:
        """
        Print progress summary to console.
        """
        stats = self.get_statistics()

        print("\nOCR Pipeline Progress Summary")
        print("=" * 60)
        print(f"Total PDFs: {stats['total_pdfs']}")
        print(
            f"Processed: {stats['processed']} ({stats['processed']/stats['total_pdfs']*100:.1f}%)"
        )
        print(f"  ✓ Successful: {stats['successful']}")
        print(f"  ⚠ Needs Review: {stats['needs_review']}")
        print(f"  ✗ Failed: {stats['failed']}")
        print(f"Pending: {stats['pending']}")
        print(f"Success Rate: {stats['success_rate']:.1f}%")
        print(f"Avg Confidence: {stats['avg_confidence']:.1%}")
        print("=" * 60)


if __name__ == "__main__":
    # Test progress tracker
    import sys

    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Create test tracker
    tracker = ProgressTracker("OCR/checkpoints/test_progress.json")

    # Set total
    tracker.set_total_pdfs(10)

    # Mark some completed
    tracker.mark_completed("ns_03_1994.pdf", 0.92, "table_1")
    tracker.mark_completed("ns_08_1994.pdf", 0.88, "table_1")

    # Mark some for review
    tracker.mark_needs_review(
        "ns_11_1994.pdf", 0.78, ["Missing columns", "Low confidence in sector names"]
    )

    # Mark one failed
    tracker.mark_failed("ns_15_1994.pdf", "PDF conversion failed")

    # Print summary
    tracker.print_summary()

    # Show files needing review
    needs_review = tracker.get_needs_review_files()
    if needs_review:
        print("\nFiles Needing Manual Review:")
        print("-" * 60)
        for file_info in needs_review:
            print(f"  {file_info['filename']} ({file_info['confidence']:.1%})")
            for issue in file_info["issues"]:
                print(f"    - {issue}")

    print(f"\n✓ Test complete. Checkpoint saved to: OCR/checkpoints/test_progress.json")
