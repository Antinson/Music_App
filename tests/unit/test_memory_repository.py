from datetime import date, datetime
from typing import List

import pytest

from music.domainmodel.track import Track
from music.domainmodel.genre import Genre
from music.domainmodel.artist import Artist
from music.domainmodel.review import Review
from music.domainmodel.user import User

from music.adapters.repository import RepositoryException