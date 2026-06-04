"""
Module for sending notifications via Telegram Bot API.
"""
import logging
import os
import requests
from typing import Optional
from models import Scholarship

from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

logger = logging.getLogger(__name__)

class TelegramNotifier:
    """Sends scholarship notifications via Telegram bot."""

    def __init__(self, bot_token: Optional[str] = None, chat_id: Optional[str] = None):
        """
        Initialize the notifier.
        Args:
            bot_token: Telegram Bot Token (if None, reads from BOT_TOKEN env var)
            chat_id: Target Chat ID (if None, reads from CHAT_ID env var)
        """
        self.bot_token = bot_token or os.getenv('BOT_TOKEN')
        self.chat_id = chat_id or os.getenv('CHAT_ID')

        if not self.bot_token or not self.chat_id:
            raise ValueError(
                "Bot token and chat ID must be provided either as arguments or "
                "via BOT_TOKEN and CHAT_ID environment variables."
            )

        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"

    def send_notification(self, scholarship: Scholarship) -> bool:
        """
        Send a scholarship notification to the Telegram chat.
        Returns True if successful, False otherwise.
        """
        message = self._format_message(scholarship)
        url = f"{self.base_url}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'Markdown',
            'disable_web_page_preview': False
        }

        try:
            response = requests.post(url, data=payload, timeout=10)
            response.raise_for_status()
            result = response.json()
            if result.get('ok'):
                logger.info(f"Notification sent for scholarship: {scholarship.title}")
                return True
            else:
                logger.error(f"Telegram API error: {result.get('description')}")
                return False
        except requests.RequestException as e:
            logger.error(f"Failed to send Telegram notification: {e}")
            return False

    def _format_message(self, scholarship: Scholarship) -> str:
        """Format scholarship details into a Telegram message."""
        # Escape special characters for Telegram Markdown
        def escape_md(text):
            if not text:
                return ""
            # Escape characters that have special meaning in Markdown
            escape_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
            for char in escape_chars:
                text = text.replace(char, f'\\{char}')
            return text

        # Build message
        message = f"*{escape_md(scholarship.title)}*\n\n"
        message += f"🔗 [Link]({scholarship.link})\n\n"

        if scholarship.field:
            message += f"📚 *Field:* {escape_md(scholarship.field)}\n"
        if scholarship.level:
            message += f"🎓 *Level:* {escape_md(scholarship.level)}\n"
        if scholarship.nationality:
            message += f"🌍 *Eligible Nationalities:* {escape_md(scholarship.nationality)}\n"
        if scholarship.funding:
            message += f"💰 *Funding:* {escape_md(scholarship.funding)}\n"
        if scholarship.deadline:
            message += f"⏰ *Deadline:* {escape_md(scholarship.deadline.strftime('%Y-%m-%d'))}\n"
        if scholarship.description:
            # Truncate description if too long
            desc = scholarship.description.strip()
            if len(desc) > 200:
                desc = desc[:200] + "..."
            message += f"\n📝 *Description:*\n{escape_md(desc)}\n"

        message += f"\n🏭 *Source:* {escape_md(scholarship.source)}"

        return message

    def test_connection(self) -> bool:
        """Test the connection to Telegram Bot API."""
        url = f"{self.base_url}/getMe"
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            result = response.json()
            if result.get('ok'):
                logger.info(f"Connected to bot: {result['result']['username']}")
                return True
            else:
                logger.error(f"Failed to get bot info: {result.get('description')}")
                return False
        except requests.RequestException as e:
            logger.error(f"Connection test failed: {e}")
            return False