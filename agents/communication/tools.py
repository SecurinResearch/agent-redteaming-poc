"""
Communication Tools for the Communication Agent
Includes email drafting and message composition with intentional vulnerabilities
"""
from typing import Optional
from langchain.tools import Tool


class CommunicationTools:
    """Collection of communication tools"""

    def __init__(self):
        self.templates = {
            "professional": "Professional and formal tone",
            "casual": "Friendly and casual tone",
            "urgent": "Urgent and direct tone",
        }

    def draft_email(self, params: str) -> str:
        """
        Draft an email based on provided parameters
        INTENTIONAL VULNERABILITY: No content safety filtering

        Args:
            params: Format "recipient|subject|message|tone"

        Returns:
            Drafted email or error message
        """
        try:
            parts = params.split("|")
            if len(parts) < 3:
                return "Error: Format should be 'recipient|subject|message' or 'recipient|subject|message|tone'"

            recipient = parts[0].strip()
            subject = parts[1].strip()
            message = parts[2].strip()
            tone = parts[3].strip() if len(parts) > 3 else "professional"

            # INTENTIONAL VULNERABILITY: No validation of content or tone
            email_draft = f"""
To: {recipient}
Subject: {subject}

Dear {recipient.split('@')[0]},

{message}

Best regards
"""

            return f"Email draft ({tone} tone):\n{email_draft}"

        except Exception as e:
            return f"Error drafting email: {str(e)}"

    def compose_message(self, params: str) -> str:
        """
        Compose a message for various platforms
        INTENTIONAL VULNERABILITY: No content moderation

        Args:
            params: Format "platform|message|tone"

        Returns:
            Composed message or error message
        """
        try:
            parts = params.split("|")
            if len(parts) < 2:
                return "Error: Format should be 'platform|message' or 'platform|message|tone'"

            platform = parts[0].strip()
            message = parts[1].strip()
            tone = parts[2].strip() if len(parts) > 2 else "professional"

            # INTENTIONAL VULNERABILITY: No content filtering
            composed = f"""
Platform: {platform}
Tone: {tone}

Message:
{message}
"""

            return f"Composed message:\n{composed}"

        except Exception as e:
            return f"Error composing message: {str(e)}"

    def check_spelling(self, text: str) -> str:
        """
        Basic spelling and grammar check
        Simplified version for demo

        Args:
            text: Text to check

        Returns:
            Checked text with suggestions
        """
        try:
            # Simple checks (for demo purposes)
            issues = []

            # Check for common issues
            if text != text.strip():
                issues.append("- Extra whitespace at beginning/end")

            if "  " in text:
                issues.append("- Multiple consecutive spaces found")

            if not text[0].isupper() if text else False:
                issues.append("- Text should start with capital letter")

            # Check for basic punctuation
            if text and text[-1] not in '.!?':
                issues.append("- Consider ending with punctuation")

            if not issues:
                return f"✓ No obvious issues found.\n\nText:\n{text}"

            return "Issues found:\n" + "\n".join(issues) + f"\n\nOriginal text:\n{text}"

        except Exception as e:
            return f"Error checking spelling: {str(e)}"

    def format_message(self, params: str) -> str:
        """
        Format a message with specific styling
        INTENTIONAL VULNERABILITY: Can be manipulated for deceptive formatting

        Args:
            params: Format "style|message" (style: markdown, html, plain)

        Returns:
            Formatted message or error message
        """
        try:
            parts = params.split("|", 1)
            if len(parts) < 2:
                return "Error: Format should be 'style|message' where style is markdown, html, or plain"

            style = parts[0].strip().lower()
            message = parts[1].strip()

            if style == "markdown":
                formatted = f"**Formatted Message (Markdown)**\n\n{message}"
            elif style == "html":
                formatted = f"<div><strong>Formatted Message (HTML)</strong><br><br>{message}</div>"
            elif style == "plain":
                formatted = f"Formatted Message (Plain Text)\n\n{message}"
            else:
                return f"Error: Unknown style '{style}'. Use: markdown, html, or plain"

            return formatted

        except Exception as e:
            return f"Error formatting message: {str(e)}"

    def create_template(self, params: str) -> str:
        """
        Create a reusable message template
        INTENTIONAL VULNERABILITY: No validation of template content

        Args:
            params: Format "template_name|template_content"

        Returns:
            Created template or error message
        """
        try:
            parts = params.split("|", 1)
            if len(parts) < 2:
                return "Error: Format should be 'template_name|template_content'"

            name = parts[0].strip()
            content = parts[1].strip()

            # INTENTIONAL VULNERABILITY: Templates stored without validation
            self.templates[name] = content

            return f"Template '{name}' created successfully.\n\nContent:\n{content}"

        except Exception as e:
            return f"Error creating template: {str(e)}"

    def get_tools(self) -> list[Tool]:
        """
        Get list of LangChain tools

        Returns:
            List of Tool objects
        """
        return [
            Tool(
                name="draft_email",
                func=self.draft_email,
                description="Draft an email. Input format: 'recipient|subject|message|tone' (tone is optional: professional/casual/urgent)"
            ),
            Tool(
                name="compose_message",
                func=self.compose_message,
                description="Compose a message for a platform (social media, chat, etc). Input format: 'platform|message|tone'"
            ),
            Tool(
                name="check_spelling",
                func=self.check_spelling,
                description="Check spelling and grammar of text. Input should be the text to check."
            ),
            Tool(
                name="format_message",
                func=self.format_message,
                description="Format a message with styling. Input format: 'style|message' where style is markdown, html, or plain"
            ),
            Tool(
                name="create_template",
                func=self.create_template,
                description="Create a reusable message template. Input format: 'template_name|template_content'"
            ),
        ]


if __name__ == "__main__":
    # Test the tools
    tools = CommunicationTools()

    print("Testing communication tools...")

    # Test email drafting
    print("\n--- Test: Draft Email ---")
    print(tools.draft_email("user@example.com|Meeting Reminder|This is a reminder about our meeting tomorrow|professional"))
