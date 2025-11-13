"""Notes module containing the Note class."""

from datetime import datetime
class Note:
    """Represents a single note with title, content, creation time, and tags.

    Attributes:
        title: The title of the note (non-empty, stripped).
        content: The content/body of the note (non-empty, stripped).
        created_at: The datetime when the note was created.
        tags: A list of lowercase tags without duplicates.
    """
    def __init__(self, title: str, content: str):
        
        if not title or not title.strip():
            raise ValueError("title must not be empty")
        if not content or not content.strip():
            raise ValueError("content must not be empty")
        
        self.title = title
        self.content = content
        self.created_at = datetime.now()
        self.tags = []
        
    def add_tag(self, tag: str) -> None:
        """Add a lowercase tag if non-empty and not already present.

        Args:
            tag: The tag to add.
        """
        if tag is None:
            return
        normalized = tag.strip().lower()
        if not normalized:
            return
        if normalized not in self.tags:
            self.tags.append(normalized)

    def remove_tag(self, tag: str) -> None:
        """Remove a tag if present.

        Args:
            tag: The tag to remove.
        """
        if tag is None:
            return
        normalized = tag.strip().lower()
        if not normalized:
            return
        try:
            self.tags.remove(normalized)
        except ValueError:
            # Tag not present; ignore
            pass

    def __str__(self) -> str:
        """Return a human-friendly string representation of the note."""
        timestamp = self.created_at.strftime("%d.%m.%Y %H:%M")
        header_line = f"[{timestamp}] {self.title}"
        body_line = self.content
        if self.tags:
            tags_line = f"Tags: {', '.join(self.tags)}"
            return f"{header_line}\n{body_line}\n{tags_line}"
        return f"{header_line}\n{body_line}"


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
