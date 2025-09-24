## app/utils/monitor.py
"""
Performance monitoring utilities for the AI Middleware Platform.

This module provides a centralized monitoring system that tracks API performance,
records metrics, and handles alerting for failures. It integrates with the
application's logging system to provide comprehensive observability.
"""

import time
from typing import Dict, Any
from collections import defaultdict

from app.utils.logger import logger
from app.core.config import config


class Monitor:
    """
    Centralized performance monitor for the AI Middleware Platform.
    
    This class provides methods for recording API calls, tracking performance metrics,
    and handling failure alerts. It maintains in-memory statistics for real-time
    monitoring and integrates with the logging system for persistent records.
    """
    
    def __init__(self) -> None:
        """Initialize the monitor with default metrics storage."""
        self.metrics: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "call_count": 0,
            "total_duration": 0.0,
            "success_count": 0,
            "failure_count": 0
        })
        
        # Enable or disable monitoring based on configuration
        self.enabled = config.monitoring_enabled
    
    def record_api_call(self, api_name: str, duration: float, status: str) -> None:
        """
        Record an API call with its duration and status.
        
        Args:
            api_name: The name of the API endpoint.
            duration: The time taken for the API call in seconds.
            status: The status of the API call ('success' or 'failure').
        """
        if not self.enabled:
            return
            
        metrics = self.metrics[api_name]
        metrics["call_count"] += 1
        metrics["total_duration"] += duration
        
        if status.lower() == "success":
            metrics["success_count"] += 1
        else:
            metrics["failure_count"] += 1
            
        # Log the API call
        logger.info(f"API Call: {api_name} | Duration: {duration:.4f}s | Status: {status}")
    
    def get_performance_metrics(self) -> Dict[str, Dict[str, Any]]:
        """
        Get current performance metrics for all APIs.
        
        Returns:
            A dictionary containing performance metrics for each API.
        """
        if not self.enabled:
            return {}
            
        result = {}
        for api_name, metrics in self.metrics.items():
            call_count = metrics["call_count"]
            total_duration = metrics["total_duration"]
            success_count = metrics["success_count"]
            
            # Calculate average duration and success rate
            avg_duration = total_duration / call_count if call_count > 0 else 0
            success_rate = success_count / call_count if call_count > 0 else 0
            
            result[api_name] = {
                "call_count": call_count,
                "average_duration": avg_duration,
                "success_rate": success_rate,
                "failure_count": metrics["failure_count"]
            }
            
        return result
    
    def alert_on_failure(self, execution_id: str) -> None:
        """
        Generate an alert for a failed execution.
        
        Args:
            execution_id: The ID of the failed execution.
        """
        if not self.enabled:
            return
            
        # Log the failure alert
        logger.error(f"ALERT: Execution {execution_id} failed")
        
        # In a production environment, this would integrate with an alerting system
        # such as PagerDuty, Slack, or email notifications


# Global monitor instance
monitor = Monitor()

