from datetime import datetime

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Address(Field):
    """Class for storing contact address."""
    
    def __init__(self, value):
        super().__init__(value)


class Notebook:
    """A collection manager for Note objects keyed by their title.

    Notes are stored in an internal dictionary where keys are unique titles and
    values are Note-like objects with attributes: title, content, created_at, tags.
    """

    def __init__(self):
        """Initialize the notebook with an empty dictionary."""
        self._notes = {}

    def add_note(self, note):
        """Add a note to the notebook ensuring unique title.

        Args:
            note: A Note-like object with 'title' attribute.

        Raises:
            ValueError: If a note with the same title already exists.
        """
        key = note.title.strip() if getattr(note, "title", None) is not None else ""
        if not key:
            raise ValueError("note.title must not be empty")
        if key in self._notes:
            raise ValueError(f"Note with title '{key}' already exists")
        self._notes[key] = note

    def find_note(self, title):
        """Find a note by title.

        Args:
            title: The title of the note to find.

        Returns:
            The found note or None if not found.
        """
        if title is None:
            return None
        key = title.strip()
        if not key:
            return None
        return self._notes.get(key)

    def delete_note(self, title):
        """Delete a note by title.

        Args:
            title: The title of the note to delete.

        Returns:
            True if the note was deleted, False if it did not exist.
        """
        if title is None:
            return False
        key = title.strip()
        if not key:
            return False
        return self._notes.pop(key, None) is not None

    def edit_note(self, title, new_content, update_created_at=False):
        """Edit a note's content. Optionally update its created_at timestamp.

        Args:
            title: The title of the note to edit.
            new_content: The new content for the note.
            update_created_at: If True, update created_at to now (optional).

        Returns:
            True if the note was edited, False if not found or invalid content.
        """
        note = self.find_note(title)
        if note is None:
            return False
        if new_content is None or not str(new_content).strip():
            return False
        note.content = str(new_content).strip()
        if update_created_at and hasattr(note, "created_at"):
            note.created_at = datetime.now()
        return True

    def search_notes(self, keyword):
        """Search notes by keyword in title and content (case-insensitive).

        Args:
            keyword: The search keyword.

        Returns:
            A list of matching notes.
        """
        if keyword is None:
            return []
        query = str(keyword).strip().lower()
        if not query:
            return []
        results = []
        for note in self._notes.values():
            title_text = str(getattr(note, "title", "")).lower()
            content_text = str(getattr(note, "content", "")).lower()
            if query in title_text or query in content_text:
                results.append(note)
        return results

    def show_all(self):
        """Return all notes as a list."""
        return list(self._notes.values())

    # ---- Tag-related (bonus) methods ----
    def find_by_tag(self, tag):
        """Find all notes that contain the specified tag (case-insensitive).

        Args:
            tag: The tag to search for.

        Returns:
            A list of notes that have the given tag.
        """
        if tag is None:
            return []
        needle = str(tag).strip().lower()
        if not needle:
            return []
        results = []
        for note in self._notes.values():
            tags = getattr(note, "tags", []) or []
            if needle in [t.lower() for t in tags]:
                results.append(note)
        return results

    def get_all_tags(self):
        """Get all unique tags across all notes as a sorted list."""
        unique = set()
        for note in self._notes.values():
            tags = getattr(note, "tags", []) or []
            for t in tags:
                if isinstance(t, str) and t.strip():
                    unique.add(t.strip().lower())
        return sorted(unique)

    def sort_by_tags(self, tag_list):
        """Return notes sorted by relevance to the provided tag list.

        Relevance is the number of matching tags between the note and tag_list.
        Notes with zero matches are excluded.

        Args:
            tag_list: Iterable of tags to match against.

        Returns:
            A list of notes sorted by descending number of tag matches; ties are
            broken by ascending title.
        """
        if not tag_list:
            return []
        query_tags = {str(t).strip().lower() for t in tag_list if str(t).strip()}
        if not query_tags:
            return []

        scored = []
        for note in self._notes.values():
            note_tags = {str(t).strip().lower() for t in (getattr(note, "tags", []) or []) if str(t).strip()}
            matches = len(note_tags & query_tags)
            if matches > 0:
                scored.append((matches, getattr(note, "title", ""), note))

        # Sort by matches desc, then by title asc for deterministic ordering
        scored.sort(key=lambda x: (-x[0], x[1]))
        return [n for _, __, n in scored]
        # Check that address is not empty
        if not value or not value.strip():
            raise ValueError("Address cannot be empty")
        
        # Remove leading and trailing whitespace
        super().__init__(value.strip())


class Birthday(Field):
    """Class for storing birthday with validation."""
    
    def __init__(self, value):
        try:
            # Parse string into datetime object
            # Format: DD.MM.YYYY (e.g., 25.12.1990)
            birthday = datetime.strptime(value, "%d.%m.%Y")
            
            # Check that date is not in the future
            if birthday > datetime.now():
                raise FutureDateError("Birthday cannot be in the future")
            
            # Store as datetime object (not string!)
            super().__init__(birthday)
            
        except ValueError:
            # If strptime failed to parse
            raise InvalidDateFormatError(
                f"Invalid date format: {value}. "
                "Expected format: DD.MM.YYYY (e.g., 25.12.1990)"
            )
