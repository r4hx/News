from enum import Enum


class CeleryQueueNameConfigEnum(Enum):
    SUMMARY = "summary"
    TITLER = "titler"
    RSS_IMPORT = "rss_import"
    COVER = "cover"
    RELATED = "related"
