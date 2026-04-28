"""
Content Skeleton Ripper — Multi-creator content pattern analysis.
"""

from .pipeline import (
    SkeletonRipperPipeline,
    JobConfig,
    JobProgress,
    JobResult,
    JobStatus,
    create_job_config,
    run_skeleton_ripper,
)
from .extractor import BatchedExtractor
from .synthesizer import PatternSynthesizer
from .aggregator import SkeletonAggregator
from .cache import TranscriptCache
from .llm_client import LLMClient, get_available_providers

__all__ = [
    'SkeletonRipperPipeline',
    'JobConfig', 'JobProgress', 'JobResult', 'JobStatus',
    'create_job_config', 'run_skeleton_ripper',
    'BatchedExtractor', 'PatternSynthesizer', 'SkeletonAggregator',
    'TranscriptCache', 'LLMClient', 'get_available_providers',
]
