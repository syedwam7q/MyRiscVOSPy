"""
Preset Task Configurations for PMARS Demonstrations
Provides predefined task sets for quick demonstration scenarios
"""

from typing import List, Dict, Any

# Define scheduler types
SCHEDULER_TYPES = {
    "priority": "Priority-based Preemptive Scheduler",
    "round-robin": "Round-Robin Scheduler with Time Slicing",
    "fcfs": "First-Come-First-Served Scheduler"
}

# Define preset configurations
PRESETS = {
    "basic": {
        "description": "Basic set of 3 tasks with different priorities",
        "tasks": [
            {"name": "HighPriorityTask", "priority": 1, "entry_point": 0x9000},
            {"name": "MediumPriorityTask", "priority": 10, "entry_point": 0x9100},
            {"name": "LowPriorityTask", "priority": 20, "entry_point": 0x9200}
        ]
    },
    
    "priority_demo": {
        "description": "Set of 5 tasks to demonstrate priority scheduling",
        "tasks": [
            {"name": "Critical", "priority": 1, "entry_point": 0x9000},
            {"name": "Important", "priority": 5, "entry_point": 0x9100},
            {"name": "Normal1", "priority": 10, "entry_point": 0x9200},
            {"name": "Normal2", "priority": 10, "entry_point": 0x9300},
            {"name": "Background", "priority": 20, "entry_point": 0x9400}
        ]
    },
    
    "round_robin_demo": {
        "description": "Set of 4 tasks with same priority for round-robin demonstration",
        "tasks": [
            {"name": "EqualTask1", "priority": 10, "entry_point": 0x9000},
            {"name": "EqualTask2", "priority": 10, "entry_point": 0x9100},
            {"name": "EqualTask3", "priority": 10, "entry_point": 0x9200},
            {"name": "EqualTask4", "priority": 10, "entry_point": 0x9300}
        ]
    },
    
    "mixed_priority": {
        "description": "Mix of high, medium and low priority tasks",
        "tasks": [
            {"name": "HighPriority1", "priority": 1, "entry_point": 0x9000},
            {"name": "HighPriority2", "priority": 2, "entry_point": 0x9100},
            {"name": "MediumPriority1", "priority": 8, "entry_point": 0x9200},
            {"name": "MediumPriority2", "priority": 9, "entry_point": 0x9300},
            {"name": "LowPriority1", "priority": 15, "entry_point": 0x9400},
            {"name": "LowPriority2", "priority": 16, "entry_point": 0x9500}
        ]
    },
    
    "blocking_demo": {
        "description": "Tasks for demonstrating blocking and unblocking",
        "tasks": [
            {"name": "BlockableHigh", "priority": 1, "entry_point": 0x9000},
            {"name": "BlockableMed", "priority": 5, "entry_point": 0x9100},
            {"name": "BlockableLow", "priority": 10, "entry_point": 0x9200},
            {"name": "BackgroundTask", "priority": 20, "entry_point": 0x9300}
        ]
    },
    
    "sleeping_demo": {
        "description": "Tasks for demonstrating sleep functionality",
        "tasks": [
            {"name": "ShortSleeper", "priority": 5, "entry_point": 0x9000},
            {"name": "MediumSleeper", "priority": 5, "entry_point": 0x9100},
            {"name": "LongSleeper", "priority": 5, "entry_point": 0x9200},
            {"name": "NonSleeper", "priority": 10, "entry_point": 0x9300}
        ]
    },
    
    "aging_demo": {
        "description": "Tasks for demonstrating priority aging mechanism",
        "tasks": [
            {"name": "HighPriorityHog", "priority": 1, "entry_point": 0x9000},
            {"name": "MediumTask1", "priority": 10, "entry_point": 0x9100},
            {"name": "MediumTask2", "priority": 11, "entry_point": 0x9200},
            {"name": "LowPriorityTask", "priority": 20, "entry_point": 0x9300},
            {"name": "VeryLowPriorityTask", "priority": 30, "entry_point": 0x9400}
        ]
    },
    
    "presentation": {
        "description": "Comprehensive set of tasks for a detailed presentation (25 tasks)",
        "tasks": [
            # Critical priority tasks (1-5)
            {"name": "EmergencyHandler", "priority": 1, "entry_point": 0x9000},
            {"name": "SystemMonitor", "priority": 2, "entry_point": 0x9100},
            {"name": "SecurityManager", "priority": 3, "entry_point": 0x9200},
            {"name": "PowerController", "priority": 4, "entry_point": 0x9300},
            {"name": "ErrorHandler", "priority": 5, "entry_point": 0x9400},
            
            # High priority tasks (6-10)
            {"name": "NetworkManager", "priority": 6, "entry_point": 0x9500},
            {"name": "InputProcessor", "priority": 7, "entry_point": 0x9600},
            {"name": "DisplayDriver", "priority": 8, "entry_point": 0x9700},
            {"name": "AudioProcessor", "priority": 9, "entry_point": 0x9800},
            {"name": "MemoryManager", "priority": 10, "entry_point": 0x9900},
            
            # Medium priority tasks (11-15)
            {"name": "FileSystem", "priority": 11, "entry_point": 0x9A00},
            {"name": "DatabaseService", "priority": 12, "entry_point": 0x9B00},
            {"name": "UserInterface", "priority": 13, "entry_point": 0x9C00},
            {"name": "ApplicationLogic", "priority": 14, "entry_point": 0x9D00},
            {"name": "DataProcessor", "priority": 15, "entry_point": 0x9E00},
            
            # Low priority tasks (16-20)
            {"name": "LoggingService", "priority": 16, "entry_point": 0x9F00},
            {"name": "BackupService", "priority": 17, "entry_point": 0xA000},
            {"name": "UpdateChecker", "priority": 18, "entry_point": 0xA100},
            {"name": "StatisticsCollector", "priority": 19, "entry_point": 0xA200},
            {"name": "CacheManager", "priority": 20, "entry_point": 0xA300},
            
            # Background tasks (21-25)
            {"name": "CleanupService", "priority": 21, "entry_point": 0xA400},
            {"name": "IndexBuilder", "priority": 22, "entry_point": 0xA500},
            {"name": "NotificationService", "priority": 23, "entry_point": 0xA600},
            {"name": "SynchronizationTask", "priority": 24, "entry_point": 0xA700},
            {"name": "IdleTask", "priority": 25, "entry_point": 0xA800}
        ]
    }
}

def get_preset_names() -> List[str]:
    """Get a list of available preset names"""
    return list(PRESETS.keys())

def get_preset(name: str) -> Dict[str, Any]:
    """Get a preset configuration by name"""
    if name not in PRESETS:
        raise ValueError(f"Preset '{name}' not found")
    return PRESETS[name]

def list_presets() -> List[Dict[str, Any]]:
    """Get a list of all presets with their descriptions"""
    return [
        {
            "name": name,
            "description": preset["description"],
            "task_count": len(preset["tasks"])
        }
        for name, preset in PRESETS.items()
    ]

def get_scheduler_types() -> List[str]:
    """Get a list of available scheduler types"""
    return list(SCHEDULER_TYPES.keys())

def get_scheduler_description(scheduler_type: str) -> str:
    """Get the description of a scheduler type"""
    if scheduler_type not in SCHEDULER_TYPES:
        raise ValueError(f"Scheduler type '{scheduler_type}' not found")
    return SCHEDULER_TYPES[scheduler_type]

def list_scheduler_types() -> List[Dict[str, str]]:
    """Get a list of all scheduler types with their descriptions"""
    return [
        {
            "name": name,
            "description": description
        }
        for name, description in SCHEDULER_TYPES.items()
    ]